import cv2
import numpy as np
import os

# 讀取玩偶的模板圖片
template = cv2.imread("bread.jpg", 0)


if template is None:
    print("Error loading template image")
    exit()

scale_factor = 0.5
threshold = 250000000.  # 設定匹配門檻
template = cv2.resize(template,  (0, 0), fx=scale_factor, fy=scale_factor,
                      interpolation=cv2.INTER_AREA)
w, h = template.shape[::-1]


print("Scale_Factor :" + str(scale_factor))


cv2.namedWindow("output", cv2.WINDOW_NORMAL)
cv2.resizeWindow('output', 400, 300)
cv2.imshow('output', template)
cv2.waitKey(0)
# cv2.destroyWindow('output')


# 照片庫
photo_dir = "D:\\CouldStation_Photo\\2017\\兩姊妹\\采頤的相機"
found_images = []

for file in os.listdir(photo_dir):
    upper_filename = file.upper()
    if upper_filename.endswith("JPG") or upper_filename.endswith("JPEG"):
        img_path = os.path.join(photo_dir, file)
        img = cv2.imdecode(np.fromfile(
            img_path, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)

        if img is None:
            print(f"Error loading image: {img_path}")
        else:
            # 匹配模板
            res = cv2.matchTemplate(img, template, cv2.TM_SQDIFF)

            # 找出匹配點
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            print(upper_filename)
            print("Minimum value:", min_val)

            threshold = min_val + min_val * 0.1

            print("Threshold    :" + str(threshold))

            loc = np.where(res <= threshold)

            if len(loc[0]) > 0:  # 若有匹配結果
                print("找到的圖片：", file)

                for pt in zip(*loc[::-1]):  # 轉置位置座標
                    cv2.rectangle(
                        img, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (46, 139, 87), 3)
                    print(".")

                cv2.imshow('output', img)
                cv2.waitKey(0)
