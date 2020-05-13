#!/usr/bin/python3

import paho.mqtt.client as mqtt
import time

# Set variables for broker and topics
# mqtt_topic = "temperature"
mqtt_topic = [("NTUST/gateA",0),("NTUST/gateB",0),("NTUST/gateC",0)]
# mqtt_broker_ip = "192.168.50.21"
mqtt_broker_ip = "test.mosquitto.org"
mqtt_port = 1883

# Load credentials from config file
# TODO load mqtt cred
mqtt_username = ""
mqtt_password = ""

# These functions handle what happens when the MQTT client connects
# to the broker, and what happens then the topic receives a message
def on_connect(client, userdata, flags, rc):
    Connected = False
    # rc is the error code returned when connecting to the broker
    if rc == 0:
        print("Connected to broker")
        Connected = True                #Signal connection
    else:
        print("Connection failed, " + str(rc))

    while Connected != True:    # Wait for connection
        time.sleep(0.1)
    # Once the client has connected to the broker, subscribe to the topic
    client.subscribe(mqtt_topic)


def on_message(client, userdata, message):
    # This function is called every time the topic is published to.
    # If you want to check each message, and do something depending on
    # the content, the code to do this should be run in this function

    print("Topic: " + message.topic + "\nMessage: " + str(message.payload))
    with open("/home/ondra/temperature.txt", "w") as temp_out:
        temp_out.write("Topic " + str(message.topic) + " " + " message: " + str(message.payload))
    # The message itself is stored in the msg variable
    # and details about who sent it are stored in userdata

# time.sleep(60)

client = mqtt.Client("NTUST")
# Set the username and password for the MQTT client
# client.username_pw_set(mqtt_username, mqtt_password)


# Here, we are telling the client which functions are to be run
# on connecting, and on receiving a message
client.on_connect = on_connect
client.on_message = on_message

# Once everything has been set up, we can (finally) connect to the broker
# mqtt_port is the listener port that the MQTT broker is using
client.connect(mqtt_broker_ip, mqtt_port)

#start the loop
# client.loop_start()
client.loop_forever()

# Once we have told the client to connect, let the client object run itself
# Disconnect client
client.disconnect()

