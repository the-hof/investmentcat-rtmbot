import ConfigParser
import os, sys
import base64


def Config(config_name='investmentcat'):
    """
    reads config file and returns a dictionary of config objects
    also handles basic password decryption
    :param conf_path:
    :return:
    """
    conf_path=config_name + '.cfg'
    config = ConfigParser.ConfigParser()
    config.read(conf_path)
    dictionary = {}
    for section in config.sections():
        dictionary[section] = {}
        for option in config.options(section):
            val = config.get(section, option)
            if str(option).lower() in ('pwd', 'password'):
                val = base64.b64decode(val)
            dictionary[section][option] = val
    return dictionary