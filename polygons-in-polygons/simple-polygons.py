# https://pardhav-m.blogspot.com/2020/05/polygons-in-polygons.html
# Polygons in polygons
# Simple polygons
import turtle
import math

screen = turtle.Screen()
wh = screen.window_height()  # window height
ww = 2 * wh                  # window width
# trinket returns the same window width and height (hence square)
# set it to a rectangular area
screen.setup(ww, wh)
screen_radius = wh / 2

t = turtle.Turtle()
t.speed(0)

# draw a border
def draw_border():
  t.pu()
  t.goto(-ww/2, -wh/2)
  t.pd()
  t.goto(ww/2, -wh/2)
  t.goto(ww/2, wh/2)
  t.goto(-ww/2, wh/2)
  t.goto(-ww/2, -wh/2)

# shape radius from https://www.mathsisfun.com/geometry/regular-polygons.html
def shape_radius(sides, length):
  return length / (2 * math.sin(math.pi / sides))

# draw regular polygon
# sides  - number of sides
# cx, cy - center around which to draw this polygon
# length - length of each side
def draw_polygon(sides, cx, cy, length):
  radius = shape_radius(sides, length)
  t.pu()
  t.goto(cx, cy)
  t.seth(270)  # point down
  t.right(math.degrees(math.pi / sides))
  t.fd(radius)
  t.seth(0)
  sx, sy = t.pos()  # left most starting point
  t.pd()
  # draw each side
  for s in range(sides):
    t.fd(length)
    t.left(360 / sides)
  t.pu()
  t.goto(cx, cy)
  t.seth(0)
  t.pd()

# main

draw_border()

length = screen_radius / 2

draw_polygon(3, -ww/4, 0, length) 
draw_polygon(4, 0, 0, length) 
draw_polygon(5, ww/4, 0, length) 
