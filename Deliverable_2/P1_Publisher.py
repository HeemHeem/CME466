"""
Deliverable 2
Jason Xie
xix277
11255431


"""
import random
import time
import json as json

import paho.mqtt.client as mqtt

broker = 'broker.hivemq.com'
topic = "Pain Land 2024"
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
    msg_retain = "Welcome to Pain Land"
    try:

        initial_msg = json.dumps(msg_retain)
        # client.publish(topic, initial_msg, qos=0, retain=True) #for setting the retain flag
        # client.publish(topic, None, qos=1, retain=True) #for clearing retain flag
        
        while True:
            time.sleep(1)

            ### Uncomment depending on what message you want to send
            msg_in = random.sample(range(1, 50), 5) # generate 5 random numbers within the range of 1-50
            # msg_in = "The Realms of Pain will attenuate the train"
            
            
            msg = json.dumps(msg_in) # message to be sent

            # UNCOMMENT FOR DIFFERENT QOS
            # result = client.publish(topic,msg, qos=0, retain=False)
            # result = client.publish(topic, msg, qos=1, retain=False)
            result = client.publish(topic, msg, qos=2, retain=False)
            
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")

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