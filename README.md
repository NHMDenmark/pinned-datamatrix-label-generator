# Pinned Datamatrix Label Generator

## About

This repository hosts a work-in-progress Python package for generating single or double-sided labels with text, datamatrices, and pin holes. This package, `pinned_datamatrix`, is particularly useful for generating labels for pinned insects. The generated labels are vector graphics, which are then embedded into PDF files. These labels can be printed at any resolution, making it a versatile tool for various needs.

Please note that since the package is under active development, the code can change at any time. 

## Key Features

- Generate single or double-sided labels.
- Embed labels with text, datamatrices, and pin holes.
- Create labels as vector graphics, making them resolution-independent.
- Embed generated labels into PDF files for ease of printing.

## Installation


To install the `pinned_datamatrix` package, you have two main methods:
### 1. Cloning the repository and installing locally:
First, clone the repository:
```bash	
git clone https://github.com/lauritsf/pinned-datamatrix-label-generator.git
cd pinned-datamatrix-label-generator
```
Then, install the package using `pip`:
```bash
pip install .
```
### 2. Direct installation via `pip`:
You can directly install the package from the GitHub repository:
```bash
pip install git+https://github.com/lauritsf/pinned-datamatrix-label-generator.git
```


## Usage
### 1. As a library:
After installation, you can import components of the `pinned_datamatrix` package in your Python script or interpreter.

Example:
```python
from pinned_datamatrix import Label, Sheet
# ... your code using these components```
```

2. Command Line Utility:

You can also generate sheets of labels directly using the command-line interface. The tool can be accessed either via the entry point pinned_datamatrix or using python -m pinned_datamatrix.

Here's how you can view the available options:

```bash
python -m pinned_datamatrix --help
```
This will display:

```bash
Usage: python -m pinned_datamatrix [OPTIONS]

Generate a PDF with datamatrix labels

Options:
  -o, --output FILE       The output path of the PDF file  [required]
  -t, --top-text TEXT     The top text  [required]
  -m, --middle-text TEXT  The middle text
  -n, --numbers TEXT      The numbers as a range or list  [required]
  --help                  Show this message and exit.
```

Example usage:

```bash
python -m pinned_datamatrix -o output.pdf -t "NHMD" -n "1-2000"
```

This will generate a PDF file named output.pdf with labels having the top text "NHMD" and numbers ranging from 1 to 2000


## Examples

The `examples` directory contains a variety of examples illustrating how to generate and utilize labels:

- `create_examples.py`: An example script showing how to create datamatrix labels.
- `example_datamatrix.png`, `example_datamatrix.svg`: Examples of datamatrix barcodes.
- `example_label.pdf`, `example_label.png`, `example_label.svg`: Example labels in different formats.
- `example_sheet.pdf`: An example of a sheet of labels.

## Tests

The `tests` directory contains unit tests for the package. These tests cover the datamatrix generation, label generation, and sheet generation functionalities. To run the tests, use the pytest command:

```bash
pytest
```

## Licensing

This project is licensed under the terms of the MIT license. See the `LICENSE` file for more details.

## Contact

Laurits Fredsgaard Larsen

Feel free to reach out if you have any questions or if you would like to contribute.

## Contribution

As this is a work in progress, contributions are most welcome. Please feel free to raise issues or create pull requests.

## Acknowledgements

This project relies on several open-source packages, including `reportlab`, `pylibdmtx`, `numpy`, `Pillow`, `svglib`, and `rlPyCairo`. Their contributions to the open-source community are greatly appreciated.