# config/regex_rules.py
DLP_RULES = {
    "EMAIL": r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
    "API_KEY_AWS": r'\b(?:AKIA|ASIA|ABIA|ACCA)[0-9A-Z]{16}\b',           # ampliado prefijos
    "SECRET_GENERIC": r'(?i)(?:password|passwd|clave|secret|key|token|api_key|auth|bearer)[\s\w_=-]*[\s:=]+["\']?([A-Za-z0-9/_!@#$%^&*()\-+=]{8,128})["\']?',
    "IP_ADDRESS": r'\b(?:(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\b',  # valida rangos
    "CREDIT_CARD": r'\b(?:4\d{12}(?:\d{3})?|5[1-5]\d{14}|3[47]\d{13}|6(?:011|5\d{2})\d{12}|(?:2131|1800|35\d{3})\d{11})\b',  # patrones reales (Luhn opcional)
    "DNI_NIE_ES": r'\b(?:[0-9]{8}[A-Z]|[XYZ][0-9]{7}[A-Z])\b',
    # (alta prioridad)
    "JWT_TOKEN": r'eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+',
    "SSH_PRIVATE": r'-----BEGIN (?:RSA|OPENSSH|EC) PRIVATE KEY-----',
}
