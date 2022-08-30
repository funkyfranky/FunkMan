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
from ..utils.utils       import _GetVal

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
        print(f"New message from server {self.client_address[0]}")

        # Table data.
        table=json.loads(data)

        if False:
            print("Table from JSON:")
            #print(table)
            #print("---------------")
            #print(data.decode('utf-8'))
            #print("---------------")
            print(json.dumps(table, indent=2, sort_keys=True))
            print("---------------")

        # Evaluate table data.
        self.server.EvalData(table)


class FunkSocket(socketserver.UDPServer):
    """
    UDP socket server. It inherits "socketserver.UDPServer".
    """

    def __init__(self, Host="127.0.0.1", Port=10123) -> None:

        super().__init__((Host, Port), FunkHandler)

        self.host=Host
        self.port=Port

        self.funkbot=None
        self.funkplot=None

        print(f"FunkSocket: Host={self.host}:{self.port}")

    def SetFunkBot(self, Funkbot: FunkBot):
        """Set the FunkBot instance."""
        self.funkbot=Funkbot

    def SetFunkPlot(self, Funkplot: FunkPlot):
        """Set the FunkPlot instance."""
        self.funkplot=Funkplot

    def SetChannelIdMessage(self, ChannelID):
        """Set channel ID for text messages."""
        self.channelIDmessage=ChannelID

    def SetChannelIdRange(self, ChannelID):
        """Set channel ID for Range figures."""
        self.channelIDrange=ChannelID

    def SetChannelIdAirboss(self, ChannelID):
        """Set channel ID for Airboss."""
        self.channelIDairboss=ChannelID

    def Start(self):
        """Start socket server."""

        # Info message.
        print(f"Starting Socket server {self.host}:{self.port}")

        try:
            self.serve_forever()
        except:
            print('Keyboard Control+C exception detected, quitting.')
            os._exit(0)


    def EvalData(self, table):
        """Evaluate data received from socket. You might want to overwrite this function."""

        # Debug info.
        if False:
            print("FunkSock Eval Data:")
            print(table)
            print("--------------------------------------")

        # Treat different cases.
        if "dataType" in table:

            if table["dataType"]=="Text Message":
                print("Got text message!")

                # Extract text.
                text=table["text"]

                # Send text to Discord.
                self.funkbot.SendText(text, self.channelIDmessage)

            if table["dataType"]=="Bomb Result":
                print("Got bomb result!")

                # Create bomb run figure.
                fig, ax=self.funkplot.PlotBombRun(table)

                # Send figure to Discord.
                self.funkbot.SendFig(fig, self.channelIDrange)

            elif table["dataType"]=="Strafe Result":
                print("Got strafe result!")

                # Create strafe run figure.
                fig, ax=self.funkplot.PlotStrafeRun(table)

                # Send figure to discord.
                self.funkbot.SendFig(fig, self.channelIDrange)

            elif table["dataType"]=="Trap Sheet":
                print("Got trap sheet!")

                # Send LSO grade.
                self.funkbot.SendLSOEmbed(table, self.channelIDairboss)

                # Create trap sheet figure.
                fig, ax=self.funkplot.PlotTrapSheet(table)

                # Send figure to Discord.
                self.funkbot.SendFig(fig, self.channelIDairboss)

            else:
                print("ERROR: Unknown data type in table!")
        else:
            print("ERROR: dataType not key in table!")
            print(table)