"""
Deliverable 3
Jason Xie
xix277
11255431


"""
import time as time
import datetime as datetime
import json as json
import paho.mqtt.client as mqtt
import math as m
# import D1_SW_LED_and_Sound_Sensor as Edge_Sensor
import PCF8591 as ADC
import RPi.GPIO as GPIO
import math
import threading
# import time


class Parking_Lot(object):

    def __init__(self):
        """
        initialize parking lot class
        """

        #GPIO
        self.Gpin = 15
        self.Rpin = 24
        self.parking_1_pin = 18 
        self.parking_2_pin = 17 
        self.parking_3_pin = 27 
        self.parking_4_pin = 22 
        self.parking_5_pin = 23
        self.on_off = False

        #Sensors
        self.temp_thread = threading.Thread(target=self.send_temp)
        self.temp_thread_event = threading.Event()
        self.temp = None
        self.prev_temp = None

        # LED
        self.warning_on_off = "OFF"
        self.prev_warning = "OFF"

        # Display Board
        self.prev_display_msg = ""

        #Publisher
        self.publisher_topic = "Parking Updates - xix277"
        self.publisher_id = "Parking_Lot_Publisher"
        self.publisher_client = None
        self.publisher_payload = {}

        #Subscriber
        self.subscriber_topic = "Parking Lot Message - xix277"
        self.subscriber_id = "Parking_Lot_Subscriber"
        self.subscriber_client = None
        self.subscriber_payload = {}

        self.mqttBroker = 'broker.hivemq.com'

        # PARKING
        self.parking_spots_empty = [] # True means parking spots are empty

    def gpio_setup(self):
        """
        setting up gpio and initial parking spot values
        """
        ADC.setup(0x48)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.Gpin, GPIO.OUT)     # Set Green Led Pin mode to output
        GPIO.setup(self.Rpin, GPIO.OUT)     # Set Red Led Pin mode to output
        GPIO.output(self.Rpin, GPIO.LOW)    # turn red led off
        GPIO.output(self.Gpin, GPIO.LOW)    # turn green led off
        GPIO.setup(self.parking_1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.parking_2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.parking_3_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.parking_4_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.parking_5_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        p1 = GPIO.input(self.parking_1_pin) == 1 # turn into boolean
        p2 = GPIO.input(self.parking_2_pin) == 1
        p3 = GPIO.input(self.parking_3_pin) == 1
        p4 = GPIO.input(self.parking_4_pin) == 1
        p5 = GPIO.input(self.parking_5_pin) == 1

        self.parking_spots_empty = [p1, p2, p3, p4, p5]
        self.publisher_payload["Parking_Spots"] = self.parking_spots_empty

        GPIO.add_event_detect(self.parking_1_pin, GPIO.BOTH, callback=self.parking_taken, bouncetime=100)
        GPIO.add_event_detect(self.parking_2_pin, GPIO.BOTH, callback=self.parking_taken, bouncetime=100)
        GPIO.add_event_detect(self.parking_3_pin, GPIO.BOTH, callback=self.parking_taken, bouncetime=100)
        GPIO.add_event_detect(self.parking_4_pin, GPIO.BOTH, callback=self.parking_taken, bouncetime=100)
        GPIO.add_event_detect(self.parking_5_pin, GPIO.BOTH, callback=self.parking_taken, bouncetime=100)

    def parking_taken(self,pin):
        """
        checks which parking spots are taken and sends it to the gui
        """
        p1 = GPIO.input(self.parking_1_pin) == 1 #turn into boolean
        p2 = GPIO.input(self.parking_2_pin) == 1
        p3 = GPIO.input(self.parking_3_pin) == 1
        p4 = GPIO.input(self.parking_4_pin) == 1
        p5 = GPIO.input(self.parking_5_pin) == 1
        
        self.parking_spots_empty = [p1,p2,p3,p4,p5]
        self.publisher_payload["Parking_Spots"] = self.parking_spots_empty
        self.__publish("Parking Spot Availability " + str(self.parking_spots_empty))
        # print(self.parking_spots_empty)

    def send_temp(self):
        """
        send temperature value only if it changes
        """
        while True:
            analogVal = ADC.read(0)
            Vr = 3.3 * float(analogVal) / 255
            Rt = 10000 * Vr / (3.3 - Vr)
            temp = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15+25)))
            self.temp = round(temp - 273.15, 2)

            if self.temp != self.prev_temp:
                self.publisher_payload["Temperature"] = self.temp
                self.prev_temp = self.temp
                self.__publish(str(self.temp) + " C")

            # print ('temperature = ', temp, 'C') 
            time.sleep(1)

            if self.temp_thread_event.is_set():
                break


    def turn_on_off_warning(self):
        """
        Flash warning light or turn off light based on ON or OFF 
        from subscribers ON_OFF dictionary value
        """

        if "ON_OFF" in self.subscriber_payload.keys():
            self.warning_on_off = self.subscriber_payload["ON_OFF"]
            if self.warning_on_off == "ON":
                GPIO.output(self.Rpin, GPIO.HIGH)
                time.sleep(0.5)
                GPIO.output(self.Rpin, GPIO.LOW)
                time.sleep(0.5)

            else:
                GPIO.output(self.Rpin, GPIO.LOW)
                
            if self.prev_warning != self.subscriber_payload["ON_OFF"]:
                outgoing_msg = ''
                if self.subscriber_payload["ON_OFF"] == "ON":
                    outgoing_msg = "Message Received. Warning ON"
                else:
                    outgoing_msg = "Message Received. Warning OFF"

                self.publisher_payload["Warning_Message_Received"] = outgoing_msg 
                self.__publish(outgoing_msg)
            self.prev_warning = self.subscriber_payload["ON_OFF"]
    
    def DisplayBoard(self):
        if "DisplayBoardMsg" in self.subscriber_payload.keys():
                if self.subscriber_payload["DisplayBoardMsg"].strip() == "clear":
                    self.subscriber_payload["DisplayBoardMsg"] = ''
                    print("")
                elif self.prev_display_msg != self.subscriber_payload["DisplayBoardMsg"]:
                    self.prev_display_msg = self.subscriber_payload["DisplayBoardMsg"]
                    print(self.subscriber_payload["DisplayBoardMsg"])

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
        print(f"Send {msg} To Parking Monitor")
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
            self.DisplayBoard()


        self.subscriber_client.subscribe(self.subscriber_topic)
        self.subscriber_client.on_message = on_message
        self.subscriber_client.loop_start()

    def destroy(self):
        """
        cleanup gpio
        """
        GPIO.output(self.Gpin, GPIO.LOW)
        GPIO.output(self.Rpin, GPIO.LOW)
        GPIO.cleanup()

    def run(self):
        """
        run program
        """
        try:
            self.subscriber_connect_mqtt()
            self.publisher_connect_mqtt()
            self.gpio_setup()
            #initial publish
            self.__publish("Initial Parking Availability " + str(self.publisher_payload["Parking_Spots"]))
            self.subscribe()
            self.temp_thread.start()

            while True:
                self.turn_on_off_warning()

        except KeyboardInterrupt:
            self.temp_thread_event.set()
            self.destroy()
            self.subscriber_client.loop_stop()
            self.publisher_client.loop_stop()
            self.subscriber_client.disconnect()
            self.publisher_client.disconnect()

            print("Closed Subscriber")
            print("Closed Publisher")
            

if __name__=='__main__':
    parking_lot = Parking_Lot()
    parking_lot.run()
