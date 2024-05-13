from machine import Pin
import time, _thread
import mylib



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

reset_pin = Pin(16, Pin.IN, Pin.PULL_UP)


numbers = [ [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  # 0
            [1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0],  # 1
            [0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],  # 2
            [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],  # 3
            [0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0],  # 4
            [0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0],  # 5
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],  # 6
            [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0],  # 7
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  # 8
            [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],  # 9
            [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]]  # .

value = "0000"
seconds_counter = 0
show_dot = True

def display (num):
    global numbers, gpios, seconds_counter, show_dot
    
    digit_index = 0
    
        
    for n in num:
        digit = int(n)
        
        seconds_counter = seconds_counter + 1
        
        if seconds_counter == 500:
            show_dot = not show_dot
            seconds_counter = 0 
            
        if show_dot and digit_index == 3 :
            numbers[digit][7] = 0
        else:
            numbers[digit][7] = 1

        
        numbers[digit][digit_index+8] = 1
        i = 0
        for gpio in gpios:
            gpio.value ((numbers[digit][i]))
            i = i + 1

        numbers[digit][digit_index+8] = 0
        
        digit_index = digit_index + 1
        
        time.sleep(0.002)

def task ():
    global value
    
    while not mylib.EXIT:
        display (value)


_thread.start_new_thread(task,() )

while not mylib.EXIT:
    try:
        now = time.localtime() ;
        value = mylib.zfil(str(now[3]), 2) + mylib.zfil(str(now[4]),2)
        time.sleep (1)
        print (now)

        mylib.EXIT = (reset_pin.value() == 0)
            
    except OSError as e:
        print (e)
        break 
    


        


