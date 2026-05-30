import streamlit as st
import os
from dotenv import load_dotenv

# 1. Cargar variables de entorno ocultas
load_dotenv()

# 2. Importar los motores con manejo de errores robusto
try:
    from core.ai_guard_engine import NexusAIGuard
    from core.osint_engine import OSINTEngine
except ImportError as e:
    st.error(f"Error crítico de importación: {e}")
    NexusAIGuard = None
    OSINTEngine = None

# 3. Configuración táctica de la página
st.set_page_config(
    page_title="Nexus Digital C2",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PANEL DE CONTROL LATERAL (SIDEBAR) ---
with st.sidebar:
    st.title("🛡️ Nexus Digital C2")
    st.markdown("**Panel de Inteligencia y Operaciones**")
    st.markdown("---")
    
    opcion = st.radio(
        "SELECCIONA EL MÓDULO:", 
        ["📡 Reconocimiento OSINT", "🧠 Prevención Shadow AI (DLP)"]
    )
    
    st.markdown("---")
    st.caption("Operador: David Jaimes | DevSecOps")
    st.caption("Estado: En línea 🟢")

# --- MÓDULO 1: RECONOCIMIENTO OSINT ---
if opcion == "📡 Reconocimiento OSINT":
    st.header("📡 Escáner OSINT B2B (Reconocimiento Pasivo)")
    st.markdown("Analiza la postura de seguridad externa y cabeceras críticas.")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        objetivo = st.text_input("Dominio Objetivo", placeholder="ejemplo.com")
    with col2:
        st.write(" ")
        st.write(" ")
        btn_escanear = st.button("🚀 Iniciar Escaneo", use_container_width=True)
        
    if btn_escanear:
        if objetivo and OSINTEngine:
            engine = OSINTEngine()
            with st.spinner(f"Analizando perímetros de {objetivo}..."):
                report = engine.analyze_domain(objetivo)
                
                if "error" in report:
                    st.error(report["error"])
                else:
                    st.subheader(f"Resultado para: {report['target']}")
                    st.metric("Puntuación de Seguridad", f"{report['security_score']}/100")
                    
                    col_headers, col_missing = st.columns(2)
                    with col_headers:
                        st.write("✅ Cabeceras Detectadas")
                        st.table(report["findings"])
                    with col_missing:
                        st.write("⚠️ Vulnerabilidades por Omisión")
                        for item in report["missing_headers"]:
                            st.warning(f"**{item['header']}**: {item['risk']}")
        elif not OSINTEngine:
            st.error("Motor OSINT no disponible.")
        else:
            st.error("Por favor, introduce un dominio válido.")

# --- MÓDULO 2: SHADOW AI GUARD (DLP) ---
elif opcion == "🧠 Prevención Shadow AI (DLP)":
    st.header("🧠 Motor de Intercepción DLP")
    
    prompt_usuario = st.text_area("Entrada de datos:", height=150, 
                                  placeholder="Escribe o pega aquí el contenido sensible...")
    
    # Inicialización segura del motor en la sesión
    if 'guard' not in st.session_state:
        if NexusAIGuard:
            st.session_state.guard = NexusAIGuard()
        else:
            st.error("❌ Motor DLP no disponible. Revisa core/ai_guard_engine.py")

    if st.button("🛡️ Interceptar y Sanear Payload"):
        if 'guard' in st.session_state:
            resultado = st.session_state.guard.sanitize_prompt(prompt_usuario)
            st.session_state.last_result = resultado # Persistencia para restauración
            
            col_res, col_tel = st.columns(2)
            
            # Extracción segura de metadatos para evitar KeyErrors
            metadata = resultado.get('metadata', {})
            safe_payload = resultado.get('safe_payload', 'Error al procesar')
            items_blocked = metadata.get('items_blocked', 0)
            mapa_tokens = metadata.get('replacements_map', {})

            with col_res:
                st.success("🟢 Payload Seguro (Listo para el LLM)")
                st.code(safe_payload, language="text")
            
            with col_tel:
                st.warning("📊 Telemetría de Intercepción")
                st.metric("Elementos Bloqueados", items_blocked)
                # Mostramos el JSON solo si hay datos, de forma elegante
                if mapa_tokens:
                    st.json(mapa_tokens)
                else:
                    st.info("No se detectaron datos sensibles bajo las reglas actuales.")
        else:
            st.error("⚠️ El motor no pudo iniciarse.")

    # --- SECCIÓN DE RESTAURACIÓN (Identidad Real) ---
    if 'last_result' in st.session_state:
        st.markdown("---")
        st.subheader("🔄 Simulación de Respuesta de IA")
        st.write("Copia un token del resultado anterior y pégalo aquí para probar la reversión.")
        
        ai_reply = st.text_input("Respuesta de la IA:", 
                                 placeholder="Ej: El usuario con DNI <DNI_NIE_ES_xxxx> ha sido validado.")
        
        if st.button("🔓 Restaurar Identidad Real"):
            if ai_reply:
                texto_claro = st.session_state.guard.restore_response(ai_reply)
                st.info("Texto Restaurado localmente (Privado):")
                st.success(texto_claro)
            else:
                st.warning("Por favor, introduce un texto con tokens para restaurar.")
    # --- Al final de Módulo 2 en main_dashboard.py ---
if 'last_result' in st.session_state:
    st.markdown("---")
    if st.button("📥 Generar Reporte Forense Final"):
        from core.pdf_reporter import NexusReporter
        reporter = NexusReporter()
        
        # Obtenemos datos de la sesión actual
        dlp_info = st.session_state.last_result
        # Si tienes datos de OSINT previos, podrías pasarlos aquí también
        
        pdf_file = reporter.generate_full_report(dlp_data=dlp_info)
        
        with open(pdf_file, "rb") as f:
            st.download_button(
                label="Click para descargar Informe PDF",
                data=f,
                file_name=pdf_file,
                mime="application/pdf"
            )
        st.success(f"Reporte {pdf_file} generado con éxito.")            
