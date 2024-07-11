# https://pardhav-m.blogspot.com/2020/06/checkerboards.html
# Checkerboards
# Circular checkerboards
import turtle

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

# get current position and heading
def get_position():
  return t.pos(), t.heading()

# draw circular checkerboard
# cx, cy - center around which to draw this polygon
# radius - radius of the largest circle
# rows - number of inside circles
# cols - number of divisions
# draw_cols - whether to draw the dividing lines
# cb - whether to fill checkerboard pattern
def draw_circular_cb(cx, cy, radius, rows, cols, draw_cols = True, cb = True):
  t.pu()
  t.goto(cx, cy)
  t.pd()
  rd = radius / rows
  angle = 360 / cols
  for r in range(rows):
    for c in range(cols):
      sr = rd * r
      lr = rd * (r + 1)
      # get starting and end position of quad
      t.pu()
      t.goto(cx, cy)
      t.seth(0)
      t.left(angle * c)
      t.fd(sr)
      pos1, h1 = get_position()
      t.left(90)
      t.circle(sr, angle)
      pos4, h4 = get_position()
      t.goto(pos1)
      t.seth(h1)
      t.pd()
      # Determine whether to fill
      fill = False
      if (r % 2 == 0 and c % 2 == 0) or (r % 2 == 1 and c % 2 == 1):
        fill = True
      if cb and fill:
        t.begin_fill()
        t.fillcolor('gray')
      # draw quad
      # pos1 -> pos2
      if not draw_cols:
        t.pu()
      t.fd(rd)
      t.pd()
      # pos2 -> pos3
      t.left(90)
      t.circle(lr, angle)
      if not draw_cols:
        t.pu()
      # pos3 -> pos4
      t.goto(pos4)
      t.pd()
      # pos4 -> pos1
      t.seth(h4)
      t.right(180)
      t.circle(-sr, angle)
      if fill:
        t.end_fill()


draw_border()

length = screen_radius / 2
rows = 6
cols = 16

if cols % 2 == 1:
  cols += 1

draw_circular_cb(-ww/3, 0, length, rows, cols, draw_cols = False, cb = False )
draw_circular_cb(0, 0, length, rows, cols, cb = False)
draw_circular_cb(ww/3, 0, length, rows, cols)

t.update()
