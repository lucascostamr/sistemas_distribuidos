from typing import Callable

import paho.mqtt.client as mqtt


class  MqttService:
    def __init__(self, topic: str):
        self.broker = "mqtt"
        self.port = 1883
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.topic = topic

    def connect(self) -> None:
        self.client.connect(self.broker, self.port)

    def setPublishHandler(self, publishHandler: Callable):
        self.client.on_publish = publishHandler

    def setOnConnectHandler(self, onConnectHandler: Callable):
        self.client.on_connect = onConnectHandler

    def setOnMessageHandler(self, onMessageHandler: Callable):
        self.client.on_message = onMessageHandler

    def publish(self, message: str):
        self.client.publish(self.topic, message)

    def listen(self):
        self.client.subscribe(self.topic)
        self.client.loop_forever()