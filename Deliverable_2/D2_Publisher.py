import random
import time

import paho.mqtt.client as mqtt

broker = 'broker.hivemq.com'
topic = "Try_this_on_for_size_xix277"
client_id = "test_xix277"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt.Client("")
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker)
    return client


def publish(client):
    msg_count = 0
    try:
        while True:
            time.sleep(1)
            msg = f"messages: {msg_count}"
            result = client.publish(topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")
            msg_count += 1
    except KeyboardInterrupt:
        client.disconnect()
        client.loop_stop()
        print("\nDisconnected")

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()