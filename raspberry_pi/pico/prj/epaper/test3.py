from epaper_7_5 import EPD_7in5_B_Optimized
import utime

# ==================== 效能比較測試 ====================
def benchmark():
    """測試不同模式的效能差異"""
    print("\n=== 效能測試 ===\n")
    
    # 測試標準模式
    print("1. 標準模式:")
    start = utime.ticks_ms()
    epd_normal = EPD_7in5_B_Optimized(mode=EPD_7in5_B_Optimized.MODE_NORMAL)
    epd_normal.clear("white")
    init_time = utime.ticks_diff(utime.ticks_ms(), start)
    print(f"   初始化 + 清除時間: {init_time} ms")
    epd_normal.enter_deep_sleep()
    
    # 釋放記憶體
    del epd_normal
    
    # 測試快速模式
    print("\n2. 快速模式:")
    start = utime.ticks_ms()
    epd_fast = EPD_7in5_B_Optimized(mode=EPD_7in5_B_Optimized.MODE_FAST)
    epd_fast.clear("white")
    init_time = utime.ticks_diff(utime.ticks_ms(), start)
    print(f"   初始化 + 清除時間: {init_time} ms")
    epd_fast.enter_deep_sleep()
    
    del epd_fast
    
    print("\n=== 建議 ===")
    print("- 一般使用: 標準模式 (最穩定)")
    print("- 頻繁更新: 快速模式 (犧牲少許對比度)")
    print("- 電池供電: 更新後立即進入深度睡眠")
    print("- 降低電壓可省電但會影響顯示品質")
    

# 效能測試 (可選)
benchmark()

# 選擇模式: MODE_NORMAL, MODE_FAST, MODE_PARTIAL
epd = EPD_7in5_B_Optimized(mode=EPD_7in5_B_Optimized.MODE_NORMAL)

# 基本測試
epd.clear("white")
epd.draw_text(10, 10, "Optimized Version", epd.BLACK, 1)
epd.draw_text(10, 40, "Fast & Power Efficient", epd.RED, 1)
epd.draw_rect(10, 70, 200, 100, epd.BLACK, fill=False)
epd.draw_rect(20, 80, 180, 80, epd.RED, fill=True)
epd.display()

# 等待 3 秒後進入睡眠
utime.sleep(3)
epd.enter_deep_sleep()
print("程式結束")