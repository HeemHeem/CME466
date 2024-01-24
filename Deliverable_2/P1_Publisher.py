import random
import time
import json as json

import paho.mqtt.client as mqtt

broker = 'broker.hivemq.com'
topic = "Try_this_on_for_size_xix277"
client_id = "test_xix277_1"

def connect_mqtt():
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
    msg_count = 0
    try:
        msg_retain = json.dumps("Welcome to pain land")
        # client.publish(topic, msg_retain, qos=0, retain=True) #for setting the retain flag
        client.publish(topic, None, qos=0, retain=True) #for cleaing retain flag
        client.publish(topic, json.dumps("hello"), qos=2, retain=True)
        while True:
            time.sleep(1)
            # msg = f"messages: {msg_count}"
            my_list = [14, 23, 43, 55, 60]
            # msg = json.dumps(my_list) # encode data
            # msg = json.dumps("CHEESE")
            msg = json.dumps("Lucis")
            # result = client.publish(topic,msg, qos=1, retain=True)
            result = client.publish(topic, msg, qos=0, retain=False)
            # result = client.publish(topic, None, retain=True)
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