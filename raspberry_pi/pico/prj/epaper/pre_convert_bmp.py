"""
影像預處理工具 - 在電腦端執行
將任何圖片轉換為電子紙可直接讀取的格式
"""

from PIL import Image
import struct

def convert_image_to_epaper(input_path, output_bw_path, output_red_path, 
                            target_size=(800, 480), red_threshold=128):
    """
    將圖片轉換為電子紙格式
    
    參數:
        input_path: 輸入圖片路徑 (支援 PNG/JPG/BMP 等)
        output_bw_path: 黑白資料輸出檔案 (.bin)
        output_red_path: 紅色資料輸出檔案 (.bin)
        target_size: 目標尺寸 (預設 800x480)
        red_threshold: 紅色判斷閾值 (0-255)
    """
    # 開啟圖片並調整尺寸
    img = Image.open(input_path).convert('RGB')
    img = img.resize(target_size, Image.Resampling.LANCZOS)
    
    width, height = img.size
    print(f"處理中: {width}x{height}")
    
    # 計算需要的 bytes 數量
    bytes_per_row = (width + 7) // 8
    total_bytes = bytes_per_row * height
    
    bw_data = bytearray(total_bytes)
    red_data = bytearray(total_bytes)
    
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            
            idx = y * bytes_per_row + (x // 8)
            bit = 7 - (x % 8)
            
            # 紅色判斷
            if r > g and r > b and r > red_threshold:
                # 紅色區域
                red_data[idx] |= (1 << bit)
                bw_data[idx] |= (1 << bit)  # 紅色區域以白色為底
            else:
                # 非紅色區域，計算亮度
                brightness = (r * 299 + g * 587 + b * 114) // 1000
                if brightness < 128:
                    # 黑色
                    bw_data[idx] &= ~(1 << bit)
                    red_data[idx] &= ~(1 << bit)
                else:
                    # 白色
                    bw_data[idx] |= (1 << bit)
                    red_data[idx] &= ~(1 << bit)
    
    # 寫入檔案
    with open(output_bw_path, 'wb') as f:
        f.write(bw_data)
    with open(output_red_path, 'wb') as f:
        f.write(red_data)
    
    print(f"已儲存: {output_bw_path} ({len(bw_data)} bytes)")
    print(f"已儲存: {output_red_path} ({len(red_data)} bytes)")
    
    return bw_data, red_data


def convert_bmp_to_bin(bmp_path, output_bw_path, output_red_path):
    """
    將 BMP 檔案轉換為電子紙格式
    
    使用方式:
        convert_bmp_to_bin("image.bmp", "image_bw.bin", "image_red.bin")
    """
    convert_image_to_epaper(bmp_path, output_bw_path, output_red_path)


def create_test_pattern(output_bw_path, output_red_path):
    """建立測試圖案 (棋盤格 + 紅色條紋)"""
    width, height = 800, 480
    bytes_per_row = width // 8
    total_bytes = bytes_per_row * height
    
    bw_data = bytearray(total_bytes)
    red_data = bytearray(total_bytes)
    
    for y in range(height):
        for x in range(width):
            idx = y * bytes_per_row + (x // 8)
            bit = 7 - (x % 8)
            
            # 上 1/3 紅色
            if y < height // 3:
                red_data[idx] |= (1 << bit)
                bw_data[idx] |= (1 << bit)
            # 中 1/3 棋盤格 (黑白)
            elif y < 2 * height // 3:
                if (x + y) % 20 < 10:
                    bw_data[idx] |= (1 << bit)  # 白色
                else:
                    bw_data[idx] &= ~(1 << bit)  # 黑色
            # 下 1/3 全黑
            else:
                bw_data[idx] &= ~(1 << bit)
    
    with open(output_bw_path, 'wb') as f:
        f.write(bw_data)
    with open(output_red_path, 'wb') as f:
        f.write(red_data)
    
    print(f"測試圖案已儲存")


# 使用範例
if __name__ == "__main__":
    # 轉換一般圖片
    convert_image_to_epaper("input.jpg", "image_bw.bin", "image_red.bin")
    
    # 或建立測試圖案
    create_test_pattern("test_bw.bin", "test_red.bin")