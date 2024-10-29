import turtle
import time

delay = 0.01

# Pontuação
score = 0
high_score = 0

# Configura a tela
wn = turtle.Screen()
wn.title("Move Game by @Garrocho")
wn.bgcolor("green")
wn.setup(width=1.0, height=1.0)  
wn.tracer(0)  
screen_width = wn.window_width() // 2  
screen_height = wn.window_height() // 2

# Jogador 1
head = turtle.Turtle()
head.speed(0)
head.shape("circle")
head.color("red")
head.penup()
head.goto(0, 0)
head.direction = "stop"

#jogador 2
#head = turtle.Turtle()
#head.speed(0)
#head.shape("square")
#head.color("blue")
#head.penup
#head.goto(0, 0)
#head.direction = "stop"

# Funções de controle
def go_up():
    head.direction = "up"

def go_down():
    head.direction = "down"

def go_left():
    head.direction = "left"

def go_right():
    head.direction = "right"

def close():
    wn.bye()

def move():
    if head.direction == "up":
        y = head.ycor()
        if y < screen_height - 10:  
            head.sety(y + 5)

    if head.direction == "down":
        y = head.ycor()
        if y > -screen_height + 10:  
            head.sety(y - 5)

    if head.direction == "left":
        x = head.xcor()
        if x > -screen_width + 10:  
            head.setx(x - 5)

    if head.direction == "right":
        x = head.xcor()
        if x < screen_width - 10:  
            head.setx(x + 5)

# Mapeamento do teclado
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
wn.onkeypress(close, "Escape")

# Loop principal do jogo
while True:
    wn.update()
    move()
    time.sleep(delay)

wn.mainloop()
