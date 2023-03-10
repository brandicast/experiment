from deepface.detectors import FaceDetector
import cv2
import numpy as np

'''
   1) The library deepface for ANACONDA is ONLY available on OS-X and Linux.   On Windows, use pip...however, that also create some library issues.
   2) It seems that support only python version < 3.10   (because of other numpy version compatibility issues)

'''

img_path = "resources\\99.jpg"

# face working model found :  0 , 1, 3, 4
#  0 and 1 sometimes can find all the faces
#  dlib requires cmake, but after install still compile fail
#  mediapipe requires further installation

backends = [
  'opencv', 
  'ssd', 
  'dlib', 
  'mtcnn', 
  'retinaface', 
  'mediapipe'
]

backend_index = 4

img = cv2.imread(img_path)

detector = FaceDetector.build_model(backends[backend_index]) #set opencv, ssd, dlib, mtcnn or retinaface

faces = FaceDetector.detect_faces(detector, backends[backend_index], img, False)    # the parameter face_align: to align the FOUND face or not  
        # this guy returns detected objects as list 
        #  inside each list  -> tuple  
        #                           ->  first element of the tuple is numpy.ndarray which represents the object images
        #                           ->  second element of the tuple is a list is a list, 
        #                                           first 2 elements could be x, y coordinates of where the object located from original image
        #                                           later 2 elements are the size of the object

print("there are ",len(faces)," faces")

if len(faces) > 0:
  print (type(faces))

  print(type(faces[0]))
  print (len(faces[0]))

  print (type(faces[0][0]))
  print (len(faces[0][0]))
  print (np.shape(faces[0][0]))

  print (type(faces[0][1]))
  print (len(faces[0][1]))

  print (faces[0][1])

  cv2.namedWindow("output", cv2.WINDOW_NORMAL)    

  tmp = img.copy() 
  for item in faces :
    #cv2.imshow ("output", item[0])
    #cv2.waitKey(0)
    cv2.rectangle(tmp, item[1], (255,0,255), 2)
  
  cv2.imshow ("output", tmp)
  cv2.waitKey(0)


 







    




