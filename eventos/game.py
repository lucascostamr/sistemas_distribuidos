import turtle
import time

from MqttService import MqttService

class Game:
    def __init__(self):
        self.mqttService = MqttService()
        self.ball_list = []
        self.currentPlayer = None

        self.create_screen()

    def create_screen(self):
        screen = turtle.Screen()
        screen.title("Move Game by @Garrocho")
        screen.bgcolor("green")
        screen.setup(width=1.0, height=1.0, startx=None, starty=None)
        screen.tracer(0) # Turns off the screen updates
        self.screen = screen

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected with result code " + str(reason_code))

    ip = "123"
    color = "red"

    ball = turtle.Turtle()
    ball.speed(0)
    ball.shape("circle")
    ball.color("red")
    ball.penup()
    ball.goto(0,0)
    ball.direction = "stop"

    player = {
        ip: {
            "ball": ball,
            "color": color
        }
    }

    ball_list.append(player)

    client.subscribe("/data")

mqttService.setOnConnectHandler(on_connect)
mqttService.connect()

print(ball_list)


# gamer 1
for key, value in ball_list:
    if key == "123":
        currentPlayer = value.ball
mqttService.listen("/data")
# Functions
def go_up():
    currentPlayer.direction = "up"

def go_down():
    currentPlayer.direction = "down"

def go_left():
    currentPlayer.direction = "left"

def go_right():
    currentPlayer.direction = "right"

def close():
    wn.bye()

def move():
    if currentPlayer.direction == "up":
        y = currentPlayer.ycor()
        currentPlayer.sety(y + 2)

    if currentPlayer.direction == "down":
        y = currentPlayer.ycor()
        currentPlayer.sety(y - 2)

    if currentPlayer.direction == "left":
        x = currentPlayer.xcor()
        currentPlayer.setx(x - 2)

    if currentPlayer.direction == "right":
        x = currentPlayer.xcor()
        currentPlayer.setx(x + 2)

# Keyboard bindings
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
wn.onkeypress(close, "Escape")


# Main game loop
while True:

    wn.update()
    move()
    time.sleep(delay)


wn.mainloop()
