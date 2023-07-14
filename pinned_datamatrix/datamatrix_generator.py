from pylibdmtx.pylibdmtx import encode
import numpy as np
from PIL.Image import frombytes


def create_svg_datamatrix(data: str, size: str = "SquareAuto") -> str:
    """
    Create a SVG file with a datamatrix code.
    Args:
        data: The data to encode in the datamatrix (as a string).
        size: The size (in modules) of the datamatrix. Default is "SquareAuto". See pylibdmtx documentation for more details.

    Returns:
        A string containing the SVG code of the datamatrix.
    """

    datamatrix = encode(data.encode("utf-8"), size=size)

    img = frombytes("RGB", (datamatrix.width, datamatrix.height), datamatrix.pixels)
    img = np.array(img)
    # Downscale 5x
    img = img[::5, ::5, :]
    # True where black
    img = np.all(img == [0, 0, 0], axis=-1)

    svg_str = array_to_svg(img)

    return svg_str


def array_to_svg(array: np.ndarray) -> str:
    """
    Convert a binary array to an SVG string.
    Args:
        array: A 2D NumPy array of booleans representing black and white pixels.

    Returns:
        A string containing the SVG code of the image.
    """
    if array.ndim != 2:
        raise ValueError("Array must be 2D.")
    if array.dtype != bool:
        raise ValueError("Array must be boolean.")

    height, width = array.shape

    svg_params = [
        "baseProfile='tiny'",
        "version='1.2'",
        f"viewBox='0 0 {height} {width}'",
        "xmlns='http://www.w3.org/2000/svg'",
    ]

    bg_path = f"<path d='M0 0h{width}v{height}H0z' fill='#fff' />"

    black_modules = []
    for y in range(height):
        for x in range(width):
            if array[y, x]:
                black_modules.append(f"M{x} {y}h1v1h-1z")

    black_modules_path = f"<path d='{''.join(black_modules)}'/>"

    return f"<svg {' '.join(svg_params)}>{bg_path}{black_modules_path}</svg>"
