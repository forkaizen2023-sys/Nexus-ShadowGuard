# config/regex_rules.py
DLP_RULES = {
    "EMAIL": r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
    # Captura la clave AWS completa (20 caracteres) buscando el prefijo AKIA/ASIA
    "API_KEY_AWS": r'\b(?:AKIA|ASIA)[0-9A-Z]{16}\b', 
    # Captura secretos complejos incluyendo símbolos y comillas
    "SECRET_GENERIC": r'(?i)(?:password|passwd|clave|secret|key|token)[\s:=]+["\']?([A-Za-z0-9/_!@#$%^&*()-]{8,64})["\']?',
    "IP_ADDRESS": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
    "CREDIT_CARD": r'\b(?:\d[ -]*?){13,16}\b',
    "DNI_NIE_ES": r'[0-9]{8}[A-Z]|[XYZ][0-9]{7}[A-Z]'
}
