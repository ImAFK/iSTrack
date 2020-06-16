#include <MCS.h>
#include <MCS_debug.h>

#include <LWiFi.h>
#include <WiFiClient.h>
//#include <LWiFiClient.h>
#include <PubSubClient.h>
#include <SPI.h>
#include <MFRC522.h>
#include "DHT.h"

#define DHTPIN 3     // what pin we're connected to
#define DHTTYPE DHT11   // DHT 11

//------------------------------------------------------------------------------------------------------------------
// set variables
// Replace the next variables with your SSID/Password combination
const char* ssid = "cioffice";
const char* pass = "cioffice3770";
//char ssid[] = "Factory2_2.4G";     ///  your network SSID (name)
//char pass[] = "118factory2";  // your network password
int status = WL_IDLE_STATUS;     // the Wifi radio's status

// Add your MQTT Broker IP address, example:
const char* mqtt_server = "192.168.1.138";
//const char* mqtt_server = "140.118.147.51";

WiFiClient wifiClient;
PubSubClient client( wifiClient );
long lastMsg = 0;
char msg[50];
int value = 0;

// LED Pin
//const int ledPin = 4;
DHT dht_p3(DHTPIN, DHTTYPE);

//------------------------------------------------------------------------------------------------------------------
// Connect to MCS
//MCSDevice mcs("your_device_id", "your_device_key");
//MCSControllerOnOff led("your_channel1_id");
//MCSDisplayOnOff    remote("your_channel2_id");
//// setup MCS connection
//mcs.addChannel(led);
//mcs.addChannel(remote);
//while(!mcs.connected())
//{
//  Serial.println("MCS.connect()...");
//  mcs.connect();
//}
//if(led.updated())
//{
//  Serial.print("LED updated, new value = ");
//  Serial.println(led.value());
//  digitalWrite(LED_PIN, led.value() ? HIGH : LOW);
//  if(!remote.set(led.value()))
//  {
//    Serial.print("Failed to update remote");
//    Serial.println(remote.value());
//  }
//}
//------------------------------------------------------------------------------------------------------------------
// RFID setup
String read_id;
MFRC522 rfid(/*SS_PIN*/ 10, /*RST_PIN*/ 9);
// read from MF RC522 reader
String mfrc522_readID()
{
  String ret;
  if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial())
  {
    MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);

    // here call temperature sensor and get data
    // Reading temperature or humidity takes about 250 milliseconds!
    // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
    float humid = dht_p3.readHumidity();
    float temperature = dht_p3.readTemperature();

    if (isnan(temperature) || isnan(humid))
    {
        Serial.println("Failed to read from DHT");
    }
    else
    {
        Serial.print("Humidity: ");
        Serial.print(humid);
        Serial.print(" %\t");
        Serial.print("Temperature: ");
        Serial.print(temperature);
        Serial.println(" *C");
    }

    for (byte i = 0; i < rfid.uid.size; i++) {
      ret += (rfid.uid.uidByte[i] < 0x10 ? "0" : "");
      ret += String(rfid.uid.uidByte[i], HEX);
    }
    // int n = read_id.length();
    // declaring character array
    char char_array[60];

    // copying the contents of the
    // string to char array
    // strcpy(char_array, read_id.c_str());
    // json format
    // {"id":"dkjfk4k23jk","temperature":"36.9"}
    String msgStr= "{\"id\":\"" + ret + "\",\"temperature\":\"" + temperature + "\"}";
    //{"id":"dkjfk4k23jk","temperature":"36.9"}
    msgStr.toCharArray(char_array, 60);
    client.publish("NTUST/gateA", char_array);
  }

  // Halt PICC
  rfid . PICC_HaltA ();

  // Stop encryption on PCD
  rfid.PCD_StopCrypto1();

  return ret;
}

//------------------------------------------------------------------------------------------------------------------
void readTemperature() {

}
//------------------------------------------------------------------------------------------------------------------
void setup() {
  SPI.begin();
  rfid.PCD_Init();
  Serial.begin(9600);
  // default settings
  // (you can also pass in a Wire library object like &Wire2)
  // setup_wifi();
  // attempt to connect to Wifi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network:
    status = WiFi.begin(ssid, pass);
  }

  // you're connected now, so print out the data:
  Serial.print("You're connected to the network");
  printCurrentNet();
  printWifiData();

  dht_p3.begin();

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

//  pinMode(ledPin, OUTPUT);
}
//------------------------------------------------------------------------------------------------------------------
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i=0;i<length;i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

//void callback(char* topic, byte* message, unsigned int length) {
//  Serial.print("Message arrived on topic: ");
//  Serial.print(topic);
//  Serial.print(". Message: ");
//  String messageTemp;
//
//  for (int i = 0; i < length; i++) {
//    Serial.print((char)message[i]);
//    messageTemp += (char)message[i];
//  }
//  Serial.println();
//
//  // Feel free to add more if statements to control more GPIOs with MQTT
//
//  // If a message is received on the topic esp32/output, you check if the message is either "on" or "off".
//  // Changes the output state according to the message
//  if (String(topic) == "esp32/output") {
//    Serial.print("Changing output to ");
//    if(messageTemp == "on"){
//      Serial.println("on");
//      digitalWrite(ledPin, HIGH);
//    }
//    else if(messageTemp == "off"){
//      Serial.println("off");
//      digitalWrite(ledPin, LOW);
//    }
//  }
//}
//------------------------------------------------------------------------------------------------------------------

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("LinkIt7697")) {
      Serial.println("connected");
      // Subscribe
      // client.subscribe("esp32/output"); // subscribe if need to some topic
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
//------------------------------------------------------------------------------------------------------------------

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  read_id = mfrc522_readID();
  if (read_id != "") {
    Serial.print("RFID: ");
    Serial.println(read_id);
    delay(100);
    client.subscribe("NTUST/gateAresponse");
  }

  delay(1000);
}

//------------------------------------------------------------------------------------------------------------------
void printWifiData() {
  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
  Serial.println(ip);

  // print your MAC address:
  byte mac[6];
  WiFi.macAddress(mac);
  Serial.print("MAC address: ");
  Serial.print(mac[5], HEX);
  Serial.print(":");
  Serial.print(mac[4], HEX);
  Serial.print(":");
  Serial.print(mac[3], HEX);
  Serial.print(":");
  Serial.print(mac[2], HEX);
  Serial.print(":");
  Serial.print(mac[1], HEX);
  Serial.print(":");
  Serial.println(mac[0], HEX);

}

void printCurrentNet() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print the MAC address of the router you're attached to:
  byte bssid[6];
  WiFi.BSSID(bssid);
  Serial.print("BSSID: ");
  Serial.print(bssid[5], HEX);
  Serial.print(":");
  Serial.print(bssid[4], HEX);
  Serial.print(":");
  Serial.print(bssid[3], HEX);
  Serial.print(":");
  Serial.print(bssid[2], HEX);
  Serial.print(":");
  Serial.print(bssid[1], HEX);
  Serial.print(":");
  Serial.println(bssid[0], HEX);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.println(rssi);

  // print the encryption type:
  byte encryption = WiFi.encryptionType();
  Serial.print("Encryption Type:");
  Serial.println(encryption, HEX);
  Serial.println();
}