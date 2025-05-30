# *****************************************************************************
# * | File        :	  Pico_ePaper-7.5-B.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2021-05-27
# # | Info        :   python demo
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from machine import Pin, SPI
import framebuf
import utime

# Display resolution
EPD_WIDTH = 800
EPD_HEIGHT = 480

RST_PIN = 12
DC_PIN = 8
CS_PIN = 9
BUSY_PIN = 13


class EPD_7in5_B:
    def __init__(self):
        self.reset_pin = Pin(RST_PIN, Pin.OUT)

        self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self.partFlag = 1

        self.spi = SPI(1)
        self.spi.init(baudrate=4000_000)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)

        self.buffer_black = bytearray(self.height * self.width // 8)
        self.buffer_red = bytearray(self.height * self.width // 8)
        self.imageblack = framebuf.FrameBuffer(
            self.buffer_black, self.width, self.height, framebuf.MONO_HLSB)
        self.imagered = framebuf.FrameBuffer(
            self.buffer_red, self.width, self.height, framebuf.MONO_HLSB)
        self.init()
        # self.init_Fast()

    def digital_write(self, pin, value):
        pin.value(value)

    def digital_read(self, pin):
        return pin.value()

    def delay_ms(self, delaytime):
        utime.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        self.spi.write(bytearray(data))

    def module_exit(self):
        self.digital_write(self.reset_pin, 0)

    # Hardware reset
    def reset(self):
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(200)
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(2)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(200)

    def send_command(self, command):
        self.digital_write(self.dc_pin, 0)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([command])
        self.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([data])
        self.digital_write(self.cs_pin, 1)

    def send_data1(self, buf):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi.write(bytearray(buf))
        self.digital_write(self.cs_pin, 1)

    def send_data_rowbyte(self, data):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi.write(data)
        self.digital_write(self.cs_pin, 1)

    def WaitUntilIdle(self):
        print("e-Paper busy")
        while (self.digital_read(self.busy_pin) == 0):   # Wait until the busy_pin goes LOW
            self.delay_ms(20)
        self.delay_ms(20)
        print("e-Paper busy release")

    def TurnOnDisplay(self):
        self.send_command(0x12)  # DISPLAY REFRESH
        self.delay_ms(100)  # !!!The delay here is necessary, 200uS at least!!!
        self.WaitUntilIdle()

    def init(self):
        # EPD hardware init start
        self.reset()

        self.send_command(0x06)     # btst
        self.send_data(0x17)
        self.send_data(0x17)
        # If an exception is displayed, try using 0x38
        self.send_data(0x28)
        self.send_data(0x17)

#         self.send_command(0x01)  # POWER SETTING
#         self.send_data(0x07)
#         self.send_data(0x07)     # VGH=20V,VGL=-20V
#         self.send_data(0x3f)     # VDH=15V
#         self.send_data(0x3f)     # VDL=-15V

        self.send_command(0x04)  # POWER ON
        self.delay_ms(100)
        self.WaitUntilIdle()

        self.send_command(0X00)   # PANNEL SETTING
        self.send_data(0x0F)      # KW-3f   KWR-2F	BWROTP 0f	BWOTP 1f

        self.send_command(0x61)     # tres
        self.send_data(0x03)     # source 800
        self.send_data(0x20)
        self.send_data(0x01)     # gate 480
        self.send_data(0xE0)

        self.send_command(0X15)
        self.send_data(0x00)

        self.send_command(0X50)     # VCOM AND DATA INTERVAL SETTING
        self.send_data(0x11)
        self.send_data(0x07)

        self.send_command(0X60)     # TCON SETTING
        self.send_data(0x22)

        self.send_command(0x65)     # Resolution setting
        self.send_data(0x00)
        self.send_data(0x00)     # 800*480
        self.send_data(0x00)
        self.send_data(0x00)

        return 0

    def init_Fast(self):
        # EPD hardware init start
        self.reset()

        self.send_command(0X00)  # PANNEL SETTING
        self.send_data(0x0F)     # KW-3f   KWR-2F	BWROTP 0f	BWOTP 1f

        self.send_command(0x04)  # POWER ON
        self.delay_ms(100)
        self.WaitUntilIdle()

        self.send_command(0x06)   # btst
        self.send_data(0x27)
        self.send_data(0x27)
        self.send_data(0x18)
        self.send_data(0x17)

        self.send_command(0xE0)
        self.send_data(0x02)
        self.send_command(0xE5)
        self.send_data(0x5A)

        self.send_command(0X50)  # VCOM AND DATA INTERVAL SETTING
        self.send_data(0x11)
        self.send_data(0x07)

        return 0

    def init_part(self):
        # EPD hardware init start
        self.reset()

        self.send_command(0X00)
        self.send_data(0x1F)

        self.send_command(0x04)
        self.delay_ms(100)
        self.WaitUntilIdle()

        self.send_command(0xE0)
        self.send_data(0x02)
        self.send_command(0xE5)
        self.send_data(0x6E)

        self.send_command(0X50)
        self.send_data(0xA9)
        self.send_data(0x07)

        # EPD hardware init end
        return 0

    def Clear(self):
        high = self.height
        if (self.width % 8 == 0):
            wide = self.width // 8
        else:
            wide = self.width // 8 + 1

        self.send_command(0x10)
        for i in range(0, wide):
            self.send_data1([0xff] * high)

        self.send_command(0x13)
        for i in range(0, wide):
            self.send_data1([0x00] * high)

        self.TurnOnDisplay()

    def ClearRed(self):

        high = self.height
        if (self.width % 8 == 0):
            wide = self.width // 8
        else:
            wide = self.width // 8 + 1

        self.send_command(0x10)
        for i in range(0, wide):
            self.send_data1([0xff] * high)

        self.send_command(0x13)
        for i in range(0, wide):
            self.send_data1([0xff] * high)

        self.TurnOnDisplay()

    def ClearBlack(self):

        high = self.height
        if (self.width % 8 == 0):
            wide = self.width // 8
        else:
            wide = self.width // 8 + 1

        self.send_command(0x10)
        for i in range(0, wide):
            self.send_data1([0x00] * high)

        self.send_command(0x13)
        for i in range(0, wide):
            self.send_data1([0x00] * high)

        self.TurnOnDisplay()

    def Clear_Without_Display(self):
        high = self.height
        if (self.width % 8 == 0):
            wide = self.width // 8
        else:
            wide = self.width // 8 + 1

        self.send_command(0x10)
        for i in range(0, wide):
            self.send_data1([0xff] * high)

        self.send_command(0x13)
        for i in range(0, wide):
            self.send_data1([0x00] * high)

        # self.TurnOnDisplay()

    def display(self):

        high = self.height
        if (self.width % 8 == 0):
            wide = self.width // 8
        else:
            wide = self.width // 8 + 1

        # send black data
        self.send_command(0x10)
        for i in range(0, wide):
            self.send_data1(self.buffer_black[(i * high): ((i+1) * high)])

        # send red data
        self.send_command(0x13)
        for i in range(0, wide):
            self.send_data1(self.buffer_red[(i * high): ((i+1) * high)])

        self.TurnOnDisplay()

    def display_Base_color(self, color):
        if (self.width % 8 == 0):
            Width = self.width // 8
        else:
            Width = self.width // 8 + 1
        Height = self.height
        self.send_command(0x10)  # Write Black and White image to RAM
        for j in range(Height):
            for i in range(Width):
                self.send_data(color)

        self.send_command(0x13)  # Write Black and White image to RAM
        for j in range(Height):
            for i in range(Width):
                self.send_data(~color)

        # self.send_command(0x12)
        # self.delay_ms(100)
        # self.WaitUntilIdle()

    def display_Partial(self, Image, Xstart, Ystart, Xend, Yend):
        if ((Xstart % 8 + Xend % 8 == 8 & Xstart % 8 > Xend % 8) | Xstart % 8 + Xend % 8 == 0 | (Xend - Xstart) % 8 == 0):
            Xstart = Xstart // 8 * 8
            Xend = Xend // 8 * 8
        else:
            Xstart = Xstart // 8 * 8
            if Xend % 8 == 0:
                Xend = Xend // 8 * 8
            else:
                Xend = Xend // 8 * 8 + 1

        Width = (Xend - Xstart) // 8
        Height = Yend - Ystart

        # self.send_command(0x50)
        # self.send_data(0xA9)
        # self.send_data(0x07)

        # This command makes the display enter partial mode
        self.send_command(0x91)
        self.send_command(0x90)  # resolution setting
        self.send_data(Xstart//256)
        self.send_data(Xstart % 256)  # x-start

        self.send_data((Xend-1)//256)
        self.send_data((Xend-1) % 256)  # x-end

        self.send_data(Ystart//256)  #
        self.send_data(Ystart % 256)  # y-start

        self.send_data((Yend-1)//256)
        self.send_data((Yend-1) % 256)  # y-end
        self.send_data(0x01)

        if self.partFlag == 1:
            self.partFlag = 0
            self.send_command(0x10)
            for i in range(0, Width):
                self.send_data1([0xFF] * Height)

        self.send_command(0x13)  # Write Black and White image to RAM
        for i in range(0, Width):
            self.send_data1(Image[(i * Height): ((i+1) * Height)])

        self.send_command(0x12)
        self.delay_ms(100)
        self.WaitUntilIdle()

    def sleep(self):
        self.send_command(0x02)  # power off
        self.WaitUntilIdle()
        self.send_command(0x07)  # deep sleep
        self.send_data(0xa5)


if __name__ == '__main__':
    epd = EPD_7in5_B()
    epd.Clear()

    epd.imageblack.fill(0xff)
    epd.imagered.fill(0x00)

    epd.imageblack.text("Waveshare", 5, 10, 0x00)
    epd.imagered.text("Pico_ePaper-7.5-B", 5, 40, 0xff)
    epd.imageblack.text("Raspberry Pico", 5, 70, 0x00)
    epd.display()
    epd.delay_ms(5000)

    epd.imageblack.vline(10, 90, 60, 0x00)
    epd.imageblack.vline(120, 90, 60, 0x00)
    epd.imagered.hline(10, 90, 110, 0xff)
    epd.imagered.hline(10, 150, 110, 0xff)
    epd.imagered.line(10, 90, 120, 150, 0xff)
    epd.imagered.line(120, 90, 10, 150, 0xff)
    epd.display()
    epd.delay_ms(5000)

    epd.imageblack.rect(10, 180, 50, 80, 0x00)
    epd.imageblack.fill_rect(70, 180, 50, 80, 0x00)
    epd.imagered.rect(10, 300, 50, 80, 0xff)
    epd.imagered.fill_rect(70, 300, 50, 80, 0xff)
    epd.display()
    epd.delay_ms(5000)

    for k in range(0, 3):
        for j in range(0, 3):
            for i in range(0, 5):
                epd.imageblack.fill_rect(
                    200+100+j*200, i*20+k*200, 100, 10, 0x00)
            for i in range(0, 5):
                epd.imagered.fill_rect(
                    200+0+j*200, i*20+100+k*200, 100, 10, 0xff)
    epd.display()
    epd.delay_ms(5000)

    # # partial update
    # epd.init()
    # epd.imageblack.fill(0xff)
    # epd.display_Base_color(0xFF)
    # epd.init_part()
    # for i in range(0, 10):
    # epd.imageblack.fill_rect(175, 105, 10, 10, 0xff)
    # epd.imageblack.text(str(i), 177, 106, 0x00)
    # epd.display_Partial(epd.buffer_black, 0, 0, 800, 480)

    epd.init()
    epd.Clear()
    epd.delay_ms(2000)
    print("sleep")
    epd.sleep()
