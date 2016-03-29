import logging, os, traceback, sys
import logging.config
from os.path import dirname

logconf = os.path.join(dirname(dirname(__file__)), "config", "log.ini")
logging.config.fileConfig(logconf)
elog = logging.getLogger("exception")

def getDlog(name):
    return logging.getLogger(name)
 

