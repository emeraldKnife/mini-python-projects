import turtle
import time
from snake import Snake
from food import Food
from scoreboard import Scoreboard

sc = turtle.Screen()
sc.setup(width = 600, height = 600)
sc.bgcolor("black")
sc.title("snake_game")
sc.tracer(0)

snake = Snake()
food = Food()
scoreboard = Scoreboard()

game_on = True

sc.listen()
sc.onkey(snake.up, "Up")
sc.onkey(snake.down, "Down")
sc.onkey(snake.left, "Left")
sc.onkey(snake.right, "Right")


while game_on:
    time.sleep(0.11)
    snake.move()

    if snake.head.distance(food) < 15:
        food.refresh()
        snake.grow(1)
        scoreboard.increase_score(1)
        scoreboard.clear()
        scoreboard.update_scoreboard()
    
    if snake.head.xcor() > 290 or snake.head.ycor() > 290 or snake.head.xcor() < -290 or snake.head.ycor() < -290:
        game_on = False
        scoreboard.game_over()

    for tim in snake.tims[1:]:
        if snake.head.distance(tim) < 10:
            game_on = False
            scoreboard.game_over()

    sc.update()

sc.exitonclick()