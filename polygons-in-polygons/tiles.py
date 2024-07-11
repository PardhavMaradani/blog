# https://pardhav-m.blogspot.com/2020/05/polygons-in-polygons.html
# Polygons in polygons
# Tiles
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

# shape radius from https://www.mathsisfun.com/geometry/regular-polygons.html
def shape_radius(sides, length):
  return length / (2 * math.sin(math.pi / sides))

# shape apothem from https://www.mathsisfun.com/geometry/regular-polygons.html
def shape_apothem(sides, length):
  return shape_radius(sides, length) * math.cos(math.pi / sides)

# draw regular polygon
# sides  - number of sides
# cx, cy - center around which to draw this polygon
# length - length of each side
# xangle - angle this polygon wrt x axis
def draw_polygon(sides, cx, cy, length, xangle):
  radius = shape_radius(sides, length)
  t.pu()
  t.goto(cx, cy)
  t.seth(270)  # point down
  t.right(math.degrees(math.pi / sides))
  t.fd(radius)
  sx, sy = t.pos()  # left most starting point
  # get the rotated starting point
  # see https://stackoverflow.com/questions/2259476/rotating-a-point-about-another-point-2d
  sx -= cx
  sy -= cy
  s = math.sin(math.radians(xangle))
  c = math.cos(math.radians(xangle))
  rsx = cx + (sx * c - sy * s)
  rsy = cy + (sx * s + sy * c)
  t.goto(rsx, rsy)  # goto rotated starting point
  t.seth(xangle)  # rotate turtle to start angle
  t.pd()
  # draw each side
  for s in range(sides):
    t.fd(length)
    t.left(360 / sides)
  t.pu()
  t.goto(cx, cy)
  t.seth(0)
  t.pd()

# draw rotated polygons within a regular polygon (spirals)
# see parameters to draw_polygon
# levels - number of levels to draw inside
# direction - clockwise or anti-clockwise (1 or -1)
def draw_polygon_spiral(sides, cx, cy, length, levels, xangle, direction):
  delta = 10  # spacing
  # calculate common angle to rotate and reducing factor
  nt = turtle.Turtle()
  nt.speed(0)
  nt.ht()
  nt.pu()
  nt.fd(delta)
  x1, y1 = nt.pos()  # first point
  nt.fd(length - delta)
  nt.left(360 / sides)
  nt.fd(delta)
  x2, y2 = nt.pos()  # second point
  nt.goto(x1, y1)
  # angle between the two points wrt x axis
  # can also use math.atan2(xdelta, ydelta)
  rangle = nt.towards(x2, y2)
  # distance between the two points
  # can also use math.sqrt(xdelta*xdelta + ydelta*ydelta)
  new_len = nt.distance(x2, y2)
  # factor by which distance reduces each level
  reducing_factor =  new_len / length

  # draw each level
  for level in range(levels):
    # 'rangle * level' increases the common angle for each level
    # 'xangle + ' ensures it stays rotated wrt x axis angle
    # 'direction' - multiplying by 1 or -1 changes the direction
    draw_polygon(sides, cx, cy, length, (xangle + (rangle * level)) * direction)
    length = length * reducing_factor  # reduce length each time

# get a point radius distance from cx, cy with angle
def get_mini_shape_center(cx, cy, radius, angle):
  nt = turtle.Turtle()
  nt.speed(0)
  nt.ht()
  nt.up()
  nt.goto(cx, cy)
  nt.seth(0)
  nt.left(angle)
  nt.fd(radius)
  return nt.pos()

# draw a tile comprising of a set of polygon spirals
# pattern has angle and directions eg: [(0, 1), (0, 1), (0, 1), (0, 1)]
def draw_tile(sides, cx, cy, length, pattern):
  radius = shape_radius(sides, length)
  sa = 360 / (2 * len(pattern))
  for i in range(len(pattern)):
    ra = sa + (i * 2 * sa)
    (mcx, mcy) = get_mini_shape_center(cx, cy, radius, ra)
    (angle, direction) = pattern[i]
    draw_polygon_spiral(sides, mcx, mcy, length, levels, angle, direction)

# main

draw_border()

length = screen_radius / 3
levels = 20

sq_pattern1 = [(0, 1), (0, 1), (0, 1), (0, 1)]
sq_pattern2 = [(0, -1), (0, 1), (0, -1), (0, 1)]
tri_pattern1 = [(0, -1), (180, 1), (0, -1), (180, 1), (0, -1), (180, 1)]
tri_pattern2 = [(0, 1), (180, 1), (0, 1), (180, 1), (0, 1), (180, 1)]
 
draw_tile(3, -(ww/10 + ww/5), 0, length, tri_pattern1)
draw_tile(3, -ww/10, 0, length, tri_pattern2)
draw_tile(4, ww/10, 0, length, sq_pattern1)
draw_tile(4, (ww/10 + ww/5), 0, length, sq_pattern2)

t.update()
