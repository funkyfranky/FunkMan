# FunkMan
 FunkMan is a python program that creates an easy-to-use interface between the DCS scripting environment and a Discord bot via a UDP socket connection.
 This allows you, *e.g.*, to send text messages from DCS to Discord channels.
 
 Furthermore, FunkMan contains special interfaces to the MOOSE classes AIRBOSS and RANGE. For the AIRBOSS class, you get embeded messages when a player receives an LSO
 grade and fancy images of the trap sheet. For the RANGE class, images of the bombing impact point are send to Discord as well as as summary of a strafing run.

## Requirements
- You need to de-sanitize the MissionScripting.lua file in your DCS install directory.

## Subpackages
FunkMan contains three subpackages:
- `FunkSock`: A socket server that handles data received via an UDP connection
- `FunkBot`: An interface to Discord bots using discord.py.
- `FunkPlot`: Contains a class to make pretty figures for the `MOOSE` `RANGE` and `AIRBOSS`classes using matplotlib.

You can use each of these subpackges on its own or in combination with the `FunkMan` package.

## Config File
The config file consists of multiple section each starting with square brackets.

### [DEFAULT]
This sections contains a parameter for debugging:

### [FUNKBOT]
This section contains information about the Discord bot parmeters:
- `TOKEN`: Is the secret (!) token of the bot.
- `CHANNELID_MAIN`: The main channel ID used for all messages by default.
- `CHANNELID_RANGE`: (Optional) Channel ID where RANGE messages are send to.
- `CHANNELID_AIRBOSS`: (Optional) Channel ID where AIRBOSS messages are send to.

### [FUNKSOCK]
This section contains information about the UDP socket:
- `PORT`: UDP Port. Default is 10042.
- `HOST`: Host name. Default is 127.0.0.1.

### [FUNKPLOT]
This section contains information for plotting images.
- `IMAGEPATH`: Directory where the necessary images are stored.

### Example
```
[DEFAULT]
DEBUGLEVEL=1

[FUNKBOT]
TOKEN=MTAwNTAwMDA0NDc4MjU2MzQ0MQ.GmUqVd.cMRDGb6JxFMpN3cAAU-DX2Z4SymgTJLAwL-C8I
CHANNELID_MAIN=1011372894162526329
CHANNELID_RANGE=1006216842509041786
CHANNELID_AIRBOSS=1011372920968323155

[FUNKSOCK]
PORT=10042
HOST=127.0.0.1

[FUNKPLOT]
IMAGEPATH=./funkpics/
```
