from pinned_datamatrix.label_generator import Label, Text
from pinned_datamatrix.sheet_generator import Sheet
from pinned_datamatrix.utils import svg_to_pil, svg_to_png
from svglib.svglib import svg2rlg
import io
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


check_overlap = False
def NHMA(number: int) -> Label:
    return Label(
        data=str(number).zfill(9),
        width=10,
        height=15,
        font_size=7,
        text_lines=[
            Text(
                text='NHMA',
                alignment='left',
                orientation='right',
                margins=(1, 0, 0, 3.2),
                font_size=7
            ),
            Text(
                text='ENT',
                alignment='left',
                orientation='right',
                margins=(2.3, 0, 0, 1.2),
                font_size=7
            ), 
            Text(
                text=str(number),
                alignment='left',
                orientation='right',
                margins=(3.5, 0, 0, 7),
                font_size=7
            )
        ],
        check_overlap=check_overlap,
        dot_alignment="center_left",
        dot_offset=(0.2 * 14, 0),
        datamatrix_alignment="bottom_left",
        datamatrix_length=6.5,
    )
    

def create_NHMA_label():
    label = NHMA(525001)

    png_bytes = svg_to_png(label.svg, dpi=1200)
    with open("NHMA_label.png", "wb") as f:
        f.write(png_bytes)

    drawing = svg2rlg(io.StringIO(label.svg_to_string()))
    width, height = label.width * mm, label.height * mm
    c = canvas.Canvas("NHMA_label.pdf", pagesize=(width, height))
    renderPDF.draw(drawing, c, 0, 0)
    c.save()

def create_NHMA_sheet():
    sheet = Sheet(
        labels=[NHMA(num) for num in range(525001, 550000)],
        output_path="NHMA_doublesided_sheet.pdf",
        double_sided=True,
    )
    sheet.generate()
    sheet.c.save()


create_NHMA_label()
# create_NHMA_sheet()