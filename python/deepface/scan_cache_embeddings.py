import os
import sys
import math
import pathlib

from deepface import DeepFace

import opencv_util as cv_util
import cv2

import pickle


isDirty = False


def loadPersistentCache():
    db_file = {}
    file = pathlib.Path(DB_FILE)
    if file.exists():
        f = open(DB_FILE, 'rb')
        db_file = pickle.load(f)
        print("Loading persistent db from : " + DB_FILE +
              " with size of " + str(len(db_file)))

    return db_file


def savePersistentCache(db_file):
    f = open(DB_FILE, "wb")
    pickle.dump(db_file, f)
    print("Dumping db to : " + DB_FILE)
    f.close()


def getNormalizedFaceImage(img, coordinates):
    thumbnail_size = 90

    # crop the face from the original image
    face_img = img[coordinates['y']:coordinates['y']+coordinates['h'],
                   coordinates['x']:coordinates['x']+coordinates['w']]

    # Fit the face into the size of 256*256
    scale = max(math.ceil(coordinates['h']/thumbnail_size),
                math.ceil(coordinates['w']/thumbnail_size))

    # resize function is dst (w * h)
    # double slash to get the math.floor result
    normalized_face_img = cv2.resize(
        face_img, (coordinates['w']//scale, coordinates['h']//scale), interpolation=cv2.INTER_AREA)

    return normalized_face_img


def scan_extract_cache(path, cache):

    persistent_db = cache

    with os.scandir(path) as entries:
        for entry in entries:

            if entry.is_dir():
                scan_extract_cache(entry.path, persistent_db)
            else:
                # print (entry.path)
                # print (entry.stat().st_mtime)

                do_inference = True
                if entry.path in persistent_db:
                    if persistent_db[entry.path]["last_modified_time"] == entry.stat().st_mtime:
                        do_inference = False

                if do_inference:
                    global isDirty
                    isDirty = True
                    """
                    try to use python-magic but only available on linux/osx platform.  
                    though there's alternative package on windows.  maybe test later...
                    """
                    cap_filename = entry.name.upper()
                    if cap_filename.endswith(".JPEG") or cap_filename.endswith(".JPG"):

                        print("Extracting faces from : " + entry.path)
                        faces_in_one_picture = {}
                        # Keep track the last modified date for caching mechanism
                        faces_in_one_picture["last_modified_time"] = entry.stat(
                        ).st_mtime
                        persistent_db[entry.path] = faces_in_one_picture

                        try:

                            # adding the parameter cv2.IMREAD_COLOR for opencv to read image in the right orientation based on EXIF
                            target_img = cv_util.cv2_loadimage(
                                entry.path, cv2.IMREAD_COLOR)

                            #  returns  an array of face info.  Each face is also an dict  with 2 elements:  [0] is the vector of the face [1] is the coordinates of the face
                            representations = DeepFace.represent(
                                target_img, detector_backend=backends[backend_index])

                            print(str(len(representations)) +
                                  " face(s) found ! ")

                            if (len(representations) > 0):
                                faces_array = []

                                for representation in representations:

                                    face_area = representation["facial_area"]
                                    print(face_area)
                                    face_thumbnail = getNormalizedFaceImage(
                                        target_img, face_area)

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
                            print(err1)
                        except TypeError as err2:
                            print(err2)
                        except KeyError as err3:
                            print(err3)
                        except:
                            print("Error occured when processing : " +
                                  entry.path + "  with error :  ")
                            print(sys.exc_info()[0])

    return persistent_db


if __name__ == '__main__':

    backends = [
        'opencv',
        'ssd',
        'dlib',
        'mtcnn',
        'retinaface',
        'mediapipe'
    ]

    backend_index = 4

    # SOURCE_DIRECTORY = 'D:\\CouldStation_Photo\\2022'
    SOURCE_DIRECTORY = 'resources_big'
    # DB_FILE = 'D:\\2022.' + backends[backend_index]
    DB_FILE = 'D:\\persistent.' + backends[backend_index]

    db = loadPersistentCache()
    db = scan_extract_cache(SOURCE_DIRECTORY, db)
    if isDirty:
        savePersistentCache(db)
