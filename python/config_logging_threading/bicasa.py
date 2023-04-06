from conf.configmodule import *
import logging, logging.config

import threading, time
import sys

from scandir import scan_extract
from jobs import *

from facedb import FaceDB


logging.config.fileConfig(fname=config["logging"]["config_file"],disable_existing_loggers=False)
logger = logging.getLogger(__name__)

STOP = False
"""
[TO BE STUDY]
    initialize FaceDB first to avodi thread's racing problem 
    check if threading.lock applicable here.... (find something like synchroized as in java)
"""
FaceDB()

scan_job = threading.Thread(target=scan_extract, args=(config["app"]["source_directory"],config["deepface"]["backend"]))
scan_job.start()

persistent_job = threading.Thread(target=PersistentWorker, args=(STOP,scan_job))
persistent_job.start()

stdin_job = threading.Thread(target=ConsoleInput)
stdin_job.daemon = True
stdin_job.start()

logger.info ("2 threads fire up....")



