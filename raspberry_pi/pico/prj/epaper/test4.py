from epaper_7_5_b import EPD_7in5_B
import utime    


# 初始化 (可選擇 normal/fast/partial)
epd = EPD_7in5_B(mode="normal")

print("=== 開始測試 ===\n")

# 測試 1: 基本繪圖
print("1. 基本繪圖測試...")
epd.clear("white")
epd.imageblack.text("Hello Waveshare!", 10, 10, 0x00)
epd.imagered.text("7.5 inch e-Paper", 10, 40, 0xFF)
epd.draw_rect(10, 70, 200, 100, epd.BLACK, fill=False)
epd.draw_rect(20, 80, 180, 80, epd.RED, fill=True)
epd.display()
utime.sleep(3)

# 測試 2: BMP 顯示 (需準備 BMP 檔案)
print("\n2. BMP 顯示測試...")
epd.clear("white")

# 嘗試顯示單色 BMP (如果檔案存在)
try:
    epd.display_bmp("output.bmp", x=0, y=0)
    epd.display()
    utime.sleep(2)
except:
    print("  找不到 /sd/test_bw.bmp，跳過")

# 嘗試顯示彩色 BMP (如果檔案存在)
try:
    epd.display_bmp_color("/sd/test_color.bmp", x=0, y=0)
    epd.display()
    utime.sleep(2)
except:
    print("  找不到 /sd/test_color.bmp，跳過")

# 測試 3: 圓形與線條
print("\n3. 幾何圖形測試...")
epd.clear("white")
epd.draw_circle(400, 240, 100, epd.BLACK, fill=False)
epd.draw_circle(400, 240, 50, epd.RED, fill=True)
epd.draw_line(0, 0, 799, 479, epd.BLACK)
epd.draw_line(0, 479, 799, 0, epd.RED)
epd.display()
utime.sleep(3)

# 測試 4: 清除畫面並進入睡眠
print("\n4. 清除畫面並進入睡眠...")
epd.clear("white")
epd.sleep()

print("\n=== 測試完成 ===")