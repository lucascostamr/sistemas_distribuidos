import paho.mqtt.client as mqtt

#hostname
broker="mqtt"
#port
port=1883
#time to live
timelive=60
def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected with result code "+str(reason_code))
    client.subscribe("/data")
def on_message(client, userdata, msg):
    print(msg.payload.decode())

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(broker,port,timelive)
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()
