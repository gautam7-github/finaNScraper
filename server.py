from flask import Flask, jsonify
from flask.wrappers import Response
from . import scraper
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route("/")
def home():
    return "FinaNScraper"


@app.route("/help/")
def help():
    return """
        <h1>FinaNScraper - HELP</h1>
    """


@app.route("/api/<string:symbol>/")
def getter(symbol):
    data = scraper.main(symbol.upper())
    return jsonify(data)


# json.loads(jsonn)[0]['financials']['ttm'] - working
app.run()
