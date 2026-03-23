import click
from tqdm import tqdm
from functools import partial as Partial

from .sheet_generator import Sheet
from .label_generator import Label
from .styles import NHMD, NHMA, NHMD_fish


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
    type=click.Choice(["NHMD", "NHMA", "NHMD_fish"]),
    help="The label style",
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
    default=0.25,  # = 0.5mm between each label
    help="The padding around the label in mm (default: 0.25)",
    callback=validate_non_negative,
)
@click.option(
    "--double-sided",
    "-d",
    default=True,
    help="Whether to print double sided labels (default: True)",
)

def main(style, numbers, output, label_padding, double_sided=True):
    """
    Generate a PDF with datamatrix labels
    """
    if style == "NHMD":
        label_func = Partial(NHMD)
    elif style == "NHMA":
        label_func = Partial(NHMA)
    elif style == "NHMD_fish":
        label_func = Partial(NHMD_fish)

    labels = generate_labels(label_func, numbers)
    generate_pdf(labels, output, double_sided, label_padding=label_padding)


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
