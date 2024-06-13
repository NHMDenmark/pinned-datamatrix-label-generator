from .label_generator import Label


def NHMD(number: int) -> Label:
    return Label(
        data=str(number).zfill(9),
        width=12,
        height=5,
        font_size=3.55,
        text_lines=["NHMD", str(number)],
        text_align="right",
        text_area_margins=(0, 5, 0, 1.3),
        text_oritentation="top",
        check_overlap=True,
        dot_alignment="center_left",
        dot_offset=(0.7, 0),
        datamatrix_alignment="top_right",
        datamatrix_length=5.0,
    )


def NHMA(number: int, bottom_text: str) -> Label:
    return Label(
        data=str(number).zfill(9),
        width=14,
        height=19,
        font_size=7,
        text_lines=["NHMA-ENT", str(number)],
        text_align="center",
        text_area_margins=(0, 0.5, 0, 6.5),
        text_oritentation="right",
        check_overlap=True,
        dot_alignment="center_left",
        dot_offset=(0.2 * 14, 0),
        datamatrix_alignment="bottom_left",
        datamatrix_length=6.5,
    )
