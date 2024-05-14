from machine import Pin
import _thread
import time


gpios = [
    Pin( 0, Pin.OUT, value=1),
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

square_animate = [ [1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0], 
                    [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0], 
                    [1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0], 
                    [1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1], 
                    [1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1], 
                    [1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1], 
                    [1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1], 
                    [1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0], 
                    [1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0], 
                    [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0], 
                    [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0], 
                    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]]

mic_lee_animate = [[0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                   [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0],
                   [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
                   [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
                   [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
                   [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0]]
                   

stop_sign =  [0 ,1, 1, 1, 1, 1, 1 ,1, 1, 1, 1, 1]
clear_sign = [1 ,1, 1, 1, 1, 1, 1 ,1, 0, 0, 0, 0]


class seven_segment:

    def __init__ (self):
        self.value = "0000"
        self.stop = False
        self.seconds_counter = 0 
        self.show_dot = True

    def set_value (self, val):
        self.value = val

    def handle_number (self):
        global numbers, gpios
    
        digit_index = 0    
        for n in self.value:
            digit = int(n)
            
            self.seconds_counter = self.seconds_counter + 1
            
            if self.seconds_counter == 500:
                self.show_dot = not self.show_dot
                self.seconds_counter = 0 
                
            if self.show_dot and digit_index == 3 :
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

    def display_number (self):
        print (self.stop)
        self.stop = False
        print (self.stop)
        while not self.stop:
            try:
               self.handle_number()
            except OSError as e:
                pass

    def start_with_thread (self, obj, paras=()):        
        try:
            _thread.start_new_thread(obj,paras)
        except:
            pass            


    def clear(self):
        global clear_sign
        self.stop = True
        self.display_sign (clear_sign)
        time.sleep(1)

    def display_sign (self, sign):
        i = 0
        for gpio in gpios:
            gpio.value (sign[i])
            i = i + 1

    def display_animate (self, mode=0):
        global square_animate, mic_lee_animate
        self.stop = False

        animate = square_animate
        if mode == 1:
            animate = mic_lee_animate
        
        i = 0 
        while not self.stop:
            try:  
                j = 0
                for gpio in gpios:
                    gpio.value (animate[i][j])
                    j = j + 1
                time.sleep(0.25)
                i = i + 1
                if i == len(animate):
                    i = 0     
            except:
                pass

    def set_dot_status (self, digit, on_off):
        global numbers
        numbers[10][digit+8] =  1
        


if __name__ == '__main__':

    _7seg = seven_segment()
    _7seg.clear()

    _7seg.start_with_thread (_7seg.display_animate)
    time.sleep(3)
    _7seg.clear() 
    _7seg.set_value("1234")
    _7seg.start_with_thread (_7seg.display_number)
    

    reset_pin = Pin(16, Pin.IN, Pin.PULL_UP)
    
    counter = 0
    while not _7seg.stop:
        _7seg.stop = (reset_pin.value() == 0)
        time.sleep (1)
        print (_7seg.stop)
        '''
        counter = counter + 1
        if counter == 10:
            
            time.sleep(5)
        '''

        
        

   