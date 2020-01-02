"""Create valuations"""
from tinydb import TinyDB, Query
from datetime import datetime

from ..state_manager import StateManager

class Valuation():
    def __init__(self):
        state_db = TinyDB('state_db.json')
        self.state_manager = StateManager(state_db=state_db.table("valuation_table"))

    def add_valuation(self, symbol, valuation):
        cache_key = f"VALUATION_{symbol}"
        cache_value = {
            "symbol": symbol,
            "valuation": valuation,
            "refresh_date": f"{datetime.today().strftime('%Y-%m-%d')}"
        }
        try:
            self.state_manager.save_key_value(cache_key, cache_value)
            return 1
        except Exception as e:
            print(e)
            return f"There was a problem saving valuation {valuation} for symbol {symbol}"

    def get_valuations(self, symbols):
        valuations = []
        for symbol in symbols:
            cache_value = self.state_manager.get_key_value(f"VALUATION_{symbol}")
            if cache_value:
                valuation = cache_value.get("valuation", None)
            else:
                valuation = None
            valuations.append(valuation)
        return valuations

    def list_valuations(self):
        result = {}
        # cached_values = db.all()
        # for value in cached_values:
        #     symbol = value.get("symbol", "")
        #     valuation = value.get("valuation", "")
        #     result[symbol] = valuation
        return result

# class RedisValuation(object):
#     """Access valuations in Redis"""
#     def __init__(self, key="redis"):
#         """Get configurations to open a connection"""
#         conf = Config()
#         self.host = conf[key]['host']
#         self.port = conf[key]['port']
#         self.db_index = conf[key]['db']
#         self.conn = redis.StrictRedis(self.host, self.port, self.db_index)

#     def add_valuation(self, symbol, valuation):
#         """Add valuation for one symbol"""
#         return self.conn.hset("valuation", symbol, valuation)

#     def get_valuations(self, symbols):
#         """Get valuations for a list of symbols"""
#         return self.conn.hmget("valuation", symbols)

#     def list_valuations(self):
#         """List all valuations"""
#         valuations = self.conn.hgetall("valuation")
#         return valuations

# Static conversational methods to simplify access -----------------------------
def ask_add_valuation(entities):
    """Ask to addd a new valuation
    Expects:
        entities[0] => symbol
        entities[1] => valuation"""
    # print entities
    if entities:
        valuation = Valuation()
        response = valuation.add_valuation(entities[0], entities[1])
        if response == 1:
            return "Valuation added for {}".format(entities[0])
        else:
            return "Something went wrong, your valuation was not saved.\n" \
                   "Response: {}".format(response)
    else:
        return "I don't know what you mean.\n" \
               "Please say something like \"Add valuation 123 for PG\""

def ask_get_valuation(entities):
    """Ask to get the valuation for one stock"""
    if entities:
        valuation = Valuation()
        response = valuation.get_valuations(entities)
        if response:
            text = "I found the following valuations:\n"
            for symbol, valuation in zip(entities, response):
                text += "{}: {}\n".format(symbol, valuation or "N/A")
            return text
        else:
            text = "I didn't find those valuations.\n" \
                   "Type \"list valuations\" to list all."
    else:
        return "I don't understand.\n" \
               "Please say something like " \
               "\"Get valuations for PG, KO and MMM\""

def ask_list_valuations():
    """Ask to list all valuations"""
    valuation = Valuation()
    response = valuation.list_valuations()
    if response:
        text = "These are all the valuations I have:\n"
        for symbol in response.keys():
            text += "{}: {}\n".format(symbol, response[symbol])
        return text
    else:
        return "I didn't find any valuations.\n"\
               "Type something like\"Add valuation 123 for PG\" to add a new one."
