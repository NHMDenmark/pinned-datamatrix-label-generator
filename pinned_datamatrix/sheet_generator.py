from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing, Rect
from svglib.svglib import svg2rlg
import io
import os
from datetime import datetime
from tqdm import tqdm

from .label_generator import Label


class Sheet:
    def __init__(
        self,
        labels: list[Label],
        output_path: str,
        label_padding: float = 0.5 / 2,  # mm
        page_size: tuple[float, float] = (297, 210),  # A4 landscape
        page_margins: tuple[float, float, float, float] = (15, 15, 15, 15),  # mm
        double_sided: bool = False,
        numbered: bool = False,
    ):
        self.labels = labels
        self.width = page_size[0] * mm
        self.height = page_size[1] * mm
        self.margin_top = page_margins[0] * mm
        self.margin_right = page_margins[1] * mm
        self.margin_bottom = page_margins[2] * mm
        self.margin_left = page_margins[3] * mm
        self.output_path = output_path
        self.label_padding = label_padding * mm
        self.double_sided = double_sided
        self.numbered = numbered
        self.c = canvas.Canvas(self.output_path, pagesize=(self.width, self.height))

        self._validate_inputs()

        # make a drawing of the label padding box
        label_width, label_height = (
            self.labels[0].width * mm,
            self.labels[0].height * mm,
        )
        padding_box_width = label_width + self.label_padding * 2
        padding_box_height = label_height + self.label_padding * 2
        self.label_padding_box = Drawing(
            width=padding_box_width, height=padding_box_height  # type: ignore # expects int, but any number is fine
        )
        self.label_padding_box.add(
            Rect(
                x=0,
                y=0,
                width=padding_box_width,
                height=padding_box_height,
                fillColor="#eeeeee",
                strokeColor=None,
            )
        )
        self.label_padding_box.add(
            Rect(
                x=self.label_padding,
                y=self.label_padding,
                width=label_width,
                height=label_height,
                fillColor="#ffffff",
                strokeColor=None,
            )
        )
        self.label_padding_box_back = self.label_padding_box.copy()
        self.label_padding_box_back.rotate(180)

    def _validate_inputs(self):
        if not all(isinstance(label, Label) for label in self.labels):
            raise TypeError("labels must be of type Label")
        if not all(
            isinstance(margin, (int, float))
            for margin in (
                self.margin_top,
                self.margin_right,
                self.margin_bottom,
                self.margin_left,
            )
        ):
            raise TypeError("page_margins must be a tuple of numbers.")
        if self.width - self.margin_left - self.margin_right < self.labels[0].width:
            raise ValueError("Page width is smaller than label width")
        if self.height - self.margin_top - self.margin_bottom < self.labels[0].height:
            raise ValueError("Page height is smaller than label height")

    def _draw_label(self, drawing: Drawing, x: float, y: float, is_back=False):
        """
        Draw a label on the page
        Args:
            drawing: The drawing to draw
            x: The x position of the label
            y: The y position of the label
            is_back: Whether the label is on the back side of the page
        """
        if is_back:
            # Position the label on the back side of the page (rotated 180 degrees)
            drawing.rotate(180)
            x_back = self.width - x
            renderPDF.draw(
                self.label_padding_box_back,
                self.c,
                x_back + self.label_padding,
                y + self.label_padding,
            )
            renderPDF.draw(drawing, self.c, x_back, y)
        else:
            # draw padding box first. substract padding from x and y
            renderPDF.draw(
                self.label_padding_box,
                self.c,
                x - self.label_padding,
                y - self.label_padding - drawing.height,
            )
            renderPDF.draw(drawing, self.c, x, y - drawing.height)

    def _handle_page_overflow(
        self, drawing: Drawing, x: float, y: float, backs: list
    ) -> tuple[float, float, list, bool]:
        """
        Handle page overflow by moving to the next page.
        Args:
            drawing: The drawing to draw
            x: The x position of the label
            y: The y position of the label
            backs: A list of drawings to print on the back side of the page
        Returns:
            The new x and y position and the list of drawings to print on the back side of the page
        """
        new_page = False
        if x + drawing.width > self.width - self.margin_right:
            x = self.margin_left
            y -= drawing.height + self.label_padding * 2
            if y - drawing.height < self.margin_bottom:
                new_page = True
                self.c.showPage()
                self.draw_header()
                if self.double_sided:
                    # Print the back side of the page
                    for drawing_back, x_back, y_back in backs:
                        self._draw_label(drawing_back, x_back, y_back, is_back=True)
                    backs = []  # reset backs
                    new_page = True
                    self.c.showPage()
                y = self.height - self.margin_top
        return x, y, backs, new_page

    def _draw_row_number(self, number: int, y: float, drawing_height: float):
        self.c.setFont("Helvetica", 4)

        self.c.drawRightString(
            self.margin_left / 2,
            y - drawing_height / 2,
            str(number),
        )

    def draw_header(self):
        filename = os.path.basename(self.output_path)
        date = datetime.now().strftime("%Y-%m-%d")

        self.c.setFont("Helvetica", 6)

        self.c.drawRightString(
            self.width - self.margin_right -15 * mm,
            self.height - 8 * mm,
            filename,
        )

        self.c.drawRightString(
            self.width - self.margin_right,
            self.height - 8 * mm,
            date,
        )

    def generate(self) -> None:
        """Generate the pdf with labels"""
        backs = []

        x = self.margin_left
        y = self.height - self.margin_top

        row_number = 1
        row_started = False

        self.draw_header()

        labels = tqdm(self.labels, desc="Drawing labels on pdf pages")

        for label in labels:
            # The conversion from svg to rlg is the slowest part of the process
            drawing = svg2rlg(io.StringIO(label.svg_to_string()))

            if drawing is None:
                raise ValueError("Failed to create drawing from SVG data.")

            x, y, backs, new_page = self._handle_page_overflow(
                drawing, x, y, backs
            )

            if self.numbered:
                if new_page:
                    row_number = 1
                    row_started = False
            
                # New row
                if x == self.margin_left and row_started:
                    row_number += 1

                # If we're starting a row, draw its number
                if x == self.margin_left:
                    self._draw_row_number(
                        row_number,
                        y,
                        drawing.height,
                    )
                    row_started = True

            self._draw_label(drawing, x, y)

            backs.append((drawing, x, y))

            x += drawing.width + self.label_padding * 2

        self.c.showPage()

        if self.double_sided:
            for drawing, x, y in backs:
                self._draw_label(drawing, x, y, is_back=True)

            self.c.showPage()
