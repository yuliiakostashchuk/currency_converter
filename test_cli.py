import json

import pytest
from click.testing import CliRunner

from cli import converter


@pytest.mark.vcr()
def test_options():
    """Verify that application works correctly when all supported options are passed."""
    runner = CliRunner()
    result = runner.invoke(
        converter,
        ["--amount", 100, "--input_currency", "EUR", "--output_currency", "CZK"],
    )
    assert result.exit_code == 0
    assert json.loads(result.output) == {
        "input": {"amount": 100.0, "currency": "EUR"},
        "output": {"CZK": 2560.9},
    }


def test_required_amount():
    """Verify that amount option is required, correct error message is produced."""
    runner = CliRunner()
    result = runner.invoke(
        converter, ["--input_currency", "EUR", "--output_currency", "CZK"]
    )
    assert result.exit_code == 2
    assert 'Error: Missing option "--amount".\n' in result.output


def test_required_input_currency():
    """Verify that input_currency option is required, correct error message is produced"""
    runner = CliRunner()
    result = runner.invoke(converter, ["--amount", 100, "--output_currency", "CZK"])
    assert result.exit_code == 2
    assert 'Error: Missing option "--input_currency".\n' in result.output


@pytest.mark.vcr()
def test_not_required_output_currency():
    """Verify that output_currency option is not required, application works without it."""
    runner = CliRunner()
    result = runner.invoke(converter, ["--amount", 100, "--input_currency", "EUR"])
    assert result.exit_code == 0
    assert (
        '{\n   "input": {\n      "amount": 100.0,\n      "currency": "EUR"\n   },\n   "output":'
        in result.output
    )


@pytest.mark.vcr()
def test_symbols():
    """Verify that application recognizes currency symbols."""
    runner = CliRunner()
    result = runner.invoke(
        converter, ["--amount", 100, "--input_currency", "€", "--output_currency", "Kč"]
    )
    assert result.exit_code == 0
    assert json.loads(result.output) == {
        "input": {"amount": 100.0, "currency": "EUR"},
        "output": {"CZK": 2560.9},
    }
    print(result.output)
