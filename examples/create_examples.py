from pinned_datamatrix.datamatrix_generator import DataMatrix
from pinned_datamatrix.label_generator import Label
from pinned_datamatrix.utils import svg_to_pil
import xml.etree.ElementTree as ET


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


def create_example_label():
    # create example label and save as svg and png
    label = Label(
        data="000333999",
        width=12,
        height=5,
        font_size=3.7,
        text_lines=["NHMD", "000333999"],
        check_overlap=False,  # ignore tiny overlap between text and datamatrix
    )

    # save svg
    label.svg_to_file("examples/example_label.svg")

    # save png
    img = svg_to_pil(label.svg)
    img.save("examples/example_label.png")


if __name__ == "__main__":
    create_example_datamatrix()
    create_example_label()
