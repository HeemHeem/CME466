"""
CME466 Deliverable 1
Jason Xie
xix277
11255431

"""
import time as time
import datetime as datetime
import json as json
from cryptography.fernet import Fernet
import paho.mqtt.client as mqtt
import math as m
# import D1_SW_LED_and_Sound_Sensor as Edge_Sensor
import PCF8591 as ADC
import RPi.GPIO as GPIO
# import threading
# import time


########################## IOT
BtnPin = 17
Gpin   = 18
Rpin   = 27

on_off = False
tmp = False
count = 0
red_green = False
sound_detected = False



################## Publisher

broker = 'broker.hivemq.com'
# broker = 'test.mosquitto.org'
# broker = "broker.emqx.io"
# broker = "public.mqtthq.com"

# encryption
with open("key.txt", 'rb') as f:
    key = f.read()

fern = Fernet(key) # create Fernet object

# print(key)
topic = "Pain Land 2024 2"
topic2 = "Pain Land 2024 56"
client_id = "test_xix277_1"
client_id2 = "xix277"

################# IOT

def setup():
    ADC.setup(0x48)
    GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
    GPIO.setup(Gpin, GPIO.OUT)     # Set Green Led Pin mode to output
    GPIO.setup(Rpin, GPIO.OUT)     # Set Red Led Pin mode to output
    GPIO.output(Rpin, GPIO.LOW)    # turn red led off
    GPIO.output(Gpin, GPIO.LOW)    # turn green led off
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
    # GPIO.add_event_detect(BtnPin, GPIO.FALLING, callback=detect, bouncetime=50)
    GPIO.add_event_detect(BtnPin, GPIO.FALLING, bouncetime=300)



def switch():
    """
    Turn the system on or off upon button press

    """
    global on_off
    # if GPIO.event_detected(BtnPin) and on_off == 0:
    #     on_off = 1
    #     # print("OFF")
    # elif GPIO.event_detected(BtnPin) and on_off == 1:
    #     on_off = 0
        # print("RED")
    if GPIO.event_detected(BtnPin):
        on_off = not on_off

def Print(on_off):
    """
    Display whether the system is on or off based on the on_off boolean.

    on_off: True for on, False for off

    """
    global tmp
    if on_off != tmp:
        if on_off == False:
            print("OFF")

        if on_off == True:
            print("ON")
        tmp = on_off

def Led():
    """
    Change Led Colour based on sound input.
    If red_green is True, the LED will be red. If red_green is False, the LED will be Green.
    If on_off is True, the LED is on. If on_off is False, the LED is off 
    """

    global on_off
    global red_green
    # global sound_detected
    if on_off == True:
        

        # if sound_detected:

        if red_green: # red led
            GPIO.output(Rpin, GPIO.HIGH)
            GPIO.output(Gpin, GPIO.LOW)
        
        if not red_green: # green led
            GPIO.output(Rpin, GPIO.LOW)
            GPIO.output(Gpin, GPIO.HIGH)

        # GPIO.output(Gpin, 0)
    if on_off == False:
        GPIO.output(Rpin, GPIO.LOW)
        GPIO.output(Gpin, GPIO.LOW)

def detect():
    """
    Runs the LED function.

    """
    # Redundant, could just take it out after, but might keep it in case of using events and multithreading
    Led()
    # change_color_with_sound()

def print_color(rg):
    """
    Prints what colour the LED is currently.
    If rg is True, the LED is red. Otherwise the LED is green
    """
    if rg:
        msg = "LIGHT IS NOW RED"
        print(msg)
    else:
        msg = "LIGHT IS NOW GREEN"
        print(msg)
    return msg

def change_color_with_sound():
    """
    Changes the LED colour to either green or red upon detecting a sound value less than 75. Prints the sound value
    and a counter of how many times it has been activied.
    Upon detecting sound, it will change the red_green boolean and increase the counter of how many times it has been activated
    """

    global count
    global red_green
    global sound_detected
    sound_detected = False
    voiceValue = ADC.read(0)
    # if voiceValue:
        # print ("Value:", voiceValue)
    if on_off:
        if voiceValue < 75:
            print ("Value:", voiceValue)
            print ("Voice In!! ", count)
            sound_detected = True
            red_green = not red_green
            print_color(red_green)
            count += 1
    # time.sleep(1)

# def loop():
#     while True:
#         switch()
#         detect()
#         change_color_with_sound()
#         Print(on_off)



def destroy():
    GPIO.output(Gpin, GPIO.LOW)       # Green led off
    GPIO.output(Rpin, GPIO.LOW)       # Red led off
    GPIO.cleanup()                     # Release resource


###################################### PUBLISHER ##########################################

def connect_mqtt(client_id) -> mqtt.Client:
    """
    connect to MQTT broker

    return: client

    """
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker)
    return client

def adc_to_dB(adc_val):
    volts = (3.3/255) * adc_val
    return -20*m.log(volts/3.3, 10)




def publish(msg_in, client, topic):
    msg = json.dumps(msg_in) # message to be sent
    msg = fern.encrypt(msg.encode()) # encrypt message
    result = client.publish(topic, msg, qos=0, retain=False)
    status = result[0]
    if status == 0:
        print(f"Send `{msg_in:.2f}`dB to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


def subscribe(client: mqtt, topic: str):
    """
    Subscribe to topic and display message

    return: None
    """
    def on_message(client, userdata, msg):
        global on_off
        msg_rcv = msg.payload
        msg_decode  = fern.decrypt(msg_rcv)
        msg = json.loads(msg_decode) # decode send time from json message

        # rcv_time = datetime.datetime.now().timestamp() # get current time
        
        # latency_time_ms = (rcv_time - snd_time) * 1000 # convert time to miliseconds

        print(f"Sound Sensor Received {msg} from topic '{topic}'")

        if msg == "ON":
            on_off = True
        elif msg == "OFF":
            on_off = False


    client.subscribe(topic)
    client.on_message = on_message




def loop(client_publisher, client_subscriber, topic_pub, topic_sub):
    """
    takes in a client object and publishes to the broker
    return: None
    """
    global tmp
    global on_off
    try:
        client_subscriber.loop_start()
        # client_publisher.loop_start()
        subscribe(client_subscriber, topic_sub)
        while True:
            time.sleep(0.1)

            #create datetime object
            # dt = datetime.datetime.now()
            # msg_in = dt.timestamp()
            switch()
            detect()    
            change_color_with_sound()
            Print(on_off)   

            msg_in = ADC.read(0)

            if(on_off):
                if (msg_in < 75):
                    msg_in = adc_to_dB(msg_in)
                    publish(msg_in, client_publisher, topic_pub)
                


    except KeyboardInterrupt:
        client_subscriber.loop_stop()
        client_publisher.loop_stop()
        client_subscriber.disconnect()
        client_publisher.disconnect()
        destroy()

        print("\nDisconnected")



def run():

    client_pub = connect_mqtt(client_id)
    client_sub = connect_mqtt(client_id2)
    loop(client_pub, client_sub, topic, topic2)
    # client.loop_start()
    # publish(client)






if __name__ == '__main__':     # Program start from here
    setup()
    # try:
    run()
        
    # except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
    #     destroy()
        