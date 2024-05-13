import network, socket
import env 
import time


class WiFiClient :

    def __init__ (self, ssid, credential):
        self.ssid  = ssid 
        self.credential = credential
        self.isConnected = False
        self.wlan = network.WLAN(network.STA_IF)

    
    def connect(self) :
        print('Connecting to WiFi Network Name:',self.ssid)
        #wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True) # power up the WiFi chip
        print('Waiting for wifi chip to power up...')
        time.sleep(3) # wait three seconds for the chip to power up and initialize
        self.wlan.connect(self.ssid, self.credential)

        max_wait = 30
        while max_wait > 0:
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break
            max_wait -= 1
            print('Waiting for connection...')
            time.sleep(1)

        if self.wlan.status() != 3:
            raise RuntimeError('Network connection failed : Check SSID or Credential')
        else:
            print('Connected : ' + str(self.wlan.ifconfig()))
            self.isConnected = self.wlan.isconnected()

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

        t = ntptime.time() + 28800  # UTC + 8 

        tm = utime.gmtime(t)
        machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
