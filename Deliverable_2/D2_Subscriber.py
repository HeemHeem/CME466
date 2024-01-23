import paho.mqtt.client as mqtt
import time as time
# use public broker
mqttBroker = "broker.hivemq.com"
client = mqtt.Client("test_client_xix277_2") # my client name
client.connect(mqttBroker)

#subscribe to receive message
client.loop_start()
client.subscribe("Test_msg_xix277")
client.on_message = on_message # call a function



def on_message(client, userdata, message):
    b = message.payload.decode("utf-8")
    print("message received", b)

time.sleep(15)
client.loop_stop()