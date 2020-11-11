#to be run on the rpi/baby monitor

import paho.mqtt.client as mqtt
import time
from grovepi import *

#time inbetween reads
SLEEP_TIME = 30;
#
VOL_CHECK_TIME = 5;
SAMPLE_TIME = 5;
#preset. allows user to change depending on conditions
VOL_THRESHOLD = 400

#connect sound sensor to A0
sound_sensor = 0;

pinMode(sound_sensor,"INPUT")



def lcd_callback(client, userdata, message):
    #print("on_message: " + message.topic + " " + str(message.payload, "utf-8"))
    letter = str(message.payload, "utf-8")
    setText_norefresh(letter)

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe('llzhuang/led')
    client.message_callback_add("llzhuang/led", LED_callback)

    client.subscribe('llzhuang/lcd')
    client.message_callback_add("llzhuang/lcd", lcd_callback)

    #client.subscribe('llzhuang/ultrasonicRanger')

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        #we check for sound every 30s, if there is, we check if it is baby
        if(nightMode):
            #check for curr volume for 5s
            max_vol = 0;



        #otherwise, we don't have to check on the baby
        time.sleep


        ultVal = ultrasonicRead(ultra)
        client.publish('llzhuang/ultrasonicRanger',ultVal)
        if digitalRead(button) == 1:
            client.publish('llzhuang/button', 'Button pressed')
        time.sleep(1)
            

