import json

import click

from utils import convert


@click.command()
@click.option("--amount", type=click.FLOAT, required=True, help="Amount to convert.")
@click.option(
    "--input_currency",
    type=click.STRING,
    required=True,
    help="Input currency. ISO currency code or symbol.",
)
@click.option(
    "--output_currency",
    type=click.STRING,
    help="Output currency. ISO currency code or symbol.",
)
def converter(amount, input_currency, output_currency):
    if output_currency is not None:
        results = convert(amount, input_currency, output_currency)
    else:
        results = convert(amount, input_currency)

    click.echo(json.dumps(results, indent=3))


if __name__ == "__main__":
    converter()
