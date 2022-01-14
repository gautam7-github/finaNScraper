from flask import Flask, jsonify
from flask.wrappers import Response
from . import scraper


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route("/")
def home():
    return "FinaNScraper - Developed by ProdiGinix"


@app.route("/help/")
def help():
    return """
        <h1>FinaNScraper - HELP</h1>
    """


@app.route("/api/<string:symbol>/")
def getter(symbol):
    data = scraper.main(symbol.upper())
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=False)
