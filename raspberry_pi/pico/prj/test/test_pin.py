import time
from machine import Pin


EXIT = False
reset_pin = Pin(16, Pin.IN, Pin.PULL_UP)


commons= [
Pin(2, Pin.OUT),
Pin(3, Pin.OUT),
Pin(4, Pin.OUT),
Pin(5, Pin.OUT)
]


gpios = [
    Pin( 6, Pin.OUT, value=0),
    Pin( 7, Pin.OUT, value=0),  
    Pin (8, Pin.OUT, value=1),
    Pin (9, Pin.OUT, value=1),
    Pin (10, Pin.OUT, value=1),
    Pin (11, Pin.OUT, value=1),
    Pin (12, Pin.OUT, value=1),
    Pin (13, Pin.OUT, value=1)
]

'''
zero  = [0, 1, 1, 1, 1, 1, 1, 0, 0]   # [1, 2, 3, 4, 5, 6]
one   = [0, 1, 0, 0, 1, 0, 0, 0, 0]   # [1, 4]
two   = [1, 0, 1, 1, 1, 1, 0, 0, 0]   # [2, 3, 0, 4, 5]
three = [1, 0, 1, 1, 0, 1, 1, 0, 0]   # [2, 3, 0, 5, 6]
four  = [1, 1, 0, 1, 0, 0, 1, 0, 0]   # [1, 0, 3, 6]
five  = [1, 1, 1, 0, 0, 1, 1, 0, 0]   # [2, 1, 0, 6, 5]
six   = [1, 1, 1, 0, 1, 1, 1, 0, 0]   # [2, 1, 0, 4, 5, 6]
seven = [0, 0, 1, 1, 0, 1, 1, 0, 0]   # [2, 3, 6, 5]
eight = [1, 1, 1, 1, 1, 1, 1, 0, 0]   # [1, 2, 3, 4, 5, 6, 0]
nine  = [1, 1, 1, 1, 0, 1, 1, 0, 0]   # [1, 2, 3, 6, 5, 0]
dot   = [0, 0, 0, 0, 0, 0, 0, 0, 1]   # [7]
'''
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

for common in commons:
    common.value (1)

index=0
num=8
for gpio in gpios:
    gpio.value(numbers[num][index]) 
    print(numbers[num][index], end=' ')
    index = index + 1

'''
while not EXIT:
    
    EXIT = (reset_pin.value() == 0)

    print ("on")
    pin2.value(1) 
    pin3.value(1) 
    pin4.value(1) 
    pin5.value(1) 
    time.sleep(10)
    print ("off")
    pin2.value(0) 
    pin3.value(0) 
    pin4.value(0) 
    pin5.value(0)
    time.sleep(10)
    

'''
    