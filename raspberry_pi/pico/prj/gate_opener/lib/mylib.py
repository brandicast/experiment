import network, socket
import time, _thread
from machine import Pin


class WiFiClient :

    def __init__ (self, ssid, credential, max_wait=15, retry=30):
        self.ssid  = ssid 
        self.credential = credential
        self.wlan = network.WLAN(network.STA_IF)
        self.max_wait = max_wait
        self.retry = retry

    def activate_wifi_module (self):
            print('Connecting to WiFi Network Name:',self.ssid)
            #wlan = network.WLAN(network.STA_IF)
            self.wlan.active(True) # power up the WiFi chip
            print('Waiting for wifi chip to power up...')
            try:
                time.sleep(3) # wait three seconds for the chip to power up and initialize
            except KeyboardInterrupt as e:
                print (e)
    
    def connect(self) :
            self.wlan.connect(self.ssid, self.credential)
            retry = self.retry
            
            while retry > 0:
                try:
                    time.sleep(self.max_wait)
                except KeyboardInterrupt as e:
                    print ("Waiting for wifi connection is being interruptted : " + str(e))

                retry = retry - 1
                print('Waiting for connection... ' + str(self.retry - retry) + "/" + str(self.retry))                    

                wifi_status = self.wlan.status()
                print ("Wireless lan status : " + str(wifi_status))

                msg = "Network connection failed with error code : " + str(wifi_status) 
                if wifi_status == 0:
                    msg = msg + " (STAT_IDLE) no connection and no activity"
                elif wifi_status == -1: 
                    msg = msg + " (STAT_CONNECT_FAIL) failed due to other problems"
                elif wifi_status == -2: 
                    msg = msg + " (STAT_NO_AP_FOUND) failed because no access point replied"
                elif wifi_status == -3: 
                    msg = msg + " (STAT_WRONG_PASSWORD) failed due to incorrect password"
                elif wifi_status == 1:
                    msg = " (STAT_CONNECTING) connecting in progress"
                elif wifi_status == 3:
                    msg = " (STAT_GOT_IP) connection successful : "+ str(self.wlan.ifconfig())
                elif wifi_status == 2:
                    msg = " (STAT_NOIP) connected but no IP"
                else:
                    msg = " Unknown "
                
                print (msg)
                if wifi_status == 1 or wifi_status == 2:
                    pass
                else:
                    break                

    def disconnect (self):
        self.wlan.disconnect()
    
    def isConnected (self):
        return self.wlan.isconnected()

    def start_testing_http_server(self, port):

        addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]
        s = socket.socket()
        s.bind(addr)
        s.listen(1)
        print('listening on', addr)

        while True:
            try:
                cl, addr = s.accept() 
                print ('client connected from ', addr)
                request = cl.recv (1024)
                print (request)

                cl.send ('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                cl.send ("Hi " + str(addr) )
                cl.close()

            except OSError as e:
                cl.close()
                print('connection closed')


class Tools:
    
    def set_local_time(self):
        import ntptime,machine, utime

        success = False
        max_try = 20

        while not success : 
            try:
                t = ntptime.time() + 28800  # UTC + 8 
                tm = utime.gmtime(t)
                machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
                sucess = True
            except OSError as e1 :
                print (e1)
                max_try = max_try - 1 
                if max_try == 0:
                    break
                try:
                    time.sleep(3)
                except KeyboardInterrupt as e2:
                    print (e2)


    def zfil(self, s, width):
    # Pads the provided string with leading 0's to suit the specified 'chrs' length
    # Force # characters, fill with leading 0's
        return '{:0>{w}}'.format(s, w=width)
    

    STOP_BLINK = False
    IS_BLINKING = False
    BLINKING_MODE = 1 #  1 : 1 second, 2 : 0.5 second, 3 : 0.25 second
    def blink (self):
        led = led = Pin("LED", Pin.OUT)
        while not self.STOP_BLINK:
            self.IS_BLINKING = True
            if self.BLINKING_MODE == 0:
                self.STOP_BLINK = True
            else :
                led.toggle()
                time.sleep(1/self.BLINKING_MODE)
        self.IS_BLINKING = False

    def blink_start(self):
        _thread.start_new_thread(self.blink,() )

    def blink_stop(self):
        self.STOP_BLINK = True
