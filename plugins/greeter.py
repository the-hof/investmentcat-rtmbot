from __future__ import print_function
from __future__ import unicode_literals

from rtmbot.core import Plugin
from botutils.config import Config

import botutils.query_parser as q
import botutils.state_manager as state_manager

import botutils.finance as finance
import botutils.valuation as v

conf = Config()
slack_channel = conf['slack']['channel']
bot_id = str(conf['slack']['bot_id'])

class ParserPlugin(Plugin):

    def process_message(self, data):
        print (data)
        #only react when specifically addressed in a channel we're monitoring
        if bot_id in data.get('text', '') and data.get('channel', '') == slack_channel:
            input = data['text'].replace("<@" + bot_id + ">", "").strip()
            user = data['user']

            output = "meow"

            state = state_manager.get_user_state(user)

            (intent, entities) = q.parse_query(input, state, user)

            if intent == "GENERIC_HELLO":
                output = "hello"
                state = "IDLE"
            elif intent == "HELP":
                output = "I am here to help you manage your investment research.\n" \
                        "Here are some examples of things you can ask me:\n" \
                        "*Market*\n" \
                        "\"what's the news on AMZN\"\n" \
                        "\"give me the market cap for KO, PG and ABEV\"\n" \
                        "*Valuations*\n" \
                        "\"add valuation 123 for MMM\"\n" \
                        "\"list valuations\"\n" \
                        "\"get valuation for GE, PG and JNJ\""
                state = "IDLE"
            elif intent == "MARKET_CAP":
                if len(entities) > 0:
                    output = finance.ask_market_cap(entities)
                else:
                    output = "I don't know which stock you mean, please say something like 'market cap for AMZN'"
            elif intent == "NEWS":
                if len(entities) > 0:
                    output = finance.ask_news(entities[0])
                else:
                    output = "I don't know what you mean :("
            elif intent == "ADD_VALUATION":
                output = v.ask_add_valuation(entities)
            elif intent == "GET_VALUATIONS":
                output = v.ask_get_valuation(entities)
            elif intent == "LIST_VALUATIONS":
                output = v.ask_list_valuations()

            self.outputs.append([data['channel'],output])
