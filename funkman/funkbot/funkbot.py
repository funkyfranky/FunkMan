"""
FunkBot

See https://discordpy.readthedocs.io/en/stable/
"""

import discord
import threading
import matplotlib.pyplot as plt
import io

# This should be used instead of the discord.Client
#from discord.ext.commands import Bot

#TOKEN="MTAwNTAwMDA0NDc4MjU2MzQ0MQ.GfFrg2.JtrXWtXAWF3DlzOpK-cYN9Ah_sN7us_36wVbN8"


class FunkBot(discord.Client):

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

        print('Connected as {0.name} [ID: {0.id}]'.format(self.user))

        # Set message to channel.
        await self.SendMessage("FunkBot reporting for duty!")

        if True:
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
        # start the Discord bot in it's own thread
        print("Starting threaded discord bot!")
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
            try:
                self.run(self.token)
            except:
                self.logout()

    async def SendMessage(self, Text: str):
        """
        Async send text message to channel.
        """
        channel=self.get_channel(self.channelID)
        await channel.send(Text)

    def SendText(self, Text: str):
        """
        Send text message to channel using loop.create_task().
        """
        channel=self.get_channel(self.channelID)
        print("Getting channel with id"+self.channelID)
        try:
            self.loop.create_task(channel.send(Text))
        except:
            print("ERROR: Could not send text!")

    def SendDiscordFile(self, DiscordFile: discord.File):
        """
        Send discord file.
        """
        self.loop.create_task(self.channel.send(file=DiscordFile))

    def SendIO(self, DataStream: io.BytesIO):
        """
        Send text message to channel using loop.create_task().
        """
        try:
            DataStream.seek(0)
            # Create data stream.
            file= discord.File(DataStream, filename="funkbot.png", spoiler=True)
            
            #self.loop.create_task(self.channel.send(Text))
        except:
            print("ERROR: Could not send text!")

    def SendFig(self, fig):
        """
        Set matplotlib fig object.
        """

        # Create io.
        data_stream=io.BytesIO()

        # Seve figure in data stream.
        #fig.savefig(data_stream, format='png', bbox_inches="tight", dpi=150)
        fig.savefig(data_stream, format='png') #, bbox_inches="tight")

        # Close figure.
        plt.close(fig)

        # Rewind data stream.
        data_stream.seek(0)

        # Create data stream.
        file= discord.File(data_stream, filename="funkbot.png", spoiler=False)

        # Send.
        self.SendDiscordFile(file)