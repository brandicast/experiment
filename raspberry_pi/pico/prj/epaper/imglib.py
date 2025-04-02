def parse_bmp_header(file):
    # Read BMP file header (first 14 bytes)
    file.seek(0)
    file_type = file.read(2).decode()  # Should be 'BM'
    if file_type != "BM":
        raise ValueError("Not a valid BMP file!")

    file_size = int.from_bytes(file.read(4), "little")
    file.read(4)  # Reserved fields
    pixel_data_offset = int.from_bytes(file.read(4), "little")

    # Read DIB header (next 40 bytes)
    header_size = int.from_bytes(file.read(4), "little")
    width = int.from_bytes(file.read(4), "little")
    height = int.from_bytes(file.read(4), "little")
    file.read(2)  # Number of color planes
    bit_depth = int.from_bytes(file.read(2), "little")

    return {
        "file_size": file_size,
        "pixel_data_offset": pixel_data_offset,
        "width": width,
        "height": height,
        "bit_depth": bit_depth
    }


def read_bmp_pixels(filename, header, framebuffer=None):
    width = header["width"]
    height = header["height"]
    row_bytes = (width + 7) // 8  # Number of bytes per row
    pixel_data_offset = header["pixel_data_offset"]

    with open(filename, "rb") as file:
        file.seek(pixel_data_offset)  # Move to pixel data

        for y in range(height):
            # Read one row of pixels at a time
            row_data = file.read(row_bytes)

            for x in range(width):
                byte = row_data[x // 8]
                bit = (byte >> (7 - (x % 8))) & 1
                # If framebuffer is provided, write directly to it
                if framebuffer:
                    framebuffer.pixel(x, height - 1 - y, bit)  # Flip y-axis
