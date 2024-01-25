
import random
import datetime as datetime
import json as json
import paho.mqtt.client as mqtt

#comment

# broker = 'broker.hivemq.com'
# broker = 'test.mosquitto.org'
broker = "broker.emqx.io"
# broker = "public.mqtthq.com"



topic = "Pain Land 2024 2"
client_id = "test_xix277_2"


def connect_mqtt() -> mqtt.Client:
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
    client.on_connect = on_connect
    client.connect(broker)
    return client

def string_or_list_of_int(msg):
    """
    checks whether msg is a string or list. if it is a list of integers it will
    sum list up. the function will also print out the data type of the message
    received

    """
    if isinstance(msg, list):
        print(f"Received '{msg}' which is of type: ", type(msg).__name__)
        print(f"Sum of list is", sum(msg))
    else:
        print(f"Received '{msg}' which is of type:", type(msg).__name__ )
    
def print_second_element(lst):
    """
    Print every second element of the list

    """
    if isinstance(lst, list):
        print(f"{lst[1]} is the second element of the list")
    else:
        pass

def subscribe(client: mqtt):
    """
    Subscribe to topic and display message

    return: None
    """
    def on_message(client, userdata, msg):
        json_decode_msg = json.loads(msg.payload) # decode json message
        snd_time = json_decode_msg
        rcv_time = datetime.datetime.now().timestamp()
        time_dif = (rcv_time - snd_time) * 1000 # convert time to miliseconds
        # string_or_list_of_int(json_decode_msg)
        # print_second_element(json_decode_msg)
        print(f"Received from '{time_dif}' ms topic")


    client.subscribe(topic)
    client.on_message = on_message


def run():
    try:
        client = connect_mqtt()
        client.loop_start()
        subscribe(client)
        # client.loop_forever()

        while True:            
            pass
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()
        print("\nDisconnected")

if __name__ == '__main__':
    run()