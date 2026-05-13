from waveshare import EPD_7in5_B
import utime

# Initialize the ePaper display
epd = EPD_7in5_B()

# Clear the buffers: 0 for white background
epd.imageblack.fill(0)  # White background
epd.imagered.fill(0)    # White background

# Draw "Hello World" in black on the black buffer
epd.imageblack.text("Hello World", 10, 10, 1)

# Display the image
epd.display()

# Sleep for a bit to see the display
utime.sleep(5)

# Put the display to sleep
epd.module_exit()