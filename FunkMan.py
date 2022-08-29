"""
FunkMan
=======
Main code to run the discord bot (FunkBot) and UDP socket server (FunkSocket)
"""

from funkman import FunkMan

# Welcome!
print("Hello, my name is FunkMan. I'm at your service!")

# Create funkman instance.
fman=FunkMan()

# Start bot and socket.
fman.Start()