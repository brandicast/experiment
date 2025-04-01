from waveshare import EPD_7in5_B

epd = EPD_7in5_B()
epd.Clear()

epd.imageblack.text("Hi !", 5, 10, 0x00)
epd.display()
epd.delay_ms(5000)
epd.Clear()
epd.imagered.text("This is a test", 5, 40, 0xff)