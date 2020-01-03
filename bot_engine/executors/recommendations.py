from datetime import datetime

from .finance import FinanceAPI, format_significance
from .valuation import Valuation

class Recommendations():
    def undo_formatting(self, value):
        if "B" in value:
            temp = value.replace("B", "")
            numeric = float(temp) * 1000000000
        elif "M" in value:
            temp = value.replace("M", "")
            numeric = float(temp) * 1000000
        else:
            numeric = float(value)
        return int(numeric)

    def get_recommendations(self):
        finance = FinanceAPI()
        valuation = Valuation()
        stock_list = valuation.list_valuations()
        enriched_list = []

        for symbol in stock_list:
            estimate = self.undo_formatting(stock_list[symbol])
            stock_info = finance.get_market_caps([symbol])
            market_cap_raw = stock_info[0][2]
            ratio = int(market_cap_raw) / estimate
            margin_of_safety = (1.0 - ratio)
            enriched_list.append(
                {
                    "symbol": symbol,
                    "market_cap": market_cap_raw,
                    "estimate": estimate,
                    "ratio": ratio,
                    "margin_of_safety": margin_of_safety * 100
                }
            )

        text = ""
        enriched_list = sorted(enriched_list, key = lambda x: x["ratio"])
        for stock in enriched_list:
            symbol = stock["symbol"]
            market_cap = format_significance(stock["market_cap"])
            estimate = format_significance(stock["estimate"])
            margin_of_safety = format_significance(stock["margin_of_safety"])

            text += f"{symbol}:  estimate: {estimate} market cap: {market_cap}"
            text += f" margin of safety: {margin_of_safety}%\n"
        return text

def ask_recommendations():
    rec = Recommendations()
    return rec.get_recommendations()