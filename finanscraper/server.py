from flask import Flask, jsonify, render_template
from finanscraper.scraper import Choice
import scraper


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/help/")
def help():
    return """
        <h1>FinaNScraper - HELP</h1>
    """


@app.route("/api/data/<string:symbol>/all")
def getter(symbol):
    data = scraper.main(symbol.upper(), choice=Choice.all)
    return jsonify(data)


# @app.route("api/data/<string:symbol>/financials")
# def fngetter(symbol):
#     data = scraper.main(symbol.upper(), choice=Choice.financials)
#     return jsonify(data)


# @app.route("api/data/<string:symbol>/balance-sheet")
# def bshgetter(symbol):
#     data = scraper.main(symbol.upper(), choice=Choice.balance_sheet)
#     return jsonify(data)


# @app.route("api/data/<string:symbol>/cash-flow")
# def cflwgetter(symbol):
#     data = scraper.main(symbol.upper(), choice=Choice.cash_flow)
#     return jsonify(data)


if __name__ == "__main__":
    app.run(debug=False)
