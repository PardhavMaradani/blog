# https://pardhav-m.blogspot.com/2020/06/trees.html
# Treees
# Shaded Trees
import turtle
import random
import math
import time

seed = random.randrange(65536)
random.seed(seed)

# percent of line length to curve
curve_percent = 0.25
# percent of line length to use for hatch
hatch_percent = 0.14
# number of hatch lines per segment
hatch_steps = 10
# should hatch
should_hatch = True

screen = turtle.Screen()
wh = screen.window_height()  # window height
ww = 1.5 * wh                # window width
# trinket returns the same window width and height (hence square)
# set it to a rectangular area
screen.setup(ww, wh)
screen_radius = wh / 2

t = turtle.Turtle()
t.ht()
t.speed(0)
t.tracer(0)

# draw please wait
def draw_please_wait():
  t.pu()
  t.goto(-ww/2 + 20, wh/2 - 40)
  t.pd()
  t.write("Please wait...", font=("Arial", 16, "normal"))
  t.update()
  time.sleep(0.001)
  t.clear()

# draw a border
def draw_border():
  t.pu()
  t.goto(-ww/2, -wh/2)
  t.pd()
  t.goto(ww/2, -wh/2)
  t.goto(ww/2, wh/2)
  t.goto(-ww/2, wh/2)
  t.goto(-ww/2, -wh/2)

# hatch
# line_length - length of the full curved line
# radius - for curved part, radius of the curve
# angle - for curved part, angle of the curve
def hatch(line_length, radius = None, angle = None):
  delta = line_length / hatch_steps
  if angle is not None:
    delta = angle / hatch_steps
  length = line_length * hatch_percent
  # save beginning position
  bpos, bh = t.pos(), t.heading()
  # for each hatch step
  for i in range(0, hatch_steps):
    t.color('#aaaaaa')
    spos, sh = t.pos(), t.heading()
    t.right(90)
    # random angle
    a = 20 * 1.5 * random.random()
    # random length
    b = length + (length * 1.5 * random.random())
    t.left(a)
    t.fd(b)
    t.setpos(spos)
    t.seth(sh)
    t.color('black')
    if radius is not None:
      t.circle(radius, delta)
    else:
      t.fd(delta)
  # re-draw full line or arc
  t.pu()
  t.setpos(bpos)
  t.seth(bh)
  t.pd()
  if angle is not None:
    t.circle(radius, angle)
  else:
    t.fd(line_length)

# draw curved line
# fl - length of straight line (t.fd)
# cl - length of curved line (t.circle)
# angle - angle between the lines
def draw_curved_line(fl, cl, angle):
  radius = cl * math.tan(math.radians(angle / 2))
  angle = 180 - angle
  if angle < 0:
    angle *= -1
  if should_hatch:
    hatch(fl)
    hatch(fl, radius, angle)
  else:
    t.fd(fl)
    t.circle(radius, angle)

# get end position and heading from current point
# width - width of the branch
def get_end_position(width):
  t.pu()
  t.right(90)
  t.fd(width)
  t.right(90)
  epos, eh = t.pos(), t.heading()
  t.left(90)
  t.bk(width)
  t.left(90)
  t.pd()
  return epos, eh

# draw curved tree
# branch - lenght of branch
# pcl - previous curve length
def tree(branch, pcl, width, end_pos, end_heading):
  if branch <= 3:
    return
  # calculate angles and lengths
  a = 1.5 * random.random()
  b = 1.5 * random.random()
  la = 20 * a
  new_branch = branch - (10 * b)
  cl = branch * curve_percent
  fl = branch - cl - pcl
  new_cl = new_branch * curve_percent
  new_width = width * 0.8
  # draw left curve
  draw_curved_line(fl, cl, 180 - la)
  # get left tree end position
  n_end_pos, n_end_h = get_end_position(new_width / 2)
  # draw left tree
  tree(new_branch, cl, new_width, n_end_pos, n_end_h)
  # draw middle curve
  draw_curved_line(0, new_cl, la * 2)
  # get right tree end position
  n_end_pos, n_end_h = get_end_position(new_width / 2)
  # draw right tree
  tree(new_branch, cl, new_width, n_end_pos, n_end_h)
  # calculate angle towards end position (ea)
  t.pu()
  t.fd(new_cl)
  ea = t.towards(end_pos) - t.heading()
  t.bk(new_cl)
  t.pd()
  # draw curve towards end position
  draw_curved_line(0, new_cl, (180 - ea) % 360)
  # go to end position
  t.goto(end_pos)
  t.seth(end_heading)

# main

draw_please_wait()
draw_border()

# set tree base
t.left(90)
t.pu()
t.goto(0, -wh/2 + (wh * 0.05))
t.pd()

# draw tree
start_branch = screen_radius * 0.20
start_width = start_branch * 0.5
end_pos, end_heading = get_end_position(start_width)
tree(start_branch, 0, start_width, end_pos, end_heading)

# print seed
t.pu()
t.color('black')
t.left(90)
t.fd(screen_radius * 0.05)
t.pd()
t.write(seed)

t.update()
