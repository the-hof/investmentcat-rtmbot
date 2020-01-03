from rtmbot.core import Plugin
from .executors.config import Config

from .state_manager import StateManager
from . import query_parser


from .executors.finance import ask_market_cap, ask_news
from .executors.valuation import ask_add_valuation, ask_get_valuation, ask_list_valuations
from .executors.recommendations import ask_recommendations
import traceback

class InvestmentCatBotPlugin(Plugin):
    def process_message_internal(self, data):
        conf = Config()
        slack_channel = conf['slack']['channel']
        bot_id = str(conf['slack']['bot_id'])

        print (f"data = {data}")
        #only react when specifically addressed in a channel we're monitoring
        if bot_id in data.get('text', '') and data.get('channel', '') == slack_channel:
            input = data['text'].replace("<@" + bot_id + ">", "").strip()
            user = data.get("user", "")
            print (f"got user {user}")

            output = "meow"

            state_manager = StateManager()
            state = state_manager.get_user_state(user)
            current_state = state.get("conversation_state", "")
            next_state = state.get("conversation_state", "")

            print (f"user is in state {current_state}")

            (intent, entities) = query_parser.parse_query(input, current_state, user)

            if intent == "GENERIC_HELLO":
                output = "hello"
                next_state = "IDLE"
            elif intent == "HELP":
                output = "I am here to help you manage your investment research.\n" \
                        "Here are some examples of things you can ask me:\n" \
                        "*Market*\n" \
                        "\"give me the market cap for KO, PG and ABEV\"\n"
                output += "*Valuations*\n" \
                        "\"add valuation 123 for MMM\"\n" \
                        "\"list valuations\"\n" \
                        "\"get valuation for GE, PG and JNJ\"\n"
                output += "*Research Analysis*\n" \
                        "\"recommendations\"\n"

                next_state = "IDLE"
            elif intent == "MARKET_CAP":
                if len(entities) > 0:
                    output = ask_market_cap(entities)
                else:
                    output = "I don't know which stock you mean, please say something like 'market cap for AMZN'"
            elif intent == "NEWS":
                if len(entities) > 0:
                    output = ask_news(entities[0])
                else:
                    output = "I don't know what you mean :("
            elif intent == "ADD_VALUATION":
                output = ask_add_valuation(entities)
            elif intent == "GET_VALUATIONS":
                output = ask_get_valuation(entities)
            elif intent == "LIST_VALUATIONS":
                output = ask_list_valuations()
            elif intent == "RECOMMENDATIONS":
                output = ask_recommendations()

            state.update({"conversation_state": next_state})

            state_manager.save_user_state(user, state)

            self.outputs.append([data['channel'],output])

    def process_message(self, data):
        try:
            self.process_message_internal(data)
        except Exception as e:
            print (e)
            traceback.print_exc()
