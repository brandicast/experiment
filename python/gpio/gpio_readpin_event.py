import RPi.GPIO as GPIO
import time

pin_do = 36
pin_ao = 32

GPIO.setmode (GPIO.BOARD)
GPIO.setup(pin_do, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # pull_up_down=GPIO.PUD_UP
GPIO.setup(pin_ao, GPIO.IN, pull_up_down=GPIO.PUD_UP) 


def my_callback(channel):

    print ("Button Hit !")

    '''
    if var == 1:
        sleep(1.5)  # confirm the movement by waiting 1.5 sec 
        if GPIO.input(7): # and check again the input
            print("Movement!")
            captureImage()

            # stop detection for 20 sec
            GPIO.remove_event_detect(7)
            sleep(20)
            GPIO.add_event_detect(7, GPIO.RISING, callback=my_callback, bouncetime=300)
    '''

GPIO.add_event_detect(pin_do, GPIO.RISING, callback=my_callback, bouncetime=300)


# To keep app not exit
while True:
    pass