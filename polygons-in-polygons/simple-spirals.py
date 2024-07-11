# https://pardhav-m.blogspot.com/2020/05/polygons-in-polygons.html
# Polygons in Polygons
# Simple Spirals
import turtle

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

# draw simple spiral
def draw_simple_spiral(sides, cx, cy, length):
  t.pu()
  t.goto(cx, cy)
  t.pd()
  angle = 360 / sides
  for i in range(25):
    t.fd(length + i * 5)
    t.left(angle + 3)

# main

draw_border()

length = screen_radius / 10

draw_simple_spiral(3, -ww/4, 0, length)
draw_simple_spiral(4, 0, 0, length)
draw_simple_spiral(5, ww/4, 0, length)
