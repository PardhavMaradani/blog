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
g_pen_colors = ['black', 'blue', 'firebrick', 'green', 'saddle brown', 'orange red', 'indian red', 'medium violet red']
g_n_cps = 3
g_control_points = []
g_control_points_coords = []
g_n_steps = 50 # number of steps of t between [0, 1]
g_t = 0
g_t_step = 1 / g_n_steps
g_levels = 5
# turtle to draw connecting lines
g_dt = turtle.Turtle()
g_dt.speed(0)
g_dt.ht()

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

# level update
def update_levels(levels):
  global g_levels
  g_levels = levels
  draw_frame()

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
  g_control_points_coords.append(g_control_points_coords[0])
  draw_frame()

# recursive functiont to get bezier point
# cps - control points
# t - t value [0, 1]
# level - recursion level
# draw - whether to draw connecting lines
# dt - turtle to draw connecting lines
def get_bezier_point(cps, t, level, draw = False, dt = None):
  # terminating condition
  if level > g_levels:
    return
  # create new control points (n - 1)
  n_cps = []
  for i, p0 in enumerate(cps):
    if i == len(cps) - 1:
      i = 0
    p1 = cps[i + 1]
    x0, y0 = p0
    x1, y1 = p1
    x2 = x0 + t * (x1 - x0)
    y2 = y0 + t * (y1 - y0)
    n_cps.append((x2, y2))
  # draw connecting lines if asked
  if draw:
    dt.pensize(2 - (0.5*level))
    for i, v in enumerate(cps):
      if i == 0:
        dt.pu()
        dt.color(g_pen_colors[level % len(g_pen_colors)])
      dt.goto(v)
      # dt.dot(5)
      if i == 0:
        dt.pd()
  # recursively call for n - 1 control points
  get_bezier_point(n_cps, t, level + 1, draw, dt)

# draw a frame
# redraw_bt - whether to redraw bezier curve up to current t
def draw_frame():
  g_dt.clear()
  get_bezier_point(g_control_points_coords, g_t, 0, True, g_dt)
  # update screen  
  g_screen.update()

# initial setup
def setup():
  g_screen.tracer(0)
  draw_border()
  create_initial_control_points()
  update_control_points()

# main

setup()
