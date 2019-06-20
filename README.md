# Currency converter

## Usage

ISO currency codes and symbols can be found in **currencies.txt**

#### Requirements:

```bash
$ pip install -r requirements.txt
```

#### Web API
app.py

```
GET /currency_converter?amount=100&input_currency=EUR HTTP/1.1
GET /currency_converter?amount=100&input_currency=EUR&output_currency=USD HTTP/1.1
GET /currency_converter?amount=100&input_currency=€ HTTP/1.1
GET /currency_converter?amount=100&input_currency=€&output_currency=Kč HTTP/1.1

```

#### CLI
cli.py

```python
./currency_converter_yk/cli.py --amount 100 --input_currency EUR --output_currency CZK
```

## Development

#### Requirements
Install dev requirements
```bash
$ pip install -r dev-requirements.txt
```

#### Tests
[`pytest`](https://docs.pytest.org/en/latest/py) is used to run tests. To check application status run:
```python
pytest
```

---

Code analysis is done by [`pylint`](https://www.pylint.org):
```python
pylint *.py
```

Code formatting is done by [`black`](https://black.readthedocs.io/en/stable/):
```python
black *.py
```