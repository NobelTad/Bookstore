import fitz  # PyMuPDF
import sys

def generate_poster(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)  # first page (0-indexed)
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x scale for better quality
    pix.save(output_path)
    print(f"Poster saved to {output_path}")

# Example
if __name__ == "__main__":
    pdf_file = "uploads/20250610155508619416.pdf"
    output_file = "poster.jpg"
    generate_poster(pdf_file, output_file)
