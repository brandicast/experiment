from PIL import Image, ImageDraw, ImageFont


# 使用範例：生成 5x7 字型，並保存成字典
FONT_PATH = "./font_libs/Rubik-Regular.ttf"  # 替換為字型文件的完整路徑
SIZE = 7
FONT_WIDTH = 32  # 字型大小
FONT_HEIGHT = 32

text = 'i'

font = ImageFont.truetype(FONT_PATH, int(FONT_HEIGHT * 0.8))
bbox = font.getbbox(text)
width = bbox[2] - bbox[0]  # Right - Left gives width
height = bbox[3] - bbox[1]  # Bottom - Top gives height


# 創建單字元圖像
img = Image.new("1", (FONT_WIDTH, FONT_HEIGHT), 0)  # 單色模式
draw = ImageDraw.Draw(img)
draw.text((round((FONT_WIDTH-width)/2), 0),
          text, font=font, fill=1,)  # 垂直居中繪製


# 提取點陣數據並統一高度
bitmap = []
for y in range(FONT_HEIGHT):
    tmp = ''
    for x in range(FONT_WIDTH):
        tmp += str(img.getpixel((x, y)))
    bitmap.append(int(tmp, 2))

img.save("output.png")
print(bitmap)
