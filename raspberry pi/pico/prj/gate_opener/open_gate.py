from lib.mylib import WiFiClient, Tools
import lib.env as env
from machine import Pin
import time

from umqtt.simple import MQTTClient



test_pin = Pin(0, Pin.OUT, value=1)

#relay_vcc_pin = Pin(19, Pin.OUT)
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
tools = Tools()

while not wifi.isConnected:
    try:
        wifi.connect()
    except RuntimeError as rerr :
        print (rerr)
        print ("Now, try to reconnect")
'''
    if  wifi.isConnected:
        tools.blink_stop()
    else:
        tools.blink_start()
'''            

mqtt_server="192.168.68.57"
client_id = "pico_gate_keeper"
topic = "brandon/iot/pico/gate"

client = MQTTClient(client_id, mqtt_server, 1883)

client.set_callback(on_mqtt_msg)
client.connect()
print('Connected to MQTT Broker "%s"' % (mqtt_server))
client.subscribe(topic)







while True:
    try:
        client.wait_msg()  # this is mqtt client

        # below are GPIO
        sw = switch_pin.value()
        if sw == 0:
            gate_pin.value(1) 
        else:
            gate_pin.value(0) 
        time.sleep (0.1)           
    except OSError as e:
        print (e)
        break 
