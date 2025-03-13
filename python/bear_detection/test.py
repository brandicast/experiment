from image_search import find_similar_images_yolo_clip
import cv2
import numpy as np

# 設定範例熊圖片資料夾 & 搜尋目錄
template_folder = "D:\\workspace\\experiment\\python\\bear_detection\\templates"
search_folder = "D:\\CouldStation_Photo\\2017\\兩姊妹\\采頤的相機"
similarity_threshold = 0.8  # 可以調整

# 執行搜尋
results = find_similar_images_yolo_clip(
    template_folder, search_folder, similarity_threshold)


cv2.namedWindow("output", cv2.WINDOW_NORMAL)
cv2.resizeWindow('output', 400, 300)


# 顯示結果
for img_path, sim, box in results:
    print(f"找到類似的熊玩偶: {img_path}（相似度: {sim:.3f}） ", box)
    img = cv2.imdecode(np.fromfile(
        img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    cv2.rectangle(
        img, box[0][:2], box[0][-2:], (255, 190, 154), 3)
    cv2.imshow('output', img)
    cv2.waitKey(0)
