#!/usr/bin/env python3.7

# import necessarry libraries
from datetime import datetime
from pymongo import MongoClient
import paho.mqtt.client as mqtt
import os
import json
from dotenv import load_dotenv
from models.record import Record
from models.RecordManager import RecordManager

# Get the path to the directory this file is in
BASEDIR = os.path.abspath(os.path.dirname(__file__),)
PATH = os.path.join(BASEDIR,'.env')
# Connect the path with your '.env' file name
load_dotenv(PATH)


# Set variables for broker and topics (optionaly load from config)
# set topics: (topic, QoS)
mqtt_topic = [('NTUST/gateA',0),('NTUST/gateB',0),('NTUST/gateC',0)]
mqtt_broker_ip = 'mqtt'
# mqtt_broker_ip = 'test.mosquitto.org'
mqtt_port = 1883

# Load credentials from config file
# improvement: pass configs as parameters
# Check if config exists
mqtt_username = os.getenv('mqtt_username')
mqtt_password = os.getenv('mqtt_password')

# Connect to the local MongoDB
mongoClient = MongoClient('mongo', 27017)

# options: OK, NOT OK, WRONG, False
receivedMsg = 'False'
topic = ''

# Check wheter received message is okay (user id, temperature etc.)
def check_msg():
    pass

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
    # Once the client has connected to the broker, subscribe to the topic
    mqtt_client.subscribe(mqtt_topic)

def on_publish(mqtt_client, userdata, result):
    print('Data published')
    pass


def on_message(mqtt_client, userdata, message):
    # This function is called every time the topic is published to.
    # If you want to check each message, and do something depending on
    # the content, the code to do this should be run in this function
    m_decode = str(message.payload.decode('utf-8', 'ignore'))
    m_in = json.loads(m_decode)

    temperature = m_in['temperature']
    temperature = float(temperature)
    user_id = m_in['id']
    topic = message.topic

    # JSON Example
    # {"id":"f6e314a3","temperature":"36.9"}

    # service prints
    print(str(message.topic))
    print('Id:' + user_id)
    print('Temperature:' + temperature)
    # The message itself is stored in the msg variable
    # and details about who sent it are stored in userdata

    ## SAVING DATA TO CLOUD DB

    #Create new object with all informations
    record = Record(id_number=user_id, location='NTUST', body_temperature=temperature, date=datetime.now())
    # record = Record(user_id, "NTUST" , temperature, datetime.date.now())
    #Save to Database
    recordManagerAdvantech = RecordManager('advantech')
    recordManagerAdvantech.save(record)

    recordManagerRpi = RecordManager('rpi')

    # TODO put records into DB in appropriate format
    # Write received data into DB
    with mongoClient:
        db = mongoClient.recordsData
        col = db.data

        # check id, publish message to the edge
        check_id = {'id': user_id}
        checked = None
        checked = col.find(check_id)
        # for i in checked:
        #     print(i)
        if checked is not None:
            print('Msg checked, id exists')
            if temperature < 37.5:
                receivedMsg = 'OK'
            else:
                receivedMsg = 'NOT OK'
        else:
            print('Msg checked, error')
            receivedMsg = 'WRONG'
            return
        # basically check wheter id exists or not
        # if not, publish mqtt msg to the edge device

        # If id exists
	    # Read data and save to database
        current_time = datetime.now()

        read = { 'time': current_time, 'id': user_id, 'temperature': temperature}
        x = col.insert_one(read)
        print('Data inserted...')

        # Testing purpose for printing some stuff from DB
        # myquery = {'id': 'f6e314a3'}
        # mydoc = col.find(myquery)
        # for i in mydoc:
        #     print(i)



# Create MQTT client
mqtt_client = mqtt.Client('NTUST')
# Set the username and password for the MQTT client

# client.username_pw_set(mqtt_username, mqtt_password)


# Here, we are telling the client which functions are to be run
# on connecting, and on receiving a message
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.on_publish = on_publish

# Once everything has been set up, we can (finally) connect to the broker
# mqtt_port is the listener port that the MQTT broker is using
mqtt_client.connect(mqtt_broker_ip, mqtt_port)

#start the loop
mqtt_client.loop_start()

while True:
    if receivedMsg is not 'False':
        topic = topic + 'response'
        mqtt_client.publish(topic=topic, payload=receivedMsg)
        receivedMsg = 'False'
    # if receivedMsg is 'OK':
    #     mqtt_client.publish(topic=topic, payload=receivedMsg)
    #     pass
    # elif receivedMsg is 'NOT OK':
    #     pass
    # elif receivedMsg is 'WRONG':

    else:
        continue


mqtt_client.loop_stop()
# mqtt_client.loop_forever()


# Once we have told the client to connect, let the client object run itself
# Disconnect client
mqtt_client.disconnect()

