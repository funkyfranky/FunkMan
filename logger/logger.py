import logging
import logging.handlers
import os
import gzip
import discord

log_file: str = "logs/FunkMan.log"


def namer(name):
    return name + ".log"


def rotator(source, dest):
    """Compress rotated log file"""
    os.rename(source, dest)
    f_in = open(dest, "rb")
    f_out = gzip.open("%s.gz" % dest, "wb")
    f_out.writelines(f_in)
    f_out.close()
    f_in.close()
    os.remove(dest)


# Check if logs folder exists, if not, create it.
if not os.path.exists("logs"):
    os.makedirs("logs")

# Get the root logger
logger = logging.getLogger()

# Create a stream handler for console output and a file handler to write to log file.
# The file handler rotates the logs based on size, 10MB, and will keep a total of 100 backups.
handler_stream = logging.StreamHandler()
handler_file = logging.handlers.RotatingFileHandler(log_file, maxBytes=10000000, backupCount=100)
handler_file.rotator = rotator
handler_file.namer = namer

# Create a formatter and use it for both the stream and file handler output.
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)-6s] [%(module)s:%(funcName)s():%(lineno)s]\t %(message)s", "%y-%m-%d %H:%M:%S"
)
handler_stream.setFormatter(formatter)
handler_file.setFormatter(formatter)

# Add the stream and file handler to the root logger
logger.addHandler(handler_stream)
logger.addHandler(handler_file)

# Initially set logging level to INFO
logger.setLevel(logging.INFO)

# Write a few lines to visually note in the logs when the application bas been restarted.
logger.info("\n\n-------------------Application Start-------------------\n")

# The default discord bot logger creates a lot of output so specifically setting the discord
# class logger to level CRITICAL helps eleviate the amount of output.
# This overides the root logger for the discord class only.
logging.getLogger("discord").setLevel(logging.CRITICAL)
