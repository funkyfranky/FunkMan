"""
FunkMan
=======
Main code to run the discord bot (FunkBot) and UDP socket server (FunkSocket)
"""

from funkman.funkman import FunkMan
from funkman.funkbot.funkbot import FunkBot
from funkman.funksock.funksock import FunkSocket
from time import sleep

if __name__ == "__main__":

    # Welcome!
    print("Hello from FunkMan!")

    if True:
        # Create funkman instance.
        fman=FunkMan()

        # Start bot and socket.
        fman.Start()

    if False:
        from funkman.utils.tests import testTrap, testBomb, testStrafe
        from funkman.funkplot.funkplot import FunkPlot

        funkyplot=FunkPlot()

        #testTrap(funkyplot)
        #testBomb(funkyplot)
        testStrafe(funkyplot)

    if False:
        token="MTAwNTAwMDA0NDc4MjU2MzQ0MQ.GfFrg2.JtrXWtXAWF3DlzOpK-cYN9Ah_sN7us_36wVbN8"
        channelID=1005055301092913172

        fbot=FunkBot(token, channelID)
        fbot.Start()

        fsock=FunkSocket(fbot)
        fsock.Start()

        sleep(10)
        print("Sending bot message")
        fbot.SendMessage("Hello, I am awake now!")





