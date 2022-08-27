"""
FunkBot

See https://discordpy.readthedocs.io/en/stable/
"""

import discord
from discord.ext import commands, tasks
import threading
import matplotlib.pyplot as plt
import io
from ..utils.utils import _GetVal

class FunkBot(commands.Bot):
    """
    API class wrapper for Discord based on discord.py.
    """

    def __init__(self, Token: str, ChannelID: int, Command_Prefix="!"):

        # Init discord.Client superclass.
        super().__init__(Command_Prefix)

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
            pass
            from funkman.utils.tests import testTrap, testBomb, testStrafe, getResultTrap
            from funkman.funkplot.funkplot import FunkPlot

            funkyplot=FunkPlot()

            trapfile="D:/Users/frank/Saved Games/DCS.openbeta/AIRBOSS-CVN-74_Trapsheet-New callsign_FA-18C_hornet-0003.csv"

            result=getResultTrap(trapfile)
            self.SendLSOEmbed(result, self.channelID)

            # Test trap.
            f1, a1=testTrap(funkyplot, trapfile)
            self.SendFig(f1, self.channelID)

            # Test bomb.
            #f2, a2=testBomb(funkyplot)
            #self.SendFig(f2, self.channelID)

            # Test strafe.
            #f3, a3=testStrafe(funkyplot)            
            #self.SendFig(f3, self.channelID)

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

    def SendDiscordFile(self, DiscordFile: discord.File, ChannelID: int, Embed: discord.Embed):
        """
        Send discord file.
        """
        channel=self.get_channel(ChannelID)
        self.loop.create_task(channel.send(file=DiscordFile, embed=Embed))

    def SendDiscordEmbed(self, DiscordFile: discord.Embed, ChannelID: int):
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


    def SendLSOEmbed(self, result, ChannelID: int):

        print("Creating LSO Embed")
        #print(result)

        actype=_GetVal(result, "airframe", "Unkown")
        Tgroove=_GetVal(result, "Tgroove", "?")

        player=_GetVal(result, "name", "Ghostrider")
        grade=_GetVal(result, "finalscore", "?")
        points=_GetVal(result, "points", "?")
        details=_GetVal(result, "details", "?")
        case=_GetVal(result, "case", "?")
        wire=_GetVal(result, "wire", "?")

        carriertype=_GetVal(result, "carriertype", "?")
        carriername=_GetVal(result, "carriername", "?")
        windondeck=_GetVal(result, "wind", "?")
        missiontime=_GetVal(result, "mitime", "?")
        missiondate=_GetVal(result, "midate", "?")
        theatre=_GetVal(result, "theatre", "Unknown Map")

        # Create Embed
        embed = discord.Embed(title="LSO Grade", description=f"Result for {player} at carrier {carriername} [{carriertype}]", color=0x00ff00)

        # Create file.
        fileLSO = discord.File("./images/LSO.png", filename="lso.png")
        filePts = discord.File("./images/Points2.png", filename="points.png")

        embed.set_image(url="attachment://lso.png")
        embed.set_thumbnail(url="attachment://points.png")

        # Author.
        embed.set_author(name="FunkMan")

        embed.add_field(name="Grade", value=grade, inline=True)
        embed.add_field(name="Points", value=points, inline=True)
        embed.add_field(name="Details", value=details, inline=True)
        embed.add_field(name="Tgroove", value=Tgroove, inline=True)
        embed.add_field(name="Wire", value=wire, inline=True)

        embed.add_field(name="Case", value=case, inline=True)
        embed.add_field(name="Wind", value=windondeck, inline=True)

        embed.set_footer(text="I am the footer!")

        self.SendDiscordFile(fileLSO, ChannelID, embed)