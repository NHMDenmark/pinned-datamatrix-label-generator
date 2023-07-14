import pytest
import numpy as np
from PIL import Image
import io
import zxingcpp
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg
from pylibdmtx.pylibdmtx import PyLibDMTXError
from pinned_datamatrix.datamatrix_generator import array_to_svg, create_svg_datamatrix


# Test fixture for the SVG fixture file
@pytest.fixture
def svg_hello_world() -> str:
    with open("tests/test_data/hello_world.svg", "r") as f:
        svg = f.read()
    return svg


# Tests for array_to_svg function
class TestArrayToSVG:
    @pytest.mark.parametrize(
        "input_array, svg_file",
        [
            (np.zeros((10, 10), dtype=bool), "10x10_all_white"),
            (np.ones((10, 10), dtype=bool), "10x10_all_black"),
        ],
    )
    def test_array_to_svg(self, input_array, svg_file):
        expected_svg = self._read_svg_file(svg_file)
        svg = array_to_svg(input_array)
        assert svg == expected_svg

    def _read_svg_file(self, svg_file):
        with open(f"tests/test_data/{svg_file}.svg", "r") as f:
            svg = f.read()
        return svg


# Tests for create_svg_datamatrix function
class TestCreateSVGDataMatrix:
    @pytest.mark.parametrize("size", ["16x16", "20x20", "32x32"])
    def test_svg_dimensions(self, size):
        svg = create_svg_datamatrix("Hello world!", size=size)
        width, height = self._extract_svg_dimensions(svg)
        expected_width, expected_height = [int(x) + 4 for x in size.split("x")]
        assert width == expected_width
        assert height == expected_height

    def test_svg_square_auto(self):
        data = "Hello world!"
        svg = create_svg_datamatrix(data, size="SquareAuto")
        width, height = self._extract_svg_dimensions(svg)
        assert width == height

    def _extract_svg_dimensions(self, svg):
        _, _, width, height = svg.split("viewBox='")[1].split("'")[0].split(" ")
        return int(width), int(height)


# Tests for decoding DataMatrix barcode
class TestDecodeDataMatrix:
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
        svg = create_svg_datamatrix(data, size=size)
        img = self._svg_to_image(svg)
        result = zxingcpp.read_barcode(img, zxingcpp.BarcodeFormat.DataMatrix)
        assert result is not None
        assert result.text == data

    def _svg_to_image(self, svg):
        drawing = svg2rlg(io.StringIO(svg))
        img = renderPM.drawToString(drawing, fmt="png", dpi=300)
        return Image.open(io.BytesIO(img))

    def test_saved_svg_decodes_correctly(self, svg_hello_world):
        img = self._svg_to_image(svg_hello_world)
        result = zxingcpp.read_barcode(img, zxingcpp.BarcodeFormat.DataMatrix)
        assert result is not None
        assert result.text == "Hello world!"


# Test cases for create_svg_datamatrix function with invalid inputs
class TestInvalidInputCreateSVGDataMatrix:
    @pytest.mark.parametrize(
        "input_data, expected_error",
        [
            ((1234, "ShapeAuto"), AttributeError),
            (("Hello world!", "InvalidSize"), PyLibDMTXError),
            (("Hello world!" * 100, "10x10"), PyLibDMTXError),
        ],
    )
    def test_invalid_input_create_svg_datamatrix(self, input_data, expected_error):
        data, size = input_data
        if size is not None:
            with pytest.raises(expected_error):
                create_svg_datamatrix(data, size=size)
        else:
            with pytest.raises(expected_error):
                create_svg_datamatrix(data)


# Test cases for array_to_svg function with invalid inputs
class TestInvalidInputArrayToSVG:
    @pytest.mark.parametrize(
        "input_array, expected_error",
        [
            (np.array([[1, 2], [3, 4]]), ValueError),
            (np.random.randint(2, size=(10, 10, 3), dtype=bool), ValueError),
        ],
    )
    def test_invalid_input_array_to_svg(self, input_array, expected_error):
        with pytest.raises(expected_error):
            array_to_svg(input_array)
