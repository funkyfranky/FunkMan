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
