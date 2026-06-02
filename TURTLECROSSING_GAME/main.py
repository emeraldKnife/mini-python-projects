import turtle
import random
import time
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

screen = turtle.Screen()
screen.setup(width = 600, height = 600)
screen.tracer(0)

tim = Player()
scoreboard = Scoreboard()

screen.listen()

screen.onkey(tim.move, "Up")

game_on = True
counter = 0
cars = []

while game_on:
    time.sleep(0.01)
    screen.update()
    scoreboard.update_scoreboard()

    if tim.finish():
        scoreboard.increase_level(1)
        scoreboard.update_scoreboard()
    
    if scoreboard.level == 4:
        scoreboard.game_over_s()
        game_on = False

    counter += 1
    if counter == 50:
        counter = 0
        car = CarManager((300, random.randrange(-250, 250)))
        cars.append(car)

    for car in cars:
        if car.xcor() < -290:
            car.hideturtle()
            cars.remove(car)
            continue

        if car.xcor() < 30:
            if tim.distance(car) < 20:
                scoreboard.game_over_f()
                game_on = False
        elif car.xcor() > 30:
            if tim.distance(car) < 35:
                scoreboard.game_over_f()
                game_on = False
        
        car.move(scoreboard.level)
        scoreboard.percent = (tim.ycor() + 250) / 5

screen.exitonclick()