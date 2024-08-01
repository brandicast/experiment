
from machine import Pin, Timer
import time
import machine


# GPIO Definition
ds = Pin(13, Pin.OUT)
stcp = Pin(14, Pin.OUT)  # latch
shcp = Pin(15, Pin.OUT)  # clock

common1 = Pin(2, Pin.OUT, value=0)
common2 = Pin(3, Pin.OUT, value=0)
common3 = Pin(4, Pin.OUT, value=0)
common4 = Pin(5, Pin.OUT, value=0)



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
            [1, 1, 1, 1, 1, 1, 1, 0]]

numbers_2 = [ [0, 1, 1, 1, 1, 1, 1, 1],
              [1, 0, 1, 1, 1, 1, 1, 1],
              [1, 1, 0, 1, 1, 1, 1, 1],
              [1, 1, 1, 0, 1, 1, 1, 1],
              [1, 1, 1, 1, 0, 1, 1, 1],
              [1, 1, 1, 1, 1, 0, 1, 1],
              [1, 1, 1, 1, 1, 1, 0, 1],
              [1, 1, 1, 1, 1, 1, 1, 0]]
            

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



numbers = numbers_2
x = 0

while not EXIT:
    try:
        for n in range(len(numbers)):
            print ("show number" + str(n))
            x = x ^ 1
            print ("")
            print ("x = " + str(x))
            common1.value (x)
            common2.value (x)
            common3.value (x)
            common4.value (x)
            output_data(n)
            time.sleep(3)
    except OSError as e:
            print (e)
            break 




