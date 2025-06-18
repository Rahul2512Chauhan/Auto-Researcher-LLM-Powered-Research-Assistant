import fitz # PyMuPDF

def extract_text_from_pdf(pdf_path:str) -> str:
    """
    Extracts and concatenates text from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF.
    """
    try:
       doc = fitz.open(pdf_path)
       full_text = ""

         # Iterate through each page and extract text
       for page in doc:
           text = page.get_text().strip()
           full_text += text + "\n"

       doc.close()
       return full_text.strip()
    except FileNotFoundError:
       return f"Error: The file {pdf_path} was not found."
    except Exception as e:
       return f"An error occurred while extracting text from the PDF: {str(e)}"
    
