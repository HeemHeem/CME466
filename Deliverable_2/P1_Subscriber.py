
import random
import time

import paho.mqtt.client as mqtt

#comment

broker = 'broker.hivemq.com'
topic = "Try_this_on_for_size_xix277"
client_id = "test_xix277"


def connect_mqtt() -> mqtt:
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


def subscribe(client: mqtt):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    try:
        client = connect_mqtt()
        subscribe(client)
        client.loop_forever()
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()
        print("\nDisconnected")

if __name__ == '__main__':
    run()