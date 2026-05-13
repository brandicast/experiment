from epaper_7_5 import EPD_7in5_B

epd = EPD_7in5_B()

try:
    # 執行內建測試範例
    epd.demo()

    # 額外測試：顯示訊息後進入睡眠
    print("\n=== 額外測試：顯示訊息 ===")
    epd.clear("white")
    epd.draw_text(200, 200, "Test Complete!", epd.BLACK, 2)
    epd.draw_text(180, 250, "Entering Sleep Mode...", epd.RED, 1)
    epd.display()
    epd._delay_ms(3000)

    # 進入睡眠模式
    epd.sleep()

except KeyboardInterrupt:
    print("\n程式被中斷")
    epd.sleep()
except Exception as e:
    print(f"發生錯誤: {e}")
    epd.sleep()