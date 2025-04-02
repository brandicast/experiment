from PIL import Image, ImageDraw, ImageFont
import pickle
import cv2
import numpy as np


def generate_ascii_font_fixed_height(font_path, size, target_height, ascii_range=(32, 127)):
    """
    生成具有固定高度的 ASCII 字型點陣
    Args:
        font_path: 字型文件的路徑 (如 .ttf)
        size: 字型大小 (例如 12)
        target_height: 強制的目標高度 (例如 7 像素)
        ascii_range: ASCII 字元範圍 (默認為 32 到 126)
    Returns:
        font_dict: 點陣字型字典，格式 {'A': [0b01110, 0b10001, ...]}
    """
    font_dict = {}
    font = ImageFont.truetype(font_path, target_height)

    ascent, descent = font.getmetrics()  # 獲取字型度量

    print(ascent)
    print(descent)

    for code in range(ascii_range[0], ascii_range[1] + 1):
        char = chr(code)
        # 創建單字元圖像
        img = Image.new("1", (size, target_height), 0)  # 單色模式
        draw = ImageDraw.Draw(img)
        draw.text((0, target_height - ascent),
                  char, font=font, fill=1, align="center")  # 垂直居中繪製

        # 提取點陣數據並統一高度
        bitmap = []
        for y in range(target_height):
            tmp = ''
            for x in range(size):
                tmp += str(img.getpixel((x, y)))
            bitmap.append(int(tmp, 2))
            # 格式化為 '0bXXXX' 的字串
            # bitmap.append(f"0b{row:0{size}b}")

        # 裁剪和填充以強制固定高度
        bitmap = [row for row in bitmap if row != 0]  # 移除全零行
        while len(bitmap) < target_height:  # 添加空白行補齊高度
            bitmap.insert(0, 0)  # 在頂部添加空行
        bitmap = bitmap[-target_height:]  # 確保不超過目標高度

        font_dict[char] = bitmap

    return font_dict


# 使用範例：生成 5x7 字型，並保存成字典
FONT_PATH = "./font_libs/Rubik-Regular.ttf"  # 替換為字型文件的完整路徑
FONT_SIZE = 32  # 字型大小
TARGET_HEIGHT = 32
FONT_5x7 = generate_ascii_font_fixed_height(
    FONT_PATH, FONT_SIZE, TARGET_HEIGHT)

with open("rubik_5x7.fonts", "wb") as f:
    pickle.dump(FONT_5x7, f)

# 查看生成的字型點陣
for char, bitmap in FONT_5x7.items():
    print(f"'{char}': {bitmap},")
