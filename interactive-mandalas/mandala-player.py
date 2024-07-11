# https://pardhav-m.blogspot.com/2020/07/interactive-mandalas.html
# Interactive Mandalas
# Mandala Player
import json
import math
import turtle
import time

# screen setup
g_screen = turtle.Screen()
g_wh = int(g_screen.window_height())
g_ww = int(1.5 * g_wh)
g_screen_radius = g_wh / 2
g_screen.setup(g_ww, g_wh)
g_screen.tracer(0)
g_center = (0, 0)

# new turtle
def new_turtle():
  t = turtle.Turtle()
  t.ht()
  t.speed(0)
  return t

# main drawing turtle
t = new_turtle()

# draw a border
def draw_border():
  t = new_turtle()
  t.pu()
  t.goto(-g_ww/2, -g_wh / 2)
  t.pd()
  t.goto(g_ww/2, -g_wh / 2)
  t.goto(g_ww/2, g_wh / 2)
  t.goto(-g_ww/2, g_wh / 2)
  t.goto(-g_ww/2, -g_wh / 2)
  t.update()

# rotate point
def rotate_point(x, y, angle):
  cx, cy = g_center
  x -= cx
  y -= cy
  sin = math.sin(math.radians(angle))
  cos = math.cos(math.radians(angle))
  rx = cx + (x * cos - y * sin)
  ry = cy + (x * sin + y * cos)
  return (rx, ry)

# angle of point wrt center
def point_angle(x, y):
  cx, cy = g_center
  return math.degrees(math.atan2(y - cy, x - cx))

# draw line between two points
def draw_line(t, px, py, x, y, angle):
  (rpx, rpy) = rotate_point(px, py, angle)
  (rx, ry) = rotate_point(x, y, angle)
  t.pu()
  t.goto(rpx, rpy)
  t.pd()
  t.goto(rx, ry)

# draw line segment
def draw_segment(t, px, py, x, y, sectors, mirror):
  sector_angle = 360 / sectors
  h_sector_angle = sector_angle / 2
  for i in range(sectors):
    draw_line(t, px, py, x, y, sector_angle * i)
    if mirror == 1:
      pa = point_angle(px, py) % sector_angle
      pma = h_sector_angle - pa
      (rpx, rpy) = rotate_point(px, py, 2 * pma)
      a = point_angle(x, y) % sector_angle
      ma = h_sector_angle - a
      (rx, ry) = rotate_point(x, y, 2 * ma)
      if abs(pma - ma) > h_sector_angle:
        continue
      draw_line(t, rpx, rpy, rx, ry, sector_angle * i)

# draw
def draw(path):
  state, points = path
  pensize = state["pensize"]
  color = state["color"]
  sectors = state["sectors"]
  mirror = state["mirror"]
  t.pensize(pensize)
  t.color(color)
  (px, py) = points[0]
  for v in points:
    x, y = v
    draw_segment(t, px, py, x, y, sectors, mirror)
    px, py = x, y
    # time.sleep(0.01)
    t.update()

# map points to our window size
def map_points(points, center, radius):
  output = []
  cx, cy = center
  my_cx, my_cy = g_center
  for point in points:
    x, y = point
    nx = (x - cx) / radius
    ny = (y - cy) / radius
    my_x = (nx * g_screen_radius) + my_cx
    my_y = (ny * g_screen_radius) + my_cy
    output.append([my_x, my_y])
  return output

# display mandalas in a loop
def play():
  global g_state
  global g_points
  # read from data file
  file = open("data.txt", "r")
  lines = file.readlines()
  file.close()
  # convert to this screen coordinates
  mandalas = []
  for line in lines:
    if len(line) < 2 or line[0:1] == '#':
      continue
    paths = json.loads(line)
    my_paths = []
    for path in paths:
      state, points = path
      points = map_points(points, state["center"], state["radius"])
      my_paths.append([state, points])
    mandalas.append(my_paths)
  # draw all mandalas in a loop  
  while True:
    for mandala in mandalas:
      for path in mandala:
        draw(path)
      time.sleep(1)
      t.clear()

# main

draw_border()
play()
