# investmentcat

The logic for investmentcat can be found in the botutils folder.  It logs interaction to the logs/ folder.

The bot can be started with

    rtmbot

## configuration

Investmentcat uses two configuration files, rtmbot.conf (used to configure the RTMbot framework) and
investmentcat.cfg

### rtmbot.conf
    # Add the following to rtmbot.conf
    DEBUG: True # make this False in production
    SLACK_TOKEN: "xoxb-11111111111-222222222222222"
    ACTIVE_PLUGINS:
        - plugins.greeter.ParserPlugin

### investmentcat.cfg
    [slack]
    channel=CXXXXXXXX
    bot_id=UYYYYYYYY

# investmentcat architecture

# bot architecture

The main script for the bot can be found in bot_engine/investmentcat_bot.py

This script uses several components from the bot_engine module.

## query_parser

This component is responsible for determining the entities and intents that were passed to the bot.

## state_manager

As the bot becomes more complex, it will need to remember the current state of the interaction with the end-user and use that to help drive the interaction.

## executors

The folder bot_engine/executors has a series of functions that handle the execution of incoming requests.  Examples include a module to manage valuations,
one to manage recommendations, and one to handle the low-level interaction with the finance data api.

# Adding new functionality to the bot

Add the new logic to the query parser, adding code to isolate the configuration of tokens and return an intent & entities.

Write the executor, either as a new file under bot_engine/executors or as additional functions in existing files in bot_engine/executors.  The executor is a function that takes whatever parameters it needs to call external logic and returns the full formatted text of the output that will be displayed back to the user.

Import the executor function into the special bot_engine/investmentcat_bot.py file and handle the new intent.

