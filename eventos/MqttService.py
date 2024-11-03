from typing import Callable

import paho.mqtt.client as mqtt


class  MqttService:
    ballList = []
    def __init__(self):
        self.broker = "mqtt"
        self.port = 1883
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    def connect(self) -> None:
        self.client.connect(self.broker, self.port)

    def setPublishHandler(self, publishHandler: Callable):
        self.client.on_publish = publishHandler

    def setOnConnectHandler(self, onConnectHandler: Callable):
        self.client.on_connect = onConnectHandler

    def setOnMessageHandler(self, onMessageHandler: Callable):
        self.client.on_message = onMessageHandler

    def publish(self, topic: str, message: str):
        self.client.publish(topic, message)

    def listen(self, topic: str):
        self.client.subscribe(topic)
        self.client.loop_forever()


if __name__ == "__main__":
    def on_publish(client, userdata, flags, reason_code, properties):
        print(properties)
        MqttService.ballList.append("data")
        print("Dispositivo 1: Dados Publicados.")
        pass
    mqttService = MqttService()
    mqttService.setPublishHandler(on_publish)
    mqttService.connect()
    mqttService.publish("/data", "message")
    mqttService.publish("/data", "message")

    print(MqttService.ballList)