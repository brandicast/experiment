"""
7.5inch e-Paper B V3 - 最佳化版本
整合 Waveshare 穩定性 + Spec 完整性 + 效能優化
"""

from machine import Pin, SPI
import framebuf
import utime

EPD_WIDTH = 800
EPD_HEIGHT = 480

# 腳位定義
RST_PIN = 12
DC_PIN = 8
CS_PIN = 9
BUSY_PIN = 13


class EPD_7in5_B_Optimized:
    # 顏色常數
    BLACK = 0
    WHITE = 1
    RED = 2
    
    # 刷新模式
    MODE_NORMAL = 0      # 標準模式 (~15秒)
    MODE_FAST = 1        # 快速模式 (~10秒，對比度略降)
    MODE_PARTIAL = 2     # 局部模式 (僅黑白，速度更快)
    
    def __init__(self, spi_bus=1, mode=MODE_NORMAL):
        # 硬體初始化
        self.rst_pin = Pin(RST_PIN, Pin.OUT)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)
        self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        
        # SPI 初始化 (可調整速率)
        self.spi = SPI(spi_bus)
        self.spi.init(baudrate=4000000, polarity=0, phase=0)
        
        # 雙 buffer
        self.buffer_black = bytearray(self.height * self.width // 8)
        self.buffer_red = bytearray(self.height * self.width // 8)
        self.imageblack = framebuf.FrameBuffer(
            self.buffer_black, self.width, self.height, framebuf.MONO_HLSB)
        self.imagered = framebuf.FrameBuffer(
            self.buffer_red, self.width, self.height, framebuf.MONO_HLSB)
        
        # 根據模式選擇初始化
        self.mode = mode
        if mode == self.MODE_FAST:
            self._init_fast()
        elif mode == self.MODE_PARTIAL:
            self._init_partial()
        else:
            self._init_normal()
        
        print(f"初始化完成 - 模式: {['標準', '快速', '局部'][mode]}")
    
    # ==================== 底層函式 (與官方版相同) ====================
    def _digital_write(self, pin, value):
        pin.value(value)
    
    def _digital_read(self, pin):
        return pin.value()
    
    def _delay_ms(self, ms):
        utime.sleep(ms / 1000.0)
    
    def _send_command(self, cmd):
        self._digital_write(self.dc_pin, 0)
        self._digital_write(self.cs_pin, 0)
        self.spi.write(bytearray([cmd]))
        self._digital_write(self.cs_pin, 1)
    
    def _send_data(self, data):
        self._digital_write(self.dc_pin, 1)
        self._digital_write(self.cs_pin, 0)
        self.spi.write(bytearray([data]))
        self._digital_write(self.cs_pin, 1)
    
    def _send_data_bytes(self, data_bytes):
        self._digital_write(self.dc_pin, 1)
        self._digital_write(self.cs_pin, 0)
        self.spi.write(data_bytes)
        self._digital_write(self.cs_pin, 1)
    
    def _reset(self):
        self._digital_write(self.rst_pin, 1)
        self._delay_ms(200)
        self._digital_write(self.rst_pin, 0)
        self._delay_ms(2)
        self._digital_write(self.rst_pin, 1)
        self._delay_ms(200)
    
    def _wait_until_idle(self):
        while self._digital_read(self.busy_pin) == 0:
            self._delay_ms(10)
        self._delay_ms(10)
    
    # ==================== 三種初始化模式 ====================
    def _init_normal(self):
        """標準初始化 (Waveshare 官方版，最穩定)"""
        self._reset()
        
        self._send_command(0x01)  # POWER SETTING
        self._send_data(0x07)
        self._send_data(0x07)
        self._send_data(0x3f)
        self._send_data(0x3f)
        
        self._send_command(0x06)  # BOOSTER SOFT START
        self._send_data(0x17)
        self._send_data(0x17)
        self._send_data(0x28)
        self._send_data(0x17)
        
        self._send_command(0x04)  # POWER ON
        self._delay_ms(100)
        self._wait_until_idle()
        
        self._send_command(0x00)  # PANEL SETTING
        self._send_data(0x0F)
        
        self._send_command(0x61)  # RESOLUTION
        self._send_data(0x03)
        self._send_data(0x20)
        self._send_data(0x01)
        self._send_data(0xE0)
        
        self._send_command(0x50)  # VCOM INTERVAL
        self._send_data(0x11)
        self._send_data(0x07)
        
        self._send_command(0x60)  # TCON
        self._send_data(0x22)
    
    def _init_fast(self):
        """快速初始化 (犧牲少許對比度換取速度)"""
        self._reset()
        
        self._send_command(0x00)
        self._send_data(0x0F)
        
        self._send_command(0x04)
        self._delay_ms(100)
        self._wait_until_idle()
        
        self._send_command(0x06)
        self._send_data(0x27)
        self._send_data(0x27)
        self._send_data(0x18)
        self._send_data(0x17)
        
        self._send_command(0xE0)
        self._send_data(0x02)
        self._send_command(0xE5)
        self._send_data(0x5A)
        
        self._send_command(0x50)
        self._send_data(0x11)
        self._send_data(0x07)
        
        self._send_command(0x61)
        self._send_data(0x03)
        self._send_data(0x20)
        self._send_data(0x01)
        self._send_data(0xE0)
        
        self._send_command(0x60)
        self._send_data(0x22)
    
    def _init_partial(self):
        """局部更新初始化 (僅黑白，速度最快)"""
        self._reset()
        
        self._send_command(0x00)
        self._send_data(0x1F)
        
        self._send_command(0x04)
        self._delay_ms(100)
        self._wait_until_idle()
        
        self._send_command(0xE0)
        self._send_data(0x02)
        self._send_command(0xE5)
        self._send_data(0x6E)
        
        self._send_command(0x50)
        self._send_data(0xA9)
        self._send_data(0x07)
    
    # ==================== 效能優化函式 ====================
    def set_spi_speed(self, baudrate):
        """動態調整 SPI 速率 (預設 4MHz，最高可到 10MHz)"""
        self.spi.init(baudrate=baudrate, polarity=0, phase=0)
        print(f"SPI 速率設為 {baudrate} Hz")
    
    def set_frame_rate(self, fps):
        """設定幀率 (影響刷新速度，預設 5Hz)"""
        fps_table = {5: 0x00, 10: 0x01, 15: 0x02, 20: 0x03, 30: 0x04,
                     40: 0x05, 50: 0x06, 60: 0x07, 70: 0x08, 80: 0x09,
                     90: 0x0A, 100: 0x0B, 110: 0x0C, 130: 0x0D, 150: 0x0E, 200: 0x0F}
        if fps in fps_table:
            self._send_command(0x30)
            self._send_data(fps_table[fps])
            print(f"幀率設為 {fps} Hz")
    
    def set_voltage(self, vgh_vgl="20V", vdh="15V", vdl="-15V"):
        """調整驅動電壓 (影響對比度與功耗)"""
        vgh_table = {"9V": 0x00, "10V": 0x01, "11V": 0x02, "12V": 0x03,
                     "17V": 0x04, "18V": 0x05, "19V": 0x06, "20V": 0x07}
        
        # 電壓越低越省電，但對比度較差
        vdh_table = {10: 0x28, 11: 0x2C, 12: 0x30, 13: 0x34, 14: 0x38, 15: 0x3C}
        vdl_table = {-10: 0x28, -11: 0x2C, -12: 0x30, -13: 0x34, -14: 0x38, -15: 0x3C}
        
        self._send_command(0x01)  # POWER SETTING
        self._send_data(0x07)
        self._send_data(vgh_table.get(vgh_vgl, 0x07))
        self._send_data(vdh_table.get(vdh, 0x3F))
        self._send_data(vdl_table.get(vdl, 0x3F))
        print(f"電壓設定: VGH/VGL={vgh_vgl}, VDH={vdh}V, VDL={vdl}V")
    
    def enter_deep_sleep(self):
        """進入深度睡眠 (最省電: ~15μA)"""
        self._send_command(0x02)  # POWER OFF
        self._wait_until_idle()
        self._send_command(0x07)  # DEEP SLEEP
        self._send_data(0xA5)
    
    def enter_sleep(self):
        """進入睡眠 (省電: ~20μA，保留 RAM)"""
        self._send_command(0x02)  # POWER OFF
        self._wait_until_idle()
        # 注意：0x07 是深度睡眠，這裡只用 POWER OFF
        print("進入睡眠模式")
    
    def wake_up(self):
        """從睡眠中喚醒"""
        self._send_command(0x04)  # POWER ON
        self._delay_ms(100)
        self._wait_until_idle()
        print("已喚醒")
    
    # ==================== 畫面操作 ====================
    def clear(self, color="white"):
        if color == "white":
            self.imageblack.fill(0xFF)
            self.imagered.fill(0x00)
        elif color == "black":
            self.imageblack.fill(0x00)
            self.imagered.fill(0x00)
        elif color == "red":
            self.imageblack.fill(0xFF)
            self.imagered.fill(0xFF)
        self.display()
    
    def display(self):
        """刷新畫面"""
        high = self.height
        wide = self.width // 8 if self.width % 8 == 0 else self.width // 8 + 1
        
        self._send_command(0x10)  # 黑白資料
        for i in range(wide):
            start = i * high
            end = (i + 1) * high
            self._send_data_bytes(self.buffer_black[start:end])
        
        self._send_command(0x13)  # 紅色資料
        for i in range(wide):
            start = i * high
            end = (i + 1) * high
            self._send_data_bytes(self.buffer_red[start:end])
        
        self._send_command(0x12)  # 刷新
        self._delay_ms(100)
        self._wait_until_idle()
    
    # ==================== 繪圖函式 ====================
    def set_pixel(self, x, y, color):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return
        if color == self.BLACK:
            self.imageblack.pixel(x, y, 0)
            self.imagered.pixel(x, y, 0)
        elif color == self.WHITE:
            self.imageblack.pixel(x, y, 1)
            self.imagered.pixel(x, y, 0)
        elif color == self.RED:
            self.imageblack.pixel(x, y, 1)
            self.imagered.pixel(x, y, 1)
    
    def draw_rect(self, x, y, w, h, color, fill=False):
        if fill:
            for i in range(x, min(x + w, self.width)):
                for j in range(y, min(y + h, self.height)):
                    self.set_pixel(i, j, color)
        else:
            for i in range(x, min(x + w, self.width)):
                self.set_pixel(i, y, color)
                if h > 1:
                    self.set_pixel(i, min(y + h - 1, self.height - 1), color)
            if h > 2:
                for j in range(y + 1, min(y + h - 1, self.height)):
                    self.set_pixel(x, j, color)
                    if w > 1:
                        self.set_pixel(min(x + w - 1, self.width - 1), j, color)
    
    def draw_text(self, x, y, text, color, size=1):
        if size == 1:
            if color == self.BLACK or color == self.WHITE:
                self.imageblack.text(text, x, y, 0 if color == self.BLACK else 1)
            else:
                self.imagered.text(text, x, y, 1)
        else:
            # 放大文字
            for i, ch in enumerate(text):
                temp_buf = bytearray(8 * 16 // 8)
                temp_fb = framebuf.FrameBuffer(temp_buf, 8, 16, framebuf.MONO_HLSB)
                temp_fb.text(ch, 0, 0, 1)
                for py in range(16):
                    for px in range(8):
                        if (temp_buf[py] >> (7 - px)) & 1:
                            for sy in range(size):
                                for sx in range(size):
                                    self.set_pixel(x + i * 8 * size + px * size + sx,
                                                  y + py * size + sy, color)


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


# ==================== 主程式 ====================
if __name__ == '__main__':
    # 選擇模式: MODE_NORMAL, MODE_FAST, MODE_PARTIAL
    epd = EPD_7in5_B_Optimized(mode=EPD_7in5_B_Optimized.MODE_NORMAL)
    
    # 效能測試 (可選)
    # benchmark()
    
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