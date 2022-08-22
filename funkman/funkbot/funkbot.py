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

        # Debug tests.
        if False:
            from funkman.utils.tests import testTrap, testBomb, testStrafe
            from funkman.funkplot.funkplot import FunkPlot

            funkyplot=FunkPlot()

            f1, a1=testTrap(funkyplot)
            #f2, a2=testBomb(funkyplot)
            #f3, a3=testStrafe(funkyplot)

            self.SendFig(f1)
            #self.SendFig(f2)
            #self.SendFig(f3)

    def _Start(self):
        """ Start the Discord bot in it's own thread"""

        # Info message.
        print("Starting threaded discord bot!")

        # Start thread.
        discordThread=threading.Thread(target=self.Start)
        discordThread.start()

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