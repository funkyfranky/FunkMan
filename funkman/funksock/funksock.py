"""
FunkSock
========

See https://docs.python.org/3/library/socketserver.html
"""

import socketserver
import json
import os

class FunkHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def __init__(self, request, client_address, server, funkbot) -> None:
        super().__init__(request, client_address, server)

        self.funkbot=funkbot


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

        self.EvalTable(table)

        print("EOF----------\n")

    def EvalTable(self, table):
        # Treat different cases.
        if "messageString" in table:
            text=table["messageString"]
            #sendtext(text)
            self.funkbot.SendText(text)
        elif "type" in table:
            if table["type"]=="Bomb Result":
                print("Got bomb result!")
            elif table["type"]=="Strafe Result":    
                print("Got bomb result!")
            elif table["type"]=="Trap Sheet":
                print("Got trap sheet!")
            else:
                print("ERROR: Unknown type in table!")
        else:
            print("Unknown message type!")        

class FunkSocket():

    def __init__(self, Funkbot, Host="127.0.0.1", Port=10123) -> None:
        self.host=Host
        self.port=Port
        self.funkbot=Funkbot

        print(f"FunkSocket: Host={self.host}:{self.port}")

    def Start(self):

        #self.port=10081
        #self.host="127.0.0.1"

        # Info message
        print(f"Starting Socket server {self.host}:{self.port}")
        
        # Start UDP sever
        self.server=socketserver.UDPServer((self.host, self.port), FunkHandler, self.funkbot)
        #self.server=socketserver.UDPServer(("127.0.0.1", 10081), FunkHandler, self.funkbot)

        with self.server:
            try:
                self.server.serve_forever()
            except:
                print('Keyboard Control+C exception detected, quitting.')
                os._exit(0)