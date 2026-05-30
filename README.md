# 🛡️ Nexus Digital C2 - Shadow AI Proxy & Security Suite

**Nexus Digital C2** es una solución de ciberseguridad híbrida diseñada para resolver el desafío de la "Shadow AI". Actúa como un middleware inteligente que permite a los empleados utilizar LLMs (como ChatGPT o DeepSeek) sin comprometer la propiedad intelectual o los datos sensibles de la empresa.

## 🚀 Características Principales

- **🧠 Shadow AI Guard (DLP):** Interceptación y tokenización reversible de PII, IPs, credenciales y secretos industriales antes de que salgan al exterior.
- **📡 OSINT B2B Auditor:** Escaneo pasivo de perímetros web para detectar malas configuraciones de seguridad (HSTS, CSP, etc.).
- **📄 Forensics PDF Reporter:** Generación automática de informes técnicos con sellos de tiempo para cumplimiento normativo (GDPR/PCI-DSS).
- **🛡️ Integrity Audit:** Suite de pruebas estáticas (SAST) integradas para garantizar que el código sea seguro antes de cada despliegue.

## 🛠️ Tecnologías
- **Python 3.10+ o 3.12** (Lógica de núcleo y Regex avanzado)
- **Streamlit** (Dashboard de mando)
- **FPDF** (Motores de reportabilidad)
- **PowerShell Integration** (Logs de auditoría en sistemas Windows)

## 📦 Instalación Rápida
1. Clonar: `git clone https://github.com/forkaizen2023-sys/nexus-digital-c2.git`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Auditar: `python nexus_security_audit.py`
4. Lanzar: `streamlit run main_dashboard.py`

---
*Desarrollado por David Jaimes | DevSecOps & AI Security*
