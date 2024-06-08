from lib.mylib import WiFiClient, Tools
import lib.env as env
from machine import Pin
import time


'''
wifi = WiFiClient(env.SSID, env.PASSWORD)
tools = Tools()

while not wifi.isConnected:
    wifi.connect()
    if not wifi.isConnected:
        if not tools.IS_BLINKING:
            tools.blink()
    else:
        tools.blink_stop()


'''

test_pin = Pin(0, Pin.OUT, value=1)

relay_vcc_pin = Pin(19, Pin.OUT)

switch_pin = Pin (14, Pin.IN, Pin.PULL_UP)

gate_pin = Pin (16, Pin.OUT)



while True:
    try:
        
        sw = switch_pin.value()
        #print (sw)
        if sw == 0:
            relay_vcc_pin.value(1)
            time.sleep (3) 
            gate_pin.value(1) 
        else:
            gate_pin.value(0) 
            relay_vcc_pin.value(0)
        time.sleep (0.1)           
    except OSError as e:
        print (e)
        break 
