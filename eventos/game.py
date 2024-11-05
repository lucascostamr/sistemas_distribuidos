import time
from turtle import Screen, Turtle
from threading import Thread
from uuid import uuid1
from json import dumps, loads

from MqttService import MqttService
from utils import random_color


class Game:
    player_dict = {}

    def __init__(self):
        self.current_player = None
        self.screen_width = None
        self.screen_height = None
        self.current_player_id = None
        self.topic = "/data"

        self.delay = 0.01
        self.mqttService = MqttService(self.topic)
        self.screen = self.create_screen()
        self.bind_keys()

    def create_screen(self) -> Screen:
        screen = Screen()
        screen.title("Move Game by @Garrocho")
        screen.bgcolor("black")
        screen.setup(width=1.0, height=1.0, startx=None, starty=None)
        screen.tracer(0)

        self.screen_width = screen.window_width() // 2
        self.screen_height = screen.window_height() // 2

        return screen

    def create_player(self, color):
        player = Turtle()
        player.speed(0)
        player.shape("turtle")
        player.color(color)
        player.penup()
        player.goto(0,0)
        player.direction = "stop"

        if not self.current_player:
            self.current_player = player

        return player

    def go_up(self):
        self.current_player.direction = "up"

        message = dumps({
            "id": self.current_player_id,
            "direction": "up"
        })

        self.mqttService.publish(message=message)


    def go_down(self):
        self.current_player.direction = "down"

        message = dumps({
            "id": self.current_player_id,
            "direction": "down"
        })

        self.mqttService.publish(message=message)


    def go_left(self):
        self.current_player.direction = "left"

        message = dumps({
            "id": self.current_player_id,
            "direction": "left"
        })

        self.mqttService.publish(message=message)

    def go_right(self):
        self.current_player.direction = "right"

        message = dumps({
            "id": self.current_player_id,
            "direction": "right"
        })

        self.mqttService.publish(message=message)

    def close(self):
        self.screen.bye()

    def move(self):
        for player_data in Game.player_dict.values():
            turtle = player_data.get("turtle")

            if not turtle:
                continue

            if player_data.get("direction") == "up":
                y = turtle.ycor()
                if y < self.screen_height - 10:
                    turtle.sety(y + 7)

            if player_data.get("direction") == "down":
                y = turtle.ycor()
                if y > -self.screen_height + 10:
                    turtle.sety(y - 7)

            if player_data.get("direction") == "left":
                x = turtle.xcor()
                if x > -self.screen_width + 10:
                    turtle.setx(x - 7)

            if player_data.get("direction") == "right":
                x = turtle.xcor()
                if x < self.screen_width - 10:
                    turtle.setx(x + 7)

    def generate_players(self):
        for player_id, player_data in Game.player_dict.items():
            if not player_data.get("in_game"):
                player_data["turtle"] = self.create_player(color=player_data.get("color"))
                player_data["in_game"] = True
                Game.player_dict[player_id] = player_data

                print(Game.player_dict)

    def publish_players(self):
        for player_id, player_data in Game.player_dict.items():
            message = dumps({
                "id": player_id,
                "color": player_data.get("color"),
                "direction": player_data.get("direction")
            })
            self.mqttService.publish(message)

    def bind_keys(self):
        self.screen.listen()
        self.screen.onkeypress(self.go_up, "w")
        self.screen.onkeypress(self.go_down, "s")
        self.screen.onkeypress(self.go_left, "a")
        self.screen.onkeypress(self.go_right, "d")
        self.screen.onkeypress(self.close, "Escape")

    def start(self):
        def on_connect(client, userdata, flags, reason_code, properties):
            self.current_player_id = str(uuid1())
            color = random_color()

            message = dumps({
                "id": self.current_player_id,
                "color": color,
                "direction": "stop"
            })

            self.mqttService.publish(message=message)

            client.subscribe(self.topic)

        def on_message(client, userdata, msg):
            player = loads(msg.payload.decode())

            if player.get("id") not in Game.player_dict:
                Game.player_dict[player.get("id")] = {
                    "color": player.get("color"),
                    "direction": player.get("direction"),
                    "in_game": False
                }
                return

            Game.player_dict[player.get("id")]["direction"] = player.get("direction")


        self.mqttService.setOnConnectHandler(on_connect)
        self.mqttService.setOnMessageHandler(on_message)

        self.mqttService.connect()

        Thread(target=self.mqttService.listen, daemon=True).start()

        while True:
            self.publish_players()
            self.generate_players()
            self.screen.update()
            self.move()
            time.sleep(self.delay)

        self.screen.mainloop()

if __name__ == "__main__":
    game = Game()
    game.start()
