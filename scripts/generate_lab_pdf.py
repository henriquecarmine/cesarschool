from pathlib import Path
import shutil
import xml.sax.saxutils as saxutils

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Image, Paragraph, Preformatted, SimpleDocTemplate, Spacer


SRC_MD = Path("docs/labs/relatorio-open5gs-ueransim.md")
LOGO = Path("docs/labs/evidence/logo_cesar.png")
PDF_OUT = Path("docs/labs/relatorio-open5gs-ueransim.pdf")
PDF_OUT_COPY = Path("entrega_trabalho/relatorio-open5gs-ueransim.pdf")
ZIP_PATH = Path("entrega_trabalho.zip")
DELIVERY_DIR = Path("entrega_trabalho")


def escape(text: str) -> str:
    return saxutils.escape(text, {"\u2019": "'", "\u2013": "-", "\u2014": "-"})


def load_styles():
    styles = getSampleStyleSheet()
    if "MyHeading1" not in styles:
        styles.add(ParagraphStyle(name="MyHeading1", parent=styles["Heading1"], fontSize=18, leading=22, spaceAfter=12))
    if "MyHeading2" not in styles:
        styles.add(ParagraphStyle(name="MyHeading2", parent=styles["Heading2"], fontSize=14, leading=18, spaceAfter=10))
    if "MyBodyText" not in styles:
        styles.add(ParagraphStyle(name="MyBodyText", parent=styles["BodyText"], fontSize=11, leading=15, spaceAfter=8))
    if "MyCode" not in styles:
        styles.add(ParagraphStyle(name="MyCode", parent=styles["Code"], fontName="Courier", fontSize=9, leading=12, backColor=colors.whitesmoke, leftIndent=6, rightIndent=6, spaceBefore=6, spaceAfter=6))
    if "MyBullet" not in styles:
        styles.add(ParagraphStyle(name="MyBullet", parent=styles["BodyText"], bulletIndent=12, leftIndent=18, spaceBefore=2))
    return styles


def get_logo_flowable(max_width=180, max_height=90):
    if not LOGO.exists():
        return None
    image = ImageReader(str(LOGO))
    iw, ih = image.getSize()
    ratio = min(max_width / iw, max_height / ih, 1.0)
    width = iw * ratio
    height = ih * ratio
    return Image(str(LOGO), width=width, height=height)


def parse_markdown(markdown_path: Path, styles):
    lines = markdown_path.read_text(encoding="utf-8").splitlines()
    flowables = []
    in_code = False
    code_lines = []

    def flush_code():
        nonlocal code_lines
        if code_lines:
            flowables.append(Preformatted("\n".join(code_lines), styles["MyCode"]))
            code_lines = []

    def flush_paragraph(text):
        if text.strip():
            flowables.append(Paragraph(escape(text.strip()), styles["MyBodyText"]))

    for line in lines:
        if line.startswith("```"):
            if in_code:
                flush_code()
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_lines.append(line)
            continue

        if line.startswith("# "):
            flush_code()
            flowables.append(Paragraph(escape(line[2:].strip()), styles["MyHeading1"]))
        elif line.startswith("## "):
            flush_code()
            flowables.append(Paragraph(escape(line[3:].strip()), styles["MyHeading2"]))
        elif line.startswith("### "):
            flush_code()
            flowables.append(Paragraph(escape(line[4:].strip()), styles["MyHeading2"]))
        elif line.startswith("- "):
            flush_code()
            flowables.append(Paragraph(escape(line[2:].strip()), styles["MyBullet"], bulletText="•"))
        elif not line.strip():
            flush_code()
            flowables.append(Spacer(1, 8))
        else:
            flush_code()
            flowables.append(Paragraph(escape(line.strip()), styles["MyBodyText"]))

    flush_code()
    return flowables


def build_pdf(output_path: Path, story):
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )
    doc.build(story)


def build_report():
    styles = load_styles()
    story = []
    logo = get_logo_flowable()
    if logo:
        story.append(logo)
        story.append(Spacer(1, 12))

    story.extend(parse_markdown(SRC_MD, styles))
    build_pdf(PDF_OUT, story)
    shutil.copy2(PDF_OUT, PDF_OUT_COPY)

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()

    shutil.make_archive(str(ZIP_PATH.with_suffix("")), "zip", root_dir=str(DELIVERY_DIR))


if __name__ == "__main__":
    if PDF_OUT.exists():
        PDF_OUT.unlink()
    if PDF_OUT_COPY.exists():
        PDF_OUT_COPY.unlink()
    build_report()
    print(f"Generated {PDF_OUT} and copied to {PDF_OUT_COPY}")
    print(f"Updated ZIP package at {ZIP_PATH}")
