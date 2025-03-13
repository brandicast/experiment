import torch
import clip
import os
from PIL import Image

# 選擇 GPU 或 CPU
device = "cuda" if torch.cuda.is_available() else "cpu"

# 讀取 CLIP 模型
model, preprocess = clip.load("ViT-B/32", device=device)

# 設定搜尋的目標
search_text = [
    "a photo of a teddy bear",
    "a photo of a plush bear",
    "a photo of a stuffed bear with other objects",
    "a toy bear in a room",
    "a teddy bear on a table with other things",
    "a person holding a teddy bear"
]
text_tokens = clip.tokenize(search_text).to(device)

# 照片庫路徑
photo_dir = "D:\\CouldStation_Photo\\2017\\兩姊妹\\采頤的相機"

# 儲存結果
found_images = []

# 預先計算文字特徵
with torch.no_grad():
    text_features = model.encode_text(text_tokens)
    text_features /= text_features.norm(dim=-1, keepdim=True)  # L2 正規化

# 逐張圖片處理
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

    print(img_path, ":", max_similarity)
    # 設定相似度閾值（可調整）
    if max_similarity > 0.3:
        found_images.append((img_path, max_similarity))

# 顯示找到的圖片
found_images.sort(key=lambda x: x[1], reverse=True)  # 按相似度排序
for img, sim in found_images:
    print(f"{img} (相似度: {sim:.4f})")

if not found_images:
    print("沒有找到 teddy bear 的圖片")
