# https://pardhav-m.blogspot.com/2020/07/interactive-mandalas.html
# Interactive Mandalas
# Mandala Creator
import json
import math
import turtle
from _slider import Slider
from _line_clip import cohensutherland

# global vars
g_sectors = 8
g_pensize = 1
g_mirror = 0
g_show_sectors = 1
g_color = 'black'
g_colors = ["black", "dark grey", "cornflower blue", "deep sky blue", "dark turquoise", "aquamarine", "medium sea green", "khaki", "sienna", "firebrick", "coral", "red", "crimson", "hot pink", "dark orchid", "medium slate blue"]
g_show_save = False

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

# internal
g_undo_available = True
g_clicked = False
g_dragging = False
g_points = []
g_state = {}
[g_px, g_py] = [None, None]
g_prev_ct = None
g_save_data = []

# new turtle
def new_turtle():
  t = turtle.Turtle()
  t.ht()
  t.speed(0)
  return t

# sector turtle
st = new_turtle()
st.color('lightgray')
# undo turtle
ut = new_turtle()
# main drawing turtles
dt1 = new_turtle() # primary
dt2 = new_turtle() # secondary

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
  g_prev_ct.shape('circle')
  g_prev_ct.update()
  g_color = color
  g_prev_ct = ct

# set undo button state
def set_undo_state(available):
  global g_undo_available
  color = 'black' if available else 'lightgray'
  ut.color(color)
  g_undo_available = available
  ut.update()

# handle undo button click
def handle_undo(x, y):
  global g_points
  g_points = []
  dt2.clear()
  dt2.update()
  set_undo_state(False)

# setup undo button
def setup_undo_button(x, y):
  ut.shape('circle')
  ut.pu()
  ut.goto(x + 20, y - 4)
  ut.write('Undo', font=("Arial", 10, "normal"))
  ut.goto(x, y)
  ut.onclick(handle_undo)
  ut.st()
  set_undo_state(False)

# clear button click handler
def handle_clear(x, y):
  global g_save_data
  global g_points
  g_points = []
  g_save_data = []
  dt1.clear()
  dt1.update()
  dt2.clear()
  dt2.update()
  set_undo_state(False)

# save button click handler
def handle_save(x, y):
  if len(g_points) == 0:
    return
  g_save_data.append([g_state, g_points])
  file = open("data.txt", "a")
  ds = json.dumps(str(g_save_data))[1:-1]
  ds = ds.replace('\'', '"') + '\n'
  file.write(ds)
  file.close()

# simple button
def setup_button(x, y, name, handler):
  t = new_turtle()
  t.shape('circle')
  t.pu()
  t.goto(x + 20, y - 4)
  t.write(name, font=("Arial", 10, "normal"))
  t.goto(x, y)
  t.onclick(handler)
  t.st()

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
      if ci == 0:
        cb.shape('turtle')
        g_prev_ct = cb
      ci += 1
  # undo, clear and save buttons
  setup_undo_button(x, y - 240)
  setup_button(x, y - 270, 'Clear', handle_clear)
  if g_show_save:
    setup_button(x, y - 300, 'Save', handle_save)

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
def draw_segment(t, px, py, x, y):
  sector_angle = 360 / g_state["sectors"]
  h_sector_angle = sector_angle / 2
  for i in range(g_state["sectors"]):
    draw_line(t, px, py, x, y, sector_angle * i)
    if g_state["mirror"] == 1:
      pa = point_angle(px, py) % sector_angle
      pma = h_sector_angle - pa
      (rpx, rpy) = rotate_point(px, py, 2 * pma)
      a = point_angle(x, y) % sector_angle
      ma = h_sector_angle - a
      (rx, ry) = rotate_point(x, y, 2 * ma)
      if abs(pma - ma) > h_sector_angle:
        continue
      draw_line(t, rpx, rpy, rx, ry, sector_angle * i)

# update primary turtle
def update_dt1():
  dt1.pensize(g_state["pensize"])
  dt1.color(g_state["color"])
  (px, py) = g_points[0]
  for v in g_points:
    x, y = v
    draw_segment(dt1, px, py, x, y)
    px, py = x, y
  dt1.update()
  if g_show_save:
    g_save_data.append([g_state, g_points])

# click handler
def handle_click(x, y):
  global g_points
  global g_state
  global g_clicked
  global g_px
  global g_py
  if g_clicked:
    return
  if len(g_points) > 0:
    update_dt1()
  g_clicked = True
  g_state = {
    "sectors": g_sectors,
    "pensize": g_pensize,
    "mirror": g_mirror,
    "color": g_color,
    "center": g_center,
    "radius": g_screen_radius
  }
  g_points = []
  g_points.append([x, y])
  (g_px, g_py) = (x, y)
  dt2.reset()
  dt2.ht()
  dt2.pensize(g_pensize)
  dt2.color(g_color)
  dt2.pu()
  dt2.goto(x, y)
  dt2.pd()
  set_undo_state(False)
  dt2.update()

# drag handler
def handle_drag(x, y):
  global g_dragging
  global g_px
  global g_py
  if g_dragging or not g_clicked:
    return
  g_dragging = True
  g_points.append([x, y])
  draw_segment(dt2, g_px, g_py, x, y)
  dt2.update()
  (g_px, g_py) = x, y
  g_dragging = False

# release handler
def handle_release(x, y):
  global g_clicked
  g_clicked = False
  set_undo_state(True)

# setup screen turtle to capture click/drag/release
def setup_screen_turtle():
  s = g_screen_radius
  g_screen.register_shape('st', ((-s, -s), (s, -s), (s, s), (-s, s)))
  t = new_turtle()
  t.shape('st')
  t.pu()
  t.goto(g_center)
  t.onclick(handle_click)
  t.ondrag(handle_drag)
  t.onrelease(handle_release)
  t.update()

# setup
def setup():
  draw_border()
  create_ui()
  draw_sectors()
  setup_screen_turtle()

# main

setup()
