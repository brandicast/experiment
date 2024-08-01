import network, socket
import env 
import time


def connect_wifi ():
    print('Connecting to WiFi Network Name:',env.SSID)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True) # power up the WiFi chip
    print('Waiting for wifi chip to power up...')
    time.sleep(3) # wait three seconds for the chip to power up and initialize
    wlan.connect(env.SSID, env.PASSWORD)

    max_wait = 30
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
    #    print( 'ip = ' + status[0] )
        print (status)

def test_server(port):

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

