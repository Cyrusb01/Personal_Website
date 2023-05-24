from datetime import datetime

from flask import render_template

from app import app
from app.scrape import get_coinbase_assets, get_eth_assets, get_sol_assets


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/portfolio", methods=["GET", "POST"])
def portfolio():

    # Fetch data once a day from apis and cache it
    today = datetime.now().strftime("%Y/%m/%d")
    try:
        sol_tokens = get_sol_assets(today)  # Returns list
    except:
        sol_tokens = []
    try:
        eth_tokens = get_eth_assets(today)  # Returns dict
    except:
        eth_tokens = {}
    try:

        coinbase_tokens = get_coinbase_assets(today)  # Returns dict
    except:
        coinbase_tokens = {}
    # Sorts coinbase Tokens by value

    eth_tickers = list(eth_tokens.keys())
    coinbase_tickers = [token["asset"] for token in coinbase_tokens]
    sol_tickers = sol_tokens

    pie_data = [
        {"name": coinbase_tokens["asset"], "y": coinbase_tokens["allocation"]}
        for coinbase_tokens in coinbase_tokens
    ]
    print(pie_data)

    return render_template(
        "portfolio.html",
        pie_data=pie_data,
        eth_l=len(eth_tickers),
        eth_tickers=eth_tickers,
        sol_l=len(sol_tickers),
        sol_tickers=sol_tickers,
        cb_l=len(coinbase_tickers),
        cb_tickers=coinbase_tickers,
    )


@app.route("/trading")
def trading():
    return render_template("trading.html")
