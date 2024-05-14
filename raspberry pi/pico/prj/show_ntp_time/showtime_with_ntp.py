from machine import Pin
import time, _thread
from lib.mylib import WiFiClient, Tools
from lib import env 
from my_seven_segment import seven_segment

EXIT = False
reset_pin = Pin(16, Pin.IN, Pin.PULL_UP)


_7seg = seven_segment()
_7seg.start_with_thread(_7seg.display_animate)

wifi = WiFiClient(env.SSID, env.PASSWORD)
wifi.connect()
tools = Tools()
tools.set_local_time()

_7seg.clear()
_7seg.start_with_thread(_7seg.display_number)

while not EXIT:
    try:
        
        now = time.localtime() 
        value = tools.zfil(str(now[3]), 2) + tools.zfil(str(now[4]),2)
        _7seg.set_value(value)
        
        time.sleep (1)
        print (now)

        EXIT = (reset_pin.value() == 0)
        _7seg.stop = EXIT
        
        if EXIT:
            _7seg.clear()
            
    except OSError as e:
        print (e)
        break 
    
