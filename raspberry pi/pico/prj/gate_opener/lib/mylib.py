import network, socket
import time
from machine import Pin


class WiFiClient :

    def __init__ (self, ssid, credential):
        self.ssid  = ssid 
        self.credential = credential
        self.isConnected = False
        self.wlan = network.WLAN(network.STA_IF)

    
    def connect(self) :
        try:
            print('Connecting to WiFi Network Name:',self.ssid)
            #wlan = network.WLAN(network.STA_IF)
            self.wlan.active(True) # power up the WiFi chip
            print('Waiting for wifi chip to power up...')
            try:
                time.sleep(3) # wait three seconds for the chip to power up and initialize
            except KeyboardInterrupt as e:
                print (e)

            self.wlan.connect(self.ssid, self.credential)

            max_wait = 30
            while max_wait > 0:
                if self.wlan.status() < 0 or self.wlan.status() >= 3:
                    break
                max_wait -= 1
                print('Waiting for connection...')
                try:
                    time.sleep(1)
                except KeyboardInterrupt as e:
                    print (e)

            if self.wlan.status() != 3:
                raise RuntimeError('Network connection failed : Check SSID or Credential')
            else:
                print('Connected : ' + str(self.wlan.ifconfig()))
                self.isConnected = self.wlan.isconnected()
        except KeyboardInterrupt as e:
            print (e)

    def disconnect (self):
        self.wlan.disconnect()

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
    def blink (self):
        led = led = Pin("LED", Pin.OUT)
        while not self.STOP_BLINK:
            led.toggle()
            self.IS_BLINKING = True
            time.sleep(1)
        self.IS_BLINKING = False

    def blink_stop(self):
        self.STOP_BLINK = True
