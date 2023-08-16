from .datamatrix_generator import DataMatrix
import xml.etree.ElementTree as ET
from svglib.svglib import svg2rlg
from svglib.fonts import register_font
import io
from .utils import are_overlapping


FONT_PATH = "resources/fonts/Inconsolata/Inconsolata-ExtraBold.ttf"
SVG_NAMESPACE = "http://www.w3.org/2000/svg"
PT_TO_MM = 0.352778  # 1pt = 0.352778mm

# register font
register_font(
    font_name="Inconsolata",
    font_path=FONT_PATH,
    style="normal",
    weight="800",
)


class Label:
    DOT_DISTANCE = 0.7  # 0.7mm from left side
    DOT_RADIUS = 0.25  # 0.25mm radius
    TEXT_SIDE_MARGIN = 1.3
    TEXT_VERTICAL_SPACE = 0.5

    def __init__(
        self,
        data: str,
        width: float,
        height: float,
        text_lines: list[str],
        font_size: float,
        check_overlap: bool = True,
    ):
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive")
        if font_size <= 0:
            raise ValueError("font_size must be positive")
        if len(text_lines) == 0:
            raise ValueError("text_lines must contain at least one line")
        if not all(isinstance(line, str) for line in text_lines):
            raise TypeError("text_lines must contain only strings")
        self.data = data
        self.width = width
        self.height = height
        self.text_lines = text_lines
        self.font_size = font_size

        self.svg: ET.Element = self._setup_svg()
        self.datamatrix = self._add_datamatrix()
        self.dot = self._add_dot()
        self.text = self._add_text()

        if check_overlap:
            self._check_overlap()

    def svg_to_string(self) -> str:
        return ET.tostring(self.svg, encoding="unicode")

    def svg_to_file(self, path: str) -> None:
        ET.ElementTree(self.svg).write(path)

    def _setup_svg(self) -> ET.Element:
        ET.register_namespace("", SVG_NAMESPACE)
        svg = ET.Element(
            "svg",
            {
                "baseProfile": "tiny",
                "version": "1.2",
                "viewBox": f"0 0 {self.width} {self.height}",
                "width": f"{self.width}mm",
                "height": f"{self.height}mm",
                "style": "background-color: white",
                "{http://www.w3.org/XML/1998/namespace}space": "preserve",
            },
        )
        return svg

    def _add_datamatrix(self) -> ET.Element:
        datamatrix = DataMatrix(self.data, size="SquareAuto")
        datamatrix = datamatrix.create_svg()

        datamatrix.tag = "g"
        datamatrix.attrib = {
            "id": "datamatrix",
            "width": f"{datamatrix.attrib['width']}",
            "height": f"{datamatrix.attrib['height']}",
            "viewBox": datamatrix.attrib["viewBox"],
        }

        scale = min(
            self.width / float(datamatrix.attrib["width"]),
            self.height / float(datamatrix.attrib["height"]),
        )
        x_pos = self.width - float(datamatrix.attrib["width"]) * scale
        datamatrix.attrib["transform"] = f"translate({x_pos}, 0) scale({scale})"
        self.svg.append(datamatrix)
        return datamatrix

    def _add_dot(self) -> ET.Element:
        dot = ET.Element(
            "circle",
            {
                "id": "pin_dot",
                "cx": str(self.DOT_DISTANCE),  # 0.7mm from left side
                "cy": str(self.height / 2),  # center of label
                "r": str(self.DOT_RADIUS),
            },
        )
        self.svg.append(dot)
        return dot

    def _add_text(self) -> ET.Element:
        text_group = ET.Element(
            "g", {"id": "text", "transform": f"translate({self.TEXT_SIDE_MARGIN}, 0)"}
        )
        font_size = self.font_size * PT_TO_MM
        for i, line in enumerate(self.text_lines):
            y_pos = (i + 1) * font_size + (i + 1) * self.TEXT_VERTICAL_SPACE
            text = ET.Element(
                "text",
                {
                    "id": f"text_line_{i}",
                    "x": "0",
                    "y": str(y_pos),
                    "font-family": "Inconsolata",
                    "font-style": "normal",
                    "font-weight": "800",
                    "font-size": str(font_size),
                },
            )
            text.text = line
            text_group.append(text)
        self.svg.append(text_group)
        return text_group

    def _check_overlap(self) -> None:
        drawing = svg2rlg(io.StringIO(ET.tostring(self.svg, encoding="unicode")))
        if drawing is None:
            raise Exception("Could not convert SVG to ReportLab drawing.")

        objs = drawing.contents[0].contents
        for i in range(len(objs)):
            for j in range(i + 1, len(objs)):
                bounds1: tuple[float, float, float, float] = objs[i].getBounds()
                bounds2: tuple[float, float, float, float] = objs[j].getBounds()
                if are_overlapping(bounds1, bounds2):
                    dx = min(bounds1[2], bounds2[2]) - max(bounds1[0], bounds2[0])
                    dy = min(bounds1[3], bounds2[3]) - max(bounds1[1], bounds2[1])
                    msg = f"Objects {objs[i]} and {objs[j]} are overlapping by {min(dx, dy)}mm."
                    raise Warning(msg)
