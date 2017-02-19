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

    log.l("I decided the intent was " + intent)
    if len(entities) > 0:
        log.l("I found entities " + ",".join(entities))
    return (intent, entities)
