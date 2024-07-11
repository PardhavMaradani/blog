# https://pardhav-m.blogspot.com/2020/07/interactive-voronoi.html
# Interactive Voronoi
# Voronoi Collage
import turtle
import random
from _Voronoi import Voronoi
from _voronoi_helpers import get_voronoi_polygons
from _slider import Slider
from _collage_helpers import Seed, get_polygon_centroid

# global vars
g_n_seeds = 3
g_gap = 0.05
g_edit = 1

# seeds
g_seeds = []
g_seed_coords = []

# screen setup
g_screen = turtle.Screen()
g_wh = int(g_screen.window_height())
g_ww = int(1.5 * g_wh)
g_screen_radius = g_wh / 2
g_screen.setup(g_ww, g_wh)
g_screen.tracer(0)

# new turtle
def new_turtle():
  t = turtle.Turtle()
  t.ht()
  t.speed(0)
  return t

# voronoi turtle
vt = new_turtle()

g_bb_minx = int(-g_ww / 2.5)
g_bb_maxx = int(g_ww / 2.5)
g_bb_miny = int((-g_wh / 3) - (g_wh/10))
g_bb_maxy = int((g_wh / 3) - (g_wh/10))

g_bounding_box = (g_bb_minx, g_bb_miny, g_bb_maxx, g_bb_maxy)

# draw bounding box
def draw_bounding_box():
  t = new_turtle()
  t.pu()
  t.goto(g_bb_minx, g_bb_miny)
  t.pd()
  t.goto(g_bb_maxx, g_bb_miny)
  t.goto(g_bb_maxx, g_bb_maxy)
  t.goto(g_bb_minx, g_bb_maxy)
  t.goto(g_bb_minx, g_bb_miny)
  t.update()

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

# handle slider updates
def handle_slider_update(id, value):
  if id == 0:
    update_n_seeds(value)
  elif id == 1:
    update_gap(value)
  elif id == 2:
    update_edit(value)

# resize polygon based on gap
def resize_polygon(polygon):
  cx, cy = get_polygon_centroid(polygon)
  output = []
  for v in polygon:
    x, y = v
    x1 = x + (g_gap * (cx - x))
    y1 = y + (g_gap * (cy - y))
    output.append((x1, y1))
  return output

# draw polygon
def draw_polygon(polygon):
  new_polygon = resize_polygon(polygon)
  for i, v in enumerate(new_polygon):
    if i == 0:
      vt.pu()
    vt.goto(v)
    if i == 0:
      vt.pd()
  vt.goto(new_polygon[0])

# draw voronoi
def draw_voronoi():
  voronoi = Voronoi(g_seed_coords)
  voronoi.process()
  voronoi_edges = voronoi.get_output()
  # clear turtle to redraw
  vt.clear()
  # get polygons
  polygons = get_voronoi_polygons(g_seed_coords, voronoi_edges, g_bounding_box)
  # draw polygons
  for polygon in polygons:
    draw_polygon(polygon)
  vt.update()

# seed move handler
def handle_seed_move(id):
  update_seed_coords()

# create a random seed
def create_random_seed(i):
  gap = 6
  bb_width = g_bb_maxx - g_bb_minx - 2*gap
  bb_height = g_bb_maxy - g_bb_miny - 2*gap
  x = random.randrange(0, bb_width) - (bb_width / 2)
  y = random.randrange(0, bb_height) - (bb_height / 2) - (g_wh/10)
  seed = Seed(i, x, y, g_bounding_box, handle_seed_move)
  seed.shape('seed')
  if g_edit == 0:
    seed.ht()
  seed.update()
  g_seeds.append(seed)

# create initial seeds
def create_initial_seeds():
  global g_seeds
  # create seed shape
  s = g_screen_radius * 0.025
  g_screen.register_shape("seed", ((-s, -s), (s, -s), (s, s), (-s, s)))
  # create initial seeds
  for i in range(g_n_seeds):
    create_random_seed(i)
  update_seed_coords()

# update seed coordinates (after drag)
def update_seed_coords():
  global g_seed_coords
  g_seed_coords = []
  for seed in g_seeds:
    g_seed_coords.append(seed.pos())
  draw_voronoi()

# seeds slider update
def update_n_seeds(n):
  global g_n_seeds
  if n == g_n_seeds:
    return
  diff = n - g_n_seeds
  if diff > 0:
    for i in range(diff):
      create_random_seed(g_n_seeds)
      g_n_seeds += 1
  else:
    for i in range(abs(diff)):
      g_n_seeds -= 1
      seed = g_seeds.pop()
      seed.clear()
      seed.ht()
      del seed
  update_seed_coords()

# update gap
def update_gap(value):
  global g_gap
  g_gap = value
  draw_voronoi()

# update edit
def update_edit(value):
  global g_edit
  g_edit = value
  for seed in g_seeds:
    if g_edit == 1:
      seed.st()
    else:
      seed.ht()
    seed.update()

# create sliders
def create_sliders():
  x = -g_ww/2 + 20
  y = g_wh/2 - 20
  slider_length = g_screen_radius * 0.6
  # create sliders
  Slider(0, x, y, slider_length, 2, 10, 1, g_n_seeds, 'seeds', handle_slider_update)
  Slider(1, x, y - 30, slider_length, 0, 0.2, 0.01, g_gap, 'gap', handle_slider_update)
  Slider(2, x, y - 60, g_screen_radius * 0.15, 0, 1, 1, g_edit, 'edit', handle_slider_update)

# setup
def setup():
  draw_border()
  draw_bounding_box()
  create_sliders()
  create_initial_seeds()

# main

setup()
