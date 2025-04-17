
def bmp_to_binary_from_bytes(filepath, framebuffer=None):

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
