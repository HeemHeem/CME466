from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from PyQt5.QtGui import QCloseEvent
import lab_exam_ui
import json as json
import paho.mqtt.client as mqtt


class Lab_Exam_Interface(QtWidgets.QMainWindow, lab_exam_ui.Ui_MainWindow):
    """UI Window class"""

    def __init__(self):
        """initialize the window class"""
        super(Lab_Exam_Interface, self).__init__()
        self.setupUi(self)


                # client
        self.publisher_topic = "Image Message - xix277"
        self.publisher_id = "Image_Publisher-xix277"
        self.publisher_client = None
        self.publisher_payload = {}

        self.subscriber_topic = "Image Update - xix277"
        self.subscriber_id = "Image_Subscriber-xix277"
        self.subscriber_client = None
        self.subscriber_payload = {} # parking spots will be a list of True or False - True for empty, False for full
        
        self.mqttBroker = "broker.hivemq.com"

    
    def change_layout(self):

        if "ImageUpdate" in self.subscriber_payload.keys():
            msg = self.subscriber_payload["ImageUpdate"]

            if msg == "r":
                self.setStyleSheet("background-color: blue;")
                self.publisher_client.publish(self.publisher_topic, json.dumps("default display"))
                self.label.clear()
            
            if msg == "a":
                self.label.setPixmap(QtGui.QPixmap("../../../Pictures/Screenshots/image1.jpg"))
                self.publisher_client.publish(self.publisher_topic, json.dumps("Computer engineering"))
                self.setStyleSheet("background-color: lightgray;")


            if msg == "b":
                self.label.setPixmap(QtGui.QPixmap("../../../Pictures/Screenshots/image2.jpeg"))
                self.publisher_client.publish(self.publisher_topic, json.dumps("Machine Learning"))
                self.setStyleSheet("background-color: lightgray;")


            


            

    
    
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
    

    def subscriber_connect_mqtt(self):
        """
        connect subscriber to MQTT broker
        """
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Subscriber Connected to MQTT Broker!")
            else:
                print("Failed to connect, return cod %d\n", rc)
        self.subscriber_client = mqtt.Client(self.subscriber_id, userdata={"ui":self})
        self.subscriber_client.on_connect = on_connect
        self.subscriber_client.connect(self.mqttBroker)

    def subscribe(self):
        """
        Subscribe to incoming Payload
        """
        def on_message(client, userdata, msg):
            gui = userdata["ui"]
            gui.subscriber_payload = json.loads(msg.payload)
            # gui.update_temperature()
            # # print(self.subscriber_payload)
            # gui.update_parking_spots()
            # gui.update_warning_msg_feedback()
            gui.change_layout()  

        self.subscriber_client.subscribe(self.subscriber_topic)
        self.subscriber_client.on_message = on_message
        self.subscriber_client.loop_start()



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
        # event.accept() # accept event



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Lab_Exam_Interface()
    mainWindow.show()
    mainWindow.publisher_connect_mqtt()
    mainWindow.subscriber_connect_mqtt()
    mainWindow.subscribe()
    sys.exit(app.exec_())
