from fpdf import FPDF
from io import BytesIO

def generar_pdf_en_memoria(titulo, transcripcion):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Título: {titulo}\n\n{transcripcion}")

    pdf_output = BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin1')  # Obtener el contenido como string y codificarlo
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)
    return pdf_output
