from pinned_datamatrix.datamatrix_generator import DataMatrix
from pinned_datamatrix.label_generator import Label
from pinned_datamatrix.sheet_generator import Sheet
from pinned_datamatrix.utils import svg_to_pil, svg_to_png
from pinned_datamatrix.styles import NHMD, NHMA
import xml.etree.ElementTree as ET
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from svglib.svglib import svg2rlg
import io

SVG_NAMESPACE = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NAMESPACE)


def create_example_datamatrix():
    # create example datamatrix and save as svg and png
    data = "example_data"
    size = "SquareAuto"
    dm = DataMatrix(data, size)
    svg = dm.create_svg()

    # save svg
    with open("examples/example_datamatrix.svg", "w") as f:
        f.write(ET.tostring(svg).decode())

    # save png
    img = svg_to_pil(svg)
    img.save("examples/example_datamatrix.png")


def create_NHMD_label():
    # create example label and save as svg and png
    label = NHMD(23456789)

    # save svg
    label.svg_to_file("examples/NHMD_label.svg")

    # save png
    png_bytes = svg_to_png(label.svg, dpi=1200)
    with open("examples/NHMD_label.png", "wb") as f:
        f.write(png_bytes)

    # save pdf
    drawing = svg2rlg(io.StringIO(label.svg_to_string()))
    c = canvas.Canvas("examples/NHMD_label.pdf", pagesize=(12 * mm, 5 * mm))
    renderPDF.draw(drawing, c, 0, 0)
    c.save()


def create_NHMA_label():
    # create example label and save as svg and png
    label = NHMA(137, "ENTOMOLOGY")

    # save svg
    label.svg_to_file("examples/NHMA_label.svg")

    # save png
    png_bytes = svg_to_png(label.svg, dpi=1200)
    with open("examples/NHMA_label.png", "wb") as f:
        f.write(png_bytes)

    # save pdf
    drawing = svg2rlg(io.StringIO(label.svg_to_string()))
    widht, height = label.width * mm, label.height * mm
    c = canvas.Canvas("examples/NHMA_label.pdf", pagesize=(widht, height))
    renderPDF.draw(drawing, c, 0, 0)
    c.save()


def create_NHMD_sheet():
    sheet = Sheet(
        labels=[NHMD(num) for num in range(714)],
        output_path="examples/NHMD_doublesided_sheet.pdf",
        double_sided=True,
    )
    sheet.generate()
    sheet.c.save()


def create_NHMA_sheet():
    sheet = Sheet(
        labels=[NHMA(num, "ENTOMOLOGY") for num in range(714)],
        output_path="examples/NHMA_doublesided_sheet.pdf",
        double_sided=True,
    )
    sheet.generate()
    sheet.c.save()


if __name__ == "__main__":
    create_example_datamatrix()
    create_NHMD_label()
    create_NHMA_label()
    create_NHMD_sheet()
    create_NHMA_sheet()
