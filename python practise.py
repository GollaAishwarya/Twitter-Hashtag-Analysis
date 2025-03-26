import turtle
import datetime
import time
screen=turtle.Screen()
screen.tracer(0)
screen.bgcolor("black")
s=turtle.Turtle()
t=turtle.Turtle()
s.speed(0)
t.speed(0)
s.color("white")
s.hideturtle()
s.pensize(2)
s.penup()
s.goto(-200,-50)
s.pendown()
s.forward(400)
s.left(90)
s.forward(100)
s.left(90)
s.forward(400)
s.left(90)
s.forward(100)
t.color("white")
t.hideturtle()
t.penup()
t.goto(-115,-35)
t.pendown()
s=datetime.datetime.now().second
m=datetime.datetime.now().minute
hr=datetime.datetime.now().hour
while(True):
t.write(str(hr).zfill(2)+":"+str(m).zfill(2)+":"+str(s).zfill
(2),font=(("Arial", 60, "normal")))
s+=1
if s==60:
s=0
m+=1
if m==60:
m=0
hr+=1
if hr==13:b v                                                                      
hr=1
time.sleep(1)
screen.update()
t.undo()