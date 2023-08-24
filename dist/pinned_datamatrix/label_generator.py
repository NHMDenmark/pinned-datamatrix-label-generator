import xml.etree.ElementTree as ET
from svglib.svglib import svg2rlg
from svglib.fonts import register_font
import io
import numpy as np
import pkg_resources
from .datamatrix_generator import DataMatrix
from .utils import are_overlapping


FONT_PATH = "resources/fonts/Inconsolata/Inconsolata-ExtraBold.ttf"
FONT_PATH = pkg_resources.resource_filename("pinned_datamatrix", FONT_PATH)
print(FONT_PATH)
SVG_NAMESPACE = "http://www.w3.org/2000/svg"
PT_TO_MM = 0.352778  # 1pt = 0.352778mm

# register font
register_font(
    font_name="Inconsolata",
    font_path=FONT_PATH,
    style="normal",
    weight="800",
)

ORITENTATION_ROTATION_MAP = {
    "top": 0,
    "right": 90,
    "bottom": 180,
    "left": 270,
}

TEXT_ALIGN_MAP = {
    "left": "start",
    "center": "middle",
    "right": "end",
}

ALIGNMENT_OPTIONS = [
    "top_left",
    "top_center",
    "top_right",
    "center_left",
    "center",
    "center_right",
    "bottom_left",
    "bottom_center",
    "bottom_right",
]


class Label:
    def __init__(
        self,
        data: str,
        width: float,
        height: float,
        text_lines: list[str],
        font_size: float,
        text_oritentation: str = "top",  # top, right, bottom, left
        text_align="right",  # left, center, right
        text_area_margins: tuple[float, float, float, float] = (
            0,
            5,
            0,
            1.3,
        ),  # mm (top, right, bottom, left)
        text_line_spacing: float = 0.5,  # mm
        datamatrix_length: float = 5,  # 5x5 mm
        datamatrix_alignment: str = "top_right",
        datamatrix_offset: tuple[float, float] = (0, 0),  # (x, y) in mm
        dot_radius: float = 0.25,  # 0.25 mm
        dot_offset: tuple[float, float] = (0.7, 0),  # 0.7 mm from left side
        dot_alignment: str | None = "center_left",
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
        if text_oritentation not in ORITENTATION_ROTATION_MAP.keys():
            raise ValueError(
                "text_orientation must be either top, right, bottom, or left"
            )
        if text_align not in TEXT_ALIGN_MAP.keys():
            raise ValueError("text_align must be either left, center, or right")
        if dot_alignment is not None and dot_alignment not in ALIGNMENT_OPTIONS:
            raise ValueError(f"dot_alignment must be one of {ALIGNMENT_OPTIONS}")
        if datamatrix_alignment not in ALIGNMENT_OPTIONS:
            raise ValueError(f"datamatrix_alignment must be one of {ALIGNMENT_OPTIONS}")
        if datamatrix_length <= 0:
            raise ValueError("datamatrix_length must be positive")

        self.data = data
        self.width = width
        self.height = height

        self.text_lines = text_lines
        self.font_size = font_size
        self.text_orientation = text_oritentation
        self.text_align = text_align
        self.text_area_margins = text_area_margins
        self.text_line_spacing = text_line_spacing

        self.datamatrix_length = datamatrix_length
        self.datamatrix_offset = datamatrix_offset
        self.datamatrix_alignment = datamatrix_alignment

        self.dot_radius = dot_radius
        self.dot_offset = dot_offset
        self.dot_alignment = dot_alignment

        self.svg: ET.Element = self._setup_svg()
        self.datamatrix = self._add_datamatrix()
        if self.dot_alignment is not None:
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
        if self.datamatrix_length > min(self.width, self.height):
            raise ValueError(f"datamatrix_length cannot be larger than width or height")

        datamatrix = DataMatrix(self.data, size="SquareAuto")
        datamatrix = datamatrix.create_svg()

        datamatrix.tag = "g"
        datamatrix.attrib = {
            "id": "datamatrix",
            "width": f"{datamatrix.attrib['width']}",
            "height": f"{datamatrix.attrib['height']}",
            "viewBox": datamatrix.attrib["viewBox"],
        }

        if self.datamatrix_alignment in ["top_left", "center_left", "bottom_left"]:
            x = 0
        elif self.datamatrix_alignment in [
            "top_center",
            "center",
            "bottom_center",
        ]:
            x = (self.width - self.datamatrix_length) / 2
        elif self.datamatrix_alignment in ["top_right", "center_right", "bottom_right"]:
            x = self.width - self.datamatrix_length
        else:
            raise ValueError(f"datamatrix_alignment must be one of {ALIGNMENT_OPTIONS}")
        if self.datamatrix_alignment in ["top_left", "top_center", "top_right"]:
            y = 0
        elif self.datamatrix_alignment in [
            "center_left",
            "center",
            "center_right",
        ]:
            y = (self.height - self.datamatrix_length) / 2
        elif self.datamatrix_alignment in [
            "bottom_left",
            "bottom_center",
            "bottom_right",
        ]:
            y = self.height - self.datamatrix_length
        else:
            raise ValueError(f"datamatrix_alignment must be one of {ALIGNMENT_OPTIONS}")

        x += self.datamatrix_offset[0]
        y += self.datamatrix_offset[1]

        scale = self.datamatrix_length / float(datamatrix.attrib["width"])
        datamatrix.attrib["transform"] = f"translate({x}, {y}) scale({scale})"
        #        x_pos = self.width - float(datamatrix.attrib["width"]) * scale
        #        datamatrix.attrib["transform"] = f"translate({x_pos}, 0) scale({scale})"
        self.svg.append(datamatrix)
        return datamatrix

    def _add_dot(self) -> ET.Element:
        if self.dot_alignment in ["top_left", "center_left", "bottom_left"]:
            x = 0
        elif self.dot_alignment in ["top_center", "center", "bottom_center"]:
            x = self.width / 2
        elif self.dot_alignment in ["top_right", "center_right", "bottom_right"]:
            x = self.width
        else:
            raise ValueError(f"dot_alignment must be one of {ALIGNMENT_OPTIONS}")
        if self.dot_alignment in ["top_left", "top_center", "top_right"]:
            y = 0
        elif self.dot_alignment in ["center_left", "center", "center_right"]:
            y = self.height / 2
        elif self.dot_alignment in ["bottom_left", "bottom_center", "bottom_right"]:
            y = self.height
        else:
            raise ValueError(f"dot_alignment must be one of {ALIGNMENT_OPTIONS}")

        x += self.dot_offset[0]
        y += self.dot_offset[1]

        if x < 0 or x > self.width:
            raise ValueError(f"dot is outside of label width")
        if y < 0 or y > self.height:
            raise ValueError(f"dot is outside of label height")

        dot = ET.Element(
            "circle",
            {
                "id": "pin_dot",
                "cx": str(x),
                "cy": str(y),
                "r": str(self.dot_radius),
            },
        )
        self.svg.append(dot)
        return dot

    def _add_text(self) -> ET.Element:
        angle = ORITENTATION_ROTATION_MAP.get(self.text_orientation, 0)

        text_anchor = TEXT_ALIGN_MAP.get(self.text_align, "end")

        top, right, bottom, left = self.text_area_margins

        if text_anchor == "start":
            x = left
        elif text_anchor == "middle":
            x = left + (self.width - left - right) / 2
        elif text_anchor == "end":
            x = self.width - right
        else:
            raise ValueError(f"text_align must be one of {TEXT_ALIGN_MAP.keys()}")

        rotation = ""
        translation = ""
        rot_y = top
        if self.text_orientation == "top":
            dy = (self.height - top - bottom) / 2
            translation = f"translate(0 {dy})"
        elif self.text_orientation == "right":
            dx = 0
            dy = 0
            if text_anchor == "start":
                rot_x = left
                dx = (self.width - left - right) / 2
            elif text_anchor == "middle":
                dy = (self.height - top - bottom) / 2
                rot_x = left + (self.width - left - right) / 2
            else:  # text_anchor == "end":
                dx = -(self.width - left - right) / 2
                dy = self.height - top - bottom
                rot_x = self.width - right
            rotation = f"rotate ({angle} {rot_x} {rot_y})"
            translation = f"translate({dx} {dy})"
        elif self.text_orientation == "bottom":
            dx = 0
            dy = 0
            if text_anchor == "start":
                rot_x = left
                dx = self.width - left - right
                dy = (self.height - top - bottom) / 2
            elif text_anchor == "middle":
                rot_x = left + (self.width - left - right) / 2
                dy = (self.height - top - bottom) / 2
            else:  # text_anchor == "end":
                rot_x = self.width - right
                dx = -(self.width - left - right)
                dy = (self.height - top - bottom) / 2
            rotation = f"rotate ({angle} {rot_x} {rot_y})"
            translation = f"translate({dx} {dy})"
        else:  # self.text_orientation == "left":
            dx = 0
            dy = 0
            if text_anchor == "start":
                dx = (self.width - left - right) / 2
                dy = self.height - top - bottom
            elif text_anchor == "middle":
                dy = (self.height - top - bottom) / 2
            else:  # text_anchor == "end":
                dx = -(self.width - left - right) / 2

            rotation = f"rotate ({angle} {x} {rot_y})"
            translation = f"translate({dx} {dy})"

        text_group = ET.Element(
            "g",
            {"id": "text", "transform": f"{translation} {rotation}"},
        )
        font_size = self.font_size * PT_TO_MM

        total_height = (font_size + self.text_line_spacing) * (len(self.text_lines) - 1)
        y_positions = np.linspace(
            -total_height / 2,
            total_height / 2,
            len(self.text_lines),
        )
        # svglib doesn't support dominant-baseline, so we have to manually adjust the y positions
        y_positions += font_size * 0.3

        for i, line in enumerate(self.text_lines):
            text = ET.Element(
                "text",
                {
                    "id": f"text_line_{i}",
                    "x": str(x),
                    "y": str(top + y_positions[i]),
                    "font-family": "Inconsolata",
                    "text-anchor": text_anchor,
                    # "dominant-baseline": "middle",  # svglib doesn't support this
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
            bounds1: tuple[float, float, float, float] = objs[i].getBounds()
            # check that it is within the label
            if (
                bounds1[0] < 0
                or bounds1[1] < 0
                or bounds1[2] > self.width
                or bounds1[3] > self.height
            ):
                msg = f"Object {objs[i]} is outside of the label."
                raise Warning(msg)
            for j in range(i + 1, len(objs)):
                bounds2: tuple[float, float, float, float] = objs[j].getBounds()
                if are_overlapping(bounds1, bounds2):
                    dx = min(bounds1[2], bounds2[2]) - max(bounds1[0], bounds2[0])
                    dy = min(bounds1[3], bounds2[3]) - max(bounds1[1], bounds2[1])
                    id1 = objs[i].getProperties().get("svgid", None)
                    id2 = objs[j].getProperties().get("svgid", None)
                    msg = f"Objects {id1} and {id2} are overlapping by {min(dx, dy)}mm."
                    raise Warning(msg)
            if objs[i].getProperties().get("svgid", None) == "text":
                # check that bounds are within the text area
                if (
                    bounds1[0] < self.text_area_margins[3]
                    or bounds1[1] < self.text_area_margins[0]
                    or bounds1[2] > self.width - self.text_area_margins[1]
                    or bounds1[3] > self.height - self.text_area_margins[2]
                ):
                    msg = f"Text object {objs[i]} is outside of the text area."
                    raise Warning(msg)
