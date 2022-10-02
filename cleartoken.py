"""
Clears out the Discord Bot Token as we do not want it on the github repo
"""

import fileinput

# Name of the config file.
filename="FunkMan.ini"

for line in fileinput.input(filename, inplace=True):
    if "TOKEN=" in line:
      print("TOKEN=YOUR_BOT_TOKEN_HERE", end="\n")
    else:
      print(line, end="")