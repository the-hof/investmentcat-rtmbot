from __future__ import print_function
from __future__ import unicode_literals

from rtmbot.core import Plugin
from botutils.config import Config

import botutils.query_parser as q
import botutils.state_manager as state_manager

import botutils.finance as finance

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
                output = "I am here to help you manage your investment research.  " \
                        "Ask me something like \"what's the news on AMZN\" or "\
                        "\"give me the market cap for PG\""
                state = "IDLE"
            elif intent == "MARKET_CAP":
                output = finance.ask_market_cap(input)
            elif intent == "NEWS":
                output = finance.ask_news(input)

            self.outputs.append([data['channel'],output])
