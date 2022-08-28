"""
FunkMan
=======
Main code to run the discord bot (FunkBot) and UDP socket server (FunkSocket)
"""

from funkman.funkman           import FunkMan
#from funkman.funkbot.funkbot   import FunkBot
#from funkman.funkplot.funkplot import FunkPlot
#from funkman.funksock.funksock import FunkSocket

if __name__ == "__main__":

	# Welcome!
	print("Hello, my name is FunkMan. I'm at your service!")

	# Create funkman instance.
	fman=FunkMan()

	# Start bot and socket.
	fman.Start()