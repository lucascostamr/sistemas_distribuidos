import time
from turtle import Screen, Turtle

from MqttService import MqttService
from utils import random_color


class Game:
    def __init__(self):
        self.currentPlayer = None
        self.screen_width = None
        self.screen_height = None

        self.delay = 0.01
        self.mqttService = MqttService()
        self.player_list = {}
        self.screen = self.create_screen()
        self.bind_keys()
        self.create_player()

    def create_screen(self) -> Screen:
        screen = Screen()
        screen.title("Move Game by @Garrocho")
        screen.bgcolor("green")
        screen.setup(width=1.0, height=1.0, startx=None, starty=None)
        screen.tracer(0)

        self.screen_width = screen.window_width() // 2
        self.screen_height = screen.window_height() //2

        return screen

    def create_player(self):
        player = Turtle()
        player.speed(0)
        player.shape("turtle")
        player.color(random_color())
        player.penup()
        player.goto(0,0)
        player.direction = "stop"

        self.currentPlayer = player

    def go_up(self):
        self.currentPlayer.direction = "up"

    def go_down(self):
        self.currentPlayer.direction = "down"

    def go_left(self):
        self.currentPlayer.direction = "left"

    def go_right(self):
        self.currentPlayer.direction = "right"

    def close(self):
        self.screen.bye()

    def move(self):
        if self.currentPlayer.direction == "up":
            y = self.currentPlayer.ycor()
            if y < self.screen_height - 10:
                self.currentPlayer.sety(y + 2)

        if self.currentPlayer.direction == "down":
            y = self.currentPlayer.ycor()
            if y > -self.screen_height + 10:
                self.currentPlayer.sety(y - 2)

        if self.currentPlayer.direction == "left":
            x = self.currentPlayer.xcor()
            if x > -self.screen_width + 10:
                self.currentPlayer.setx(x - 2)

        if self.currentPlayer.direction == "right":
            x = self.currentPlayer.xcor()
            if x < self.screen_width - 10:
                self.currentPlayer.setx(x + 2)

    def bind_keys(self):
        self.screen.listen()
        self.screen.onkeypress(self.go_up, "w")
        self.screen.onkeypress(self.go_down, "s")
        self.screen.onkeypress(self.go_left, "a")
        self.screen.onkeypress(self.go_right, "d")
        self.screen.onkeypress(self.close, "Escape")

    def start(self):
        while True:
            self.screen.update()
            self.move()
            time.sleep(self.delay)

        self.screen.mainloop()

if __name__ == "__main__":
    game = Game()
    game.start()