import xml.etree.ElementTree as ET
import io
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg
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


def svg_to_png(svg: ET.Element, dpi: int = 300) -> bytes:
    """
    Convert an SVG to a PNG.
    Args:
        svg: The SVG to convert.
        dpi: The DPI of the PNG.
    Returns:
        The PNG as a bytes object.
    """
    svg_bytes = ET.tostring(svg, encoding="unicode")
    svg_file = io.StringIO(svg_bytes)
    drawing = svg2rlg(svg_file)
    png_bytes = renderPM.drawToString(drawing, fmt="PNG", dpi=dpi)
    return png_bytes


def are_overlapping(
    bounds1: tuple[float, float, float, float],
    bounds2: tuple[float, float, float, float],
) -> bool:
    """
    Check if two objects are overlapping.
    Args:
        bounds1: The bounds (x0, y0, x1, y1) of the first object (in mm).
        bounds2: The bounds (x0, y0, x1, y1) of the second object (in mm).

    Returns:
        True if the objects are overlapping, False otherwise.
    """
    return (
        bounds1[0] < bounds2[2]
        and bounds1[2] > bounds2[0]
        and bounds1[1] < bounds2[3]
        and bounds1[3] > bounds2[1]
    )
