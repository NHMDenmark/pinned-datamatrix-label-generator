import pytest
from pinned_datamatrix.label_generator import Label, SVG_NAMESPACE, PT_TO_MM
import xml.etree.ElementTree as ET
from pinned_datamatrix.utils import svg_to_pil
import zxingcpp


class TestLabel:
    @pytest.fixture
    def test_label(self):
        return Label(
            data="123456789",
            width=12,
            height=5,
            text_lines=["NHMD", "123456789"],
            font_size=3.7,
            check_overlap=False,
        )

    def test_svg_to_string(self, test_label):
        """Test that the svg_string can be generated and loaded as an svg file"""
        svg_string = test_label.svg_to_string()

        try:
            svg_et = ET.fromstring(svg_string)
            assert svg_et.tag == "svg"
        except Exception as e:
            pytest.fail(f"svg_string could not be loaded as an svg file: {e}")

    def test_svg_to_file(self, tmpdir, test_label):
        """Test that the svg_string can be generated and loaded as an svg file"""
        p = tmpdir.mkdir("subdir").join("test.svg")
        test_label.svg_to_file(str(p))

        try:
            svg_et = ET.parse(str(p))
            assert svg_et.getroot().tag == "svg"
        except Exception as e:
            pytest.fail(f"svg_string could not be loaded as an svg file: {e}")

    def test_setup_svg(self, test_label):
        svg = test_label._setup_svg()
        assert svg.tag == "svg"
        assert svg.attrib["width"] == f"{test_label.width}mm"
        assert svg.attrib["height"] == f"{test_label.height}mm"

    def test_add_datamatrix(self, test_label):
        dm = test_label._add_datamatrix()
        assert dm.tag == "g"
        assert "datamatrix" in dm.attrib["id"]

    def test_add_dot(self, test_label):
        dot = test_label._add_dot()
        assert dot.tag == "circle"
        assert dot.attrib["cx"] == str(test_label.dot_margin)

    def test_add_text(self, test_label):
        text = test_label._add_text()
        assert text.tag == "g"
        assert len(text) == len(test_label.text_lines)
        for i, line in enumerate(text):
            assert line.tag == "text"
            assert line.attrib["font-family"] == "Inconsolata"
            assert line.attrib["font-size"] == str(test_label.font_size * PT_TO_MM)

    def test_check_overlap(self, test_label):
        try:
            test_label._check_overlap()
        except Warning as e:
            assert "are overlapping by" in str(e)

    @pytest.mark.parametrize(
        "data",
        [
            "ab12",
            "Hello World",
            "NHMD123456789",
            "abcdefghijklmnopqrstuvwxyz0123456789",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" * 5,
        ],
    )
    def test_decode_data(self, data):
        label = Label(
            data=data,
            width=12,
            height=5,
            text_lines=["NHMD", "123456789"],
            font_size=3.7,
            check_overlap=False,
        )
        img = svg_to_pil(label.svg, dpi=600)
        decoded_data = zxingcpp.read_barcode(img, zxingcpp.BarcodeFormat.DataMatrix)
        assert decoded_data is not None
        assert decoded_data.text == data

    @pytest.mark.parametrize(
        "data, width, height, text_lines, font_size, expected_error",
        [
            (
                "123456789",
                0,
                0,
                ["NHMD", "123456789"],
                3.7,
                ValueError,
            ),  # zero width/height
            (
                "123456789",
                -12,
                5,
                ["NHMD", "123456789"],
                3.7,
                ValueError,
            ),  # negative width
            (
                "123456789",
                12,
                -5,
                ["NHMD", "123456789"],
                3.7,
                ValueError,
            ),  # negative height
            ("123456789", 12, 5, [], 3.7, ValueError),  # no text lines
            (
                "123456789",
                12,
                5,
                ["NHMD", "123456789"],
                0,
                ValueError,
            ),  # zero font size
            (
                "123456789",
                12,
                5,
                ["NHMD", "123456789"],
                -3.7,
                ValueError,
            ),  # negative font size
            (
                "123456789",
                12,
                5,
                ["NHMD", "123456789" * 100],
                3.7,
                Warning,
            ),  # text and barcode overlap
        ],
    )
    def test_label_edge_cases(
        self,
        data: str,
        width: float,
        height: float,
        text_lines: list,
        font_size: float,
        expected_error,
    ):
        if expected_error is not None:
            with pytest.raises(expected_error):
                label = Label(
                    data=data,
                    width=width,
                    height=height,
                    text_lines=text_lines,
                    font_size=font_size,
                    check_overlap=True,
                )
        else:
            label = Label(
                data=data,
                width=width,
                height=height,
                text_lines=text_lines,
                font_size=font_size,
                check_overlap=True,
            )
            svg = label.svg_to_string()
            assert svg is not None
