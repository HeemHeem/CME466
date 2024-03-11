import paho.mqtt.client as mqtt
import json as json

class pi_sender(object):
    def __init__(self):
        # client
        self.subscriber_topic = "Image Message - xix277"
        self.subscriber_id = "Image_Publisher-xix2772"
        self.subscriber_client = None
        self.subscriber_payload = {}

        self.publisher_topic = "Image Update - xix277"
        self.publisher_id = "Image_Subscriber-xix2772"
        self.publisher_client = None
        self.publisher_payload = {} # parking spots will be a list of True or False - True for empty, False for full
        
        
        self.mqttBroker = "broker.hivemq.com"
    
    
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
        self.subscriber_client = mqtt.Client(self.subscriber_id)
        self.subscriber_client.on_connect = on_connect
        self.subscriber_client.connect(self.mqttBroker)
        
    def subscribe(self):
        """
        Subscribe to incoming Payload
        """
        def on_message(client, userdata, msg):

            print(json.loads(msg.payload))
            


        self.subscriber_client.subscribe(self.subscriber_topic)
        self.subscriber_client.on_message = on_message
        self.subscriber_client.loop_start()



    def run(self):

        try:

            #initial publish
            # self.__publish("Initial Parking Availability " + str(self.publisher_payload["Parking_Spots"]))
            self.subscriber_connect_mqtt()
            self.publisher_connect_mqtt()
            self.subscribe()
        

            while True:
                msg = input("input r, a, or b: ")
                self.subscriber_payload["ImageUpdate"] = msg

                sent_msg = json.dumps(self.subscriber_payload)
                self.publisher_client.publish(self.publisher_topic, sent_msg)

        except KeyboardInterrupt:
            self.subscriber_client.loop_stop()
            self.publisher_client.loop_stop()
            self.subscriber_client.disconnect()
            self.publisher_client.disconnect()

            print("Closed Subscriber")
            print("Closed Publisher")
            
if __name__=='__main__':
    gui = pi_sender()
    # gui.subscriber_connect_mqtt()
    # gui.publisher_connect_mqtt()
    # gui.subscribe()
    gui.run()