from deepface.detectors import FaceDetector
#from deepface import DeepFace
import cv2
import numpy as np

import os,sys
from pathlib import Path

import opencv_util as cv_util

'''
   1) The library deepface for ANACONDA is ONLY available on OS-X and Linux.   On Windows, use pip...however, that also create some library issues.
   2) It seems that support only python version < 3.10   (because of other numpy version compatibility issues)

'''

root_path = Path("resources")

face_data_path = root_path.parent.joinpath("faces_data")

print ("Output to " + str(face_data_path))

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


detector = FaceDetector.build_model(backends[backend_index]) #set opencv, ssd, dlib, mtcnn or retinaface



for (base, twig, files) in os.walk (root_path,topdown=True,followlinks=True):
       for f in files:
            try:
                cap_filename = f.upper()
                if cap_filename.endswith(".JPEG") or cap_filename.endswith(".JPG"):

                    full_filename = Path(base).joinpath(f)
                    print("Extracting faces from : "  + str(full_filename))

                    img = cv_util.cv2_loadimage (str(full_filename))

                    
                    faces = FaceDetector.detect_faces(detector, backends[backend_index], img, True)    # the parameter face_align: to align the FOUND face or not  

                    print (str(len(faces)) + " face(s) are Found ")

                    if (len(faces)>0):

                        face_path = Path(str(full_filename).replace(str(root_path),str(face_data_path)) + "_faces")

                        #face_path = face_data_path.joinpath(full_filename.name, f + "_faces")
                        if not face_path.exists():
                            try:
                                face_path.mkdir(parents=True)
                            except OSError as error:
                                print (error) 

                        counter = 0
                        for face in faces:
                            output_filename = face_path.joinpath("face"+str(counter)+".jpg")
                            print ("Writing face" + str(counter) + " as " + str(output_filename))
                            cv2.imwrite(str(output_filename), face[0])
                            counter = counter + 1 
            except:
                print ("Error occured when processing : " + str(Path(base).joinpath(f))) 