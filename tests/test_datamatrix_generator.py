import pytest
from xml.etree import ElementTree as ET
import zxingcpp
from pylibdmtx.pylibdmtx import PyLibDMTXError, ENCODING_SIZE_NAMES
from pinned_datamatrix.datamatrix_generator import (
    DataMatrix,
)
from pinned_datamatrix.utils import svg_to_pil

DM_SILENT_ZONE_SIZE = 2  # 2 modules on each side of the datamatrix


def is_num_x_num(size_string: str) -> bool:
    sizes = size_string.split("x")
    return len(sizes) == 2 and sizes[0].isdigit() and sizes[1].isdigit()


class TestDataMatrix:
    @pytest.mark.parametrize(
        "size", [size for size in ENCODING_SIZE_NAMES if is_num_x_num(size)]
    )
    def test_datamatrix_num_x_num_size(self, size):
        data = "ab12"
        dm = DataMatrix(data, size=size)
        svg = dm.create_svg()
        width, height = self.extract_svg_dimensions(svg)
        expected_width, expected_height = [
            int(x) + 2 * DM_SILENT_ZONE_SIZE for x in size.split("x")
        ]
        assert width == expected_width
        assert height == expected_height

    @pytest.mark.parametrize(
        "data",
        [
            "123",
            "Hello world!",
            "Hello world! 1234567890",
            "Hello world! 1234567890 1234567890",
        ],
    )
    def test_datamatrix_square_auto_size(self, data: str):
        dm = DataMatrix(data, size="SquareAuto")
        svg = dm.create_svg()
        width, height = self.extract_svg_dimensions(svg)
        assert width == height

    @staticmethod
    def extract_svg_dimensions(svg: ET.Element) -> tuple[int, int]:
        _, _, width, height = svg.attrib["viewBox"].split(" ")
        return int(width), int(height)

    @pytest.mark.parametrize(
        "data, size",
        [
            ("hey", "10x10"),
            ("Hello world!", "16x16"),
            ("Hello world!", "32x32"),
            ("Hello world! 1234567890", "20x20"),
            ("Hello world! 1234567890", "32x32"),
        ],
    )
    def test_datamatrix_decodes_correctly(self, data, size):
        dm = DataMatrix(data, size)
        svg = dm.create_svg()
        img = svg_to_pil(svg)
        result = zxingcpp.read_barcode(img, zxingcpp.BarcodeFormat.DataMatrix)
        assert result is not None
        assert result.text == data

    @pytest.mark.parametrize(
        "input_data, expected_error",
        [
            ((1234, "ShapeAuto"), TypeError),
            (("Hello world!", "InvalidSize"), ValueError),
            (("Hello world!" * 100, "10x10"), PyLibDMTXError),
        ],
    )
    def test_invalid_input(self, input_data, expected_error):
        data, size = input_data
        with pytest.raises(expected_error):
            DataMatrix(data, size)
