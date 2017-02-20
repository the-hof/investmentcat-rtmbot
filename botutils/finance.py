"""Gets financial data"""
import json
from myql.contrib.finance.stockscraper import StockRetriever

def ask_market_cap(symbols):
    """Interpret a query for market cap."""
    stocks = get_stock_info(symbols)

    if stocks:
        text = ""
        for stock in stocks:
            if stock['MarketCapitalization']:
                text += ("Market cap for {} is {}\n"
                         .format(stock['symbol'],
                                 stock['MarketCapitalization']))
            else:
                text += ("I can't find the information for {}.\n"
                         .format(stock['symbol']))
    return text

def ask_news(symbol):
    """Interpret a query for news for a stock"""
    news = get_news_feed(symbol)
    if news:
        return news
    else:
        return "I don't have any news for you."

def get_stock_info(symbols):
    """Retrive information for multiple stocks
    For documentation on StockRetriever methods, please refer to:
    https://myql.readthedocs.io/en/latest/stockscraper/"""
    stocks = StockRetriever(format='json', debug=False)
    response = stocks.get_current_info(symbols)
    data = json.loads(response.content)
    # print data
    try:
        if isinstance(data['query']['results']['quote'], list):
            stocks = data['query']['results']['quote']
        else:
            print "this is an object!"
            stocks = []
            stocks.append(data['query']['results']['quote'])
        return stocks
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
