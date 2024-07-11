# https://pardhav-m.blogspot.com/2020/07/interactive-voronoi.html
# Interactive Voronoi
# Voronoi Kaleidoscope
import turtle
import math
from _Voronoi import Voronoi 

g_n_sectors = 6
g_added_points = []
g_seeds = []

# screen setup
g_screen = turtle.Screen()
g_wh = int(g_screen.window_height())
g_ww = int(1.5 * g_wh)
g_screen.setup(g_ww, g_wh)
g_screen.tracer(0)

# new turtle
def new_turtle():
  t = turtle.Turtle()
  t.ht()
  t.speed(0)
  return t

# turtle
vt = new_turtle()
# help
ht = new_turtle()
g_showing_help = None
# show sectors
st = new_turtle()
st.color('red')
g_showing_sectors = False

# draw a border
def draw_border():
  t = new_turtle()
  t.pu()
  t.goto(-g_ww/2, -g_wh/2)
  t.pd()
  t.goto(g_ww/2, -g_wh/2)
  t.goto(g_ww/2, g_wh/2)
  t.goto(-g_ww/2, g_wh/2)
  t.goto(-g_ww/2, -g_wh/2)
  t.update()

# draw seeds
def draw_seeds(seeds):
  vt.pu()
  for seed in seeds:
    vt.goto(seed)
    vt.dot(3)

# draw voronoi
def draw_voronoi():
  if len(g_seeds) == 0:
    vt.clear()
    vt.update()
    return
  # get voronoi edges
  voronoi = Voronoi(g_seeds)
  voronoi.process()
  voronoi_edges = voronoi.get_output()
  # clear turtle to redraw
  vt.clear()
  # draw seeds
  draw_seeds(g_seeds)
  # draw edges
  for edge in voronoi_edges:
    (x1, y1, x2, y2) = edge
    vt.pu()
    vt.goto(x1, y1)
    vt.pd()
    vt.goto(x2, y2)
  # update screen
  vt.update()

# generate seeds from raw points and draw
def generate_seeds_and_draw():
  global g_seeds
  g_seeds = []
  sector_angle = 2 * math.pi / g_n_sectors
  for point in g_added_points:
    x, y = point
    # normalize point to first sector
    point_angle = math.atan2(y, x)
    point_angle_norm = math.atan2(y, x) % sector_angle
    n_rotate_angle = point_angle_norm - point_angle
    nx = x * math.cos(n_rotate_angle) - y * math.sin(n_rotate_angle)
    ny = x * math.sin(n_rotate_angle) + y * math.cos(n_rotate_angle)
    # rotate normalized point in all sectors
    for i in range(g_n_sectors):
      rotate_angle = sector_angle * i
      rx = nx * math.cos(rotate_angle) - ny * math.sin(rotate_angle)
      ry = nx * math.sin(rotate_angle) + ny * math.cos(rotate_angle)
      g_seeds.append((rx, ry))
  # draw voronoi
  draw_voronoi()

# show voronoi
def show_voronoi():
  draw_voronoi()

# hide voronoi
def hide_voronoi():
  vt.clear()
  vt.update()

# show help
def show_help():
  hide_voronoi()
  hide_sectors()
  global g_showing_help
  x, y = (-g_ww/2 + 20, g_wh/2 - 40)
  ht.pu()
  ht.goto(x, y)
  ht.write("Click to add points...", font=("Arial", 16, "normal"))
  ht.goto(x, y - 30)
  keys_font = ("Arial", 14, "normal")
  ht.write("Keys", font = keys_font)
  ht.goto(x + 20, y - 60)
  ht.write("u - undo", font = keys_font)
  ht.goto(x + 20, y - 90)
  ht.write("↑ - inc sectors", font = keys_font)
  ht.goto(x + 20, y - 120)
  ht.write("↓ - dec sectors", font = keys_font)
  ht.goto(x + 20, y - 150)
  ht.write("s - show / hide sectors", font = keys_font)
  ht.goto(x + 20, y - 180)
  ht.write("h - toggle help", font = keys_font)
  ht.update()
  g_showing_help = True

# hide help
def hide_help():
  global g_showing_help
  ht.clear()
  ht.update()
  g_showing_help = False
  show_voronoi()

# toggle help screen
def toggle_help():
  if g_showing_help:
    hide_help()
  else:
    show_help()

# undo - remove most recent point
def undo():
  if g_showing_help or len(g_added_points) == 0:
    return
  remove_event_handlers()
  g_added_points.pop()
  generate_seeds_and_draw()
  add_event_handlers()

# inc sectors
def inc_sectors():
  global g_n_sectors
  if g_showing_help:
    return
  remove_event_handlers()
  g_n_sectors += 1
  generate_seeds_and_draw()
  if g_showing_sectors:
    show_sectors()
  add_event_handlers()

# dec sectors
def dec_sectors():
  global g_n_sectors
  if g_showing_help or g_n_sectors == 1:
    return
  remove_event_handlers()
  g_n_sectors -= 1
  generate_seeds_and_draw()
  if g_showing_sectors:
    show_sectors()
  add_event_handlers()

# show sectors
def show_sectors():
  st.clear()
  global g_showing_sectors
  sector_angle = 2 * math.pi / g_n_sectors
  for i in range(g_n_sectors):
    st.seth(math.degrees(sector_angle * i))
    st.fd(g_ww)
    st.bk(g_ww)
  st.update()
  g_showing_sectors = True

# hide sectors
def hide_sectors():
  global g_showing_sectors
  st.clear()
  st.update()
  g_showing_sectors = False

# toggle showing sectors
def toggle_sectors():
  if g_showing_help:
    return
  if g_showing_sectors:
    hide_sectors()
  else:
    show_sectors()

# add point callback
def add_point(x, y):
  if g_showing_help:
    hide_help()
    if len(g_added_points) > 0:
      return
  if (x, y) in g_added_points:
    return
  remove_event_handlers()
  g_added_points.append((x, y))
  generate_seeds_and_draw()
  add_event_handlers()

# remove event handlers
def remove_event_handlers():
  g_screen.onkey(None, "h")
  g_screen.onkey(None, "u")
  g_screen.onkey(None, "Up")
  g_screen.onkey(None, "Down")
  g_screen.onkey(None, "s")
  g_screen.onscreenclick(None)

# add event handlers
def add_event_handlers():
  g_screen.onkey(toggle_help, "h")
  g_screen.onkey(undo, "u")
  g_screen.onkey(inc_sectors, "Up")
  g_screen.onkey(dec_sectors, "Down")
  g_screen.onkey(toggle_sectors, "s")
  g_screen.onscreenclick(add_point)

# setup
def setup():
  global g_n_sectors
  draw_border()
  show_help()
  add_event_handlers()
  g_screen.listen()

# main

setup()
