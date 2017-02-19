"""Parses the incoming query into an intent and an optional array of entities"""
import re
from botutils.botlogger import Logger

save_queries = False

log = Logger(logname="investmentcat")

def words_in_string(word_list, string):
    """
    finds all words within a string
    :param word_list:
    :param string:
    :return:
    """
    if all(word in string for word in word_list):
        return True
    else:
        return False

def parse_query(query, state, user):
    """
    parses an incoming query based on the text, the current state, and the user
    :param query:
    :param state:
    :param user:
    :return:
    """
    entities = []
    intent = ""

    log.l("user " + user + " in state " + state + " asked " + query)

    if query == "":
        return intent, entities

    if words_in_string(["hello"], query):
        intent = "GENERIC_HELLO"
    if words_in_string(["hellos"], query):
        intent = "GENERIC_HELLO"
    if words_in_string(["help", ], query):
        intent = "HELP"
    if words_in_string(["market cap"], query):
        intent = "MARKET_CAP"
        find_symbol = re.search(r"(for|of) (\w+)", query)
        if find_symbol:
            symbol = find_symbol.group(2)
            entities.append(symbol)
    if words_in_string(["news"], query):
        intent = "NEWS"
        find_symbol = re.search(r"(on|for) (\w+)", query)
        if find_symbol:
            symbol = find_symbol.group(2)
            entities.append(symbol)
    elif words_in_string(["list valuations"], query):
        intent = "LIST_VALUATIONS"

    elif words_in_string(["add valuation"], query):
        intent = "ADD_VALUATION"
        # remove intent to make it easier to take things apart
        query = query.replace("add valuation", "")
        (val, remaining_query) = get_numeric_part(query)
        # remove prefixes, you should be left with symbol
        symbol = re.sub(r"(of|for)", "", remaining_query).strip()
        if symbol and val:
            entities.append(symbol)
            entities.append(val)

    elif (words_in_string(["get valuation"], query) or
          words_in_string(["get valuations"], query)):
        intent = "GET_VALUATIONS"
        # remove intent to make it easier to take things apart
        remaining_query = re.sub(r"get valuation(s)*", "", query)
        # remove prefixes, you should be left with symbols
        remaining_query = re.sub(r"(of|for)", "", remaining_query)
        remaining_query = remaining_query.replace("and", ",")
        symbols = remaining_query.split(",")
        for symbol in symbols:
            entities.append(symbol.strip())

    log.l("I decided the intent was " + intent)
    if len(entities) > 0:
        log.l("I found entities " + ",".join(entities))
    return (intent, entities)

def get_numeric_part(query):
    """Gets the numeric part in the string
    Returns numeric part and what's left of the string"""
    pattern = r"([0-9.,]+)"
    find_numeric = re.search(pattern, query)
    remaining_query = re.sub(pattern, "", query)
    if find_numeric.groups > 0:
        return (find_numeric.group(0),
                remaining_query)
    else:
        return (None, remaining_query)
