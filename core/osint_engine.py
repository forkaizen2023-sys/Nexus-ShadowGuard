import requests
import urllib3

# Solo deshabilitamos advertencias si realmente vamos a permitir sitios con SSL roto
# Pero para tu repo de Git, es mejor dejar que el sistema avise.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class OSINTEngine:
    """
    Motor de Reconocimiento Pasivo: Analiza la postura de seguridad externa
    sin realizar ataques intrusivos.
    """
    def __init__(self):
        self.critical_headers = {
            "Strict-Transport-Security": "Previene ataques Man-in-the-Middle (HSTS).",
            "Content-Security-Policy": "Previene Cross-Site Scripting (XSS).",
            "X-Frame-Options": "Protege contra ataques de Clickjacking.",
            "X-Content-Type-Options": "Evita el sniffing de MIME types.",
            "Referrer-Policy": "Controla qué información se envía en el referer."
        }

    def analyze_domain(self, domain):
        # Normalización de URL
        if not domain.startswith('http'):
            url = f"https://{domain}"
        else:
            url = domain

        results = {
            "target": url,
            "security_score": 100,
            "findings": [],
            "missing_headers": []
        }

        try:
            # 1. Corregido: Definimos 'headers' para que coincida con la llamada
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) NexusDigital/1.0'
            }
            
            try:
                # verify=True garantiza que no aceptamos certificados falsos
                response = requests.get(url, headers=headers, timeout=10, verify=True)
                response.raise_for_status()
            except requests.exceptions.SSLError:
                # En lugar de None, devolvemos un error estructurado para la UI
                return {"error": f"Certificado SSL inválido o inseguro en {url}. Escaneo abortado por seguridad."}
            except requests.exceptions.RequestException as e:
                return {"error": f"Fallo de conexión: {str(e)}"}

            # 2. Corregido: Extraemos las cabeceras de la respuesta
            actual_headers = response.headers

            for header, desc in self.critical_headers.items():
                if header in actual_headers:
                    results["findings"].append({
                        "header": header,
                        "status": "✅ PRESENTE",
                        "value": actual_headers[header][:50] + "..." if len(actual_headers[header]) > 50 else actual_headers[header]
                    })
                else:
                    results["missing_headers"].append({
                        "header": header,
                        "status": "❌ FALTANTE",
                        "risk": desc
                    })
                    results["security_score"] -= 20 # Penalización

            return results

        except Exception as e:
            return {"error": f"Error inesperado en el motor OSINT: {str(e)}"}
