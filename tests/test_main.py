import tempfile

import pytest
from click.exceptions import BadParameter
from click.testing import CliRunner


from pinned_datamatrix.__main__ import main, parse_number_range


def test_parse_number_range():
    # Test range
    assert parse_number_range(None, None, "1-5") == [1, 2, 3, 4, 5]

    # Test individual numbers
    assert parse_number_range(None, None, "1,2,3") == [1, 2, 3]

    # Test mixed
    assert parse_number_range(None, None, "1-5,7,9-11") == [1, 2, 3, 4, 5, 7, 9, 10, 11]

    # Test invalid
    with pytest.raises(BadParameter):
        parse_number_range(None, None, "a,b,c")

    with pytest.raises(BadParameter):
        parse_number_range(None, None, "1-2-3")

    with pytest.raises(BadParameter):
        parse_number_range(None, None, "abcdef")


def test_main_command():
    runner = CliRunner()

    # Successful execution
    with tempfile.TemporaryDirectory() as tempdir:
        output_path = tempdir + "/test.pdf"
        result = runner.invoke(main, ["-o", output_path, "-t", "NHMD", "-n", "1-5"])
        assert result.exit_code == 0, "Failed to execute main command successfully"

    # Invalid number format
    with tempfile.TemporaryDirectory() as tempdir:
        output_path = tempdir + "/test.pdf"
        result = runner.invoke(main, ["-o", output_path, "-t", "NHMD", "-n", "a-b"])
        assert result.exit_code != 0, "Failed to handle invalid number format"
