import os

import ccxt
import requests
import yfinance as yf
from app import cache


@cache.memoize(timeout=86400)
def get_coinbase_assets(date):
    print("Getting Coinbase Assets")
    api_key = os.getenv("CB_KEY")
    api_secret = os.getenv("CB_SECRET")
    passphrase = os.getenv("CB_PASSPHRASE")
    
    # client = Client(api_key, api_secret)
    exchange_class = getattr(ccxt, "coinbase")
    ccxt_object = exchange_class(
        {"apiKey": api_key, "secret": api_secret, "password": passphrase}
    )

    raw_balances = ccxt_object.fetch_balance()
    # print(raw_balances)

    for balance in raw_balances["free"]:
        print(balance)

    positive_balances = [
        {"asset": asset, "balance": float(raw_balances["free"][asset]),}
        for asset in raw_balances["free"]
        if float(raw_balances["free"][asset]) > 0
    ]

    print(positive_balances)
    total_value = 0
    for balance in positive_balances:
        ticker = balance["asset"]
        amount = balance["balance"]

        try:
            ticker_info = ccxt_object.fetch_ticker(ticker + "/USD")
            price = float(ticker_info["last"])
        except:
            try:
                ticker_info = ccxt_object.fetch_ticker(ticker + "/USDT")
                price = float(ticker_info["last"])
            except:
                pass
        if ticker == "USD" or ticker == "USDT" or ticker == "USDC" or ticker == "USDB":
            price = 1

        balance["price"] = price
        balance["value"] = price * amount
        total_value += balance["value"]

    positive_balances = [
        {"asset": balance["asset"], "allocation": balance["value"] / total_value}
        for balance in positive_balances
    ]
    print("Done")
    return positive_balances


@cache.memoize(86400)
def get_eth_assets(date):
    print("Getting ETH Assets")
    ETHERSCAN_API = os.getenv("ETHERSCAN_API")
    address = "0x6B6372D6d785752688461cB41b08D155914f42D7"
    ether_call = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={ETHERSCAN_API}"
    response = requests.get(ether_call)
    response_dict = response.json()
    # print(response_dict)

    df = yf.download("ETH-USD")
    latest_eth = df["Close"][-1]
    eth_assets = {}
    eth_assets["ETH"] = (float(response_dict["result"]) * 10 ** -18) * latest_eth
    # print(eth_assets)
    print("Done")
    return eth_assets


@cache.memoize(86400)
def get_sol_assets(date):
    print("Getting SOL Assets")
    address = "9zQQvGgDNF57Givi2AVLpaydWNPYgmQhDkxZsxnc3hNj"
    ether_call = f"https://public-api.solscan.io/account/tokens?account={address}"
    response = requests.get(ether_call)
    print(response)
    response_dict = response.json()
    tokens = []
    for response in response_dict:
        try:
            # print(response["tokenSymbol"])
            tokens.append(response["tokenSymbol"])
        except:
            pass

    print("Done")
    return tokens
