import paho.mqtt.client as mqtt
import json

THE_BROKER = "eu.thethings.network"
THE_TOPIC = "+/devices/+/up"
CLIENT_ID = ""

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected to ", client._host, "port: ", client._port)
    print("Flags: ", flags, "returned code: ", rc)

    client.subscribe(THE_TOPIC, qos=0)

def on_message(client, userdata, msg):

    if ("lopysense2" in msg.topic):
        print(msg.topic)
        tmsg = json.loads(msg.payload)
        print("Got this temperature value:")
        print(tmsg["payload_fields"]["temperature"])

        print("from these gateways:")
        for g in tmsg["metadata"]["gateways"]:
          print(g["gtw_id"], g["rssi"])

client = mqtt.Client(client_id=CLIENT_ID, 
                     clean_session=True, 
                     userdata=None, 
                     protocol=mqtt.MQTTv311, 
                     transport="tcp")

client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("lopy2ttn", password="ttn-account-v2.TPE7-bT_UDf5Dj4XcGpcCQ0Xkhj8n74iY-rMAyT1bWg")
client.connect(THE_BROKER, port=1883, keepalive=60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
client.loop_forever()

