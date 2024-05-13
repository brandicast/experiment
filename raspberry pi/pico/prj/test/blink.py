from machine import Pin, Timer
import time

led = Pin("LED", Pin.OUT)
tim = Timer()
def tick(timer):
  global led
  led.toggle()

tim.init(freq=1, mode=Timer.PERIODIC, callback=tick)

print (time.localtime())