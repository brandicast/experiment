from lib.mylib import WiFiClient, Tools
import lib.env as env
from machine import Pin
import time

from umqtt.simple import MQTTClient

EXIT = False
is_MQTT_CONNECTED = False

test_pin = Pin(0, Pin.OUT, value=1)

led = led = Pin("LED", Pin.OUT, value=1)

switch_pin = Pin (14, Pin.IN, Pin.PULL_UP)
gate_pin = Pin (16, Pin.OUT)



def on_mqtt_msg(topic, msg):
    cmd = msg.decode("utf-8")
    print ("Receiving message : " + cmd + " from : " + topic.decode("utf-8"))

    if cmd == "OPEN":
        gate_pin.value(1)
        time.sleep(0.5)
        gate_pin.value(0)

wifi = WiFiClient(env.SSID, env.PASSWORD, 10)
wifi.activate_wifi_module()

mqtt_server="192.168.68.57"
client_id = "pico_gate_keeper"
topic = "brandon/iot/pico/gate"
client = MQTTClient(client_id, mqtt_server, 1883)
client.set_callback(on_mqtt_msg)

while not EXIT:

    if not wifi.isConnected():
        wifi.connect()
    
    if wifi.isConnected() and not is_MQTT_CONNECTED:
        try:
            print('Connecting to MQTT Broker "%s"' % (mqtt_server))
            client.connect()
            print('Connected to MQTT Broker "%s"' % (mqtt_server))
            is_MQTT_CONNECTED = True
            client.subscribe(topic)
        except OSError as e:
            is_MQTT_CONNECTED = False
            print ("MQTT connection error : " + str(e))

    # below are GPIO
    sw = switch_pin.value()
    if sw == 0:
        gate_pin.value(1) 
    else:
        gate_pin.value(0) 

    if wifi.isConnected() and is_MQTT_CONNECTED:
        try:            
            client.check_msg()  # this is mqtt client
            time.sleep (0.1)           
            if (led.value() != 1):
                led.value(1)
        except OSError as e:
            is_MQTT_CONNECTED = False
            print (e)
    else:
        led.toggle()
        time.sleep(0.5)
        
