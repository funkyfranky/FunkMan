"""
FunkSock
========

See https://docs.python.org/3/library/socketserver.html
"""

import socketserver
import json
import os

from ..funkplot.funkplot import FunkPlot
from ..funkbot.funkbot   import FunkBot

class FunkHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):

        # Get data.
        data = self.request[0].strip()

        # Debug message.
        print("{} new message from server: ".format(self.client_address[0]))

        # Table data.
        table=json.loads(data)

        if True:
            print("Table from JSON:")
            print(table)
            print("---------------")
            print(data.decode('utf-8'))
            print("---------------")
            print(json.dumps(table, indent=4, sort_keys=True))
            print("---------------")

        # Evaluate table data.
        self.EvalTable(table, self.server.funkbot, self.server.funkplot)

    def EvalTable(self, table, funkbot: FunkBot, funkplot: FunkPlot):
        """Evaluate table."""

        # Treat different cases.
        if "messageString" in table:
            text=table["messageString"]
            print("Got text message!")
            funkbot.SendText(text, self.server.channelIDmessage)
        elif "type" in table:
            if table["type"]=="Bomb Result":
                print("Got bomb result!")
                fig, ax=funkplot.PlotBombRun(table)
                funkbot.SendFig(fig, self.server.channelIDrange)
            elif table["type"]=="Strafe Result":    
                print("Got strafe result!")
                fig, ax=funkplot.PlotStrafeRun(table)
                funkbot.SendFig(fig, self.server.channelIDrange)
            elif table["type"]=="Trap Sheet":                
                print("Got trap sheet!")
                fig, ax=funkplot.PlotTrapSheet(table)
                funkbot.SendFig(fig, self.server.channelIDairboss)
            else:
                print("ERROR: Unknown type in table!")
        else:
            print("Unknown message type!")

class FunkSocket():
    """
    UDP socket server.
    """

    def __init__(self, Host="127.0.0.1", Port=10123) -> None:

        self.host=Host
        self.port=Port

        self.funkbot=None
        self.funkplot=None

        print(f"FunkSocket: Host={self.host}:{self.port}")

    def SetFunkBot(self, Funkbot: FunkBot):
        self.funkbot=Funkbot

    def SetFunkPlot(self, Funkplot: FunkPlot):
        self.funkplot=Funkplot

    def SetChannelIdMessage(self, ChannelID):
        self.setchannelIDmessage=ChannelID

    def SetChannelIdRange(self, ChannelID):
        self.setchannelIDrange=ChannelID

    def SetChannelIdAirboss(self, ChannelID):
        self.setchannelIDairboss=ChannelID

    def Start(self):

        # Info message
        print(f"Starting Socket server {self.host}:{self.port}")

        #self.host="127.0.0.1"
        #self.port=10081

        # Start UDP sever
        self.server=socketserver.UDPServer((self.host, self.port), FunkHandler)

        if self.funkbot:
            self.server.funkbot=self.funkbot
        if self.funkplot:
            self.server.funkplot=self.funkplot

        with self.server:
            try:
                self.server.serve_forever()
            except:
                print('Keyboard Control+C exception detected, quitting.')
                os._exit(0)