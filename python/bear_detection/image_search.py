from ultralytics import YOLO  # 確保已安裝 YOLOv8 (`pip install ultralytics`)
import torch
import clip
import os
import cv2
import numpy as np
from PIL import Image


def find_similar_images(template_dir: str, search_dir: str, similarity_threshold: float = 0.75):
    """
    使用 CLIP 在 search_dir 及其子目錄中尋找與 template_dir 內範例圖片相似的玩偶熊。

    :param template_dir: 範例熊圖片的資料夾
    :param search_dir: 要搜尋的照片資料夾（包含子目錄）
    :param similarity_threshold: 相似度門檻（預設 0.75）
    :return: 符合條件的圖片清單
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    clip_model, preprocess = clip.load("ViT-B/32", device=device)

    # 讀取範例圖片並計算特徵
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

    # 計算範例圖片的 CLIP 特徵（取平均值）
    with torch.no_grad():
        example_features = [clip_model.encode_image(
            tensor) for tensor in example_tensors]
        example_features = torch.stack(example_features).mean(dim=0)
        example_features /= example_features.norm(dim=-1, keepdim=True)

    found_images = []

    # 遞迴遍歷搜尋資料夾及其子目錄
    for root, _, files in os.walk(search_dir):
        for file in files:
            img_path = os.path.join(root, file)
            if not file.lower().endswith((".png", ".jpg", ".jpeg")):
                continue

            img_array = cv2.imdecode(np.fromfile(
                img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
            image = Image.fromarray(cv2.cvtColor(
                img_array, cv2.COLOR_BGR2RGB)).resize((256, 256))
            image_tensor = preprocess(image).unsqueeze(0).to(device)

            with torch.no_grad():
                image_features = clip_model.encode_image(image_tensor)
                image_features /= image_features.norm(dim=-1, keepdim=True)
                similarity = (image_features @ example_features.T).item()

            if similarity >= similarity_threshold:
                found_images.append((img_path, similarity))

    found_images.sort(key=lambda x: x[1], reverse=True)  # 依相似度排序
    return found_images


def find_similar_images_with_clip_yolo(template_dir: str, search_dir: str, similarity_threshold: float = 0.75):
    """
    1. 使用 CLIP 在 search_dir 及其子目錄中尋找與 template_dir 內範例圖片相似的圖片。
    2. 在這些圖片中，使用 YOLOv8 偵測 "熊" 的位置，回傳座標。

    :param template_dir: 範例熊圖片的資料夾
    :param search_dir: 要搜尋的照片資料夾（包含子目錄）
    :param similarity_threshold: CLIP 相似度門檻（預設 0.75）
    :return: 包含 (圖片路徑, 相似度, [偵測到的熊的座標]) 的列表
    """
    # 設定裝置
    device = "cuda" if torch.cuda.is_available() else "cpu"
    clip_model, preprocess = clip.load("ViT-B/32", device=device)

    print("Loading Templates from : ", template_dir)
    # 讀取範例圖片並計算特徵
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

    # 計算範例圖片的 CLIP 特徵（取平均值）
    with torch.no_grad():
        example_features = [clip_model.encode_image(
            tensor) for tensor in example_tensors]
        example_features = torch.stack(example_features).mean(dim=0)
        example_features /= example_features.norm(dim=-1, keepdim=True)

    found_images = []

    print("Start searching from : ", search_dir,
          "with similarity : ", similarity_threshold)
    # 遞迴遍歷搜尋資料夾及其子目錄
    for root, _, files in os.walk(search_dir):
        for file in files:
            img_path = os.path.join(root, file)
            print(".", end="")
            if not file.lower().endswith((".png", ".jpg", ".jpeg")):
                continue

            try:
                img_array = cv2.imdecode(np.fromfile(
                    img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
                image = Image.fromarray(cv2.cvtColor(
                    img_array, cv2.COLOR_BGR2RGB)).resize((256, 256))
                image_tensor = preprocess(image).unsqueeze(0).to(device)

                with torch.no_grad():
                    image_features = clip_model.encode_image(image_tensor)
                    image_features /= image_features.norm(dim=-1, keepdim=True)
                    similarity = (image_features @ example_features.T).item()

                if similarity >= similarity_threshold:
                    found_images.append((img_path, similarity))
            except Exception:
                continue

    print("Now Yolo")
    # 使用 YOLO 偵測 "熊" 的位置
    yolo_model = YOLO("yolov8n.pt")  # 載入 YOLOv8 的預訓練模型

    results = []
    for img_path, similarity in found_images:
        img_array = cv2.imdecode(np.fromfile(
            img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        yolo_results = yolo_model(img_array,  verbose=False)

        bear_boxes = []
        for result in yolo_results:
            for box in result.boxes:
                cls = int(box.cls.item())  # 物件類別索引
                if cls == 0:  # 0 是 "person"，但 YOLOv8 沒有直接的 "teddy bear" 類別
                    continue  # 如果不確定熊的類別，可以列出所有可能的類別

                x1, y1, x2, y2 = map(int, box.xyxy[0])  # 取得邊界框座標
                bear_boxes.append({"x1": x1, "y1": y1, "x2": x2, "y2": y2})

        results.append((img_path, similarity, bear_boxes))

    return results


def find_similar_images_yolo_clip(template_dir: str, search_dir: str, similarity_threshold: float = 0.75):
    """
    先用 YOLO 找 "teddy bear"，再用 CLIP 判斷是否是特定玩偶熊
    """

    # 使用 GPU 或 CPU
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # 載入 CLIP
    clip_model, preprocess = clip.load("ViT-B/32", device=device)

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

    print("Now do YOLO")
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
            # print(img_path, end=" ")
            for result in yolo_results:
                for box, cls in zip(result.boxes.xyxy, result.boxes.cls):
                    class_id = int(cls.item())
                    class_name = result.names[class_id]
             #       print(class_name, end=" ")
                    # 只保留 teddy bear (YOLO 類別 ID = 77)
                    if class_name == "teddy bear":
                        bear_boxes.append(box.cpu().numpy())

            # print()
            # 如果沒找到熊，跳過
            if not bear_boxes:
                continue

            print(img_path, end=" ")
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
                print(bear_similarity,  end=" ")
                if bear_similarity >= similarity_threshold:
                    final_boxes.append((x1, y1, x2, y2))

            # 只回傳符合條件的結果
            if final_boxes:
                found_images.append((img_path, bear_similarity, final_boxes))
            print()

    return found_images
