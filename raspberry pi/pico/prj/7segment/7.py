from machine import Pin
import time, _thread


leds = [
    Pin( 0, Pin.OUT, value=0),
    Pin( 1, Pin.OUT, value=0),
    Pin( 2, Pin.OUT, value=0),
    Pin( 3, Pin.OUT, value=0),
    Pin( 4, Pin.OUT, value=0),
    Pin( 5, Pin.OUT, value=0),
    Pin( 6, Pin.OUT, value=0),
    Pin( 7, Pin.OUT, value=0)]

commons = [
    Pin (10, Pin.OUT, value=1),
    Pin (11, Pin.OUT, value=1),
    Pin (12, Pin.OUT, value=1),
    Pin (13, Pin.OUT, value=1)
]



gpios = [
    Pin( 0, Pin.OUT, value=0),
    Pin( 1, Pin.OUT, value=0),
    Pin( 2, Pin.OUT, value=0),
    Pin( 3, Pin.OUT, value=0),
    Pin( 4, Pin.OUT, value=0),
    Pin( 5, Pin.OUT, value=0),
    Pin( 6, Pin.OUT, value=0),
    Pin( 7, Pin.OUT, value=0),  
    Pin (10, Pin.OUT, value=1),  # commons
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
numbers = [ [0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
            [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
            [1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
            [0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]]
    

def display (num):
    global numbers, gpios
    
    
    digit_index = 0
    for n in num:
        digit = int(n)

        
        numbers[digit][digit_index+8] = 0
        i = 0
        for gpio in gpios:
            gpio.value ((numbers[digit][i] ^ 1))

            i = i + 1    
        numbers[digit][digit_index+8] = 0
        
        digit_index = digit_index + 1
        
        time.sleep(0.002)


while True:    
    display ("1234")
       
    
   
    
'''


state = 1
commons[0].value (state)
commons[1].value (state)
commons[2].value (state)
commons[3].value (state)

for led in leds:
    led.value(0)
'''
