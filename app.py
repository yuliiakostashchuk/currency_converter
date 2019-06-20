import flask
from flask import jsonify
from webargs import fields
from webargs.flaskparser import use_args

from utils import convert

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route("/", methods=["GET"])
def home():
    return """<h1>Currency Converter</h1>
<p>A prototype API for exchanging your money for another currency.</p>"""


conv_args = {
    "amount": fields.Float(required=True),
    "input_currency": fields.Str(required=True),
    "output_currency": fields.Str(),
}


@app.route("/currency_converter", methods=["GET"])
@use_args(conv_args)
def converter(args):

    amount = args["amount"]
    input_currency = args["input_currency"]
    if args.get("output_currency"):
        output_currency = args["output_currency"]
        results = convert(amount, input_currency, output_currency)
    else:
        results = convert(amount, input_currency)

    return jsonify(results)


if __name__ == "__main__":
    app.run()
