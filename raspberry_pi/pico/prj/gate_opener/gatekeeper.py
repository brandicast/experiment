from lib.mylib import WiFiClient, Tools
import lib.env as env
from machine import Pin
import time

from umqtt.simple import MQTTClient

EXIT = False

is_MQTT_CONNECTED = False
MQTT_PING_COUNTER = 600

led = led = Pin("LED", Pin.OUT, value=1)
gate_pin = Pin (15, Pin.OUT)

button_pin = Pin (2, Pin.IN, Pin.PULL_UP)


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
client = MQTTClient(client_id, mqtt_server, 1883, keepalive=65)
client.set_callback(on_mqtt_msg)


while not EXIT:

    if not wifi.isConnected():
        wifi.connect()
    
    if wifi.isConnected() and not is_MQTT_CONNECTED:
        try:
            print('Connecting to MQTT Broker "%s"' % (mqtt_server))
            client.connect(False)
            print('Connected to MQTT Broker "%s"' % (mqtt_server))
            is_MQTT_CONNECTED = True
            client.subscribe(topic)
        except OSError as e:
            is_MQTT_CONNECTED = False
            print ("MQTT connection error : " + str(e))

    # below are GPIO
    sw = button_pin.value()
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
            if MQTT_PING_COUNTER == 0:
                MQTT_PING_COUNTER = 600
                client.ping()
            MQTT_PING_COUNTER = MQTT_PING_COUNTER - 1 
        except OSError as e:
            is_MQTT_CONNECTED = False
            print (e)
    else:
        led.toggle()
        time.sleep(0.5)
        
