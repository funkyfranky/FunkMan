"""
FunkMan
=======

FunkMan is a package that establishes a connection between DCS and Discord
via an UDP socket.

Features:
- Send simple text messages.
- Send pictures.
- Interface with AIRBOSS class to show LSO grades and trap sheets
- Interface with RANGE class to show bombing and strafing results

"""

from .funkplot.funkplot import FunkPlot
from .funksock.funksock import FunkSocket
from .funkbot.funkbot   import FunkBot

import os
import configparser

class FunkMan():
    
    def __init__(self, ConfigFile="./FunkMan.ini") -> None:

        # Set config file.
        self.ConfigFile=ConfigFile
    
        # Define parameters used later on.
        self.port=None
        self.host=None
        self.token=None
        self.channelID=None

        # Read config file.
        _ReadConfig(self)

        # Create funkplot instance.
        self.funkplot=FunkPlot()

        # Create funkbot instance.
        self.funkbot=FunkBot(self.token, self.channelID)

        # Create funksocket instance.
        self.funksock=FunkSocket(Host=self.host, Port=self.port)

        # Set Bot.
        self.funksock.SetFunkBot(self.funkbot)

        # Set Plot.
        self.funksock.SetFunkPlot(self.funkplot)
        

    def Start(self):
        """
        Start socket and bot.
        """
        self.funkbot.Start(True)
        self.funksock.Start()
        

def _ReadConfig(funkman: FunkMan) -> None:
    """
    Reads the config file.
    """

    # Get the current working directory
    cwd = os.getcwd()

    # Print the current working directory
    print("Current working directory: {0}".format(cwd))

    # Check if config file exists
    file_exists = os.path.exists(funkman.ConfigFile)

    if file_exists:
        pass
    else:
        print(f"ERROR: Could not find ini file {funkman.ConfigFile}!")
        quit()

    # Config parser.
    config = configparser.ConfigParser()

    # Read config file.
    config.read(funkman.ConfigFile)

    # Section name of config.
    SectionName="FUNKMAN"

    # Get config parameters:
    funkman.port=int(config[SectionName]['PORT'])
    funkman.host=str(config[SectionName]['HOST'])
    funkman.token=config[SectionName]['TOKEN']
    funkman.channelID=int(config[SectionName]['CHANNELID'])

    # Debug message.
    text =str(f"------------------------------------")
    text+=str(f"\nReading config file:")
    text+=str(f"\nPort={funkman.port}")
    text+=str(f"\nHost={funkman.host}")
    text+=str(f"\nToken={funkman.token}")
    text+=str(f"\nChannel={funkman.channelID}")
    text+=str(f"\n------------------------------------")
    print(text)