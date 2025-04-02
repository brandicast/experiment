import pickle
from PIL import Image, ImageDraw, ImageFont
import numpy as np


def generate_ascii_dict(font_path, width, height, output_pickle):
    ascii_chars = [chr(i) for i in range(32, 127)]  # ASCII 可見字符
    char_dict = {}

    try:
        font = ImageFont.truetype(font_path, height)
    except Exception as e:
        print(f"無法載入字型: {e}")
        return

    for char in ascii_chars:
        image = Image.new("L", (width, height), 0)  # 建立黑底影像
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), char, font=font, fill=255)
        char_array = np.array(image)
        binary_rows = []
        for row in char_array:
            binary_value = int(
                ''.join(['1' if pixel > 128 else '0' for pixel in row]), 2)
            binary_rows.append(binary_value)
        char_dict[char] = binary_rows

    print(char_dict)

    with open(output_pickle, "wb") as f:
        pickle.dump(char_dict, f)

    print(f"字元影像已儲存至 {output_pickle}")


# 使用範例
font_file = "./font_libs/Rubik-Regular.ttf"  # 替換成字型路徑
output_file = "rubik_5x7.fonts"
generate_ascii_dict(font_file, width=5, height=12, output_pickle=output_file)
