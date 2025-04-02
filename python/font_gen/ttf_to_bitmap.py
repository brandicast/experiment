import pickle
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen


class GlyphToBitmapPen(BasePen):
    def __init__(self, grid_width, grid_height, scale_x, scale_y):
        super().__init__(None)
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.bitmap = [[0] * grid_width for _ in range(grid_height)]

    def _moveTo(self, p):
        self.current_point = p

    def _lineTo(self, p):
        self._draw_line(self.current_point, p)
        self.current_point = p

    def _curveToOne(self, p1, p2, p3):
        self._lineTo(p3)  # Approximating curves as lines for simplicity

    def _draw_line(self, start, end):
        # Map coordinates to pixel grid
        x1 = int(start[0] / self.scale_x)
        y1 = int(start[1] / self.scale_y)
        x2 = int(end[0] / self.scale_x)
        y2 = int(end[1] / self.scale_y)

        # Bresenham's line algorithm for grid plotting
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            if 0 <= x1 < self.grid_width and 0 <= y1 < self.grid_height:
                self.bitmap[y1][x1] = 1
            if (x1 == x2) and (y1 == y2):
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy


def generate_ascii_bitmap_fixed(font_path, grid_width, grid_height, ascii_range=(32, 126)):
    """
    生成所有 ASCII 字元的 5x7 點陣並返回整數形式字典
    Args:
        font_path: 字型文件 (.ttf)
        grid_width: 網格寬度 (像素)
        grid_height: 網格高度 (像素)
        ascii_range: ASCII 字元範圍 (預設為 32-126)
    Returns:
        font_dict: 字型字典，格式 {'A': [14, 17, ...]}
    """
    font_dict = {}
    font = TTFont(font_path)

    # 確定縮放比例
    scale_x = font["head"].unitsPerEm / grid_width
    scale_y = font["head"].unitsPerEm / grid_height

    # 遍歷 ASCII 範圍內的所有字符
    for code in range(ascii_range[0], ascii_range[1] + 1):
        char = chr(code)
        glyph_name = font.getBestCmap().get(ord(char))
        if not glyph_name:
            continue
        glyph = font.getGlyphSet()[glyph_name]

        # 使用 GlyphToBitmapPen 渲染字符
        pen = GlyphToBitmapPen(grid_width, grid_height, scale_x, scale_y)
        glyph.draw(pen)

        # 將二維 bitmap 數據轉換為一維整數陣列
        bitmap = [int(''.join(str(pixel) for pixel in row), 2)
                  for row in pen.bitmap]
        font_dict[char] = bitmap

    return font_dict


def save_font_dict_pickle(font_dict, filename):
    """
    使用 pickle 保存字型資料到文件
    Args:
        font_dict: 字型字典
        filename: 保存的文件名
    """
    with open(filename, 'wb') as f:
        pickle.dump(font_dict, f)
    print(f"字型資料已保存到 {filename}")


def display_font_dict(font_dict, grid_width):
    """
    在終端輸出字型點陣字典的內容
    Args:
        font_dict: 字型字典
        grid_width: 點陣寬度，用於二進制表示
    """
    for char, bitmap in font_dict.items():
        print(f"{char}:")
        for row in bitmap:
            print(f"{row:0{grid_width}b}")  # 用二進制格式顯示每行
        print("")  # 每個字符之間留空行


        # Example usage
        # Replace with your actual font file path
FONT_PATH = "./font_libs/Rubik-Regular.ttf"
GRID_WIDTH = 12
GRID_HEIGHT = 10
OUTPUT_FILE = "ascii_5x7.fonts"

ascii_font = generate_ascii_bitmap_fixed(FONT_PATH, GRID_WIDTH, GRID_HEIGHT)
display_font_dict(ascii_font, GRID_WIDTH)
save_font_dict_pickle(ascii_font, OUTPUT_FILE)
