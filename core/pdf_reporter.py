from fpdf import FPDF
import datetime

class NexusReporter(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.set_text_color(33, 37, 41)
        self.cell(0, 10, 'NEXUS DIGITAL C2 - SECURITY REPORT', 0, 1, 'C')
        self.set_draw_color(0, 123, 255)
        self.line(10, 22, 200, 22)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()} | Nexus AI-Guard | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 0, 'C')

    def generate_full_report(self, dlp_data=None, osint_data=None):
        # Abrimos la página (Vital para evitar el RuntimeError)
        self.add_page()
        
        # --- SECCION DLP ---
        if dlp_data:
            self.set_font('Arial', 'B', 14)
            self.set_fill_color(233, 236, 239)
            self.cell(0, 10, "INFORME DE PREVENCION DE FUGA (DLP)", 0, 1, 'L', True)
            self.ln(4)
            
            metadata = dlp_data.get('metadata', {})
            self.set_font('Arial', '', 11)
            self.cell(0, 8, f"ID Sesion: {metadata.get('session_id')}", 0, 1)
            self.cell(0, 8, f"Elementos bloqueados: {metadata.get('items_blocked')}", 0, 1)
            self.ln(5)
            
            self.set_font('Arial', 'B', 11)
            self.cell(0, 8, "Payload Anonimizado (Seguro para LLM):", 0, 1)
            
            # Formateo de texto para que los tokens sean visibles
            self.set_font('Courier', '', 9)
            self.set_fill_color(248, 249, 250)
            
            payload = dlp_data.get('safe_payload', '')
            # Sustituimos < > por [ ] solo para el PDF para asegurar legibilidad
            payload_visual = payload.replace('<', '[').replace('>', ']')
            payload_safe = payload_visual.encode('latin-1', 'replace').decode('latin-1')
            
            self.multi_cell(0, 5, payload_safe, border=1, fill=True)

        filename = f"Nexus_Final_Report_{datetime.datetime.now().strftime('%H%M%S')}.pdf"
        self.output(filename)
        return filename
