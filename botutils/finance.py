"""Gets financial data"""
import json
import re
from myql.contrib.finance.stockscraper import StockRetriever

def ask_market_cap(query):
    """Interpret a query for market cap.
    Right now I'm pretty dumb, so I'm using regex to find the symbol in a phrase"""
    find_symbol = re.search(r"(for|of) (\w+)", query)
    if find_symbol:
        symbol = find_symbol.group(2)
        stock = get_stock_info(symbol)

        if stock and stock['MarketCapitalization']:
            return "Market cap for {} is {}".format(stock['symbol'],
                                                    stock['MarketCapitalization'])
        else:
            return "I can't find the information for {}. "\
                   "Please use the stock symbol to ask me questions.".format(symbol)
    else:
        return "I don't know which stock you mean, please say something like 'market cap for AMZN'"

def ask_news(query):
    """Interpret a query for news for a stock"""
    find_symbol = re.search(r"(on|for) (\w+)", query)
    if find_symbol:
        symbol = find_symbol.group(2)
        news = get_news_feed(symbol)
        if news:
            return news
        else:
            return "I don't have any news for you."
    else:
        return "I don't know what you mean :("

def get_stock_info(symbol):
    """Retrive a stock's information
    For documentation on StockRetriever methods, please refer to:
    https://myql.readthedocs.io/en/latest/stockscraper/"""
    stocks = StockRetriever(format='json', debug=False)
    response = stocks.get_current_info([symbol])
    data = json.loads(response.content)
    # print data
    try:
        stock = data['query']['results']['quote']
        # print stock
        return stock
    except ValueError, exception:
        print exception
        return None

def get_news_feed(symbol):
    """Get latest news on a stock"""
    stocks = StockRetriever(format='json', debug=False)
    response = stocks.get_news_feed(symbol)
    data = json.loads(response.content)
    try:
        news = data['query']['results']['item']
    except ValueError, exception:
        print exception
        return None

    result = []
    for item in news:
        url_parts = item['link'].split("*") #strip the yahoo prefix url
        result.append(url_parts[len(url_parts)-1])

    return "\n".join(result)
