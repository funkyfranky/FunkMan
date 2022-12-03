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
from .funkbot.funkbot import FunkBot

import os
import configparser

from logger import logger

log = logger.logging.getLogger(__name__)


class FunkMan:
    def __init__(self, ConfigFile="./FunkMan.ini") -> None:

        # Set config file.
        self.configFile: str = ConfigFile

        # Define parameters used later on.
        self.port: int
        self.host: str
        self.token: str
        self.channelIDmain: int
        self.channelIDrange: int
        self.channelIDairboss: int
        self.imagePath: str

        # Default debug level.
        self.debugLevel: int = 0
        self.debug: bool = False

        # Read config file.
        _ReadConfig(self)

        # Create funkplot instance.
        self.funkplot = FunkPlot(self.imagePath)

        # Create funkbot instance.
        self.funkbot = FunkBot(self.token, self.channelIDmain, ImagePath=self.imagePath, DebugLevel=self.debugLevel)

        # Create funksocket instance.
        self.funksock = FunkSocket(Host=self.host, Port=self.port)

        # Set Bot.
        self.funksock.SetFunkBot(self.funkbot)

        # Set Plot.
        self.funksock.SetFunkPlot(self.funkplot)

        # Set message channel ID.
        self.funksock.SetChannelIdMessage(self.channelIDmain)

        # Set channel ID for range data.
        self.funksock.SetChannelIdRange(self.channelIDrange)

        # Set channel ID for airboss data.
        self.funksock.SetChannelIdAirboss(self.channelIDairboss)

    def SetCallbackStart(self, Func, *argv, **kwargs):
        """Callback function called at start."""
        log.debug("callback fman")
        log.debug(argv)
        self.funkbot.SetCallbackStart(Func, *argv, **kwargs)

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

    # Info message.
    log.info(f"Reading config file {funkman.configFile}")

    # Check if config file exists
    try:
        os.path.exists(funkman.configFile)
    except FileNotFoundError:
        log.critical(f"Could not find ini file {funkman.configFile} in {os.getcwd()}!")
        quit()

    # Config parser.
    config = configparser.ConfigParser()

    # Read config file.
    config.read(funkman.configFile)

    # DEBUG
    try:
        section = config["DEFAULT"]
        funkman.debug = section.getboolean("DEBUG", False)

        # Set the root logger log level based on value from ini file.
        if funkman.debug:
            logger.logging.getLogger().setLevel(logger.logging.DEBUG)
        else:
            logger.logging.getLogger().setLevel(logger.logging.INFO)
    except:
        pass

    # FUNKMAN
    try:
        section = config["DEFAULT"]
        funkman.debugLevel = section.getint("DEBUGLEVEL", 0)
    except:
        pass

    # FUNKBOT
    try:
        section = config["FUNKBOT"]
        funkman.token = section.get("TOKEN", "FROM_OS_ENV")
        funkman.channelIDmain = section.getint("CHANNELID_MAIN", 123456789)
        funkman.channelIDrange = section.getint("CHANNELID_RANGE", funkman.channelIDmain)
        funkman.channelIDairboss = section.getint("CHANNELID_AIRBOSS", funkman.channelIDmain)
    except:
        log.error("ERROR: [FUNKBOT] section missing in ini file!")

    # FUNKSOCK
    try:
        section = config["FUNKSOCK"]
        funkman.port = section.getint("PORT", 10042)
        funkman.host = section.get("HOST", "127.0.0.1")
    except:
        log.error("ERROR: [FUNKSOCK] section missing in ini file!")

    # FUNKPLOT
    try:
        section = config["FUNKPLOT"]
        funkman.imagePath = section.get("IMAGEPATH", "./funkpics/")
    except:
        log.error("ERROR: [FUNKPLOT] section missing in ini file!")

    # Debug message.
    if funkman.debug:
        text = str(f"\n------------------------------------")
        text += str(f"\nConfig parameters:")
        text += str(f"\nDebug level     = {funkman.debugLevel}")
        text += str(f"\nDebug           = {funkman.debug}")
        text += str(f"\nHost            = {funkman.host}")
        text += str(f"\nPort            = {funkman.port}")
        text += str(f"\nToken (5 chars) = {funkman.token[0:4]}...")
        text += str(f"\nChannel Main    = {funkman.channelIDmain}")
        text += str(f"\nChannel Range   = {funkman.channelIDrange}")
        text += str(f"\nChannel Airboss = {funkman.channelIDairboss}")
        text += str(f"\nImage Path      = {funkman.imagePath}")
        text += str(f"\n------------------------------------")
        log.debug(text)
