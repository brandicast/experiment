from deepface import DeepFace
#from deepface.commons import distance as dst, functions
import matplotlib.pyplot as plt
import cv2
import numpy as np

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
#face detection and alignment
face = DeepFace.detectFace(img_path = "resources\\002.jpg", 
        target_size = (224, 224), 
        detector_backend = backends[1], 
        enforce_detection = True,
        align=True
)

print (type(face))
print (np.shape(face))
print (face)

plt.imshow (face)
plt.waitforbuttonpress()
#cv2.imshow("XX", face)
#cv2.waitKey(0)