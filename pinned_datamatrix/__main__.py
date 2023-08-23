import click
from tqdm import tqdm
from functools import partial as Partial


from .sheet_generator import Sheet
from .label_generator import Label
from .styles import NHMD, NHMA


def validate_non_negative(
    ctx: click.Context, param: click.Parameter, value: float
) -> float:
    if value < 0:
        raise click.BadParameter("Label padding must be positive")
    return value


def parse_number_range(
    ctx: click.Context | None, param: click.Parameter | None, value: str
) -> list[int]:
    try:
        result = []
        parts = value.split(",")
        for part in parts:
            if "-" in part:
                start, end = map(int, part.split("-"))
                result.extend(range(start, end + 1))
            else:
                result.append(int(part))

        if not result:
            raise ValueError

        return result
    except ValueError:
        raise click.BadParameter("Invalid integer range or list format.")


@click.command()
@click.option(
    "--style",
    "-s",
    required=True,
    type=click.Choice(["NHMD", "NHMA"]),
    help="The label style",
)
@click.option(
    "--bottom-text",
    "-b",
    default="",
    help="The bottom text for NHMA style labels",
)
@click.option(
    "--numbers",
    "-n",
    required=True,
    callback=parse_number_range,
    help="The numbers as a range or list",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
    required=True,
    help="The output path of the PDF file",
)
@click.option(
    "--label-padding",
    "-p",
    default=0.25,  # = 5mm between each label
    help="The padding around the label in mm",
    callback=validate_non_negative,
)
def main(style, bottom_text, numbers, output, label_padding):
    """
    Generate a PDF with datamatrix labels
    """

    label_func = (
        Partial(NHMD) if style == "NHMD" else Partial(NHMA, bottom_text=bottom_text)
    )
    labels = generate_labels(label_func, numbers)
    generate_pdf(labels, output, double_sided=True, label_padding=label_padding)


def generate_labels(label_func: Partial, numbers: list[int]) -> list[Label]:
    numbers_it = tqdm(iterable=numbers, desc="Generating labels")
    labels = map(label_func, numbers_it)
    return list(labels)


def generate_pdf(
    labels: list[Label], output: str, double_sided: bool, label_padding: float
):
    sheet = Sheet(
        labels=labels,
        output_path=output,
        double_sided=double_sided,
        label_padding=label_padding,
    )
    sheet.generate()
    sheet.c.save()


if __name__ == "__main__":
    main()
