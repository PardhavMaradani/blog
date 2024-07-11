# https://pardhav-m.blogspot.com/2020/06/trees.html
# Trees
# Basic Trees
import turtle
import random

seed = random.randrange(65536)
random.seed(seed)

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

# draw a border
def draw_border():
  t.pu()
  t.goto(-ww/2, -wh/2)
  t.pd()
  t.goto(ww/2, -wh/2)
  t.goto(ww/2, wh/2)
  t.goto(-ww/2, wh/2)
  t.goto(-ww/2, -wh/2)

# draw simple tree
# Adapted from https://programmer.help/blogs/5de68666adfb1.html
def tree(branch):
  if branch <= 3:
    return
  # set color and pensize
  color = 'black'
  size = 0
  if 8 <= branch <= 12:
    if random.randint(0, 2) == 0:
      color = 'snow'
    else:
      color = 'lightcoral'
      size = branch / 3
  elif branch < 8:
    if random.randint(0, 1) == 0:
      color = 'snow'
    else:
      color = 'lightcoral'
      size = branch / 2
  else:
    color = 'sienna'
    size = branch / 10
  t.color(color)
  t.pensize(size)
  # calculate angles and lengths
  a = 1.5 * random.random()
  b = 1.5 * random.random()
  la = 20 * a
  new_branch = branch - (10 * b)
  # draw left tree
  t.fd(branch)
  t.left(la)
  tree(new_branch)
  # draw right tree
  t.right(2 * la)
  tree(new_branch)
  # return back to original position
  t.left(la)
  t.pu()
  t.bk(branch)
  t.pd()

# main

# draw border
draw_border()

# set tree base
t.left(90)
t.pu()
t.goto(0, -wh/2 + (wh * 0.05))
t.pd()

# draw tree
start_branch = screen_radius * 0.20
tree(start_branch)

# print seed
t.pu()
t.color('black')
t.right(90)
t.fd(screen_radius * 0.05)
t.pd()
t.write(seed)

t.update()
