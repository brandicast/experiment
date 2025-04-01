from waveshare import EPD_7in5_B
from textlib import *

epd = EPD_7in5_B()
epd.Clear()

#epd.imagered.fill(0x00)   
epd.imageblack.fill(0xff)

epd.imageblack.text("Black with 0x00", 100, 10, 0x00)   # 0xff 白字 , 0x00 黑字
epd.imageblack.text("Black with 0xff", 100, 20, 0xff)   # 0xff 白字 , 0x00 黑字
epd.imageblack.text("Black with 0xf0", 100, 30, 0xf0)   # 0xff 白字 , 0x00 黑字
epd.imageblack.text("Black with 0x0f", 100, 40, 0x0f)   # 0xff 白字 , 0x00 黑字
epd.imagered.text("Red with 0x00", 10, 110, 0x00)  # 0xff 紅字 , 0x00 黑字
epd.imagered.text("Red with 0xff", 10, 120, 0xff)  # 0xff 紅字 , 0x00 黑字
epd.imagered.text("Red with 0x0f", 10, 130, 0x0f)  # 0xff 紅字 , 0x00 黑字
epd.imagered.text("Red with 0xf0", 10, 140, 0xf0)  # 0xff 紅字 , 0x00 黑字

draw_string(epd.imageblack, 200, 300, "HELLO ! ABC", FONT_5x7, size=7, spacing=1)

epd.display()
'''
epd.imageblack.text("Raspberry Pico", 10, 170, 0x00)
epd.display()

'''
epd.delay_ms(5000)
print("sleep")
epd.sleep()
