import json
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY
import markdown2
from bs4 import BeautifulSoup

# 경로 설정
json_path = "outputs/results.json"
md_path = "outputs/final_report.md"
pdf_path = "outputs/final_report.pdf"

# 폰트 등록
pdfmetrics.registerFont(TTFont("NanumGothic", "fonts/NanumGothic.ttf"))

# 스타일 정의 (기존 스타일 수정)
styles = getSampleStyleSheet()
styles["Heading1"].fontName = "NanumGothic"
styles["Heading1"].fontSize = 18
styles["Heading1"].spaceAfter = 12

styles["Heading2"].fontName = "NanumGothic"
styles["Heading2"].fontSize = 14
styles["Heading2"].spaceAfter = 10

styles["Heading3"].fontName = "NanumGothic"
styles["Heading3"].fontSize = 12
styles["Heading3"].spaceAfter = 8

styles["Normal"].fontName = "NanumGothic"
styles["Normal"].fontSize = 10
styles["Normal"].leading = 14

styles.add(ParagraphStyle(name="Justify", fontName="NanumGothic", fontSize=10, leading=14, alignment=TA_JUSTIFY))

# Markdown → HTML 파싱
with open(md_path, encoding="utf-8") as f:
    md_text = f.read()
html_text = markdown2.markdown(md_text)
soup = BeautifulSoup(html_text, "html.parser")

# 요소를 Paragraph로 변환
elements = []
for tag in soup.find_all(["h1", "h2", "h3", "p", "ul", "li"]):
    text = tag.get_text(strip=True)
    if not text:
        continue
    if tag.name == "h1":
        elements.append(Paragraph(text, styles["Heading1"]))
    elif tag.name == "h2":
        elements.append(Paragraph(text, styles["Heading2"]))
    elif tag.name == "h3":
        elements.append(Paragraph(text, styles["Heading3"]))
    elif tag.name == "li":
        elements.append(Paragraph("• " + text, styles["Normal"]))
    else:
        elements.append(Paragraph(text, styles["Justify"]))
    elements.append(Spacer(1, 0.15 * inch))

# PDF 생성
doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                        rightMargin=40, leftMargin=40,
                        topMargin=60, bottomMargin=60)
doc.build(elements)
print(f"✅ PDF 저장 완료: {pdf_path}")
