
from lib.mylib import WiFiClient, Tools
from lib import env
import time
from machine import Pin

import network

#wifi = WiFiClient(env.SSID, env.PASSWORD)
wifi = WiFiClient('raspberry', '3.1415926')
wifi.connect()

tools = Tools()
tools.set_local_time()


EXIT = False
reset_pin = Pin(16, Pin.IN, Pin.PULL_UP)


while not EXIT:
    print (time.localtime())
    time.sleep(1)
    EXIT = (reset_pin.value() == 0)
    print (wifi.isConnected, end=" ")

    wlan = network.WLAN(network.STA_IF)
    print (wlan.status())









