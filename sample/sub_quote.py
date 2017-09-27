# -*- coding: utf-8 -*-
# author : ypochien＠gmail.com

import sys
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    print("Subscribe ({})".format(TOPIC))
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

if len(sys.argv) < 2: #len小於2也就是不帶參數啦
    code = '#'
else:
    code = sys.argv[1]

TOPIC = 'L/{}'.format(code)

client.connect("vpn.alvin.tw", 1883, 60)
client.loop_forever()