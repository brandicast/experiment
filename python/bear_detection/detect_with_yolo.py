from PIL import Image
import numpy as np
import clip
import torch
import cv2
import os
from ultralytics import YOLO

# 讀取 YOLOv8 物件偵測模型
yolo_model = YOLO("yolov8n.pt")  # 輕量版 YOLOv8

# 照片庫路徑
photo_dir = "D:\\CouldStation_Photo\\2017\\兩姊妹\\采頤的相機"

# 儲存結果
found_images = []

# 逐張圖片處理
for file in os.listdir(photo_dir):
    img_path = os.path.join(photo_dir, file)

    if not file.lower().endswith((".png", ".jpg", ".jpeg")):
        continue  # 忽略非圖片檔案

    # 讀取圖片
    img_cv = cv2.imread(img_path)

    # 使用 YOLOv8 進行物件偵測
    results = yolo_model(img_cv)

    # 檢查是否有 teddy bear
    for result in results:
        for box in result.boxes.data:
            _, _, _, _, _, cls = box.tolist()
            if int(cls) == 83 or int(cls) == 77:  # YOLOv8 中 teddy bear 的 class ID = 83
                found_images.append(img_path)
                break  # 找到一個就跳出

# 顯示找到的圖片
for img in found_images:
    print(f"找到 teddy bear: {img}")

if not found_images:
    print("沒有找到 teddy bear 的圖片")


def find_similar_images(template_dir: str, search_dir: str, similarity_threshold: float = 0.75):
    """
    先用 YOLO 找 "teddy bear"，再用 CLIP 判斷是否是特定玩偶熊
    """

    # 使用 GPU 或 CPU
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # 載入 CLIP
    clip_model, preprocess = clip.load("ViT-B/32", device=device, jit=True)

    # 載入 YOLO（小模型較快）
    yolo_model = YOLO("yolov8s.pt")  # 換成 "yolov8n.pt" 會更快，但準確度略低

    # 讀取範例圖片並計算 CLIP 特徵
    example_tensors = []
    for file in os.listdir(template_dir):
        img_path = os.path.join(template_dir, file)
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            img_array = cv2.imdecode(np.fromfile(
                img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
            img = Image.fromarray(cv2.cvtColor(
                img_array, cv2.COLOR_BGR2RGB)).resize((256, 256))
            example_tensors.append(preprocess(img).unsqueeze(0).to(device))

    if not example_tensors:
        raise ValueError("範例資料夾中沒有可用的圖片！")

    # 計算範例熊的 CLIP 特徵
    with torch.no_grad():
        example_features = [clip_model.encode_image(
            tensor) for tensor in example_tensors]
        example_features = torch.stack(example_features).mean(dim=0)
        example_features /= example_features.norm(dim=-1, keepdim=True)

    found_images = []

    # 遍歷搜尋資料夾
    for root, _, files in os.walk(search_dir):
        for file in files:
            img_path = os.path.join(root, file)
            if not file.lower().endswith((".png", ".jpg", ".jpeg")):
                continue

            # 讀取圖片
            img_array = cv2.imdecode(np.fromfile(
                img_path, dtype=np.uint8), cv2.IMREAD_COLOR)

            # 先用 YOLO 偵測 teddy bear
            yolo_results = yolo_model(img_array, verbose=False)

            bear_boxes = []
            for result in yolo_results:
                for box, cls in zip(result.boxes.xyxy, result.boxes.cls):
                    class_id = int(cls.item())
                    class_name = result.names[class_id]

                    # 只保留 teddy bear (YOLO 類別 ID = 77)
                    if class_name == "teddy bear":
                        bear_boxes.append(box.cpu().numpy())

            # 如果沒找到熊，跳過
            if not bear_boxes:
                continue

            # 進一步用 CLIP 判斷是否是特定熊玩偶
            final_boxes = []
            for box in bear_boxes:
                x1, y1, x2, y2 = map(int, box)
                bear_crop = img_array[y1:y2, x1:x2]  # 擷取 YOLO 偵測到的熊
                bear_img = Image.fromarray(cv2.cvtColor(
                    bear_crop, cv2.COLOR_BGR2RGB)).resize((256, 256))
                bear_tensor = preprocess(bear_img).unsqueeze(0).to(device)

                with torch.no_grad():
                    bear_features = clip_model.encode_image(bear_tensor)
                    bear_features /= bear_features.norm(dim=-1, keepdim=True)
                    bear_similarity = (
                        bear_features @ example_features.T).item()

                if bear_similarity >= similarity_threshold:
                    final_boxes.append((x1, y1, x2, y2))

            # 只回傳符合條件的結果
            if final_boxes:
                found_images.append((img_path, final_boxes))

    return found_images
