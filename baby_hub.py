#to be ran on the hub (in our case, the pc)

from flask import Flask, render_template, redirect, request
app = Flask(__name__)



import paho.mqtt.client as mqtt
import time
from pynput import keyboard

ALARM_ON = True
IS_ON = False

@app.route("/")
def start():
    client.publish('llzhuang/nightMode',"NM_OFF")
    return render_template('start.html')

@app.route("/alarm", methods = ["GET",'POST'])
def alarm():
    client.publish('llzhuang/nightMode',"NM_ON")
    onOff = request.args.get('onOff')
    global ALARM_ON
    status = 'Ok'
    if request.method == 'POST':
        ALARM_ON = False
    if(ALARM_ON):
        status = 'CRYING'
    else:
        status = 'Ok'
    return render_template('base.html', **locals())


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    #subscribe to alarm
    client.subscribe('llzhuang/alarm')
    client.message_callback_add("llzhuang/alarm", alarm_callback)

def alarm_callback(client, userdata, message):
    global ALARM_ON
    if(str(message.payload, "utf-8") == 'ALARM_ON'):
        ALARM_ON = True
    else:
        ALARM_ON = False
    alarm()

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))
"""
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
"""
if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    app.run()

