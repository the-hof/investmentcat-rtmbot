"""Parses the incoming query into an intent and an optional array of entities"""
import re

save_queries = False

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

    print("user " + user + " in state " + state + " asked " + query)

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
        symbols = re.sub(r".* (for|of)", "", query)
        symbols = symbols.replace("and", ",")
        for symbol in symbols.split(","):
            entities.append(symbol.strip())
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

    elif (words_in_string(["analysis"], query) or
          words_in_string(["recommendations"], query)):
          intent = "RECOMMENDATIONS"

    print("I decided the intent was " + intent)
    if len(entities) > 0:
        print("I found entities " + ",".join(entities))
    return (intent, entities)

def get_numeric_part(query):
    """Gets the numeric part in the string
    Returns numeric part and what's left of the string"""

    # test for pattern of 123B and convert to billions
    raw_number_pattern = r"([0-9.,]+[bB]{1})"
    find_numeric = re.search(raw_number_pattern, query)
    remaining_query = re.sub(raw_number_pattern, "", query)
    if find_numeric is not None:
        if len(find_numeric.groups()) > 0:
            retval = find_numeric.group(0)
            retval = retval.replace("b", "000000000")
            retval = retval.replace("B", "000000000")
            return (retval,
                    remaining_query)

    # test for pattern of 123M and convert to millions
    raw_number_pattern = r"([0-9.,]+[mM]{1})"
    find_numeric = re.search(raw_number_pattern, query)
    remaining_query = re.sub(raw_number_pattern, "", query)
    if find_numeric is not None:
        if len(find_numeric.groups()) > 0:
            retval = find_numeric.group(0)
            retval = retval.replace("m", "000000")
            retval = retval.replace("M", "000000")
            return (retval,
                    remaining_query)

    # test for unsuffixed number and pass through
    raw_number_pattern = r"([0-9.,]+)"
    find_numeric = re.search(raw_number_pattern, query)
    remaining_query = re.sub(raw_number_pattern, "", query)
    if find_numeric is not None:
        if len(find_numeric.groups()) > 0:
            return (find_numeric.group(0),
                    remaining_query)
    return (None, remaining_query)

