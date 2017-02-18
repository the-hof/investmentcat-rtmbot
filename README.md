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

The main script for the investmentcat bot can be found in plugins/greeter.py

This script uses several components from the botutils module.

## query_parser

This component is responsible for determining the entities and intents that were passed to investmentcat.

## state_manager

As investmentcat becomes more complex, it will need to remember the current state of the interaction with
the end-user and use that to help drive the interaction.  