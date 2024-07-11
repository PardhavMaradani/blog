# https://pardhav-m.blogspot.com/2020/07/voronoi-whirls.html
# Voronoi Whirls
# Basic Vornoi
import turtle
import random
import time
from _Voronoi import Voronoi
from _voronoi_helpers import get_voronoi_polygons

# voronoi variables to tweak
g_n_seeds = 20
g_show_seeds = True
g_fill_colors = True

# random
seed = random.randrange(65536)
random.seed(seed)

# screen setup
g_screen = turtle.Screen()
g_wh = int(g_screen.window_height())
g_ww = int(1.5 * g_wh)
g_screen.setup(g_ww, g_wh)
g_screen.tracer(0)

# turtle
t = turtle.Turtle()
t.ht()
t.speed(0)

# draw please wait
def draw_please_wait():
  t.pu()
  t.goto(-g_ww/2 + 20, g_wh/2 - 40)
  t.pd()
  t.write("Please wait...", font=("Arial", 16, "normal"))
  t.update()
  time.sleep(0.001)
  t.clear()

# draw seeds
def draw_seeds(seeds):
  t.pu()
  for seed in seeds:
    t.goto(seed)
    t.dot(3)

# draw polygon
def draw_polygon(polygon, fill_color = False):
  if fill_color:
    R = random.randrange(0,255)
    G = random.randrange(0,255)
    B = random.randrange(0,255)
    color = (R,G,B)
    t.fillcolor(color)
  for i, v in enumerate(polygon):
    if i == 0:
      t.pu()
    t.goto(v)
    # t.dot()
    if i == 0:
      t.pd()
      t.begin_fill()
  t.goto(polygon[0])
  if fill_color:
    t.end_fill()

# draw voronoi
def draw_voronoi():
  # bounding box
  maxx = g_ww/2
  maxy = g_wh/2
  minx = -g_ww/2
  miny = -g_wh/2
  # create seeds
  seeds = []
  for i in range(g_n_seeds):
    x = random.randint(1, g_ww-1) - g_ww/2
    y = random.randint(1, g_wh-1) - g_wh/2
    seeds.append((x, y))
  # get voronoi edges
  voronoi = Voronoi(seeds)
  voronoi.process()
  voronoi_edges = voronoi.get_output()
  # get voronoi polygons
  polygons = get_voronoi_polygons(seeds, voronoi_edges, (minx, miny, maxx, maxy))
  for polygon in polygons:
    draw_polygon(polygon, g_fill_colors)
  if g_show_seeds:
    draw_seeds(seeds)
  # update screen
  g_screen.update()

# main

draw_please_wait()
draw_voronoi()
