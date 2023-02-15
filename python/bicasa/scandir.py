import os, sys, math, logging
from deepface import DeepFace
from utils import opencv_util as cv_util
import cv2

from facedb import FaceDB

logger = logging.getLogger( __name__)

def scan_extract(path,recrusive=True, backend="retinaface"):
    
    # [TO BE STUDY]
    # this is a compromised way to get the singleton facedb by passing none object.  
    # It's assuming FaceDB has been initialized.
    # Should have a better way 
    db = FaceDB.get_instance()
    
    with os.scandir(path) as entries:
        for entry in entries:
                        
            if entry.is_dir() and recrusive:
                scan_extract(entry.path, True)
            else:
                """
                try to use python-magic but only available on linux/osx platform.  
                though there's alternative package on windows.  maybe test later...
                """
                cap_filename = entry.name.upper()
                if cap_filename.endswith(".JPEG") or cap_filename.endswith(".JPG"):
                    if not db.pictureExistsInDBWithSameTimestamp(entry.path, entry.stat().st_mtime) :

                        faces_in_one_picture = {}
                        faces_in_one_picture["last_modified_time"] = entry.stat().st_mtime   #  Keep track the last modified date for caching mechanism

                        db.addFaces(entry.path, entry.stat().st_mtime, faces_in_one_picture )
                        
                        try:
                            # adding the parameter cv2.IMREAD_COLOR for opencv to read image in the right orientation based on EXIF
                            target_img = cv_util.cv2_loadimage (entry.path,cv2.IMREAD_COLOR)

                            #  returns  an array of face info.  Each face is also an dict  with 2 elements:  [0] is the vector of the face [1] is the coordinates of the face
                            representations = DeepFace.represent(target_img, detector_backend=backend)    

                            logger.info(str(len(representations)) + " face(s) found in : "  + entry.path )

                            if (len(representations)>0):
                                faces_array = []
                                
                                for representation in representations:

                                    face_area = representation["facial_area"]
                                    face_thumbnail = cv_util.getThumbnailFace (target_img,face_area )

                                    """
                                    cv2.namedWindow("output", cv2.WINDOW_NORMAL)    
                                    cv2.imshow ("output", face_thumbnail)
                                    cv2.waitKey(0)                 
                                    """   
                                    single_face = {} 
                                    single_face["representation"] = representation
                                    single_face["thumbnail"] = face_thumbnail
                                    faces_array.append(single_face)
                                
                                faces_in_one_picture["faces"] = faces_array

                                """
                                It's a dict with fullpath as key, another dict as value    
                                        the value dict has 2 elements:   last_modified_time  and faces_array
                                                last_modified_time : is a string
                                                faces_array : is an array
                                                    items in array is another dict  with 2 values
                                                        ["representation] is the origin representation from deepface (which has "embedding" and "facial_area")
                                                        ["thumbnail"] is the binary of the face 

                                """
                        except ValueError as err1:
                            logger.error(str(err1) + " : " + entry.path)
                        except TypeError as err2:
                            logger.error(str(err2) + " : " + entry.path)
                        except KeyError as err3:
                            logger.error(str(err3) + " : " + entry.path)
                        except:
                            logger.error("Error occured when processing : " + entry.path +   "  with error :  " + str(sys.exc_info()[0]))
                        