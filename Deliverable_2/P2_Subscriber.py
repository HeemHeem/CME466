
import datetime as datetime
import json as json
from cryptography.fernet import Fernet
import paho.mqtt.client as mqtt

#comment

# broker = 'broker.hivemq.com'
broker = 'test.mosquitto.org'
# broker = "broker.emqx.io"
# broker = "public.mqtthq.com"

#encryption
with open("key.txt", 'rb') as f:
    key = f.read()

fern = Fernet(key) # create Fernet object
# print(fern)

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
    

def subscribe(client: mqtt):
    """
    Subscribe to topic and display message

    return: None
    """
    def on_message(client, userdata, msg):
        snd_time_encrypt = msg.payload
        snd_time = fern.decrypt(snd_time_encrypt)
        snd_time = json.loads(snd_time) # decode send time from json message

        rcv_time = datetime.datetime.now().timestamp() # get current time
        
        latency_time_ms = (rcv_time - snd_time) * 1000 # convert time to miliseconds

        print(f"Latency from '{broker}' is '{latency_time_ms:.2f}' ms for topic '{topic}'")

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