import click
from tqdm import tqdm
from .sheet_generator import Sheet
from .label_generator import Label


def parse_number_range(
    ctx: click.Context, param: click.Parameter, value: str
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
    "--output",
    "-o",
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
    required=True,
    help="The output path of the PDF file",
)
@click.option("--top-text", "-t", type=str, required=True, help="The top text")
@click.option("--middle-text", "-m", type=str, default="", help="The middle text")
@click.option(
    "--numbers",
    "-n",
    required=True,
    callback=parse_number_range,
    help="The numbers as a range or list",
)
def main(output: str, top_text: str, middle_text: str, numbers: list[int]):
    """
    Generate a PDF with datamatrix labels
    """

    labels = generate_labels(top_text, middle_text, numbers)
    generate_pdf(labels, output, double_sided=True)


def generate_labels(top_text: str, middle_text: str, numbers: list[int]) -> list[Label]:
    labels = []
    for number in tqdm(numbers, desc="Generating labels"):
        data = str(number).zfill(9)
        text_lines = [top_text]
        if middle_text:
            text_lines.append(middle_text)
        text_lines.append(str(number))
        label = Label(
            data=data, width=12.0, height=5.0, text_lines=text_lines, font_size=3.55
        )
        labels.append(label)
    return labels


def generate_pdf(labels: list[Label], output: str, double_sided: bool):
    sheet = Sheet(labels=labels, output_path=output, double_sided=double_sided)
    sheet.generate()
    sheet.c.save()


if __name__ == "__main__":
    main()
