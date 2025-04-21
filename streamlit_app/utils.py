from fpdf import FPDF  # Importa la clase FPDF para generar archivos PDF.
from io import BytesIO  # Importa BytesIO para manejar datos en memoria como si fueran un archivo.

def generar_pdf_en_memoria(titulo, transcripcion):
    """
    Genera un archivo PDF en memoria con un título y una transcripción.

    Args:
        titulo (str): El título que aparecerá en el PDF.
        transcripcion (str): El contenido de la transcripción que se incluirá en el PDF.

    Returns:
        BytesIO: Un objeto BytesIO que contiene el PDF generado en memoria.
    """
    # Crea una instancia de FPDF para generar el PDF.
    pdf = FPDF()
    pdf.add_page()  # Agrega una nueva página al PDF.
    pdf.set_font("Arial", size=12)  # Configura la fuente y el tamaño del texto.
    
    # Agrega el título y la transcripción al PDF usando multi_cell para manejar texto largo.
    pdf.multi_cell(0, 10, f"Título: {titulo}\n\n{transcripcion}")

    # Crea un objeto BytesIO para almacenar el PDF en memoria.
    pdf_output = BytesIO()
    
    # Genera el contenido del PDF como una cadena codificada en 'latin1'.
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    
    # Escribe los bytes del PDF en el objeto BytesIO.
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)  # Reinicia el puntero al inicio del archivo en memoria.
    
    # Devuelve el objeto BytesIO que contiene el PDF.
    return pdf_output