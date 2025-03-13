import torch
import clip
import cv2
import os
import numpy as np
from PIL import Image
from ultralytics import YOLO

# 使用 GPU 或 CPU
device = "cuda" if torch.cuda.is_available() else "cpu"

# 讀取 CLIP 模型
model, preprocess = clip.load("ViT-B/32", device=device)

# 讀取 YOLOv8 物件偵測模型
yolo_model = YOLO("yolov8n.pt")  # 輕量版 YOLOv8 模型

# 設定要搜尋的照片庫資料夾
photo_dir = "D:\\CouldStation_Photo\\2017\\兩姊妹\\采頤的相機"

# 設定要搜尋的類別
search_text = ["a teddy bear", "a stuffed animal", "a plush toy"]
text_tokens = clip.tokenize(search_text).to(device)

# 儲存結果
found_images = []

# 取得文字特徵並進行 L2 正規化
with torch.no_grad():
    text_features = model.encode_text(text_tokens)
    text_features /= text_features.norm(dim=-1, keepdim=True)

# 逐張處理照片
for file in os.listdir(photo_dir):
    img_path = os.path.join(photo_dir, file)

    if not file.lower().endswith((".png", ".jpg", ".jpeg")):
        continue  # 忽略非圖片檔案

    # 讀取圖片
    image = Image.open(img_path).convert("RGB").resize((256, 256))
    image_tensor = preprocess(image).unsqueeze(0).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image_tensor)
        image_features /= image_features.norm(dim=-1, keepdim=True)  # L2 正規化
        similarity = (image_features @ text_features.T)  # 計算相似度
        max_similarity = similarity.max().item()

    # 只處理相似度高的圖片
    if max_similarity < 0.7:
        continue

    # 使用 YOLOv8 進行物件偵測
    img_cv = cv2.imread(img_path)
    results = yolo_model(img_cv)

    teddy_bears = []  # 儲存 teddy bear 的 bounding box
    for result in results:
        for box in result.boxes.data:
            x1, y1, x2, y2, conf, cls = box.tolist()
            if int(cls) == 83:  # YOLOv8 中 teddy bear 的 class ID = 83
                teddy_bears.append((x1, y1, x2, y2))

    # 檢查是否有「不同大小」的 teddy bear
    if len(teddy_bears) >= 2:
        sizes = [(x2 - x1) * (y2 - y1) for x1, y1, x2, y2 in teddy_bears]
        min_size, max_size = min(sizes), max(sizes)

        if max_size / min_size > 1.5:  # 如果最大 teddy bear 是最小 teddy bear 的 1.5 倍以上
            found_images.append((img_path, max_similarity))

# 顯示找到的圖片
found_images.sort(key=lambda x: x[1], reverse=True)  # 按相似度排序
for img, sim in found_images:
    print(f"{img} (相似度: {sim:.4f})")

if not found_images:
    print("沒有找到包含大小不一的 teddy bear 的圖片")
