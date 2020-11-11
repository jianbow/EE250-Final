#to be ran on the hub (in our case, the pc)

import paho.mqtt.client as mqtt
import time
from pynput import keyboard

ALARM_ON = false

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    #subscribe to alarm
    client.subscribe('llzhuang/alarm')
    client.message_callback_add("llzhuang/alarm", alarm_callback)

def alarm_callback(client, userdata, message):
	if(str(message.payload, "utf-8") == 'ALARM_ON'):
	    ALARM_ON = true
	else:
	    ALARM_ON = false

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def on_press(key):
    try: 
        k = key.char # single-char keys
    except: 
        k = key.name # other keys
    
    if k == 'n':
        client.publish('llzhuang/nightMode','NM_ON')
        print("NIGHTMODE ON")
    elif k == 'm':
        client.publish('llzhuang/nightMode','NM_OFF')
        print("NIGHTMODE OFF")
    elif k == 'a':
        client.publish('llzhuang/acknowledge','YES')
        ALARM_ON = false

if __name__ == '__main__':
    #setup the keyboard event listener
    lis = keyboard.Listener(on_press=on_press)
    lis.start() # start to listen on a separate thread

    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    print("INPUTS: \n N = NIGHTMODE ON \n M = NIGHTMODE OFF \n A = ACKNOWLEDGE ALARM")
    while True:
    	if(ALARM_ON):
    		print("YOUR BABY IS FREAKING OUT")
        time.sleep(1)
            

