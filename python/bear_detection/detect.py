import os
import cv2
from ultralytics import YOLO
from tensorflow.keras.applications import ResNet50, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np

# 設定資料夾路徑
input_folder = "path/to/your/photos_folder"  # 待處理的圖片資料夾
output_folder = "path/to/output_folder"     # 保存標註後的圖片
os.makedirs(output_folder, exist_ok=True)

# 加載 YOLO 模型 (適用於 COCO 資料集)
model = YOLO("yolov8n.pt")  # 輕量 YOLOv8 模型
target_class_id = 88  # "teddy bear" 在 COCO 中的類別 ID

# 加載 ResNet50 模型作為特徵提取器
feature_extractor = ResNet50(
    weights="imagenet", include_top=False, pooling="avg")

# 定義提取特徵的函數


def extract_features(image, box):
    x1, y1, x2, y2 = map(int, box)
    cropped_img = image[y1:y2, x1:x2]  # 裁剪出檢測框內的區域
    resized_img = cv2.resize(cropped_img, (224, 224))  # 調整大小為 ResNet 輸入大小
    array_img = preprocess_input(img_to_array(
        resized_img).reshape((1, 224, 224, 3)))
    features = feature_extractor.predict(array_img)
    return features

# 計算餘弦相似度


def cosine_similarity(features1, features2):
    return np.dot(features1, features2.T) / (np.linalg.norm(features1) * np.linalg.norm(features2))


# 載入目標玩偶熊的特徵
target_image_path = "path/to/your/target_teddy_bear.jpg"
target_image = cv2.imread(target_image_path)
target_features = extract_features(
    target_image, (0, 0, target_image.shape[1], target_image.shape[0]))

# 遍歷資料夾中的所有圖片並進行檢測
for img_name in os.listdir(input_folder):
    img_path = os.path.join(input_folder, img_name)
    image = cv2.imread(img_path)
    if image is None:  # 檢查是否成功載入圖片
        print(f"無法載入圖片: {img_name}")
        continue

    # 使用 YOLO 模型進行物件檢測
    results = model(image)

    # 儲存每個檢測框的相似度和位置
    similarities = []
    for box in results[0].boxes.data.cpu().numpy():
        class_id, confidence, x1, y1, x2, y2 = int(box[5]), box[4], *box[:4]
        if class_id == target_class_id:  # 檢查是否為 "teddy bear"
            detected_features = extract_features(image, (x1, y1, x2, y2))
            similarity = cosine_similarity(target_features, detected_features)
            similarities.append((similarity[0][0], (x1, y1, x2, y2)))

    # 在圖片上標註檢測結果
    for idx, (similarity, box) in enumerate(similarities):
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 畫框
        cv2.putText(image, f"Sim: {similarity:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)  # 標記相似度

    # 保存結果圖片
    output_path = os.path.join(output_folder, img_name)
    cv2.imwrite(output_path, image)

    # 打印檢測結果
    print(f"圖片: {img_name}")
    for idx, (similarity, box) in enumerate(similarities):
        print(f"  - 第 {idx + 1} 個玩偶熊，相似度: {similarity:.2f}，位置: {box}")

print(f"處理完成！檢測結果已保存到資料夾: {output_folder}")
