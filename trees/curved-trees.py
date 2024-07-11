# https://pardhav-m.blogspot.com/2020/06/trees.html
# Trees
# Curved Trees
import turtle
import random
import math
import time

seed = random.randrange(65536)
random.seed(seed)

# percent of line length to curve
curve_percent = 0.25

screen = turtle.Screen()
wh = screen.window_height()  # window height
ww = 1.5 * wh                # window width
# trinket returns the same window width and height (hence square)
# set it to a rectangular area
screen.setup(ww, wh)
screen_radius = wh / 2

t = turtle.Turtle()
t.ht()
t.speed(0)
t.tracer(0)

# draw please wait
def draw_please_wait():
  t.pu()
  t.goto(-ww/2 + 20, wh/2 - 40)
  t.pd()
  t.write("Please wait...", font=("Arial", 16, "normal"))
  t.update()
  time.sleep(0.001)
  t.clear()

# draw a border
def draw_border():
  t.pu()
  t.goto(-ww/2, -wh/2)
  t.pd()
  t.goto(ww/2, -wh/2)
  t.goto(ww/2, wh/2)
  t.goto(-ww/2, wh/2)
  t.goto(-ww/2, -wh/2)


# draw curved line
# fl - length of straight line (t.fd)
# cl - length of curved line (t.circle)
# angle - angle between the lines
def draw_curved_line(fl, cl, angle):
  radius = cl * math.tan(math.radians(angle / 2))
  angle = 180 - angle
  if angle < 0:
    angle *= -1
  t.fd(fl)
  t.circle(radius, angle)

# save current state
# color - current color
# pensize - current pensize
def save_state(color, pensize):
  return t.pos(), t.heading(), color, pensize

# restore given state
def restore_state(state):
  pos, heading, color, pensize = state
  t.pu()
  t.setpos(pos)
  t.seth(heading)
  t.color(color)
  t.pensize(pensize)
  t.pd()

# draw curved tree
# branch - lenght of branch
# pcl - previous curve length
def tree(branch, pcl):
  if branch <= 3:
    return
  # set color and pensize
  color = 'black'
  pensize = 0
  if 8 <= branch <= 12:
    if random.randint(0, 2) == 0:
      color = 'snow'
    else:
      color = 'lightcoral'
      pensize = branch / 3
  elif branch < 8:
    if random.randint(0, 1) == 0:
      color = 'snow'
    else:
      color = 'lightcoral'
      pensize = branch / 2
  else:
    color = 'sienna'
    pensize = branch / 10
  t.color(color)
  t.pensize(pensize)
  # calculate angles and lengths
  a = 1.5 * random.random()
  b = 1.5 * random.random()
  la = 20 * a
  new_branch = branch - (10 * b)
  cl = branch * curve_percent
  fl = branch - cl - pcl
  # save current state
  state = save_state(color, pensize)
  # draw left curve
  draw_curved_line(fl, cl, 180 - la)
  # draw left tree
  tree(new_branch, cl)
  restore_state(state)
  # draw right curve
  draw_curved_line(fl, cl, 180 + la)
  # draw right tree
  tree(new_branch, cl)
  restore_state(state)

# main

draw_please_wait()
draw_border()

# set tree base
t.left(90)
t.pu()
t.goto(0, -wh/2 + (wh * 0.05))
t.pd()

# draw tree
start_branch = screen_radius * 0.20

tree(start_branch, 0)

# print seed
t.pu()
t.color('black')
t.right(90)
t.fd(screen_radius * 0.05)
t.pd()
t.write(seed)

t.update()
