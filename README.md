# EE250-Final
# Richard Huang and Leo Zhuang
Demo Link:

# How to execute code:
On the laptop, run the baby_hub.py file to start the server connection.
On rpi, run baby_mon_pubsub.py file: python3 baby_mon_pubsub.py [file name]
You can toggle between different mp3 files: baby1.mps, baby2.mp3, city_ambiance.mp3, babble.mp3
Open the localhost: 127.0.0.1:5000
When you click “Turn on,” the sound sensor should start taking values. The webpage will change to the alarm status page. Break the sound threshold (400), and the code should then analyze an mp3 file (in place of an actual baby). Assuming it is a baby, the status on the webpage will change.
You can continue running it by resetting the alarm, or you can turn off the system completely.
# Libraries used: 
MQTT, Flask, Grovepi, numpy 

