"""
FunkBot

See https://discordpy.readthedocs.io/en/stable/
"""

import discord
import threading
import matplotlib.pyplot as plt
import io

class FunkBot(discord.Client):
    """
    API class wrapper for Discord based on discord.py.
    """

    def __init__(self, Token: str, ChannelID: int):

        # Init discord.Client superclass.
        super().__init__()

        # Get config parameters:
        self.token=str(Token)
        self.channelID=int(ChannelID)

    def SetCallbackStart(self, Func, *argv, **kwargs):
        """Callback function called at start."""
        print("call back fbot")
        print(argv)
        self.callbackStartFunc=Func
        self.callbackStartArgv=argv
        self.callbackStartKarg=kwargs

    async def on_ready(self):
        """
        Event when connected to server.
        """
        # Get channel.
        try:
            self.channel=self.get_channel(self.channelID)
        except:
            print(f"ERROR: Could not get channel with ID={self.channelID}")

        # Info that bot is online and ready.
        print('Connected as {0.name} [ID: {0.id}]'.format(self.user))

        # Set message to channel.
        await self.SendMessage("FunkBot reporting for duty!", self.channelID)

        # Call back function.
        #try:
        #print("Call back")
        #self.callbackStartFunc(self.callbackStartArgv, self.callbackStartKarg)
        #except:
        #    print("No callback!")
        #    pass

        # Debug tests.
        if False:
            from funkman.utils.tests import testTrap, testBomb, testStrafe
            from funkman.funkplot.funkplot import FunkPlot

            funkyplot=FunkPlot()

            # Test trap.
            f1, a1=testTrap(funkyplot)
            self.SendFig(f1, self.channelID)

            # Test bomb.
            f2, a2=testBomb(funkyplot)
            self.SendFig(f2, self.channelID)

            # Test strafe.
            f3, a3=testStrafe(funkyplot)            
            self.SendFig(f3, self.channelID)

    def Start(self, Threaded=False):
        """
        Connect to server using the token.
        """
        if Threaded:
            print("Starting threaded discord bot!")
            discordThread=threading.Thread(target=self.Start, args=(False, ))
            discordThread.start()
        else:
            print(f"Starting Bot Client with Token {self.token}")
            self.run(self.token)

    async def SendMessage(self, Text: str, ChannelID: int):
        """
        Async send text message to channel.
        """
        channel=self.get_channel(ChannelID)
        await channel.send(Text)

    def SendText(self, Text: str, ChannelID: int):
        """
        Send text message to channel using loop.create_task().
        """
        channel=self.get_channel(ChannelID)
        try:
            self.loop.create_task(channel.send(Text))
        except:
            print("ERROR: Could not send text!")

    def SendDiscordFile(self, DiscordFile: discord.File, ChannelID: int):
        """
        Send discord file.
        """
        channel=self.get_channel(ChannelID)
        self.loop.create_task(channel.send(file=DiscordFile))

    def SendIO(self, DataStream: io.BytesIO, ChannelID: int):
        """
        Send text message to channel using loop.create_task().
        """
        try:
            # Rewind stream.
            DataStream.seek(0)

            # Create data stream.
            file= discord.File(DataStream, filename="funkbot.png", spoiler=False)
            
            # Send discord file.
            self.SendDiscordFile(file, ChannelID)
        except:
            print("ERROR: Could not send text!")

    def SendFig(self, fig, ChannelID: int):
        """
        Set matplotlib fig object.
        """

        # Create io.
        data_stream=io.BytesIO()

        # Seve figure in data stream.
        #fig.savefig(data_stream, format='png', bbox_inches="tight", dpi=150)
        fig.savefig(data_stream, format='png')

        # Close figure.
        plt.close(fig)

        # Send data stream.
        self.SendIO(data_stream, ChannelID)