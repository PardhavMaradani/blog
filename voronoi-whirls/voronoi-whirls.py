# https://pardhav-m.blogspot.com/2020/07/voronoi-whirls.html
# Voronoi Whirls
# Voronoi Whirls
import turtle
import random
import time
from _Voronoi import Voronoi
from _voronoi_helpers import get_voronoi_polygons
from _polygon_helpers import draw_polygon_whirl, draw_polygon_concentric

# voronoi variables to tweak
g_n_seeds = 20
g_gradient = False
g_random_colors = False # when g_gradient = True
g_offset_factor = 0.1 # when g_gradient = False
g_whirl = True # else draw concentric lines
g_equidistant = False # when concentric lines

# random
seed = random.randrange(65536)
# seed = 30737 # samples
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
t.pensize(0.75)

# draw please wait
def draw_please_wait():
  t.pu()
  t.goto(-g_ww/2 + 20, g_wh/2 - 40)
  t.pd()
  t.write("Please wait...", font=("Arial", 16, "normal"))
  t.update()
  time.sleep(0.001)
  t.clear()

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
  offset_factor = g_offset_factor
  rgb_multiples = (1, 2, 3)
  for polygon in polygons:
    if g_gradient:
      offset_factor = 0.075 if g_whirl else 0.003
      if g_random_colors:
        m1 = random.randint(0, 2)
        m2 = random.randint(0, 2)
        m3 = random.randint(0, 2)
        rgb_multiples = (m1, m2, m3)
    if g_whirl:
      draw_polygon_whirl(t, polygon, offset_factor, g_gradient, rgb_multiples)
    else:
      if g_equidistant:
          offset_factor = g_offset_factor / 2
      draw_polygon_concentric(t, polygon, offset_factor, g_equidistant, g_gradient, rgb_multiples)
  # update screen
  g_screen.update()

# main

draw_please_wait()
draw_voronoi()
