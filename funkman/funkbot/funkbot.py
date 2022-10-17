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

    def __init__(self, Token: str, ChannelID: int, Command_Prefix="!", ImagePath="./funkpics/", DebugLevel=0):

        # Intents.
        intents = discord.Intents.all()

        # Init discord.Client superclass.
        super().__init__(Command_Prefix, intents=intents)

        # Set config parameters:
        self.token=str(Token)
        self.channelID=int(ChannelID)
        self.debugLevel=DebugLevel
        self.imagePath=ImagePath

        # Init bot commands.
        self._InitCommands()

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

        if self.debugLevel>=20:
            self._TestPlots(self.channelID)

    async def on_disconnect(self):
        """
        Called when the client has disconnected from Discord, or a connection attempt to Discord has failed. This could happen either through the internet being disconnected, 
        explicit calls to close, or Discord terminating the connection one way or the other.
        """
        # Get channel.
        try:
            self.channel=self.get_channel(self.channelID)
        except:
            print(f"ERROR: Could not get channel with ID={self.channelID}")

        # Info that bot is online and ready.
        print('Connected as {0.name} [ID: {0.id}]'.format(self.user))

    def Start(self, Threaded=False):
        """
        Connect to server using the token.
        """
        if Threaded:
            print("Starting threaded discord bot!")
            discordThread=threading.Thread(target=self.Start, args=(False, ))
            discordThread.start()
        else:
            print(f"Starting Bot Client with Token {self.token[0:5]}...")
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
            print(f"ERROR: Could not send text! {Text}")

    def SendDiscordFile(self, DiscordFile: discord.File, ChannelID: int, Embed: discord.Embed=None):
        """
        Send discord file.
        """
        channel=self.get_channel(ChannelID)
        if Embed:
            self.loop.create_task(channel.send(file=DiscordFile, embed=Embed))
        else:
            self.loop.create_task(channel.send(file=DiscordFile))

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
        # Rewind stream.
        DataStream.seek(0)

        # Create data stream.
        file= discord.File(DataStream, filename="funkbot.png", spoiler=False)
        
        # Send discord file.
        self.SendDiscordFile(file, ChannelID)

    def SendFig(self, fig, ChannelID: int):
        """
        Set matplotlib fig object.
        """

        # Create io.
        data_stream=io.BytesIO()

        # Seve figure in data stream.
        fig.savefig(data_stream, format='png')

        # Close figure.
        plt.close(fig)

        # Send data stream.
        self.SendIO(data_stream, ChannelID)

    def SendLSOEmbed(self, result, ChannelID: int):

        # Info message.
        #print("Creating LSO Embed")

        # Get date from result.
        actype=_GetVal(result, "airframe", "Unkown")
        Tgroove=_GetVal(result, "Tgroove", "?", 1)
        player=_GetVal(result, "name", "Ghostrider")
        grade=_GetVal(result, "grade", "?")
        points=_GetVal(result, "points", "?")
        details=_GetVal(result, "details", "?")
        case=_GetVal(result, "case", "?")
        wire=_GetVal(result, "wire", "?")
        carriertype=_GetVal(result, "carriertype", "?")
        carriername=_GetVal(result, "carriername", "?")
        windondeck=_GetVal(result, "wind", "?", 1)
        missiontime=_GetVal(result, "mitime", "?")
        missiondate=_GetVal(result, "midate", "?")
        theatre=_GetVal(result, "theatre", "Unknown Map")
        theta=_GetVal(result, "carrierrwy", -9)

        lsoPic="LSO.png"
        if abs(theta)<0.1:
            lsoPic="LSO_Vstol.png"

        color=0x00ff00
        urlIm="https://i.imgur.com/1bWgcV7.png"
        if type(points)!=str:
            if points==0:
                color=0x000000 #black
                urlIm="https://i.imgur.com/rZpu9c0.png"
            elif points==1:
                color=0xff0000 #red
                urlIm="https://i.imgur.com/LXgD2Op.png"
            elif points==2:
                color=0xFFA500 #orange
                urlIm="https://i.imgur.com/EjviMBk.png"
            elif points==2.5:
                color=0xB47E59 #brown
                urlIm="https://i.imgur.com/nYWrL4Z.png"
            elif points==3:
                color=0xFFFF00 #yellow
                urlIm="https://i.imgur.com/wH0Gjqx.png"
            elif points==4:
                color=0x00FF00 #green
                urlIm="https://i.imgur.com/1bWgcV7.png"
            elif points==5:
                color=0x0000FF #blue
                urlIm="https://i.imgur.com/6ecFSqo.png"

        # Create Embed
        embed = discord.Embed(title="LSO Grade", description=f"Result for {player} at carrier {carriername} [{carriertype}]", color=color)

        # Create file.
        fileLSO = discord.File(self.imagePath+lsoPic, filename="lso.png")

        # Images.
        embed.set_image(url="attachment://lso.png")
        embed.set_thumbnail(url=urlIm)

        # Author.
        embed.set_author(name="FunkMan")

        # Data.
        embed.add_field(name="Grade", value=grade, inline=True)
        embed.add_field(name="Points", value=points, inline=True)
        embed.add_field(name="Details", value=details, inline=True)
        embed.add_field(name="Groove", value=Tgroove, inline=True)
        if wire!="?":
            embed.add_field(name="Wire", value=wire, inline=True)
        embed.add_field(name="Case", value=case, inline=True)
        embed.add_field(name="Wind", value=windondeck, inline=True)
        embed.add_field(name="Aircraft", value=actype, inline=True)

        # Footer.
        embed.set_footer(text=f"{theatre}: {missiondate} ({missiontime})")

        # Send to Discord.
        self.SendDiscordFile(fileLSO, ChannelID, embed)

    
    def _InitCommands(self):
        """Init commands."""

        @self.command(aliases=['testplots'])
        async def TestPlots(ctx: commands.Context):
            self._TestPlots(ctx.channel.id)

        @self.command(aliases=['testtrap'])
        async def TestTrap(ctx: commands.Context):
            self._TestTrap(ctx.channel.id)

        @self.command(aliases=['teststrafe'])
        async def TestStrafe(ctx: commands.Context):
            self._TestStrafe(ctx.channel.id)

        @self.command(aliases=['testbomb'])
        async def TestBomb(ctx: commands.Context):
            self._TestBomb(ctx.channel.id)

    def _TestTrap(self, ChannelID):
        from funkman.utils.tests import testTrap, getResultTrap
        from funkman.funkplot.funkplot import FunkPlot

        # Init FunkPlot.
        funkyplot=FunkPlot()

        # Trap sheet files.
        trapfiles=[
            "./testfiles/Trapsheet-FA-18C_hornet-001.csv", 
            "./testfiles/Trapsheet-FA-18C_hornet-002.csv",
            "./testfiles/SH_unicorn_AIRBOSS-trapsheet-Yoda_FA-18C_hornet-0001.csv",
            "./testfiles/Trapsheet-AV8B_Tarawa-001.csv"]

        for trapfile in trapfiles:

            # Get result from trap file.
            result=getResultTrap(trapfile)

            # Test LSO embed.
            self.SendLSOEmbed(result, ChannelID)

            # Test trap.
            f1, a1=testTrap(funkyplot, trapfile)
            self.SendFig(f1, ChannelID)

    def _TestStrafe(self, ChannelID):
        from funkman.utils.tests import testStrafe
        from funkman.funkplot.funkplot import FunkPlot

        # Init FunkPlot.
        funkyplot=FunkPlot()

        # Test strafe.
        fig, ax=testStrafe(funkyplot)
        self.SendFig(fig, ChannelID)

    def _TestBomb(self, ChannelID):
        from funkman.utils.tests import testBomb
        from funkman.funkplot.funkplot import FunkPlot

        # Init FunkPlot.
        funkyplot=FunkPlot()

        # Test strafe.
        fig, ax=testBomb(funkyplot)
        self.SendFig(fig, ChannelID)

    def _TestPlots(self, ChannelID):

        # Debug info.
        print("Testing Plots...")

        # Test trapsheet.
        self._TestTrap(ChannelID)

        # Test strafe.
        self._TestStrafe(ChannelID)

        # Test bomb.
        self._TestBomb(ChannelID)