"""
Deliverable 2
Jason Xie
xix277
11255431


"""
import time as time
import datetime as datetime
import json as json
from cryptography.fernet import Fernet
import paho.mqtt.client as mqtt

# broker = 'broker.hivemq.com'
# broker = 'test.mosquitto.org'
broker = "broker.emqx.io"
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
            time_smp = dt.timestamp()
            time_smp_json = json.dumps(time_smp) # message to be sent
            

            # UNCOMMENT FOR ENCRYPTION
            ################# With Encryption ################
            # time_smp_encrypt = fern.encrypt(time_smp_json.encode()) # encrypt message
            # result = client.publish(topic, time_smp_encrypt)
            

            # UNCOMMENT FOR NO ENCRYPTION
            ################# Without Encryption ############
            result = client.publish(topic, time_smp_json)
            ################################################


            # msg = json.dumps("WHAT TIME IS IT?")
            # msg_in = fern.encrypt(msg.encode()) # encrypt message

            # result = client.publish(topic, b"$" + msg_in, qos=1, retain=False)
            
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
    # client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()