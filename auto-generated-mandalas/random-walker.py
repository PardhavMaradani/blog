# https://pardhav-m.blogspot.com/2020/08/auto-generated-mandalas.html
# Auto Generated Mandalas
# Random Walker
import math
import turtle
from _slider import Slider
from _line_clip import cohensutherland
import time
import random

# global vars
g_sectors = 16
g_pensize = 1
g_mirror = 1
g_show_sectors = 1
g_color = 'black'
g_colors = ["black", "dark grey", "cornflower blue", "deep sky blue", "dark turquoise", "aquamarine", "medium sea green", "khaki", "sienna", "firebrick", "coral", "red", "crimson", "hot pink", "dark orchid", "medium slate blue"]
g_pause_for_click = False

# screen setup
g_screen = turtle.Screen()
g_wh = int(g_screen.window_height())
g_ww = int(1.5 * g_wh)
g_screen_radius = g_wh / 2
g_screen.setup(g_ww, g_wh)
g_screen.tracer(0)
g_center = [g_ww / 6, 0]
g_minx = -g_ww / 6
g_maxx = g_ww / 2
g_miny = -g_wh / 2
g_maxy = g_wh / 2

# random walker vars
g_steps_max = int(g_screen_radius)
g_magnitude_max = int(g_screen_radius * 0.08)
g_steps = int(g_steps_max / 2)
g_magnitude = int(g_magnitude_max / 2)


# internal
g_prev_ct = None
g_redraw = False
g_paused = False

# new turtle
def new_turtle():
  t = turtle.Turtle()
  t.ht()
  t.speed(0)
  return t

# sector turtle
st = new_turtle()
st.color('lightgray')
# main drawing turtle
t = new_turtle()

# draw a border
def draw_border():
  t = new_turtle()
  t.pu()
  t.goto(-g_ww/2, g_miny)
  t.pd()
  t.goto(g_ww/2, g_miny)
  t.goto(g_ww/2, g_maxy)
  t.goto(-g_ww/2, g_maxy)
  t.goto(-g_ww/2, g_miny)
  # partition
  t.color('gray')
  t.pu()
  t.goto(g_minx, g_miny)
  t.pd()
  t.goto(g_minx, g_maxy)
  t.update()

# handle slider updates
def handle_slider_update(id, value):
  global g_sectors
  global g_pensize
  global g_mirror
  global g_show_sectors
  global g_steps
  global g_magnitude
  global g_redraw
  if id == 0:
    g_sectors = value
    draw_sectors()
  elif id == 1:
    g_pensize = value
  elif id == 2:
    g_mirror = value
  elif id == 3:
    g_show_sectors = value
    draw_sectors()
  elif id == 4:
    g_steps = value
  elif id == 5:
    g_magnitude = value
  g_redraw = True

# Color button class
class ColorButton(turtle.Turtle):
  def __init__(self, x, y, color, click_callback = None):
    turtle.Turtle.__init__(self)
    self.shape('circle')
    self.speed(0)
    self.my_color = color
    self.click_callback = click_callback
    self.color(color)
    self.pu()
    self.goto(x, y)
    self.left(90)
    self.onclick(self.onclick_handler)
    self.update()
  # handle button click
  def onclick_handler(self, x, y):
    if self.click_callback:
      self.click_callback(self, self.my_color)
    self.shape('turtle')
    self.update()

# color button click handler
def handle_color_click(ct, color):
  global g_color
  global g_prev_ct
  global g_redraw
  g_prev_ct.shape('circle')
  g_prev_ct.update()
  g_color = color
  g_prev_ct = ct
  g_redraw = True

# create UI
def create_ui():
  global g_prev_ct
  x = -g_ww / 2 + 20
  y = g_wh / 2 - 20
  normal_length = g_screen_radius * 0.55
  toggle_length = g_screen_radius * 0.15
  # sliders
  Slider(0, x, y, normal_length, 1, 32, 1, g_sectors, 'sectors', handle_slider_update)
  Slider(1, x, y - 30, normal_length, 1, 16, 1, g_pensize, 'pensize', handle_slider_update)
  Slider(2, x, y - 60, toggle_length, 0, 1, 1, g_mirror, 'mirror', handle_slider_update)
  Slider(3, x, y - 90, toggle_length, 0, 1, 1, g_show_sectors, 'show_sectors', handle_slider_update)
  # color buttons
  ci = 0
  for r in range(2):
    cx = x
    cy = y - (150 + (30 * r))
    for c in range(8):
      color = g_colors[ci]
      cb = ColorButton(cx + (c * 25), cy, color, handle_color_click)
      if color == g_color:
        cb.shape('turtle')
        g_prev_ct = cb
      ci += 1
  Slider(4, x, y - 240, normal_length * 0.85, 1, g_steps_max, 10, g_steps, 'steps', handle_slider_update)
  Slider(5, x, y - 270, normal_length * 0.85, 1, g_magnitude_max, 1, g_magnitude, 'magnitude', handle_slider_update)

# draw sectors
def draw_sectors():
  st.clear()
  if g_show_sectors == 0:
    return
  sector_angle = 360 / g_sectors
  cx, cy = g_center
  for i in range(g_sectors):
    st.pu()
    st.goto(cx, cy)
    st.seth(sector_angle * (i + 1))
    st.fd(g_ww)
    (x, y) = st.pos()
    (nx1, ny1, nx2, ny2) = cohensutherland(g_minx, g_maxy, g_maxx, g_miny, cx, cy, x, y)
    if nx1 is not None:
      st.goto(nx1, ny1)
      st.pd()
      st.goto(nx2, ny2)
  st.update()

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
    if rpx < g_minx or rx < g_minx:
      return
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

# draw points
def draw_points(points):
  t.clear()
  t.pensize(g_pensize)
  t.color(g_color)
  (px, py) = points[0]
  for v in points:
    x, y = v
    draw_segment(t, px, py, x, y, g_sectors, g_mirror)
    px, py = x, y
    t.update()
    if g_redraw:
      break

# draw
def draw():
  global g_redraw
  g_redraw = False
  cx, cy = g_center
  points = []
  # px, py = 0, 0
  px = random.randint(0, int(g_screen_radius * 0.5))
  py = random.randint(0, int(g_screen_radius * 0.5))
  for i in range(g_steps):
    dx = random.randint(-g_magnitude, g_magnitude)
    dy = random.randint(-g_magnitude, g_magnitude)
    x = px + dx
    y = py + dy
    points.append((cx + x, cy + y))
    px, py = x, y
  draw_points(points)

# draw mandalas in loop
def draw_loop():
  global g_paused
  while True:
    draw()
    if g_pause_for_click and not g_redraw:
      g_paused = True
      break
    if not g_redraw:
      time.sleep(1)

# handle screen click
def handle_screen_click(x, y):
  global g_paused
  if g_pause_for_click and g_paused:
    g_paused = False
    draw_loop()

# setup
def setup():
  draw_border()
  create_ui()
  draw_sectors()
  g_screen.onclick(handle_screen_click)

# main

setup()
draw_loop()
