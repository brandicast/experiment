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

now=0
value = "1111"

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
numbers = [ [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
            [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]]
    

def display (num):
    global numbers, gpios
    
    digit_index = 0
    for n in num:
        digit = int(n)

        
        numbers[digit][digit_index+8] = 1
        i = 0
        for gpio in gpios:
            gpio.value ((numbers[digit][i]))
            
            #print (numbers[digit][i] ^ 1, end="")
            #print (" = " + str(digit))
            i = i + 1
        #print ("")
        numbers[digit][digit_index+8] = 0
        
        digit_index = digit_index + 1
        
        time.sleep(0.002)
            
def task ():
    
    while True:
        #print (value)
        display (value)    
        
        
def zfl(s, width):
# Pads the provided string with leading 0's to suit the specified 'chrs' length
# Force # characters, fill with leading 0's
    return '{:0>{w}}'.format(s, w=width)


def getCurrentTime():
    global now
    now = now + 1
    if now == 9999:
        now = 0 
    return zfl(str(now), 4)
        
_thread.start_new_thread(task,() )

while True:
    value = getCurrentTime ()
    time.sleep (1)
        

