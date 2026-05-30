import re
import uuid
import datetime
import subprocess  # Separado correctamente
from config.regex_rules import DLP_RULES

class NexusAIGuard:
    """
    Nexus AI-Guard: Motor de prevención de fuga de datos (DLP).
    Implementa tokenización reversible y desinfección profunda para LLMs.
    """
    def __init__(self):
        # Cargamos las reglas robustas desde la configuración centralizada
        self.rules = DLP_RULES
        # Diccionario privado para la reversibilidad (Vault)
        self._vault = {} 

    def log_to_windows_event(self, session_id, items_count):
        """
        Escribe una alerta de seguridad en el Visor de Eventos de Windows.
        """
        # Corregida la indentación y el uso de f-strings
        message = f"ALERTA NEXUS C2: Intento de fuga detectado en Sesion {session_id}. Elementos bloqueados: {items_count}."
        
        # Comando de PowerShell: Write-EventLog
        ps_command = f'Write-EventLog -LogName Application -Source ".NET Runtime" -EntryType Warning -EventId 999 -Message "{message}"'
        
        try:
            # Ejecución segura mediante subprocess
            subprocess.run(["powershell", "-Command", ps_command], capture_output=True)
        except Exception:
            pass #

    def sanitize_prompt(self, raw_prompt):
        """
        Analiza el texto, detecta PII/Secretos y los reemplaza por tokens únicos.
        """
        safe_prompt = raw_prompt
        session_id = str(uuid.uuid4())[:8]
        
        # Limpiamos el vault para asegurar que cada proceso sea independiente
        self.clear_vault()

        for rule_name, pattern in self.rules.items():
            matches = re.findall(pattern, safe_prompt)
            for match in matches:
                # Si el regex tiene grupos de captura (tuplas), extraemos el valor real
                original_value = match[1] if isinstance(match, tuple) else match
                
                # CRÍTICO: Validamos que no sea una cadena vacía
                if not original_value or len(original_value.strip()) == 0:
                    continue
                
                # Buscamos si el valor ya fue tokenizado en esta sesión
                existing_token = next((t for t, d in self._vault.items() if d["original"] == original_value), None)
                
                if existing_token:
                    token = existing_token
                else:
                    token = f"<{rule_name}_{uuid.uuid4().hex[:6]}>"
                    self._vault[token] = {
                        "original": original_value,
                        "timestamp": datetime.datetime.now().isoformat()
                    }
                
                safe_prompt = safe_prompt.replace(original_value, token)

        # --- INTEGRACIÓN: Si hay bloqueos, disparamos el evento de Windows ---
        if len(self._vault) > 0:
            self.log_to_windows_event(session_id, len(self._vault))

        return {
            "safe_payload": safe_prompt,
            "metadata": {
                "session_id": session_id,
                "items_blocked": len(self._vault),
                "status": "SECURED",
                "replacements_map": self._vault 
            }
        }

    def restore_response(self, ai_response):
        """Proceso inverso: Sustituye los tokens por los datos originales."""
        if not ai_response:
            return ""
            
        restored_text = ai_response
        for token, data in self._vault.items():
            restored_text = restored_text.replace(token, data["original"])
        return restored_text

    def clear_vault(self):
        """Limpia el almacén de datos en memoria RAM."""
        self._vault.clear()
