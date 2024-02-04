from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import main_window_ui
import json as json
import paho.mqtt.client as mqtt


class ParkingLotInterface(QtWidgets.QMainWindow, main_window_ui.Ui_MainWindow):
    """UI Window Class"""

    def __init__(self):
        """initialize the window class"""
        super(ParkingLotInterface,self).__init__()
        self.setupUi(self)

        # client
        self.publisher_topic = "Parking Lot Message - xix277"
        self.publisher_id = "Parking_Publisher"
        self.publisher_client = None
        self.publisher_payload = {}

        self.subscriber_topic = "Parking Updates - xix277"
        self.subscriber_id = "Parking_Subscriber"
        self.subscriber_client = None
        self.subscriber_payload = {}


        self.mqttBroker = "broker.hivemq.com"
        
        
        # events
        self.warning_on_off_flg = False
        self.warning_on_button.clicked.connect(self.turn_on_warning)
        self.warning_off_button.clicked.connect(self.turn_off_warning)
        

    def turn_on_warning(self):
        """ 
            Turn on warning light
        """
        # TODO: need to connect to LED

        # Turn on warning
        self.warning_on_light.setStyleSheet("background-color: rgba(0,200,0, 80%); border-radius: 25px")
        self.warning_off_light.setStyleSheet("background-color: rgba(200,0,0, 30%); border-radius: 25px")
        self.publisher_payload["ON_OFF"] = "ON"
        self.__publish()
        
    def turn_off_warning(self):
        """
        Turn off warning light
        """
        
        # Turn off Warning
        self.warning_off_light.setStyleSheet("background-color: rgba(200,0,0, 80%); border-radius: 25px")
        self.warning_on_light.setStyleSheet("background-color: rgba(0,200,0, 30%); border-radius: 25px")
        self.publisher_payload["ON_OFF"] = "OFF"
        self.__publish()
        
    def publisher_connect_mqtt(self):
        """
        connect publisher to MQTT broker
        """
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Publisher Connected to MQTT Broker!")
            else:
                print("Failed to connect, return cod %d\n", rc)
        self.publisher_client = mqtt.Client(self.publisher_id)
        self.publisher_client.on_connect = on_connect
        self.publisher_client.connect(self.mqttBroker)
        self.publisher_client.loop_start()
    

    def __publish(self):
        """
        Publish Payload
        """
        sent_msg = json.dumps(self.publisher_payload)
        self.publisher_client.publish(self.publisher_topic, sent_msg)


    def subscriber_connect_mqtt(self):
        """
        connect subscriber to MQTT broker
        """
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Subscriber Connected to MQTT Broker!")
            else:
                print("Failed to connect, return cod %d\n", rc)
        self.subscriber_client = mqtt.Client(self.subscriber_client)
        self.subscriber_client.on_connect = on_connect
        self.subscriber_client.connect(self.mqttBroker)

    def subscribe(self):
        pass

if __name__== "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow=ParkingLotInterface()
    mainWindow.show()
    mainWindow.publisher_connect_mqtt()
    mainWindow.publisher_client.loop_stop()
    sys.exit(app.exec())
