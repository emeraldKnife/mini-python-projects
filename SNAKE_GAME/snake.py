import turtle

INITIAL_NUMBER_OF_BLOCKS = 3
INITIAL_POSITION_OF_HEAD = (0, 0)
MOVE_DISTANCE = 20
HEAD = 0

class Snake:
    def __init__(self):
        self.tims = []
        self.create_snake()
        self.head = self.tims[HEAD]

    def create_snake(self):
        for i in range(INITIAL_NUMBER_OF_BLOCKS):
            tim = turtle.Turtle()
            tim.shape("square")
            tim.color("white")
            tim.penup()
            tim.goto(INITIAL_POSITION_OF_HEAD[0] - (i * 20), INITIAL_POSITION_OF_HEAD[1])
            self.tims.append(tim)

    def move(self):
        for i in range(len(self.tims) - 1, 0, -1):
            new_x = self.tims[i - 1].xcor()
            new_y = self.tims[i - 1].ycor()
            self.tims[i].goto(new_x, new_y)
        self.tims[HEAD].forward(MOVE_DISTANCE)

    def up(self):
        if self.tims[HEAD].heading() != 270:
            self.tims[HEAD].setheading(90)
    
    def down(self):
        if self.tims[HEAD].heading() != 90:
            self.tims[HEAD].setheading(270)

    def left(self):
        if self.tims[HEAD].heading() != 0:
            self.tims[HEAD].setheading(180)

    def right(self):
        if self.tims[HEAD].heading() != 180:
            self.tims[HEAD].setheading(0)

    def grow(self, count):
        for i in range(count):
            tim = turtle.Turtle()
            tim.shape("square")
            tim.color("white")
            tim.penup()
            x_1 = self.tims[-1].xcor()
            y_1 = self.tims[-1].ycor()
            x_2 = self.tims[-2].xcor()
            y_2 = self.tims[-2].ycor()
            tim.goto((2 * x_1) - x_2, (2 * y_1) - y_2)
            self.tims.append(tim)