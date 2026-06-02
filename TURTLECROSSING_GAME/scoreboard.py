import turtle

ALIGNMENT = "center"
FONT = ("Courier", 24, "normal")

class Scoreboard(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.level = 1
        self.percent = 0
        self.color("black")
        self.penup()
        self.goto(-220, 220)
        self.hideturtle()
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(f"LEVEL: {self.level}\n{self.percent}%", align = ALIGNMENT, font = FONT)

    def game_over_f(self):
        self.goto(0, 0)
        self.write(f"GAME OVER", align = ALIGNMENT, font = FONT)

    def increase_level(self, count):
        self.level += count

    def game_over_s(self):
        self.goto(0, 0)
        self.write(f"CONGRATULATIONS", align = ALIGNMENT, font = FONT)