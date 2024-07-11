# https://pardhav-m.blogspot.com/2020/06/bezier-curve-animations.html
# Bezier Curve Animation
# Pursuit curves 
import turtle
import random
import time

# screen setup
g_screen = turtle.Screen()
g_wh = g_screen.window_height()
g_ww = 1.5 * g_wh
g_screen.setup(g_ww, g_wh)
g_screen_radius = g_wh / 2
# other globals
g_b_side = g_screen_radius * 0.1
g_b_side2 = g_b_side / 2
g_playing = True
g_pen_colors = ['black', 'blue', 'firebrick', 'green', 'saddle brown', 'orange red', 'indian red', 'medium violet red']
g_min_cps = 2
g_max_cps = 8
g_n_cps = 3
g_control_points = []
g_control_points_coords = []
g_n_steps = 50 # number of steps of t between [0, 1]
g_t = 0
g_t_step = 1 / g_n_steps
g_dt = [None] * g_max_cps

# draw borders
def draw_borders():
  t = turtle.Turtle()
  t.speed(0)
  t.pu()
  t.goto(-g_ww/2, -g_wh/2)
  t.pd()
  for i in range(4):
    t.fd(g_ww if i % 2 == 0 else g_wh)
    t.left(90)
  t.pu()
  t.goto(-g_ww/2, g_wh/2)
  t.pd()
  for i in range(4):
    t.fd(g_b_side*8 if i % 2 == 0 else g_b_side*3)
    t.right(90)

# handle play/pause button click
def handle_pp_click(x, y):
  global g_playing
  g_playing = not g_playing
  if g_playing:
    start_loop()

# handle inc button click
def handle_inc_click(x, y):
  global g_n_cps
  if g_n_cps < g_max_cps:
    create_control_point(g_n_cps)
    g_n_cps += 1
    update_control_points()

# handle dec button click
def handle_dec_click(x, y):
  global g_n_cps
  if g_n_cps > g_min_cps:
    g_n_cps -= 1
    cp = g_control_points.pop()
    cp.clear()
    cp.ht()
    del cp
    update_control_points()

# clear, hide and penup a turtle
def clear_turtle(t):
  t.clear()
  t.ht()
  t.pu()

# create a button
def create_button(name, shape, handler, x, y, angle = 0):
  t = turtle.Turtle()
  t.speed(0)
  t.shape(shape)
  t.pu()
  if shape == 'b_square':
    t.goto(x - g_b_side2 - 15, y - g_b_side)
  else:
    t.goto(x - g_b_side2, y - g_b_side)
  t.write(name)
  t.goto(x, y)  
  t.seth(angle)
  t.onclick(handler)
  return t

# create buttons on top left
def create_buttons():
  # custom shapes
  triangle_shape = [(-g_b_side2, 0), (g_b_side2, 0), (0, g_b_side2)]
  g_screen.register_shape('b_triangle', triangle_shape)
  square_shape = [(-g_b_side2, -g_b_side2), (g_b_side2, -g_b_side2), (g_b_side2, g_b_side2), (-g_b_side2, g_b_side2)]
  g_screen.register_shape('b_square', square_shape)
  x = -g_ww/2 + g_b_side + 20
  y = g_wh/2 - g_b_side - 10
  create_button('play / pause', 'b_square', handle_pp_click, x, y)
  create_button('inc', 'b_triangle', handle_inc_click, x + g_b_side*2.5, y, 90)
  create_button('dec', 'b_triangle', handle_dec_click, x + g_b_side*5, y, -90)

# control point class
class ControlPoint(turtle.Turtle):
  def __init__(self, num = 0, x = 0, y = 0):
    turtle.Turtle.__init__(self)
    self.num = num
    self.clicked = False
    self.dragging = False
    self.is_playing = None
    self.speed(0)
    self.pu()
    self.goto(x, y)
    self.fd(10)
    self.write("p" + str(self.num))
    self.bk(10)
    # click/release/drag handlers
    self.onclick(self.onclick_handler)
    self.onrelease(self.onrelease_handler)
    self.ondrag(self.ondrag_handler)

  # handle click
  def onclick_handler(self, x, y):
    global g_playing
    self.clicked = True
    self.is_playing = g_playing
    g_playing = False

  # handle release
  def onrelease_handler(self, x, y):
    global g_playing
    self.clicked = False
    if self.is_playing:
      g_playing = True
      start_loop()

  # handle drag
  def ondrag_handler(self, x, y):
    if not self.clicked or self.dragging:
      return
    self.dragging = True
    self.clear()
    self.goto(x, y)
    self.fd(10)
    self.write("p" + str(self.num))
    self.bk(10)
    update_control_points()
    self.dragging = False

# create a control point
# i - control point number
def create_control_point(i):
  mh = int(g_wh * 0.8)
  x = random.randrange(0, mh) - g_wh/2
  y = random.randrange(0, mh) - g_wh/2
  cp = ControlPoint(i, x, y)
  cp.shape('cp')
  g_control_points.append(cp)

# create initial control points
def create_initial_control_points():
  global g_control_points
  # create control point shape
  s = g_screen_radius * 0.025
  g_screen.register_shape("cp", ((-s, -s), (s, -s), (s, s), (-s, s)))
  # create control points
  for i in range(g_n_cps):
    create_control_point(i)

# update control point coordinates (after drag)
def update_control_points():
  global g_control_points_coords
  g_control_points_coords = []
  for cp in g_control_points:
    g_control_points_coords.append(cp.pos())
  draw_frame(True)

# recursive functiont to get bezier point
# cps - control points
# t - t value [0, 1]
# level - recursion level
def get_bezier_point(cps, t, level):
  # terminating condition
  if len(cps) == 1:
    return cps[0]
  # create new control points (n - 1)
  n_cps = []
  for i, p0 in enumerate(cps):
    if i == len(cps) - 1:
      break
    p1 = cps[i + 1]
    x0, y0 = p0
    x1, y1 = p1
    x2 = x0 + t * (x1 - x0)
    y2 = y0 + t * (y1 - y0)
    n_cps.append((x2, y2))

  # recursively call for n - 1 control points
  bp = get_bezier_point(n_cps, t, level + 1)

  pt = cps[len(cps) - 1]
  if level == 0:
    pt = bp
    dt = g_dt[0]
  else:
    dt = g_dt[g_n_cps - 1 - level]
  dt.seth(dt.towards(pt))
  dt.goto(pt)
  if not dt.isvisible():
    dt.st()
    dt.pd()

  return bp

# draw a frame
# redraw_bt - whether to redraw bezier curve up to current t
def draw_frame(redraw_bt = False):
  if g_t == 0 or redraw_bt:
    for i in range(g_max_cps):
      clear_turtle(g_dt[i])
  # redraw bezier curve if needed
  if redraw_bt:
    t = 0
    for i in range(g_n_steps + 1):
      if t > g_t:
        break
      get_bezier_point(g_control_points_coords, t, 0)
      t += g_t_step
  else:
    get_bezier_point(g_control_points_coords, g_t, 0)
  # update screen  
  g_screen.update()

# loop to draw animation
def start_loop():
  global g_t
  while True:
    if not g_playing:
      break
    g_t += g_t_step
    if g_t > 1:
      g_t = 0
    draw_frame()
    time.sleep(0.01)

# initial setup
def setup():
  global g_dt
  g_screen.tracer(0)
  draw_borders()
  create_buttons()
  for i in range(g_max_cps):
    g_dt[i] = turtle.Turtle()
    g_dt[i].speed(0)
    if i == 0:
      g_dt[i].color('red')
      g_dt[i].pensize(3)
    else:
      g_dt[i].color(g_pen_colors[i % len(g_pen_colors)])
      g_dt[i].pensize(2 - (0.5*i))
  create_initial_control_points()
  update_control_points()

# main

setup()
start_loop()
