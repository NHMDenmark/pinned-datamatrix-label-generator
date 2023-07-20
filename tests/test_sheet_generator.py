import pytest
from unittest.mock import Mock
from reportlab.lib.units import mm
from pinned_datamatrix.sheet_generator import Sheet
from pinned_datamatrix.label_generator import Label


@pytest.fixture
def sheet_fixture(tmpdir):
    labels = [
        Label(
            data=str(num).zfill(9),
            width=12,
            height=5,
            font_size=3.7,
            text_lines=["NHMD", str(num).zfill(9)],
            check_overlap=False,
        )
        for num in range(20)
    ]

    output_path = str(tmpdir.join("test.pdf"))
    page_size = (297, 210)  # A4 landscape
    page_margins = (15, 15, 15, 15)  # mm
    label_padding = 0.1  # mm
    double_sided = True

    svg = Mock()
    drawing = Mock()

    return (
        labels,
        output_path,
        page_size,
        page_margins,
        label_padding,
        double_sided,
        svg,
        drawing,
    )


class TestSheet:
    def test_init(self, sheet_fixture):
        (
            labels,
            output_path,
            page_size,
            page_margins,
            label_padding,
            double_sided,
            _,
            _,
        ) = sheet_fixture
        sheet = Sheet(
            labels=labels,
            output_path=output_path,
            page_size=page_size,
            page_margins=page_margins,
            label_padding=label_padding,
            double_sided=double_sided,
        )
        assert sheet.labels == labels
        assert sheet.output_path == output_path
        assert sheet.label_padding == label_padding * mm
        assert sheet.width == page_size[0] * mm
        assert sheet.height == page_size[1] * mm
        assert sheet.margin_top == page_margins[0] * mm
        assert sheet.margin_right == page_margins[1] * mm
        assert sheet.margin_bottom == page_margins[2] * mm
        assert sheet.margin_left == page_margins[3] * mm
        assert sheet.double_sided == double_sided

    def test_init_bad_label_type(self, sheet_fixture):
        (
            _,
            output_path,
            page_size,
            page_margins,
            label_padding,
            double_sided,
            _,
            _,
        ) = sheet_fixture

        # Test initializing the sheet with a non-label object
        with pytest.raises(TypeError):
            Sheet(
                labels=[1, 2, 3],  # type: ignore
                output_path=output_path,
                page_size=page_size,
                page_margins=page_margins,
                label_padding=label_padding,
                double_sided=double_sided,
            )

    def test_init_bad_margin_type(self, sheet_fixture):
        (
            labels,
            output_path,
            page_size,
            _,
            label_padding,
            double_sided,
            _,
            _,
        ) = sheet_fixture
        # Initialize the sheet with a non-number margin
        with pytest.raises(TypeError):
            Sheet(
                labels=labels,
                output_path=output_path,
                page_size=page_size,
                page_margins=(1, 2, 3, "a"),  # type: ignore
                label_padding=label_padding,
                double_sided=double_sided,
            )

    def test_init_bad_page_size(self, sheet_fixture):
        (
            labels,
            output_path,
            _,
            page_margins,
            label_padding,
            double_sided,
            _,
            _,
        ) = sheet_fixture
        # Initialize the sheet with a size smaller than the labels
        with pytest.raises(ValueError):
            Sheet(
                labels=labels,
                output_path=output_path,
                page_size=(1, 2),
                page_margins=page_margins,
                label_padding=label_padding,
                double_sided=double_sided,
            )
