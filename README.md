# FunkMan
 FunkMan is a python program that creates an easy-to-use interface between the DCS scripting environment and a Discord bot via a UDP socket connection.
 This allows you, *e.g.*, to send text messages from DCS to Discord channels.
 
 Furthermore, FunkMan contains special interfaces to the MOOSE classes AIRBOSS and RANGE. For the AIRBOSS class, you get embeded messages when a player receives an LSO
 grade and fancy images of the trap sheet. For the RANGE class, images of the bombing impact point are send to Discord as well as as summary of a strafing run.

## Requirements
You have to
- De-sanitize the MissionScripting.lua file in your DCS install directory.
- MOOSE develop branch
- [https://www.python.org/](Python 3)
- [https://discordpy.readthedocs.io/en/stable/](discord.py)

## Installation
There are several ways to obtain the FunkMan code. You can use `git clone` if you are familiar with git
or download the [https://github.com/funkyfranky/FunkMan/releases](latest release) as zip file and unzip
it to a location of your liking, e.g. `D:\FunkMan\`.

The FunkMan directory contains three important files:
- `FunkMan.ini`: This is the config file, where you specify important parameters of your bot and socket connection.
- `FunkMan.py`: This is the file that contains the few lines of python code needed to start FunkMan.
- `FunkMan.bat`: This is the file you can click to start FunkMan by running the above python file.

So after downloading the FunkMan code, you first need to adjust the `FunkMan.ini` file. The important parameters
are the Token of your Discord bot and the ID of Discord channel(s), where FunkMan will send messages and images to.

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
DEBUGLEVEL=0

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

## Usage
Once you have configured FunkMan with the ini file, FunkMan is started by simply clicking the `FunkMan.bat` file.
If everything is setup correctly, you will obtain the following output telling you that you bot has connected:

**INSERT PICTURE HERE**

## Subpackages
FunkMan contains three subpackages:
- `FunkSock`: A socket server that handles data received via an UDP connection
- `FunkBot`: An interface to Discord bots using discord.py.
- `FunkPlot`: Contains a class to make pretty figures for the `MOOSE` `RANGE` and `AIRBOSS`classes using matplotlib.

You can use each of these subpackges on its own or in combination with the `FunkMan` package.
