"""Gets financial data"""
import json
import requests
from .config import Config

from math import log10, floor

class Finance():
    def __init__(self):
        conf = Config()
        self.api_key = conf["worldtradingdata"]["api_key"]
        self.api_base = "https://api.worldtradingdata.com/api/v1/stock"

    def make_api_request(self, symbols):
        symbol_string = ",".join(symbols)
        print (f"... making api request for {symbol_string}")
        url = f"{self.api_base}?symbol={symbol_string}&api_token={self.api_key}"
        print (f"... request url = {url}")
        try:
            response = requests.get(url).json()
            return response['data']
        except Exception as e:
            print(e)

def format_significance(number, significance=2):
    work_number = int(number)
    suffix = ""
    if work_number > 1000000000:
        work_number = work_number / 1000000000
        suffix = "B"
    elif work_number > 1000000:
        work_number = work_number / 1000000
        suffix = "M"
    sig_string = f"%.{significance}g"
    display_number = '%s' % float(sig_string % work_number)
    rounded = display_number + suffix
    return rounded

def ask_market_cap(symbols):
    """Interpret a query for market cap."""
    try:
        stocks = Finance().make_api_request(symbols)
    except Exception as e:
        print (e)

    if stocks:
        text = ""
        for stock in stocks:
            symbol = stock.get("symbol", "")
            print (f"... evaluating stock data for {symbol}")
            market_cap_raw = stock.get("market_cap", -1)
            print (f"... market cap = {market_cap_raw}")
            market_cap = format_significance(market_cap_raw)
            print (f"... market cap = {market_cap}")

            if int(market_cap_raw) > 0:
                text += f"Market cap for {symbol} is {market_cap}\n"
            else:
                text += f"I can't find the information for {symbol}.\n"
    print (f"final text = {text}")
    return text

def ask_news(symbol):
    """Interpret a query for news for a stock"""
    news = get_news_feed(symbol)
    if news:
        return news
    else:
        return "I don't have any news for you."

def get_news_feed(symbol):
    return None
