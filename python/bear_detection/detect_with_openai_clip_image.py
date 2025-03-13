import torch
import clip
import os
import cv2
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"

# 讀取 CLIP 模型
clip_model, preprocess = clip.load("ViT-B/32", device=device)

# 🐻 讀取「特定玩偶熊」的範例圖片
example_images = ["bread.jpg", ".\\templates\\1.JPG",
                  ".\\templates\\2.JPG", ".\\templates\\3.JPG"]
example_tensors = []

for img_path in example_images:
    img = Image.open(img_path).convert("RGB").resize((256, 256))
    example_tensors.append(preprocess(img).unsqueeze(0).to(device))

# 計算範例圖片的 CLIP 特徵
with torch.no_grad():
    example_features = [clip_model.encode_image(
        tensor) for tensor in example_tensors]
    example_features = torch.stack(example_features).mean(dim=0)  # 平均多張範例圖片
    example_features /= example_features.norm(dim=-1, keepdim=True)

# 📂 照片庫路徑
photo_dir = "D:\\CouldStation_Photo\\2017\\兩姊妹\\采頤的相機"
found_images = []

# 逐張圖片計算相似度
for file in os.listdir(photo_dir):
    img_path = os.path.join(photo_dir, file)

    if not file.lower().endswith((".png", ".jpg", ".jpeg")):
        continue

    # 讀取照片並轉換
    image = Image.open(img_path).convert("RGB").resize((256, 256))
    image_tensor = preprocess(image).unsqueeze(0).to(device)

    # 計算圖片特徵
    with torch.no_grad():
        image_features = clip_model.encode_image(image_tensor)
        image_features /= image_features.norm(dim=-1, keepdim=True)
        similarity = (image_features @ example_features.T).item()

    print(img_path, ":", similarity)
    # 設定相似度門檻（例如 0.75 以上才符合）
    if similarity >= 0.75:
        found_images.append((img_path, similarity))

# 依照相似度排序並顯示
found_images.sort(key=lambda x: x[1], reverse=True)

for img, sim in found_images:
    print(f"找到相似的玩偶熊: {img}（相似度: {sim:.3f}）")

if not found_images:
    print("沒有找到符合條件的特定玩偶熊圖片")
