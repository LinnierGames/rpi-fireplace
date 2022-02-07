import paho.mqtt.client as mqtt

import RPi.GPIO as GPIO, time
from gpiozero import DigitalOutputDevice

fp_toggle_power_pin = DigitalOutputDevice(26)
base2 = DigitalOutputDevice(6)
base3 = DigitalOutputDevice(13)
base4 = DigitalOutputDevice(5)

MQTT_SERVER = "localhost"
MQTT_PATH = "fireplace/#"

def fireplace_toggle_power():
    fp_toggle_power_pin.on()
    time.sleep(0.5)
    fp_toggle_power_pin.off()
    time.sleep(0.5)
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic  )
    print(msg.payload)
    
    if msg.topic == "fireplace/remote":
        print("Got message for fireplace/remote")
        
        payload_str = str(msg.payload.decode("utf-8"))
        
        if payload_str == "toggle-power":
            print("Toggle Power")
            fireplace_toggle_power()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)
 
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

