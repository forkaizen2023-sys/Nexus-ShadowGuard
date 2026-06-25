# 🛡️ Nexus ShadowGuard

> **Shadow AI Security Suite — Protege tus datos contra fugas en Inteligencia Artificial**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Enabled-red.svg)](https://streamlit.io/)

Nexus ShadowGuard es una solución de ciberseguridad diseñada para resolver el problema de **Shadow AI**. Actúa como un middleware inteligente que permite a las organizaciones utilizar Large Language Models (LLMs) de forma segura, sin comprometer datos sensibles.

---

## 🎯 ¿Qué hace?

Nexus ShadowGuard funciona como una capa de protección entre los usuarios y los modelos de Inteligencia Artificial. Su objetivo principal es prevenir la fuga de información confidencial cuando los empleados utilizan herramientas como ChatGPT, Claude, Gemini u otros LLMs.

---

## ✨ Características Principales

- **Shadow AI Guard** — Data Loss Prevention (DLP) mediante tokenización reversible de datos sensibles.
- **OSINT B2B Auditor** — Análisis de cabeceras de seguridad (HSTS, CSP, X-Frame-Options y más).
- **Forensics PDF Reporter** — Generación de reportes de cumplimiento normativo (GDPR y PCI-DSS).
- **Integrity Audit** — Controles de Static Application Security Testing (SAST) integrados.
- **Dashboard Interactivo** — Interfaz web moderna construida con Streamlit.

---

## 🛠️ Tecnologías

- **Python 3.12+**
- Streamlit
- FPDF
- PowerShell Integration

---

## 📦 Instalación

### Requisitos

- Python 3.12 o superior
- Git

### Pasos de instalación

```bash
# Clonar el repositorio
git clone https://github.com/forkaizen2023-sys/nexus-shadowguard.git
cd nexus-shadowguard

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Linux / macOS:
source venv/bin/activate

# Windows:
# venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

🚀 Uso
Iniciar el Dashboard
Bashstreamlit run main_dashboard.py
Accede a la interfaz en: http://localhost:8501
Ejecutar auditoría de seguridad
Bashpython nexus_security_audit.py --target https://tu-dominio.com

⚠️ Aviso Legal
Nexus ShadowGuard está diseñado exclusivamente para uso autorizado en auditorías de seguridad, pruebas éticas y entornos corporativos con permiso explícito.
El uso de esta herramienta contra sistemas o datos sin autorización está prohibido y puede ser ilegal.

📜 Licencia
Este proyecto está licenciado bajo la MIT License.
Consulta el archivo LICENSE para más detalles.

👤 Autor
David Jaimes
Senior Cybersecurity Engineer | DevSecOps & AI Security
Nexus Digital
🌐 nexusdigital.pro
