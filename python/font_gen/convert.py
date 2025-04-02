from PIL import Image, ImageEnhance


def parse_bmp_header(data):
    # BMP file header (14 bytes)
    file_type = data[0:2]  # Should be "BM"
    file_size = int.from_bytes(data[2:6], "little")  # File size
    pixel_data_offset = int.from_bytes(
        data[10:14], "little")  # Where pixel data starts

    # DIB header (40 bytes)
    width = int.from_bytes(data[18:22], "little")  # Image width
    height = int.from_bytes(data[22:26], "little")  # Image height
    # Bits per pixel (e.g., 1, 8, 24)
    bit_depth = int.from_bytes(data[28:30], "little")

    return {
        "file_type": file_type.decode(),
        "file_size": file_size,
        "pixel_data_offset": pixel_data_offset,
        "width": width,
        "height": height,
        "bit_depth": bit_depth,
    }


def extract_pixel_data(data, header):
    pixel_data_start = header["pixel_data_offset"]
    width = header["width"]
    height = header["height"]
    bit_depth = header["bit_depth"]

    # Only supports monochrome BMP (1-bit per pixel)
    if bit_depth != 1:
        raise ValueError("Only 1-bit BMP files are supported.")

    row_bytes = (width + 7) // 8  # Each row is padded to the nearest byte
    pixel_array = []

    for y in range(height):
        row_start = pixel_data_start + y * row_bytes
        row_data = data[row_start:row_start + row_bytes]

        # Convert each byte to bits
        row_pixels = []
        for byte in row_data:
            for i in range(8):
                if len(row_pixels) < width:
                    row_pixels.append((byte >> (7 - i)) & 1)
        pixel_array.append(row_pixels)

    return pixel_array


TARGET_WIDTH = 711
TARGET_HEIGHT = 400

# 載入 JPEG 圖片
image = Image.open("prama.png")

# image = image.resize((TARGET_WIDTH, TARGET_HEIGHT))

# 提升圖像對比度
enhancer = ImageEnhance.Contrast(image)
image = enhancer.enhance(1.5)  # 1.5 倍對比度

# 提升圖像銳度
enhancer = ImageEnhance.Sharpness(image)
image = enhancer.enhance(2.0)  # 2 倍銳度


# 將圖片轉換為 1-bit 單色 (黑白)
# image = image.convert("L", dither=Image.FLOYDSTEINBERG).resize((TARGET_WIDTH, TARGET_HEIGHT))   # '1' 模式表示每像素 1 位
image = image.convert("1", dither=Image.FLOYDSTEINBERG)  # '1' 模式表示每像素 1 位

# 保存成單色 BMP 格式
image.save("output.bmp", format="BMP")

# 可選：將像素轉換為 bytearray（適合嵌入式處理）
bitmap_data = image.tobytes()
print("Bitmap data length:", len(bitmap_data))  # 顯示資料大小


with open("output.bmp", "rb") as f:
    data = f.read()
header = parse_bmp_header(data)
print(header)
pixels = extract_pixel_data(data, header)
