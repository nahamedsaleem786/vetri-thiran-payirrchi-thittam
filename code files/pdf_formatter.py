from io import BytesIO
from pathlib import Path

from fpdf import FPDF


BASE_DIR = Path(__file__).resolve().parents[1]
FONT_DIR = BASE_DIR / "assets" / "fonts"
REGULAR_FONT = FONT_DIR / "DejaVuSerif.ttf"
BOLD_FONT = FONT_DIR / "DejaVuSerif-Bold.ttf"


class LegalPDF(FPDF):
    def __init__(self, doc_type: str):
        super().__init__()
        self.doc_type = doc_type
        self.set_auto_page_break(auto=True, margin=18)
        self.set_margins(20, 18, 20)

    def header(self):
        self.set_font("DejaVu", "B", 10)
        self.cell(0, 8, "LegalEase", align="C")
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.cell(0, 8, "Generated with LegalEase • AI-assisted draft", align="C")


def format_pdf(text: str, doc_type: str) -> bytes:
    if not REGULAR_FONT.exists() or not BOLD_FONT.exists():
        raise RuntimeError("PDF font files are missing from assets/fonts.")

    pdf = LegalPDF(doc_type)
    pdf.add_font("DejaVu", "", str(REGULAR_FONT))
    pdf.add_font("DejaVu", "B", str(BOLD_FONT))
    pdf.add_page()

    pdf.set_font("DejaVu", "B", 16)
    pdf.multi_cell(0, 9, doc_type.upper(), align="C")
    pdf.ln(5)

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            pdf.ln(3)
            continue

        is_heading = line.isupper() or any(
            line.startswith(f"{i}.") for i in range(1, 100)
        )
        pdf.set_font("DejaVu", "B" if is_heading else "", 11)
        pdf.multi_cell(0, 6, line)
        pdf.ln(1)

    return bytes(pdf.output())
