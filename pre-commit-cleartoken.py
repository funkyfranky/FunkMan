"""
Clears out the Discord Bot Token as we do not want it on the github repo
"""

import configparser

config_file: str = "./FunkMan.ini"

comment_string = """#--------------------------------------------------------------------------------------
# FUNKMAN Config File
# ===================
# The config file consists of multiple section each starting with square brackets.
#
# [DEFAULT] This sections contains a parameter for debugging:
#  DEBUGLEVEL: Set a level for debug output {0 - ~}
#  DEBUG: If True, debug logging enabled.
#
# [FUNKBOT] This section contains information about the Discord bot parmeters:
#  TOKEN: Is the secret (!) token of the bot.
#  CHANNELID_MAIN: The main channel ID used for all messages by default.
#  CHANNELID_RANGE: (Optional) Channel ID where RANGE messages are send to.
#  CHANNELID_AIRBOSS: (Optional) Channel ID where AIRBOSS messages are send to.
#
# [FUNKSOCK] This section contains information about the UDP socket:
#  PORT: UDP Port. Default is 10042.
#  HOST: Host name. Default is 127.0.0.1.
#
# [FUNKPLOT] This section contains information for plotting images.
#  IMAGEPATH: Directory where the necessary images are stored.
#--------------------------------------------------------------------------------------

"""

config = configparser.ConfigParser()
config.read(config_file)

try:
    if config["FUNKBOT"]["TOKEN"] != "YOUR_BOT_TOKEN_HERE":
        config["FUNKBOT"]["TOKEN"] = "YOUR_BOT_TOKEN_HERE"

        with open(config_file, "w") as configfile:
            configfile.write(comment_string)
            config.write(configfile)

except Exception as e:
    pass
