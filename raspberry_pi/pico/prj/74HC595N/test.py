
from machine import Pin, Timer
import time
import machine


# GPIO Definition
ds = Pin(13, Pin.OUT)
stcp = Pin(14, Pin.OUT)  # latch
shcp = Pin(15, Pin.OUT)  # clock

common = Pin(16, Pin.OUT, value=1)


EXIT = False
reset_pin = Pin(21, Pin.IN, Pin.PULL_UP)

# data for 7 segment
numbers = [ [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 0, 1],
            [0, 1, 0, 0, 0, 0, 1, 1],
            [0, 1, 0, 0, 1, 0, 0, 1],
            [0, 0, 1, 0, 1, 1, 0, 1],
            [0, 0, 0, 1, 1, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 0, 1],
            [1, 1, 0, 0, 1, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1]]


# function to display
def output_data(num):
  global numbers

  #put latch down to start data sending
  shcp.value(0)
  stcp.value(0)
  shcp.value(1)
  
  data = numbers[num]
  #load data in reverse order
  for i in range(len(data)-1, -1, -1):
    shcp.value(0)
    ds.value(data[i])
    print (data[i], end=" ")
    shcp.value(1)

  #put latch up to store data on register
  shcp.value(0)
  stcp.value(1)
  shcp.value(1)


for n in range(len(numbers)):
    output_data(n)
    print ("")
    time.sleep(3)

'''
while not EXIT:
    try:
        

        EXIT = (reset_pin.value() == 0)
        time.sleep (1)
        if EXIT:
            print ("EXIT !")
            machine.reset()            
    except OSError as e:
        print (e)
        break 
'''    



