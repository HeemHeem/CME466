"""
Deliverable 2
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
# import threading
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

        #Publisher
        self.publisher_topic = "Parking Updates - xix277"
        self.publisher_id = "Parking_Lot_Publisher"
        self.publisher_client = None
        self.publisher_payload = {}

        #Subscriber
        self.subscriber_topic = "Parking Lot Message - xix277"
        self.subscriber_id = "Parking_Lot_Subscriber"
        self.subscriber_client = None
        self.subscriber_payload = None

        self.broker = 'broker.hivemq.com'

        # PARKING
        self.parking_spots_empty = [True, True, True, True, True] # True means parking spots are empty
        self.parking_spaces = []

    def gpio_setup(self):
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

        p1 = GPIO.input(self.parking_1_pin)
        p2 = GPIO.input(self.parking_2_pin)
        p3 = GPIO.input(self.parking_3_pin)
        p4 = GPIO.input(self.parking_4_pin)
        p5 = GPIO.input(self.parking_5_pin)

        self.parking_spaces = [p1, p2, p3, p4, p5]

        GPIO.add_event_detect(self.parking_1_pin, GPIO.BOTH, callback=self.parking_taken, bouncetime=100)
        GPIO.add_event_detect(self.parking_2_pin, GPIO.BOTH, callback=self.parking_taken, bouncetime=100)
        GPIO.add_event_detect(self.parking_3_pin, GPIO.BOTH, callback=self.parking_taken, bouncetime=100)
        GPIO.add_event_detect(self.parking_4_pin, GPIO.BOTH, callback=self.parking_taken, bouncetime=100)
        GPIO.add_event_detect(self.parking_5_pin, GPIO.BOTH, callback=self.parking_taken, bouncetime=100)

    def parking_taken(self,pin):
        p1 = GPIO.input(self.parking_1_pin) == 1 #turn into boolean
        p2 = GPIO.input(self.parking_2_pin) == 1
        p3 = GPIO.input(self.parking_3_pin) == 1
        p4 = GPIO.input(self.parking_4_pin) == 1
        p5 = GPIO.input(self.parking_5_pin) == 1
        
        self.parking_spaces = [p1,p2,p3,p4,p5]
        print(self.parking_spaces)
    
    def destroy(self):
        GPIO.output(self.Gpin, GPIO.LOW)
        GPIO.output(self.Rpin, GPIO.LOW)
        GPIO.cleanup()

    def run(self):
        try:
            self.gpio_setup()
            while True:
                # print("what the fuck")
                pass

        except KeyboardInterrupt:
            self.destroy()

if __name__=='__main__':
    parking_lot = Parking_Lot()
    parking_lot.run()
