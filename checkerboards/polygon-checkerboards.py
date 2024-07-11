# https://pardhav-m.blogspot.com/2020/06/checkerboards.html
# Checkerboards
# Polygon checkerboards
import turtle
import math

screen = turtle.Screen()
wh = screen.window_height()  # window height
ww = 2 * wh                  # window width
# trinket returns the same window width and height (hence square)
# set it to a rectangular area
screen.setup(ww, wh)
screen_radius = wh / 2

t = turtle.Turtle()
t.ht()
t.speed(0)
t.tracer(0)

# draw a border
def draw_border():
  t.pu()
  t.goto(-ww/2, -wh/2)
  t.pd()
  t.goto(ww/2, -wh/2)
  t.goto(ww/2, wh/2)
  t.goto(-ww/2, wh/2)
  t.goto(-ww/2, -wh/2)

# shape radius from https://www.mathsisfun.com/geometry/regular-polygons.html
def shape_radius(sides, length):
  return length / (2 * math.sin(math.pi / sides))

# shape side from https://www.mathsisfun.com/geometry/regular-polygons.html
def shape_side(sides, radius):
  return 2 * radius * math.sin(math.pi / sides)

# get current position and heading
def get_position():
  return t.pos(), t.heading()

# restore a saved position
def restore_position(pos, h):
  t.goto(pos)
  t.seth(h)

# draw polygon checkerboard
# sides  - number of sides
# cx, cy - center around which to draw this polygon
# length - length of each side
# rows - number of inside  polygons
# cols - number of divisions
# draw_cols - whether to draw the dividing lines
# cb - whether to fill checkerboard pattern
def draw_polygon_cb(sides, cx, cy, length, rows, cols, draw_cols = True, cb = True):
  ea = 360 / sides
  radius = shape_radius(sides, length)
  angle = math.degrees(math.pi / sides)
  # get left most starting point
  
  t.pu()
  t.goto(cx, cy)
  t.seth(270)  # point down
  t.right(angle)
  t.fd(radius)
  t.seth(0)
  sx, sy = t.pos()  # left most starting point
  t.pd()
  # radius delta
  rd = radius / rows
  # For each side
  for s in range(sides):
    for r in  range(rows):
      # go to left most starting point for each r
      t.pu()
      t.goto(cx, cy)
      t.seth(270 + (s * ea))
      t.right(angle)
      t.fd(r * rd)
      spos, sh = get_position()
      t.left(90 + angle)
      t.pd()
      # calculate short and long side lengths and deltas
      s_side_length = shape_side(sides, r * rd)
      s_d = s_side_length / cols
      l_side_length = shape_side(sides, (r + 1) * rd)
      l_d = l_side_length / cols
      # angle for each division
      # calculate four positions of the quad
      for c in range(cols):
        t.pu()
        restore_position(spos, sh)
        # pos1
        t.left(90 + angle)
        t.fd(c * s_d)
        pos1, h1 = get_position()
        # pos4
        t.fd(s_d)
        pos4, h4 = get_position()
        # pos2
        restore_position(spos, sh)
        t.fd(rd)
        t.left(90 + angle)
        t.fd(c * l_d)
        pos2, h2 = get_position()
        # pos3
        t.fd(l_d)
        pos3, h3 = get_position()
        t.setpos(pos1)
        t.pd()
        # Determine whether to fill
        fill = False
        if (r % 2 == 0 and c % 2 == 0) or (r % 2 == 1 and c % 2 == 1):
          fill = True

        if cb and fill:
          t.begin_fill()
          t.fillcolor('gray')
        # Connect the positions of the quad
        # pos1 -> pos2
        if not draw_cols:
          t.pu()
        t.goto(pos2)
        t.pd()
        # pos2 -> pos3
        t.goto(pos3)
        # pos3 -> pos4
        if not draw_cols:
          t.pu()
        t.goto(pos4)
        t.pd()
        # pos4 -> pos1
        t.goto(pos1)
        
        if fill:
          t.end_fill()

# main

draw_border()

length = screen_radius / 2
sides = 6
rows = 5
cols = 6

if cols % 2 == 1:
  cols += 1

draw_polygon_cb(sides, -ww/3, 0, length, rows, cols, draw_cols = False, cb = False)
draw_polygon_cb(sides, 0, 0, length, rows, cols, cb = False)
draw_polygon_cb(sides, ww/3, 0, length, rows, cols)

t.update()
