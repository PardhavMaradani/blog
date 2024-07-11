# https://pardhav-m.blogspot.com/2020/06/checkerboards.html
# Checkerboards
# Rectangular checkerboards
import turtle

screen = turtle.Screen()
wh = screen.window_height()  # window height
ww = 2 * wh                  # window width
# trinket returns the same window width and height (hence square)
# set it to a rectangular area
screen.setup(ww, wh)
screen_radius = wh / 2

t = turtle.Turtle()
t.speed(0)
t.ht()
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

# draw rectangle
# cx, cy - center around which to draw this rectangle
# w - width of rectangle
# h - height of rectangle
def draw_rect(cx, cy, w, h):
  t.pu()
  sx = cx - (w / 2)
  sy = cy - (h / 2)
  t.goto(sx, sy)
  t.pd()
  for i in range(2):
    t.fd(w)
    t.left(90)
    t.fd(h)
    t.left(90)

# draw rectangular checkerboard
# cx, cy - center around which to draw this rectangle
# w - width of rectangle
# h - height of rectangle
# rows - number of inside circles
# cols - number of divisions
# cb - whether to fill checkerboard pattern
def draw_rect_cb(cx, cy, w, h, rows, cols, cb = True):
  # calculate starting point
  t.pu()
  sx = cx - (w / 2)
  sy = cy - (h / 2)
  t.goto(sx, sy)
  t.pd()
  # calculate x and y deltas
  xd = w / cols
  yd = h / rows
  # draw quads
  for r in range(rows):
    for c in range(cols):
      px = xd * c
      py = yd * r
      t.pu()
      t.goto(sx + px, sy + py)
      t.pd()
      # Determine whether to fill
      fill = False
      if (r % 2 == 0 and c % 2 == 0) or (r % 2 == 1 and c % 2 == 1):
        fill = True
      if cb and fill:
        t.begin_fill()
        t.fillcolor('gray')
      for i in range(2):
        t.fd(xd)
        t.left(90)
        t.fd(yd)
        t.left(90)
      if fill:
        t.end_fill()


draw_border()

length = screen_radius
rows = 8
cols = 8

draw_rect(-ww/3, 0, length, length)
draw_rect_cb(0, 0, length, length, rows, cols, cb = False )
draw_rect_cb(ww/3, 0, length, length, rows, cols)

t.update()
