import framebuf
from fonts import *

# 設定顯示器的寬度和高度
WIDTH = 800
HEIGHT = 400

# 創建 framebuffer，按位元方式初始化為單色緩衝區
buffer = bytearray(WIDTH * HEIGHT // 8)  # 每 8 個像素佔用 1 個字節
fb = framebuf.FrameBuffer(buffer, WIDTH, HEIGHT, framebuf.MONO_HLSB)

# 定義字型點陣（例如簡單的 'A' 字型，5x7）
FONT_5x7 = FONT_5x7_BIN

FONT_WIDTH = 8


def draw_char(fb, x, y, char, font, size=1):
    """在 framebuffer 上繪製字符
    Args:
        fb: FrameBuffer 物件
        x, y: 字符的起始繪製位置
        char: 要繪製的字符
        font: 字符點陣字型
        size: 字符縮放大小
    """
    if char not in font:
        print(f"字型中未定義字符: {char}")
        return

    bitmap = font[char]
    width = FONT_WIDTH if bitmap else 0
    height = len(bitmap)

    for row in range(height):
        for col in range(width):
            if bitmap[row] & (1 << (width - col - 1)):  # 判斷點陣位是否為 1
                for dy in range(size):  # 縮放高度
                    for dx in range(size):  # 縮放寬度
                        fb.pixel(x + col * size + dx, y + row * size + dy, 0)


def draw_string(fb, x, y, text, font, size=1, spacing=1):
    """在 framebuffer 上繪製整個字串
    Args:
        fb: FrameBuffer 物件
        x, y: 字串的起始繪製位置
        text: 要繪製的字串
        font: 字符點陣字型
        size: 字符縮放大小
        spacing: 字符間距（以像素為單位）
    """
    cursor_x = x
    for char in text:
        draw_char(fb, cursor_x, y, char, font, size)
        cursor_x += (FONT_WIDTH * size) + spacing  # 更新游標位置


# 使用範例：繪製字串 "A" 到 800x400 顯示器，大小為 3x 縮放
draw_string(fb, 50, 50, "A", FONT_5x7, size=3, spacing=2)

# 硬體特定的顯示處理 (視您使用的顯示器驅動而定)
# 例如：將 framebuffer 數據寫入到顯示屏
# oled.display(fb)
