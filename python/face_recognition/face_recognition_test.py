import cv2
import face_recognition
'''
# 側臉辨識效果不好，或者說沒有deepface/retinaface 好
# picture rotation seems to be a problem

'''


img_bgr = face_recognition.load_image_file('..\\deepface\\resources\\003.jpg')
img_rgb = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2RGB)
cv2.namedWindow("output", cv2.WINDOW_NORMAL)    
#cv2.imshow('output',img_rgb)
#cv2.waitKey(0)
#--------- Detecting Face -------
faces = face_recognition.face_locations(img_rgb)
print(type(faces))
#copy = img_rgb.copy()
for face in faces:
    # ------ Drawing bounding boxes around Faces------------------------
    cv2.rectangle(img_rgb, (face[3], face[0]),(face[1], face[2]), (255,0,255), 2)
cv2.imshow('output', img_rgb)
#cv2.imshow('Ori',img_rgb)
cv2.waitKey(0)


unknown_bgr = face_recognition.load_image_file('..\\deepface\\resources\\007.jpg')

my_face_encoding = face_recognition.face_encodings(img_bgr)[0]
unknown_face_encoding = face_recognition.face_encodings(unknown_bgr)[0]

results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)

if results[0] == True:
    print("It's the same person")
else:
    print("It's NOT the same person")