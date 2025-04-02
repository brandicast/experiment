from fontlibs import FONT_5x7
import pickle


def display_bitmap_font(font):
    """用 ASCII 圖形輸出 bitmap 字型"""
    width = 32  # 假設字型寬度為 5
    print(font)
    for row in font:
        line = ""
        for col in range(width):  # 正確遍歷所有位，包括最左邊
            if row & (1 << (width - col - 1)):  # 檢查每一列
                line += "■"  # 用 '■' 表示亮起的像素
            else:
                line += "_"  # 用空格表示暗的像素
        print(line)


with open("rubik_5x7.fonts", "rb") as f:
    FONT_5x7 = pickle.load(f)


print("檢視字符 'A':")
display_bitmap_font(FONT_5x7["A"])
