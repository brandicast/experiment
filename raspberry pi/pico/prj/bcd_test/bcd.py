from machine import Pin, Timer
import time
import machine


EXIT = False
reset_pin = Pin(17, Pin.IN, Pin.PULL_UP)

B = Pin(13, Pin.OUT, Pin.PULL_DOWN )
C = Pin(12, Pin.OUT, Pin.PULL_DOWN )
D = Pin(11, Pin.OUT, Pin.PULL_DOWN )
A = Pin(10, Pin.OUT, Pin.PULL_DOWN )

LT = Pin(20, Pin.OUT, Pin.PULL_DOWN )

A.value(0)
B.value(0)
C.value(0)
D.value(0)

LT.value(1)


while not EXIT:
    try:
        

        EXIT = (reset_pin.value() == 0)
        time.sleep (1)
        if EXIT:
            machine.reset()
        
        
            
    except OSError as e:
        print (e)
        break 
    









