import turtle
import random

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

# draw border
def draw_border():
  t = turtle.Turtle()
  t.speed(0)
  t.pu()
  t.goto(-g_ww/2, -g_wh/2)
  t.pd()
  for i in range(4):
    t.fd(g_ww if i % 2 == 0 else g_wh)
    t.left(90)

# t slider update
def update_t(t):
  global g_t
  g_t = t
  draw_frame()

# n control points slider update
def update_n_control_points(n):
  global g_n_cps
  if n == g_n_cps:
    return
  diff = n - g_n_cps
  if diff > 0:
    for i in range(diff):
      create_control_point(g_n_cps)
      g_n_cps += 1
  else:
    for i in range(abs(diff)):
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
    self.clicked = True

  # handle release
  def onrelease_handler(self, x, y):
    self.clicked = False

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
  initial_cps = [(-g_ww/4, -g_wh/4), (0, g_wh/4), (g_ww/4, -g_wh/4)]
  for i in range(len(initial_cps)):
    x, y = initial_cps[i]
    cp = ControlPoint(i, x, y)
    cp.shape('cp')
    g_control_points.append(cp)

# update control point coordinates (after drag)
def update_control_points():
  global g_control_points_coords
  g_control_points_coords = []
  for cp in g_control_points:
    g_control_points_coords.append(cp.pos())
  draw_frame()

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
def draw_frame():
  for i in range(g_max_cps):
    clear_turtle(g_dt[i])
  # redraw bezier curve if needed
  t = 0
  for i in range(g_n_steps + 1):
    if t > g_t + g_t_step:
      break
    get_bezier_point(g_control_points_coords, t, 0)
    t += g_t_step
  # update screen  
  g_screen.update()

# initial setup
def setup():
  global g_dt
  g_screen.tracer(0)
  draw_border()
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
