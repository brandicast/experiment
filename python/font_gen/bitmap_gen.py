from PIL import Image, ImageDraw, ImageFont


def generate_ascii_font(font_path, size, ascii_range=(32, 127)):
    """
    自動生成 ASCII 字型點陣並格式化為 0b 開頭
    Args:
        font_path: 字型文件的路徑 (如 .ttf 字型)
        size: 字型大小 (例如 8 或 12)
        ascii_range: ASCII 字元範圍 (默認為 32 到 126)
    Returns:
        font_dict: 字型點陣字典，格式如 {'A': ['0b01110', '0b10001', ...]}
    """
    font_dict = {}
    font = ImageFont.truetype(font_path, size)

    for code in range(ascii_range[0], ascii_range[1] + 1):
        char = chr(code)
        # 創建單字元圖像
        img = Image.new("1", (size, size), 0)  # 單色模式
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), char, font=font, fill=1)

        # 提取點陣數據並轉換格式
        bitmap = []
        for y in range(size):
            row = 0
            for x in range(size):
                if img.getpixel((x, y)):
                    row |= (1 << (size - x - 1))
            # 格式化為 '0bXXXX' 的字串
            # bitmap.append(f"0b{row:0{size}b}")
            bitmap.append(row)

        font_dict[char] = bitmap

    return font_dict


# 使用範例：生成 5x7 字型，並保存成字典
FONT_PATH = "./font_libs/Rubik-Regular.ttf"  # 替換為字型文件的完整路徑
FONT_SIZE = 7  # 字型大小
FONT_5x7 = generate_ascii_font(FONT_PATH, FONT_SIZE)

# 查看生成的字型點陣
for char, bitmap in FONT_5x7.items():
    print(f"'{char}': {bitmap},")
