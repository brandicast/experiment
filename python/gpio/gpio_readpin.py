import RPi.GPIO as GPIO
import time

pin_do = 36
pin_ao = 32

GPIO.setmode (GPIO.BOARD)
GPIO.setup(pin_do, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # pull_up_down=GPIO.PUD_UP
GPIO.setup(pin_ao, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

while True:

    try:
        do_value = GPIO.input(pin_do)
        ao_value = GPIO.input(pin_ao)
        print ("DO value =" + str(do_value) + ", AO value =" + str(ao_value))
    except KeyboardInterrupt as e:
        print ("Key Interrupted !")
        GPIO.cleanup()
        print (e)
        break
 


