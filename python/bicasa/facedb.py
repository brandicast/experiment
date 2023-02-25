from conf.configmodule import *
import pathlib
import pickle
import logging


# Singleton - refer to https://mark1002.github.io/2018/07/31/python-%E5%AF%A6%E7%8F%BE-singleton-%E6%A8%A1%E5%BC%8F/
#
# Provide a Singleton PersistentDB for storaging faces info from files.  

logger = logging.getLogger( __name__)

class FaceDB:

    _instance = None
    _db_file = {}
    _path = config["app"]["facedb"]

    # Equivalent to static method...
    def get_instance ():
        if FaceDB._instance is None:
            FaceDB()
        return FaceDB._instance 

    def __init__(self):
        if FaceDB._instance is not None:
            raise Exception('PersistentDB is designed as Singleton.  Use get_instance(path) to initialize')
        else:
            FaceDB._instance = self
            file = pathlib.Path(self._path)
            if file.exists ():
                f = open(self._path, 'rb')
                self._db_file = pickle.load(f)
                if self._db_file is not None:
                    logger.info ("Loading persistent db from : " + self._path + " with size of " + str(len(self._db_file)))
                else:
                    logger.error ("Loading persistent db from : " + self._path + ". File exists but the content could be corrupted")
    
    """
    Solely check picture exists in db or not
    """
    def pictureExistsInDB(self, path):
        return  pathlib.Path(path).absolute() in self._db_file
    
    """
    Check if picture exists in database and with the same timestamp
    """
    def pictureExistsInDBWithSameTimestamp (self, path, timestamp):
        isSameFile = False
        abs_path = pathlib.Path(path).absolute()
        if abs_path in self._db_file:
            isSameFile = (self._db_file[abs_path]["last_modified_time"] == timestamp)
        return isSameFile

    """
    Add founded faces in pciture to FaceDB
      path -  path of the picture
      timestamp - timestamp of the picture.  Assuming pictures with the same timestamp remain the same, save some effort
      faceList - a list contains >1 faceDict.  Each faceDict has 2 elements :  
                                                  1) 'representation' - embedding directly from DeepFace [which is also an Dict ('facial_area' and 'embedding)]
                                                  2) 'thumbnail' - a Mat which can draw directly   -->  This add up pretty much size
    """
    def addFaces (self, path, timestamp, faceList):
        abs_path = pathlib.Path(path).absolute()
        self._db_file[abs_path] = {}
        self._db_file[abs_path]["last_modified_time"] = timestamp
        self._db_file[abs_path]["faces"] = faceList

    """
    Persistent to file system
    """
    def persistent(self):
        try:
            f = open(self._path, "wb")
            pickle.dump(self._db_file, f)
            logger.info ("Dumping FaceDB to : " + self._path)
            f.close()
        except Exception as e:
            logger.error(e)