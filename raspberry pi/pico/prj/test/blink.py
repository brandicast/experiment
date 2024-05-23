from machine import Pin, Timer
import time


led = led = Pin("LED", Pin.OUT)




tim = Timer()
def tick(timer):
  global led
  led.toggle()

tim.init(freq=1, mode=Timer.PERIODIC, callback=tick)


