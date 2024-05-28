# Pinned Datamatrix Label Generator

| Style | Image |
|-------|-------|
| NHMD  | <img src="examples/NHMD_label.png" alt="NHMD" width="120" /> |
| NHMA  | <img src="examples/NHMA_label.png" alt="NHMA" width="140" style=""/> |

## About

This repository hosts a work-in-progress Python package for generating single or double-sided labels with text, datamatrices, and pin holes. This package, `pinned_datamatrix`, is particularly useful for generating labels for pinned insects. The generated labels are vector graphics, which are then embedded into PDF files. These labels can be printed at any resolution, making it a versatile tool for various needs.

Please note that since the package is under active development, the code can change at any time.

## Key Features

- Generate single or double-sided labels.
- Embed labels with text, datamatrices, and pin holes.
- Create labels as vector graphics, making them resolution-independent.
- Embed generated labels into PDF files for ease of printing.

## Installation

Requires Python 3.10 or later.

**Prerequisites**: Ensure that `git` is installed on your system for the following installation methods.

Before installing the `pinned_datamatrix` package, you need to ensure that the `libdmtx` shared library is installed on your system. This library is a requirement for `pylibdmtx`, which the package relies on. Depending on your operating system, you might need to install this library separately:

### For Mac OS X

You can use Homebrew to install `libdmtx`:

```bash
brew install libdmtx
```

### For Linux

You can use the package manager to install `libdmtx`:

```bash
sudo apt-get install libdmtx0b
```

On Windows, please note that the `libdmtx` DLLs are included with the Python wheels, so you don't need to install them separately.

For more detailed information about `pylibdmtx`, you can visit the [pylibdmtx GitHub repository](https://github.com/NaturalHistoryMuseum/pylibdmtx).

Once `libdmtx` is installed (if needed), you can proceed with installing the `pinned_datamatrix` package using either of the following methods:

### 1. Cloning the repository and installing locally

First, clone the repository:

```bash
git clone https://github.com/NHMDenmark/pinned-datamatrix-label-generator.git
cd pinned-datamatrix-label-generator
```

Then, install the package using `pip`:

```bash
python -m pip install .
```

### 2. Direct installation via `pip`

You can directly install the package from the GitHub repository:

```bash
python -m pip install git+https://github.com/NHMDenmark/pinned-datamatrix-label-generator.git
```

## Usage

### 1. As a library

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
Usage: pinned_datamatrix [OPTIONS]

  Generate a PDF with datamatrix labels

Options:
  -s, --style [NHMD|NHMA]    The label style  [required]
  -b, --bottom-text TEXT     The bottom text for NHMA style labels
  -n, --numbers TEXT         The numbers as a range or list  [required]
  -o, --output FILE          The output path of the PDF file  [required]
  -p, --label-padding FLOAT  The padding around the label in mm (default: 0.25)
  --help                     Show this message and exit.
```

Example usage:

**NHMD style labels with numbers 1-1000 and 2000-3000**

```bash
python -m pinned_datamatrix -s NHMD -n 1-1000,2000-3000 -o labels.pdf
```

**NHMA style labels with numbers ranging from 1 to 2000**

```bash
python -m pinned_datamatrix -s NHMA  -b ENTOMOLOGY -n 1-2000 -o labels.pdf
```

**NHMD style labels with numbers 10-25 and 123456789 and a label padding of 0.5mm**

```bash
python -m pinned_datamatrix -s NHMD -n 10-25,123456789 -o labels.pdf -p 0.5
```

## Examples

The `examples` directory contains a variety of examples illustrating the use of the package. These examples include:

- `create_examples.py`: An example script showing how to create datamatrices, labels, and sheets.
- `example_datamatrix.png`, `example_datamatrix.svg`: Examples of datamatrix barcodes.
- `NHMD_label.pdf`, `NHMD_label.png`, `NHMD_label.svg`: Example NHMD style labels.
- `NHMA_label.pdf`, `NHMA_label.png`, `NHMA_label.svg`: Example NHMA style labels.
- `NHMA_doublesided_sheet.pdf`, `NHMD_doublesided_sheet.pdf`: Example double-sided sheets of labels.

## Tests

The `tests` directory contains unit tests for the package. These tests cover the datamatrix generation, label generation, and sheet generation. To run the tests, you can use the `pytest` command from the root directory of the repository:

```bash
pytest
```

## Licensing

This project is licensed under the terms of the MIT license. See the `LICENSE` file for more details.

## Contribution

As this is a work in progress, contributions are most welcome. Please feel free to raise issues or create pull requests.

## Acknowledgements

This project relies on several open-source packages, including `reportlab`, `pylibdmtx`, `numpy`, `Pillow`, `svglib`, and `rlPyCairo`. Their contributions to the open-source community are greatly appreciated.
