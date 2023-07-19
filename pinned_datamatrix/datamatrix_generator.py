from pylibdmtx.pylibdmtx import encode, ENCODING_SIZE_NAMES
import numpy as np
from PIL.Image import frombytes
from xml.etree import ElementTree as ET


class DataMatrix:
    def __init__(self, data: str, size: str = "SquareAuto"):
        if size not in ENCODING_SIZE_NAMES:
            raise ValueError(f"Invalid size: {size}")

        self.data = data
        self.size = size

        self.dm_array = self._get_datamatrix_bit_array()

    def _get_datamatrix_bit_array(self) -> np.ndarray:
        """
        Get the datamatrix as a boolean array.
        Returns:
            A 2D NumPy array of booleans representing black and white pixels.
        """
        if not isinstance(self.data, str):
            raise TypeError("Data must be a string")
        datamatrix = encode(self.data.encode("utf-8"), size=self.size)

        img = frombytes("RGB", (datamatrix.width, datamatrix.height), datamatrix.pixels)
        img = np.array(img)
        # Downscale 5x
        img = img[::5, ::5, :]
        # True where black
        img = np.all(img == [0, 0, 0], axis=-1)

        return img

    def create_svg(self) -> ET.Element:
        root = ET.Element("svg")

        root.set("baseProfile", "tiny")
        root.set("version", "1.2")
        root.set("viewBox", f"0 0 {self.dm_array.shape[0]} {self.dm_array.shape[1]}")
        root.set("width", f"{self.dm_array.shape[0]}")
        root.set("height", f"{self.dm_array.shape[1]}")
        root.set("xmlns", "http://www.w3.org/2000/svg")

        root.append(self._get_white_modules())
        root.append(self._get_black_modules())

        return root

    def _get_white_modules(self) -> ET.Element:
        element = ET.Element("rect")
        element.set("width", f"{self.dm_array.shape[0]}")
        element.set("height", f"{self.dm_array.shape[1]}")
        element.set("fill", "#fff")  # white
        return element

    def _get_black_modules(self) -> ET.Element:
        black_modules = []
        for x in range(self.dm_array.shape[1]):
            for y in range(self.dm_array.shape[0]):
                if self.dm_array[y, x]:
                    black_modules.append(f"M{x} {y}h1v1h-1z")
        d_attribute = "".join(black_modules)

        element = ET.Element("path")
        element.set("d", d_attribute)
        return element
