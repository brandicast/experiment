# E-Paper

## Waveshare

- 產品頁面

    https://www.waveshare.net/shop/Pico-ePaper-7.5-B.htm

- 技術文件

    https://www.waveshare.net/wiki/Pico-ePaper-7.5-B


## About BMP

This is something (maybe) I didn't know before:

After extracting the headers from .bmp file, retrieve the actual byte array and try to paint on framebuffer.  It failed at the beginning.  Then according the AI agents, the bmp file byte array was represented from the bottom of the images.   So need to reverse the byte array so that it can paint properly.


## Challenges

- Limited resources in pico
  
  - Need to pre-process the images before sending to/loading on pico.  
    - What I did was try to resize the image to fit the actual screen size.  In this case, it's within 800 * 480
  - With limited RAM, not convenient to do some fancy animation, such as display slowly from one side to another.
- Consider to attached the display to pi zero.
  - Need to try to rewire SPI pins.  (To Do)
  
