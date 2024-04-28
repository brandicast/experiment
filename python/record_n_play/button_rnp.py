from recorder import Recorder
from alsa_err_handling import *
import time

import RPi.GPIO as GPIO


pin_button = 36
pin_switch = 32
pin_led = 10
GPIO.setmode (GPIO.BOARD)
GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # pull_up_down=GPIO.PUD_UP
GPIO.setup(pin_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # pull_up_down=GPIO.PUD_UP
GPIO.setup(pin_led,GPIO.OUT)

rec = Recorder()

isRecording = False
buttonMode = GPIO.input(pin_switch) #  0: Record ; 1: Play

def onButtonHit (self):
    global isRecording, buttonMode

    print ("Button Hit with mode : " + str (buttonMode))

    if buttonMode == 0:

        if not isRecording:
            try:
                isRecording = True
                print ("Start Recording")
                rec.start()
            except:
                pass
        else:
            try:
                isRecording = False
                print ("Stop Recording")
                rec.stop() 
            except:
                pass

        GPIO.output(pin_led, isRecording)

    elif buttonMode == 1 :
        isRecording = False 
        print ("Start Playing")
        rec.stop()
        rec.play()
    else:
        print (buttonMode)

def onSwitchOnOff (self):
    global buttonMode

    print ("Swtich On/Off Trigger") 
    #print (GPIO.input(pin_switch))
    time.sleep(0.05)
    buttonMode = GPIO.input(pin_switch)
    
    print ("is now Record Mode..." if buttonMode == 0 else "is Play mode")



    
GPIO.add_event_detect(pin_button, GPIO.RISING, callback=onButtonHit, bouncetime=300)

GPIO.add_event_detect(pin_switch, GPIO.BOTH, callback=onSwitchOnOff, bouncetime=300)

while True:
    cmd = input('Command :')
    if cmd == 'start':
        rec.start()
    elif cmd == 'stop':
        rec.stop()
    elif cmd == 'quit':
        GPIO.cleanup()
        exit()
    elif cmd == 'status':
        print("Recording status : " +
              ("is recording" if rec.isRecording else " is stopped"))
        
        print ("Pin 10 :  " + str(GPIO.input(pin_led)))
        print ("Pin 32 :  " + str(GPIO.input(pin_button)))
        print ("Pin 36 :  " + str(GPIO.input(pin_switch)))
    else:
        print("No [" + cmd + "] command, please try again")