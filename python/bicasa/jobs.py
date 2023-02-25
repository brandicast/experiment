from conf.configmodule import *
import logging
import time, sys

from facedb import FaceDB

logger = logging.getLogger(__name__)

sleep_time = int(config["app"]["persistent_frequency"])

def PersistentWorker (stop_sign, another_job):
    logger.debug("Scanning Thread status : " + "alive" if another_job.is_alive() else "stoped")
    
    db = FaceDB.get_instance()
    while not stop_sign and another_job.is_alive() :
        logger.debug("Scanning Thread status : " + "alive" if another_job.is_alive() else "stoped")
        db.persistent()
        time.sleep(sleep_time)
    db.persistent()        
    logger.info("Persistent Thread Stopped.")

def ConsoleInput ():
    for line in sys.stdin:
        if 'exit' == line.rstrip():
            STOP = True
            logger.info("Preparing for gracefully stop....wait....")
            break    