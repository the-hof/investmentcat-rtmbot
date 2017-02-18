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
    if words_in_string(["news"], query):
        intent = "NEWS"

    log.l("I decided the intent was " + intent)
    return (intent, entities)
