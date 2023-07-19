import xml.etree.ElementTree as ET
import io
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg
from pylibdmtx.pylibdmtx import ENCODING_SIZE_NAMES
from PIL import Image


def svg_to_pil(svg: ET.Element, dpi: int = 300) -> Image.Image:
    """
    Convert an SVG to a PIL Image.
    Args:
        svg: The SVG to convert.
        dpi: The DPI of the PIL Image.
    Returns:
        The PIL Image.
    """
    svg_bytes = ET.tostring(svg, encoding="unicode")
    svg_file = io.StringIO(svg_bytes)
    drawing = svg2rlg(svg_file)
    img = renderPM.drawToPIL(drawing, dpi=dpi)
    return img

