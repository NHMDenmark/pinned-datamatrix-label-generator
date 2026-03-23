from .label_generator import Label, Text

def NHMD(number: int) -> Label:
    return Label(
        data=str(number).zfill(9),
        width=12,  # 1pt = 1mm
        height=5,   # 1pt = 1mm
        font_size=1,
        text_lines=[
            Text(
                text="NHMD",
                alignment="left",
                orientation="top",
                margins=(2,0.5,0.5,4.2), # mm offset from (top, right, bottom, left)
                font_size=3.55
            ),
            Text(
                text=str(number).zfill(9),
                alignment="left",
                orientation="top",
                margins=(3.5,0.5,0.5,2.8),
                font_size=2.55
            )
        ],
        check_overlap=True,
        dot_alignment="top_left", # when set to None, the dot will not be printed
        dot_offset=(1, 2.5), # right offset, top offset
        datamatrix_alignment="top_right",
        datamatrix_length=5.0,
    )

def NHMA(number: int) -> Label:
    return Label(
        data=str(number).zfill(9),
        width=15,  # label width in mm
        height=10,   # label height in mm
        font_size=1,
        text_lines=[
            Text(
                text="NHMA",
                alignment="left",
                orientation="top",
                margins=(6.2,0,0,0.5), # mm offset from (top, right, bottom, left)
                font_size=5
            ),
            Text(
                text="ENT",
                alignment="left",
                orientation="top",
                margins=(8.5,0,0,0.5),
                font_size=5
            ),
            Text(
                text=str(number),
                alignment="left",
                orientation="top",
                margins=(2.5,0,0,5),
                font_size=5
            )
        ],
        check_overlap=True,
        dot_alignment="top_center", # when set to None, the dot will not be printed
        dot_offset=(-1, 6.5), # right offset, top offset
        dot_radius=0.25, # radius of the dot in mm
        datamatrix_alignment="bottom_right",
        datamatrix_length=6.5,
    )

def NHMD_fish(number: int) -> Label:
    return Label(
        data=str(number).zfill(9), # dont change this, it sets the data for the datamatrix.
        width=40,  # label width in mm
        height=15,   # label height in mm
        font_size=1,
        text_lines=[
            Text( # you can add more text objects to the text_lines list to customize the label further
                text="NHMD", 
                alignment="left", # how the text is aligned within its text area
                orientation="top", # which direction the text is oriented towards, top means the text will be printed with the top of the text facing towards the top of the label (normal reading orientation)
                margins=(5,0,0,5), # mm offset from (top, right, bottom, left) Generally you just want to control the top and left margins and stay within the label size
                font_size=11 # size of the font in points, 1 point is approximately 0.35 mm, so a font size of 11 would be about 3.85 mm tall. Adjust this based on how much space you have on the label and how large you want the text to appear.
            ),
            Text(
                text=str(number).zfill(9), # full barcode/catalog number with leading zeros / drop the .zfill(9) if you dont want leading zeros
                alignment="left",
                orientation="top",
                margins=(9,0,0,5),
                font_size=9
            )
        ],
        check_overlap=True,
        dot_alignment=None, # "top_center", # when set to None, the dot will not be printed - if you want a pin dot use the dot_alignment and dot_offset parameters to position it where you want on the label. If its hard to configure try and remove the text blocks first to understand how it moves.
        dot_offset=(0, 2.5), # right offset, top offset relative to dots starting position.
        dot_radius=0.5, # radius of the dot in mm
        datamatrix_alignment="top_right",
        datamatrix_length=15.0,
    )