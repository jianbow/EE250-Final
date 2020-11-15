#to be run on the rpi/baby monitor

import paho.mqtt.client as mqtt
import time
from grovepi import *
import baby_freq as baby

#time inbetween reads
SLEEP_TIME = 30

VOL_CHECK_TIME = 5
SAMPLE_TIME = 5
#preset. allows user to change depending on conditions
VOL_THRESHOLD = 400
#connect sound sensor to A0
sound_sensor = 0
#holds bool for nightmode. Night mode constantly monitors the baby, whereas non night mode just turns the device off???
nightMode = False;
#holds name for sound file
sound_file = "baby.mp3"


pinMode(sound_sensor,"INPUT")

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def nightMode_callback(client, userdata, message):
    global nightMode
    if(str(message.payload, "utf-8") == 'NM_ON'):
        nightMode = True
    else:
        nightMode = False
def sound_callback(client, userdata, message):
    global sound_file
    sound_file = str(message.payload, "utf-8")

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to nightMode, listens to whether to turn on or off
    client.subscribe('llzhuang/nightMode')
    client.message_callback_add("llzhuang/nightMode", nightMode_callback)
    client.subscribe('llzhuang/sound')
    client.message_callback_add("llzhuang/sound", sound_callback)

if __name__ == '__main__':
    global sound_file
    if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]):
        print("Usage: baby_mon_pubsub.py [file]")
        exit(1)
    sound_file = sys.argv[1]

    #connect to broker
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        #we check for sound every 30s, if there is, we check if it is baby
        if(nightMode):
            #check for curr volume for 5s
            max_val = 0;
            count = 0;
            #for 5 sec, let's get the max volume
            #we could adjust the resolution of this, but we're dealing with volume so this is fine
            while count < 10:
                sensor_value = analogRead(sound_sensor)
                print(sensor_value)
                if(sensor_value > max_val):
                    max_val = sensor_value
                count+=1
                time.sleep(.5);
            if(max_val >= VOL_THRESHOLD):
                print("HEARD SOUND")
                #TODO: CALL FFT TO SEE IF IN BABY RANGE
                #since we don't have a microphone for the rpi, we will use a premade mp3 file. In theory, this would come from a recording.
                if(baby.main(sound_file)):
                    print("publishing to alarm...")
                    client.publish('llzhuang/alarm','ALARM_ON')
                #simulate recording time
                time.sleep(10)