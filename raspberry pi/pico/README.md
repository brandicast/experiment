# Pico WH

# Sites

- https://www.raspberrypi.com/
- https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html
- https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf
- https://datasheets.raspberrypi.com/picow/pico-w-datasheet.pdf

# Pico Pin out 

- https://electrocredible.com/raspberry-pi-pico-w-pinout-guide-diagrams/

    - VBUS/VSYS

# Useful when Pico becomes bricks

https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html#resetting-flash-memory

# Quick Remimder

## MicroPython firmware

- How to load MicroPython onto Pico
    https://www.raspberrypi.com/documentation/microcontrollers/micropython.html

    ```
    1. Hold down the BOOTSEL button, and plug in the micro USB cable.
    2. A drive called RPI-RP2 should pop up. 
    3. Go ahead and drag the MicroPython firmware.uf2 file onto this drive. This     programs the MicroPython firmware onto the flash memory on your Raspberry Pi Pico

- Build your own MicroPython firmware 

    Reason?  To enable UART REPL (However, USB shall be enough)

## MicroPython library 

1.  Need to following the guildline to build the uf2
2. Go pico/micropython/lib/micropython-lib/ for more libraries which are not included by default, such as ntptime.py

### Memo 

 - wlan.status() code
```
STAT_IDLE            0  no connection and no activity
STAT_CONNECTING      1  connecting in progress,
STAT_WRONG_PASSWORD -3  failed due to incorrect password,
STAT_NO_AP_FOUND    -2  failed because no access point replied,
STAT_CONNECT_FAIL   -1  failed due to other problems,
STAT_GOT_IP          3  connection successful.
```

 - VSYS output current

   ~50ma

- Transistors

    - NPN / PNP 
        
        https://www.rohm.com.tw/electronics-basics/transistors/tr_what1

    - MOSFET

        https://cn.shindengen.co.jp/products/semi/column/basic/mosfet/mosfet_1.html

    - 電晶體 vs 場效電晶體
    
    https://www.rohm.com.tw/electronics-basics/transistors/tr_what2

# To pick up later

- [Logic Level Converter]

    https://electrocredible.com/logic-level-converter-circuit-schematic-working/

    -  NPN transistor

- [Interrupt]  IRQ

- [StateMachine]

- pioasm

- 74HC595 / STP16C596 shift register


# interesting modules

- PICO UPS
    https://www.meiyagroup.com.tw/product/%E6%A8%B9%E8%8E%93%E6%B4%BE%E5%BE%AE%E6%8E%A7%E5%88%B6%E5%99%A8pico-ups-%E6%A8%A1%E7%B5%84/