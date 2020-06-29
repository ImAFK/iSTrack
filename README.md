# iSTrack
iSTrack is an innovative solution to help track and monitor movements in a building or area.
This is the repository of our IoT solution based on listed below devices was developed in the contest of the Adventech IoT Competition.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

What things you need to install
* Python
* Visual Studio Code or your favorite IDE
* Custom code on LinkIt developed with Arduino IDE
* BalenaCloud + BalenaOS on RPI
* Docker on RPI
* MongoDB in Docker on RPI
* Custom python code in a Docker on RPI
* Mosquitto MQTT broker in a Docker on RPI


## Technical Support
### Harware 
* LinkIt 7697
* Raspberry Pi 3B+
* MiFare RC-522
* Temperature sensor

### Adventech Side
* MongoDB instance
* AFS for AI
* Dashboard for presentation layer



### Wiring devices

![](https://i.imgur.com/QOQ2K99.png)


### Architecture
![](https://i.imgur.com/xE2NSiw.png)


### Installation

1. Clone this repository
2. Create a .env file in the root directory and add the following information (Replace by your keys and ids)
```
atmongo_username = DB Username
atmongo_password = DB Password
atmongo_host = Mongo host
atmongo_port = Mongo Port
atmongo_db = MongoDB Id
mqtt_username = mqqt Username
mqtt_password = mqtt password
```
### User manual

1. Fog - Raspberry Pi
    - Register account on BalenaCloud and Install [BalenaOS](https://www.balena.io/) on RPI
    - Download and push necessary code to the BalaneCloud from [Github](https://github.com/ImAFK/iSTrack/tree/master/mqtt-mongo-sample) 

3. Edge - LinkIt
    - Wire everything as described in Wiring section
    - Download code from Github for [LinkIt](https://github.com/ImAFK/iSTrack/tree/master/Arduino/LinkIt7697)
    - Adjust WiFi connection, IP of the MQTT broker in the code for your needs
    - Make sure you have all necessary libraries installed
    - Compile code
    - Push code to the LinkIt with Arduino IDE

5. Cloud
    - Register Advantech account
    - Download code from [Github](https://github.com/ImAFK/iSTrack/tree/master/dashboard-mongo-proxy) 
    - Adjust code to your needs
    - Deploy 


### Testing

For testing, you need first to scan you card with the RFID reader. If your user is already registered, hte data is automatically sent to RPi DB. At a certain frequency, all the data in the DB is automatically send to another one on the cloud. We've set up Mongo Replicas to prevent any damage in the future. The system is then self aware and can leverage in case of problem with the primary DB.



## Author

* **[Ondrej Vokoun](https://github.com/ImAFK)** 
* **[Freddy Sossa](https://github.com/fredsossa1)** 
* **[AnTing Hu](https://github.com/HuSalt)** 
* **Andrea Blumer** 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
