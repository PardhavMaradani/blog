# https://pardhav-m.blogspot.com/2020/07/interactive-voronoi.html
# Interactive Voronoi
# Voronoi Points
import turtle
from _Voronoi import Voronoi 

# seeds
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
  if g_showing_help or len(g_seeds) == 0:
    return
  remove_event_handlers()
  g_seeds.pop()
  draw_voronoi()
  add_event_handlers()

# add point callback
def add_point(x, y):
  if (x, y) in g_seeds:
    return
  if g_showing_help:
    hide_help()
    if len(g_seeds) > 0:
      return
  remove_event_handlers()
  g_seeds.append((x, y))
  draw_voronoi()
  add_event_handlers()

# remove event handlers
def remove_event_handlers():
  g_screen.onkey(None, "h")
  g_screen.onkey(None, "u")
  g_screen.onscreenclick(None)

# add event handlers
def add_event_handlers():
  g_screen.onkey(toggle_help, "h")
  g_screen.onkey(undo, "u")
  g_screen.onscreenclick(add_point)

# setup
def setup():
  draw_border()
  show_help()
  add_event_handlers()
  g_screen.listen()

# main

setup()
