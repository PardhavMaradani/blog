# https://pardhav-m.blogspot.com/2020/07/sliders.html
# Sliders
# Polygonal Checkerboards
import turtle
from _slider import Slider
from _checkerboards import draw_polygon_cb

screen = turtle.Screen()
wh = screen.window_height()
ww = 1.5 * wh
screen_radius = wh / 2

length_factor =  0.4
sides = 6
rows = 6
cols = 6
draw_cols = True
checkerboard = True
curved = True

# draw polygon checkerboard
def draw():
  draw_polygon_cb(sides, ww/6, 0, length_factor * screen_radius, rows, cols, draw_cols, checkerboard, curved)

# handle slider updates
def handle_slider_update(id, value):
  global length_factor
  global sides
  global rows
  global cols
  global draw_cols
  global checkerboard
  global curved
  # set variables based on slider id
  if id == 0:
    length_factor = value 
  elif id == 1:
    sides = value
  elif id == 2:
    rows = value
  elif id == 3:
    cols = value
  elif id == 4:
    draw_cols = True if value == 1 else False
  elif id == 5:
    checkerboard = True if value == 1 else False
  elif id == 6:
    curved = True if value == 1 else False
  # draw polygon
  draw()    

x = -ww/2 + 20
y = wh/2 - 20

# create sliders
slider_length = screen_radius * 0.6
Slider(0, x, y, slider_length, 0.1, 1, 0.05, length_factor, 'size', handle_slider_update) 
Slider(1, x, y - 30, slider_length, 2, 30, 1, sides, 'sides', handle_slider_update) 
Slider(2, x, y - 60, slider_length, 2, 30, 1, rows, 'rows', handle_slider_update)
Slider(3, x, y - 90, slider_length, 2, 30, 2, cols, 'cols', handle_slider_update)
Slider(4, x, y - 120, screen_radius * 0.15, 0, 1, 1, 1, 'draw_cols',  handle_slider_update)
Slider(5, x, y - 150, screen_radius * 0.15, 0, 1, 1, 1, 'checkerboard', handle_slider_update)
Slider(6, x, y - 180, screen_radius * 0.15, 0, 1, 1, 1, 'curved', handle_slider_update)

draw()
