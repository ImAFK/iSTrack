#!/usr/bin/env python3.7

# import necessarry libraries
import sys
from datetime import datetime
from pymongo import MongoClient
import paho.mqtt.client as mqtt
import time
import configparser
import os
import json


# Set variables for broker and topics (optionaly load from config)
# set topics: (topic, QoS)
mqtt_topic = [('NTUST/gateA',0),('NTUST/gateB',0),('NTUST/gateC',0)]
# mqtt_broker_ip = "192.168.50.21"
mqtt_broker_ip = 'test.mosquitto.org'
mqtt_port = 1883

# Load credentials from config file
# improvement: pass configs as parameters
# Check if config exists
mqtt_username = ''
mqtt_password = ''
if not os.path.exists('/usr/src/app/src/credentials.conf'):
    print('Config not found')
else:
	# load usr & pwd
	creds_config = configparser.ConfigParser()
	creds_config.read('/usr/src/app/src/credentials.conf')
	mqtt_username = creds_config['DEFAULT']['mqtt_username']
	mqtt_password = creds_config['DEFAULT']['mqtt_password']


client = MongoClient('mongo', 27017)

# These functions handle what happens when the MQTT client connects
# to the broker, and what happens then the topic receives a message
def on_connect(mqtt_client, userdata, flags, rc):
    Connected = False
    # rc is the error code returned when connecting to the broker
    if rc == 0:
        print('Connected to broker')
        Connected = True                #Signal connection
    else:
        print('Connection failed, ' + str(rc))

    while Connected != True:    # Wait for connection
        time.sleep(0.1)
    # Once the client has connected to the broker, subscribe to the topic
    mqtt_client.subscribe(mqtt_topic)


def on_message(mqtt_client, userdata, message):
    # This function is called every time the topic is published to.
    # If you want to check each message, and do something depending on
    # the content, the code to do this should be run in this function
    m_decode = str(message.payload.decode('utf-8', 'ignore'))
    m_in = json.loads(m_decode)

    # JSON Example
    # {"id":"dkjfk4k23jk","temperature":"36.9"}

    print(str(message.topic))
    print('Id:' + m_in['id'])
    print('Temperature:' + m_in['temperature'])
    with open('./temperature.txt', 'a') as temp_out:
        temp_out.write(str(message.topic) + '\n')
        temp_out.write('Id:' + m_in['id'] + '\n')
        temp_out.write('Temperature:' + m_in['temperature'] + '\n')
    # The message itself is stored in the msg variable
    # and details about who sent it are stored in userdata

    # TODO put records into DB in appropriate format
    with client:
        db = client.recordsData
        col = db.data
	    # Read data and save to database
        current_time = datetime.now()
        read = { 'time': current_time, 'id': m_in['id'], 'temperature': m_in['temperature'] }
        x = col.insert_one(read)
        print('Data inserted...')

        # Testing purpose
        myquery = {'id': '32681ddkk'}
        mydoc = col.find(myquery)
        for i in mydoc:
            print(i)

        # TODO check id, publish message to the edge
        # basically check wheter id exists or not
        # if not, publish mqtt msg to the edge device

# Create MQTT client
mqtt_client = mqtt.Client('NTUST')
# Set the username and password for the MQTT client
# client.username_pw_set(mqtt_username, mqtt_password)


# Here, we are telling the client which functions are to be run
# on connecting, and on receiving a message
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Once everything has been set up, we can (finally) connect to the broker
# mqtt_port is the listener port that the MQTT broker is using
mqtt_client.connect(mqtt_broker_ip, mqtt_port)

#start the loop
# client.loop_start()
mqtt_client.loop_forever()


# Once we have told the client to connect, let the client object run itself
# Disconnect client
mqtt_client.disconnect()


