# simulator device 1 for mqtt message publishing
import random
import time

import paho.mqtt.client as mqtt

# hostname
broker = "mqtt"
# port
port = 1883


def on_publish(client, userdata, flags, reason_code, properties):
    print("Dispositivo 1: Dados Publicados.")
    pass


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_publish = on_publish
client.connect(broker, port)

for i in range(20):
    d = random.randint(1, 5)

    # criando mensagem
    message = "Dispositivo 1 : Dados " + str(i)
    time.sleep(d)

    # publicando mensagem
    ret = client.publish("/data", message)
print("Parou...")
