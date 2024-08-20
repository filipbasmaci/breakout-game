import time
from turtle import Screen, Turtle
import random

STARTING_POSITION = (0, -550)
LEFT_LIMIT = -600
RIGHT_LIMIT = 560

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.color("white")
        self.shape("circle")
        self.shapesize(1.25)
        self.move_speed = 0.015
        self.x_move = 5
        self.y_move = 5
        self.reset_position()

    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_wall(self):
        self.x_move *= -1

    def bounce_ceiling(self):
        self.y_move *= -1

    def bounce_brick(self, is_side):
        if is_side:
            self.x_move *= -1
        else:
            self.y_move *= -1

    def reset_position(self):
        self.goto(0, -526)
        self.y_move = abs(self.y_move)


    def reset_speed(self):
        self.move_speed = 0.015


class Pong(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.penup()
        self.speed("fastest")
        self.color("white")
        self.shapesize(stretch_wid=7, stretch_len=1)
        self.setposition(STARTING_POSITION)
        self.setheading(90)

    def go_right(self):
        new_x = self.xcor() + 40
        if new_x <= RIGHT_LIMIT:
            self.goto(new_x, self.ycor())

    def go_left(self):
        new_x = self.xcor() - 40
        if new_x >= LEFT_LIMIT:
            self.goto(new_x, self.ycor())


class Brick(Turtle):
    def __init__(self, position):
        super().__init__()
        self.penup()
        self.shape("square")
        self.color("blue")
        self.shapesize(stretch_wid=1, stretch_len=4)
        self.goto(position)


def create_bricks():
    bricks = []
    x_start = -580
    y_start = 300
    for row in range(5):
        for col in range(14):
            brick_position = (x_start + col * 90, y_start - row * 30)
            brick = Brick(brick_position)
            bricks.append(brick)
    return bricks


screen = Screen()
screen.setup(width=1280, height=1280)
screen.tracer(0)
screen.bgcolor("black")

pong = Pong()
ball = Ball()
bricks = create_bricks()

screen.update()
screen.listen()

screen.onkeypress(pong.go_right, "Right")
screen.onkeypress(pong.go_left, "Left")


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.color("white")
        self.hideturtle()
        self.score = 0
        self.lives = 3
        self.update_score()

    def update_score(self):
        self.clear()
        self.goto(-630, 550)
        self.write(f"Score: {self.score}", font=("Courier", 30, "normal"))
        self.goto(400, 550)
        self.write(f"Lives: {self.lives}", font=("Courier", 30, "normal"))

    def point(self):
        self.score += 10
        self.update_score()

    def decrease_life(self):
        self.lives -= 1
        self.update_score()

    def game_over(self):
        self.goto(-100,0)
        self.write(f"GAME OVER", font=("Courier", 30, "normal"))

    def you_win(self):
        self.goto(-90,0)
        self.write(f"YOU WIN!", font=("Courier", 30, "normal"))


scoreboard = Scoreboard()


def check_collision():
    for brick in bricks:
        if ball.distance(brick) < 40:
            if brick.ycor() - 2 < ball.ycor() < brick.ycor() + 2:
                ball.bounce_brick(is_side=True)
            else:
                ball.bounce_brick(is_side=False)
            brick.hideturtle()
            bricks.remove(brick)
            scoreboard.point()
            ball.move_speed -= 0.001


GAME_IS_ON = True

while GAME_IS_ON:
    ball.move()
    time.sleep(ball.move_speed)
    screen.update()

    if ball.xcor() >= 620 or ball.xcor() <= -620:
        ball.bounce_wall()

    if ball.ycor() >= 620:
        ball.bounce_ceiling()

    if ball.ycor() <= -530 and ball.distance(pong) <= 70:
        ball.bounce_ceiling()

    check_collision()

    if ball.ycor() <= -630:
        scoreboard.decrease_life()
        if scoreboard.lives > 0:
            time.sleep(1)
            ball.reset_position()
            ball.reset_speed()
        else:
            GAME_IS_ON = False
            scoreboard.game_over()

    if len(bricks) == 0:
        scoreboard.you_win()

screen.mainloop()
