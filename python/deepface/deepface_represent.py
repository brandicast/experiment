from deepface.detectors import FaceDetector
from deepface.commons import distance as dst
from deepface import DeepFace
import os,sys
from pathlib import Path

import opencv_util as cv_util

import cv2
import numpy as np
import math

'''
   1) The library deepface for ANACONDA is ONLY available on OS-X and Linux.   On Windows, use pip...however, that also create some library issues.
   2) It seems that support only python version < 3.10   (because of other numpy version compatibility issues)

'''

def getNormalizedFaceImage (img, coordinates):
    #crop the face from the original image
    face_img  = img[coordinates['y']:coordinates['y']+coordinates['h'],coordinates['x']:coordinates['x']+coordinates['w']]

    # Fit the face into the size of 256*256
    scale = max(math.ceil(coordinates['h']/256), math.ceil(coordinates['w']/256))
    
    # resize function is dst (w * h)   
    # double slash to get the math.floor result
    normalized_face_img = cv2.resize(face_img, (coordinates['w']//scale, coordinates['h']//scale), interpolation=cv2.INTER_AREA)    

    return normalized_face_img


root_path = Path("resources")

face_data_path = root_path.parent.joinpath("faces_data")

if len(sys.argv) >1:
    root_path = sys.argv[1]

# face working model found :  0 , 1
#  0 and 1 found only 1 face
#  dlib requires cmake, but after install still compile fail
#  mediapipe found - face
backends = [
  'opencv', 
  'ssd', 
  'dlib', 
  'mtcnn', 
  'retinaface', 
  'mediapipe'
]
backend_index = 4

base_img_path = "tmp/base.jpg"

bases = DeepFace.represent(base_img_path, detector_backend=backends[backend_index])    

#print (bases[0]["embedding"])
base_img = cv2.imread(base_img_path,cv2.IMREAD_COLOR)
coordinates = bases[0]["facial_area"] 

base_face_thumbnail = getNormalizedFaceImage (base_img,coordinates)
# create an empty image for drawing
dummy_img = np.zeros((512, 512, 3), np.uint8)

dummy_img[30:base_face_thumbnail.shape[0]  +30, 30:base_face_thumbnail.shape[1]+30] = base_face_thumbnail

cv2.namedWindow("output", cv2.WINDOW_NORMAL)    
cv2.imshow ("output", dummy_img)
cv2.waitKey(0)


for (base, twig, files) in os.walk (root_path,topdown=True,followlinks=True):
       for f in files:
            try:
                cap_filename = f.upper()
                if cap_filename.endswith(".JPEG") or cap_filename.endswith(".JPG"):

                    full_filename = Path(base).joinpath(f)
                    print("Extracting faces from : "  + str(full_filename))

                    target_img = cv_util.cv2_loadimage (str(full_filename),cv2.IMREAD_COLOR)

                    cv2.imshow ("output",target_img)
                    cv2.waitKey(0)
                    
                    
                    #  returns  an array of face info.  Each face is also an dict  with 2 elements:  [0] is the vector of the face [1] is the coordinates of the face
                    representations = DeepFace.represent(target_img, detector_backend=backends[backend_index])    

                    print (str(len(representations)) + " face(s) found ! ")
 
                    if (len(representations)>0):
                        for representation in representations:

                            distance =  dst.findCosineDistance(bases[0]["embedding"], representation["embedding"])
                            print (round(distance,3)) 

                            face_area = representation["facial_area"]
                            to_be_compared_face = getNormalizedFaceImage (target_img,face_area )

                            tmp = dummy_img.copy()
                            
                            tmp[30:30+to_be_compared_face.shape[0],
                                      base_face_thumbnail.shape[0]+60:base_face_thumbnail.shape[0]+60+to_be_compared_face.shape[1]] = to_be_compared_face

                            cv2.putText(tmp, str(round(distance,3)), (30, 400),cv2.FONT_HERSHEY_PLAIN,  3, (0, 255, 255), 1, cv2.LINE_AA)

                            cv2.imshow ("output", tmp)
                            cv2.waitKey(0)                                                    

            except ValueError as err1:
                print (err1)
            except TypeError as err2:
                print (err2)
            except KeyError as err3:
                print (err3)
            except:
                    print ("Error occured when processing : " + str(Path(base).joinpath(f)) +   "  with error :  ")
                    print (sys.exc_info()[0])
