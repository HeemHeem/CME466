"""
Deliverable 3
Jason Xie
xix277
11255431


"""
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from PyQt5.QtGui import QCloseEvent
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
        self.SendDisplayMessage.clicked.connect(self.SendToDisplay)
        

    def turn_on_warning(self):
        """ 
            Turn on warning light
        """
        # TODO: need to connect to LED

        # Turn on warning
        self.warning_on_light.setStyleSheet("background-color: rgba(0,200,0, 80%); border-radius: 25px")
        self.warning_off_light.setStyleSheet("background-color: rgba(200,0,0, 30%); border-radius: 25px")
        msg = "ON"
        self.publisher_payload["ON_OFF"] = msg
        self.__publish(msg)
        
    def turn_off_warning(self):
        """
        Turn off warning light
        """
        
        # Turn off Warning
        self.warning_off_light.setStyleSheet("background-color: rgba(200,0,0, 80%); border-radius: 25px")
        self.warning_on_light.setStyleSheet("background-color: rgba(0,200,0, 30%); border-radius: 25px")
        msg = "OFF"
        self.publisher_payload["ON_OFF"] = msg
        self.__publish(msg)
        
        
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
    

    def __publish(self, msg):
        """
        Publish Outgoing Payload
        """
        sent_msg = json.dumps(self.publisher_payload)
        print(f"Send {msg} To Parking Lot")
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
        self.subscriber_client = mqtt.Client(self.subscriber_id)
        self.subscriber_client.on_connect = on_connect
        self.subscriber_client.connect(self.mqttBroker)


    def subscribe(self):
        """
        Subscribe to incoming Payload
        """
        def on_message(client, userdata, msg):
            self.subscriber_payload = json.loads(msg.payload)    
            # self.temperature_textbox.setText(str(self.subscriber_payload))
            print(self.subscriber_payload)


        self.subscriber_client.subscribe(self.subscriber_topic)
        self.subscriber_client.on_message = on_message
        self.subscriber_client.loop_start()
    
    def SendToDisplay(self):
        """
        Send message to parking lot display board
        """
        msg = self.Display_Board_Message_Box.toPlainText()
        if not msg.strip() == '':
            print(msg)
            self.publisher_payload["DisplayBoardMsg"] = msg
            self.__publish(msg)    
    
    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Disconnect on close
        """
        self.subscriber_client.loop_stop()
        self.subscriber_client.disconnect()
        self.publisher_client.loop_stop()
        self.publisher_client.disconnect()
        print("Closed Subscriber")
        print("Closed Publisher")
        event.accept() # accept event

        


if __name__== "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow=ParkingLotInterface()
    mainWindow.show()
    mainWindow.publisher_connect_mqtt()
    mainWindow.subscriber_connect_mqtt()
    mainWindow.subscribe()
    # mainWindow.subscriber_client.loop_start()
    sys.exit(app.exec())
