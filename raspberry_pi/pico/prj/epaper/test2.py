from waveshare import EPD_7in5_B
import gc


def bmp_to_binary_from_bytes(filepath, display):
    framebuffer = display.imageblack

    with open(filepath, 'rb') as f:
        data = f.read()

    # BMP Header Info
    pixel_data_offset = int.from_bytes(data[10:14], 'little')
    width = int.from_bytes(data[18:22], 'little')
    height = int.from_bytes(data[22:26], 'little')
    bit_depth = int.from_bytes(data[28:30], 'little')

    print("width=", width, ", height=", height)
    if bit_depth != 1:
        raise ValueError("Only 1-bit BMP files are supported.")

    # Each row is padded to 4-byte alignment
    row_bytes = ((width + 31) // 32) * 4

    for y in range(height):
        # BMP rows are stored from bottom to top
        row_start = pixel_data_offset + (height - 1 - y) * row_bytes
        row_data = data[row_start:row_start + row_bytes]

        x_axis = 0
        for byte in row_data:
            for i in range(8):
                # bits.append(str((byte >> (7 - i)) & 1))
                framebuffer.pixel(x_axis, y, (byte >> (7 - i)) & 1)
                x_axis = x_axis + 1


def bmp_to_binary_write_bytes(filepath, display):

    with open(filepath, 'rb') as f:
        data = f.read(30)

        # BMP Header Info
        file_size = int.from_bytes(data[2:6], 'little')
        pixel_data_offset = int.from_bytes(data[10:14], 'little')
        width = int.from_bytes(data[18:22], 'little')
        height = int.from_bytes(data[22:26], 'little')
        bit_depth = int.from_bytes(data[28:30], 'little')

        print("width=", width, ", height=", height, " file size=", file_size)
        if bit_depth != 1:
            raise ValueError("Only 1-bit BMP files are supported.")

        # Each row is padded to 4-byte alignment
        row_bytes = ((width + 31) // 32) * 4

        display.send_command(0x10)
        for y in range(height):
            # BMP rows are stored from bottom to top
            row_start = pixel_data_offset + (height - 1 - y) * row_bytes
            # row_data = data[row_start:row_start + row_bytes]
            f.seek(row_start)
            row_data = f.read(row_bytes)
            display.send_data_rowbyte(row_data)

            '''
            display.digital_write(display.dc_pin, 1)
            display.digital_write(display.cs_pin, 0)
            display.spi.write(row_data)
            display.digital_write(display.cs_pin, 1)
            '''


def print_memory_info():
    print("----Allocated memory:", gc.mem_alloc(),
          "Free memory:", gc.mem_free())


epd = EPD_7in5_B()
print_memory_info()
print("start clear")
epd.Clear_Without_Display()
print("finish clear")
# print_memory_info()
filename = "output.bmp"
# epd.imagered.fill(0x00)
# epd.imageblack.fill(0xff)
print_memory_info()
bmp_to_binary_write_bytes(filename, epd)
print_memory_info()
epd.TurnOnDisplay()
print_memory_info()

'''

epd.imageblack.text("Black with 0x00", 100, 10, 0x00)   # 0xff 白字 , 0x00 黑字
epd.imageblack.text("Black with 0xff", 100, 20, 0xff)   # 0xff 白字 , 0x00 黑字
epd.imageblack.text("Black with 0xf0", 100, 30, 0xf0)   # 0xff 白字 , 0x00 黑字
epd.imageblack.text("Black with 0x0f", 100, 40, 0x0f)   # 0xff 白字 , 0x00 黑字
epd.imagered.text("Red with 0x00", 10, 110, 0x00)  # 0xff 紅字 , 0x00 黑字
epd.imagered.text("Red with 0xff", 10, 120, 0xff)  # 0xff 紅字 , 0x00 黑字
epd.imagered.text("Red with 0x0f", 10, 130, 0x0f)  # 0xff 紅字 , 0x00 黑字
epd.imagered.text("Red with 0xf0", 10, 140, 0xf0)  # 0xff 紅字 , 0x00 黑

draw_string(epd.imageblack, 200, 300, "HELLO ! ABC",
            FONT_5x7, size=7, spacing=1)

epd.imageblack.text("Raspberry Pico", 10, 170, 0x00)
epd.display()

'''
epd.delay_ms(5000)
print("sleep")
epd.sleep()
