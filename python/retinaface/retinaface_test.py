from retinaface import RetinaFace
import cv2

img_path = "..\\resources\\002.jpg"

faces = RetinaFace.detect_faces(img_path)   


print (type(faces))
print(faces)

img = cv2.imread (img_path)
cv2.namedWindow("output", cv2.WINDOW_NORMAL) 


for key in faces:
    identity = faces[key]
 
    facial_area = identity["facial_area"]
    landmarks = identity["landmarks"]
 
 
#highlight facial area
    cv2.rectangle(img, (facial_area[2], facial_area[3]), (facial_area[0], facial_area[1]), (255, 255, 255), 1)
 
#extract facial area
#img = cv2.imread(img_path)
    facial_img = img[facial_area[1]: facial_area[3], facial_area[0]: facial_area[2]]
    print (type(facial_img))
    cv2.imshow ("output", facial_img)
    cv2.waitKey(0)


#highlight the landmarks
# print (tuple(int(x) for x in (landmarks["left_eye"])))   ##  this conver tuple from float to int
    cv2.circle(img, tuple(int(x) for x in (landmarks["left_eye"])), 1, (0, 0, 255), -1)
    cv2.circle(img, tuple(int(x) for x in (landmarks["right_eye"])), 1, (0, 0, 255), -1)
    cv2.circle(img, tuple(int(x) for x in (landmarks["nose"])), 1, (0, 0, 255), -1)
    cv2.circle(img, tuple(int(x) for x in (landmarks["mouth_left"])), 1, (0, 0, 255), -1)
    cv2.circle(img, tuple(int(x) for x in (landmarks["mouth_right"])), 1, (0, 0, 255), -1)


cv2.imshow ("output", img)
cv2.waitKey(0)