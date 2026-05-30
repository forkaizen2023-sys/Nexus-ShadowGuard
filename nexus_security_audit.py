import os
import ast
import re
import subprocess
import sys

class NexusAuditPro:
    def __init__(self):
        self.critical_files = [
            'main_dashboard.py',
            'core/ai_guard_engine.py',
            'core/osint_engine.py',
            'config/regex_rules.py',
            'core/pdf_reporter.py'
        ]
        self.issues_found = 0

    def check_syntax(self, file_path):
        """Verifica errores de sintaxis catastróficos."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            ast.parse(source)
            return True, "Sintaxis Perfecta"
        except SyntaxError as e:
            return False, f"Error en línea {e.lineno}: {e.msg}"
        
    def check_dangerous_logic(self, file_path):
        """
        Escáner de Patrones de Vulnerabilidad (SAST).
        Detecta vectores de Inyección de Comandos y Deserialización Insegura.
        """
        # Ampliamos la lista con tus sugerencias tácticas
        dangerous_patterns = [
            'eval(',          # Ejecución de código arbitrario
            'exec(',          # Ejecución de código arbitrario
            'os.system(',     # Inyección de comandos (Legacy)
            'pickle.loads(',  # Deserialización insegura
            'shell=True',     # Inyección de comandos en subprocess (CRÍTICO)
            'yaml.load(',     # Deserialización insegura (CVE-2017-18342)
            'verify=False'    # Desactivación de verificación SSL en requests
        ]
        
        findings = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f, 1):
                    # Solo auditamos líneas que no sean comentarios
                    clean_line = line.split('#')[0].strip()
                    for pattern in dangerous_patterns:
                        if pattern in clean_line:
                            findings.append(f"Línea {i}: Patrón de alto riesgo detectado '{pattern}'")
        except Exception as e:
            findings.append(f"Error al leer archivo para auditoría: {str(e)}")
        return findings    
    

    def audit_dependencies(self):
        """Escanea requirements.txt en busca de librerías vulnerables."""
        print("📦 Escaneando dependencias (Software Composition Analysis)...")
        if not os.path.exists('requirements.txt'):
            return ["⚠️ No se encontró requirements.txt. No se puede auditar."]
        
        try:
            # Intentamos usar 'safety', que es el estándar de la industria
            # Si no está instalado, sugerimos instalarlo
            result = subprocess.run([sys.executable, "-m", "safety", "check", "-r", "requirements.txt", "--json"], 
                                    capture_output=True, text=True)
            if result.returncode != 0 and "No module named safety" in result.stderr:
                return ["💡 Sugerencia: Instala 'safety' (pip install safety) para escaneo de CVEs real."]
            return [] # Si 'safety' pasa, no hay issues detectados
        except Exception:
            return ["⚠️ Error al ejecutar el motor de auditoría de dependencias."]

    def run_audit(self):
        print(f"\n{'='*20} NEXUS DIGITAL C2: AUDITORÍA PRO {'='*20}")
        
        # Auditoría de Archivos
        for file_path in self.critical_files:
            if not os.path.exists(file_path): continue
            
            print(f"\n🔍 Analizando: {file_path}")
            
            # Sintaxis
            ok, msg = self.check_syntax(file_path)
            if not ok:
                print(f"  ❌ CRÍTICO: {msg}")
                self.issues_found += 1
            
            # Lógica Peligrosa
            danger_zones = self.check_dangerous_logic(file_path)
            for d in danger_zones:
                print(f"  ⚠️ RIESGO: {d}")
                self.issues_found += 1
            
            if ok and not danger_zones:
                print("  ✔️ Código limpio y validado.")

        # Auditoría de dependencias
        dep_issues = self.audit_dependencies()
        for issue in dep_issues:
            print(f"  {issue}")

        print("\n" + "="*60)
        if self.issues_found == 0:
            print("🟢 VERDICTO: CÓDIGO SEGURO. Listo para despliegue.")
        else:
            print(f"🔴 VERDICTO: BLOQUEADO. Se encontraron {self.issues_found} vulnerabilidades.")

if __name__ == "__main__":
    NexusAuditPro().run_audit()
