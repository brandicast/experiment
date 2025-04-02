from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen


class GlyphToBitmapPen(BasePen):
    def __init__(self, grid_width, grid_height, scale_x, scale_y, baseline_offset):
        super().__init__(None)
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.baseline_offset = baseline_offset
        self.bitmap = [[0] * grid_width for _ in range(grid_height)]

    def _moveTo(self, p):
        self.current_point = p

    def _lineTo(self, p):
        self._draw_line(self.current_point, p)
        self.current_point = p

    def _curveToOne(self, p1, p2, p3):
        self._lineTo(p3)  # Simplify curves as straight lines

    def _draw_line(self, start, end):
        # Map glyph coordinates to pixel grid, adjusting for baseline and flipping y-axis
        x1 = int(start[0] / self.scale_x)
        y1 = self.grid_height - 1 - \
            int(start[1] / self.scale_y) - self.baseline_offset
        x2 = int(end[0] / self.scale_x)
        y2 = self.grid_height - 1 - \
            int(end[1] / self.scale_y) - self.baseline_offset

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            if 0 <= x1 < self.grid_width and 0 <= y1 < self.grid_height:
                self.bitmap[y1][x1] = 1
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy


def extract_glyph_outline(font_path, char, grid_width, grid_height):
    """
    Extract bitmap from a font glyph, including ascent and descent handling.
    Args:
        font_path: Path to the .ttf font file.
        char: The character to render.
        grid_width: Width of the grid in pixels.
        grid_height: Height of the grid in pixels.
    Returns:
        bitmap: A 2D list representing the character's bitmap.
    """
    font = TTFont(font_path)
    glyph_name = font.getBestCmap().get(ord(char))
    if not glyph_name:
        raise ValueError(f"Character {char} not found in the font.")

    glyph = font.getGlyphSet()[glyph_name]
    units_per_em = font["head"].unitsPerEm

    # Get ascent and descent
    ascent = font["hhea"].ascent
    descent = abs(font["hhea"].descent)
    total_height = ascent + descent

    # Calculate scaling factors and baseline offset
    scale_x = units_per_em / grid_width
    scale_y = total_height / grid_height
    baseline_offset = int(descent / total_height * grid_height)

    # Debug: Output scaling and offset details
    print(f"Scale X: {scale_x}, Scale Y: {scale_y}")
    print(f"Baseline Offset: {baseline_offset} (Grid height: {grid_height})")

    # Use the pen to draw the glyph
    pen = GlyphToBitmapPen(grid_width, grid_height,
                           scale_x, scale_y, baseline_offset)
    glyph.draw(pen)

    return pen.bitmap


FONT_PATH = "./font_libs/Rubik-Regular.ttf"
bitmap = extract_glyph_outline(FONT_PATH, "!", 10, 20)

print(bitmap)

for row in bitmap:
    print("".join(["■" if px else " " for px in row]))

'''
for row in bitmap:
    line = ""
    for col in range(len(row)):  # 正確遍歷所有位，包括最左邊
        if row[col] == 1:  # 檢查每一列
            line += "■"  # 用 '■' 表示亮起的像素
        else:
            line += "_"  # 用空格表示暗的像素
    print(line)
'''
