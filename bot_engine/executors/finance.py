"""Gets financial data"""
import json
import requests
from datetime import datetime
from .config import Config

from ..state_manager import StateManager

class FinanceAPI():
    def __init__(self):
        conf = Config()
        self.api_key = conf["worldtradingdata"]["api_key"]
        self.api_base = "https://api.worldtradingdata.com/api/v1/stock"
        self.state_manager = StateManager()

    def make_stock_request(self, symbols):
        if symbols == []:
            return []
        symbol_string = ",".join(symbols)
        print (f"... making api request for {symbol_string}")
        url = f"{self.api_base}?symbol={symbol_string}&api_token={self.api_key}"
        print (f"... request url = {url}")
        try:
            response = requests.get(url).json()
            print(response)
            return response['data']
        except Exception as e:
            print(e)

    def get_market_caps(self, symbols):
        """Interpret a query for market cap.

        Returns
        -------
          List of tuple (symbol, name, market_cap_raw, market_cap)
        """
        uncached_symbols = []
        stocks = []
        for symbol in symbols:
            state_manager = StateManager()
            stock_data = state_manager.get_key_value(f"SYMBOL_{symbol}")
            if stock_data != {}:
                print(f"using cached data for {symbol}")
                stocks.append(stock_data)
            else:
                uncached_symbols.append(symbol)
        try:
            stocks += self.make_stock_request(uncached_symbols)
        except Exception as e:
            print (e)

        market_cap_return = []
        if stocks:
            for stock in stocks:
                symbol = stock.get("symbol", "")
                print (f"... evaluating stock data for {symbol}")
                market_cap_raw = stock.get("market_cap", -1)
                print (f"... market cap = {market_cap_raw}")
                market_cap = format_significance(market_cap_raw)
                print (f"... market cap = {market_cap}")
                name = stock.get("name", "")

                try:
                    cache_key = f"SYMBOL_{symbol}"
                    cache_value = {
                        "symbol": symbol,
                        "market_cap": market_cap_raw,
                        "name": name,
                        "refresh_date": f"{datetime.today().strftime('%Y-%m-%d')}"
                    }
                except Exception as e:
                    print (e)

                try:
                    state_manager.save_key_value(cache_key, cache_value)
                except Exception as e:
                    print (e)

                if int(market_cap_raw) > 0:
                    market_cap_return.append((symbol, name, market_cap_raw, market_cap))

        return market_cap_return

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
    market_caps = FinanceAPI().get_market_caps(symbols)
    text = ""
    for (symbol, name, market_cap_raw, market_cap) in market_caps:
        text += f"Market cap for {name} ({symbol}) is {market_cap}\n"
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
