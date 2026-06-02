import turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 1
MOVE_INCREMENT = 3


class CarManager(turtle.Turtle):
    def __init__(self, pos):
        super().__init__()
        self.color(random.choice(COLORS))
        self.shape("square")
        self.penup()
        self.setheading(180)
        self.shapesize(1, 2)
        self.goto(pos)

    def move(self, level):
        self.forward(STARTING_MOVE_DISTANCE + (level * MOVE_INCREMENT))