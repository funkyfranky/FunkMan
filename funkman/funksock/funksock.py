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
        #print(f"New message from server {self.client_address[0]}")

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

    def __init__(self, Host="127.0.0.1", Port=10042) -> None:

        super().__init__((Host, Port), FunkHandler)

        self.host=Host
        self.port=Port

        # Enable reuse, in case the restart was too fast and the port was still in TIME_WAIT.
        self.allow_reuse_address=True
        self.max_packet_size=65504

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


    def EvalData(self, table: dict):
        """Evaluate data received from socket. You might want to overwrite this function."""

        # Debug info.
        if False:
            print("FunkSock Eval Data:")
            print(table)
            print("--------------------------------------")

        key="command"
        textmessage="moose_text"
        bombresult="moose_bomb_result"
        straferesult="moose_strafe_result"
        lsograde="moose_lso_grade"

        table.get

        # Treat different cases.
        if key in table:

            command=table.get(key, "")
            server=table.get("server_name", "unknown")

            # Debug info
            print(f"Got {command} from server {server}!")

            if command==textmessage:
                #print("Got text message!")

                # Extract text.
                text=table.get("text", " ")

                # Send text to Discord.
                self.funkbot.SendText(text, self.channelIDmessage)

            elif command==bombresult:
                #print("Got bomb result!")

                # Create bomb run figure.
                fig, ax=self.funkplot.PlotBombRun(table)

                # Send figure to Discord.
                self.funkbot.SendFig(fig, self.channelIDrange)

            elif command==straferesult:
                #print("Got strafe result!")

                # Create strafe run figure.
                fig, ax=self.funkplot.PlotStrafeRun(table)

                # Send figure to discord.
                if fig is not None:
                    self.funkbot.SendFig(fig, self.channelIDrange)

            elif command==lsograde:
                #print("Got trap sheet!")

                # Send LSO grade.
                self.funkbot.SendLSOEmbed(table, self.channelIDairboss)

                # Create trap sheet figure.
                fig, ax=self.funkplot.PlotTrapSheet(table)

                # Send figure to Discord.
                self.funkbot.SendFig(fig, self.channelIDairboss)

            else:
                print(f"WARNING: Unknown command in table: {command}")
        else:
            print("WARNING: not key command in table!")
            print(table)