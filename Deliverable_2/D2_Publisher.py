import paho.mqtt.client as mqtt

# use public broker and declare objects/methods
mqttBroker = "broker.hivemq.com" # public broker
client = mqtt.Client("test_call_xix277") # client name
client.connect(mqttBroker)

# publish message
client.publish("Test_msg_xix277", "Sup Dude :p") # topic is Test_msg_xix277

