import time as time
import datetime as datetime
import json as json
from cryptography.fernet import Fernet
import paho.mqtt.client as mqtt
import D1_SW_LED_and_Sound_Sensor as Edge_Sensor

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
client_id = "test_xix277_1"

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
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker)
    return client


def publish(client):
    """
    takes in a client object and publishes to the broker
    return: None
    """
    try:
        
        while True:
            time.sleep(1)

            #create datetime object
            dt = datetime.datetime.now()
            msg_in = dt.timestamp()
            
            msg = json.dumps(msg_in) # message to be sent
            msg = fern.encrypt(msg.encode()) # encrypt message

            result = client.publish(topic, msg, qos=0, retain=False)
            
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{dt}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")

    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()
        print("\nDisconnected")

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()