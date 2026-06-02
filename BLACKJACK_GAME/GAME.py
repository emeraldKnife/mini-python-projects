import random

draw="Y"
cards=[11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
compCard=[0]*25
playerCard=[0]*25
playerCount=0
compCount=0
playerCard[0]=random.choice(cards)
playerCount+=1
playerCard[playerCount]=random.choice(cards)
playerCount+=1
compCard[0]=random.choice(cards)
compCount+=1
while(True):
    sumComp=0
    sumPlayer=0
    print("COMPUTER CARD:", compCard)
    print("PLAYER CARD:", playerCard)
    for i in compCard:
        sumComp+=i
    for i in playerCard:
        sumPlayer+=i
    print("SUM OF COMPUTER:", sumComp)
    print("SUM OF PLAYER:", sumPlayer)
    if(sumPlayer>21):
        print("YOU LOSE, CROSSED 21!!!")
        break
    draw=input("DO YOU WANT ONE MORE CARD? Y:N\n")
    if(draw=='Y'):
        playerCard[playerCount]=random.choice(cards)
        playerCount+=1
    if(draw=='N'):
        compCard[compCount]=random.choice(cards)
        compCount+=1
        print("COMPUTER CARD:", compCard)
        sumComp=0
        for i in compCard:
            sumComp+=i
        if(sumComp>21):
            print("YOU WIN!!!")
        if(sumPlayer>sumComp):
            print("YOU WIN!!!")
        if(sumPlayer==sumComp):
            print("THATS A DRAW!!!")
        if(sumPlayer<sumComp):
            print("YOU LOSE!!!")
        break