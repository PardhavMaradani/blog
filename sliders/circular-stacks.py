# https://pardhav-m.blogspot.com/2020/07/sliders.html
# Sliders
# Circular Stacks
import turtle
from _slider import Slider
from _circular_stack import draw_circular_stack

inner_sides = 4
inner_polygons_multiple = 30
inner_length_factor = 0.2
twists = 6
pen_size = 1
screen_radius_factor = 0.85
checkerboard = False

# draw circular stack
def draw():
  draw_circular_stack(inner_sides, inner_polygons_multiple, inner_length_factor, twists, pen_size, screen_radius_factor, checkerboard)

# handle slider updates
def handle_slider_update(id, value):
  global inner_sides
  global inner_polygons_multiple
  global inner_length_factor
  global twists
  global pen_size
  global screen_radius_factor
  global checkerboard
  # set variable based on slider id
  if id == 0:
    inner_sides = value
  elif id == 1:
    inner_polygons_multiple = value
  elif id == 2:
    inner_length_factor = value
  elif id == 3:
    twists = value
  elif id == 4:
    pen_size = value
  elif id == 5:
    screen_radius_factor = value
  elif id == 6:
    checkerboard = True if value == 1 else False
  # draw stack
  draw()

screen = turtle.Screen()
wh = screen.window_height()
ww = 1.5 * wh
x = -ww/2 + 20
y = wh/2 - 20
screen_radius = wh / 2

# create sliders
slider_length = screen_radius * 0.6
Slider(0, x, y, slider_length, 2, 10, 1, inner_sides, 'inner_sides', handle_slider_update)
Slider(1, x, y - 30, slider_length, 1, 100, 1, inner_polygons_multiple, 'n_polygons', handle_slider_update)
Slider(2, x, y - 60, slider_length, 0.1, 1, 0.1, inner_length_factor, 'aperture', handle_slider_update)
Slider(3, x, y - 90, slider_length, 1, 100, 1, twists, 'twists', handle_slider_update)
Slider(4, x, y - 120, slider_length, 1, 5, 1, pen_size, 'pen_size', handle_slider_update)
Slider(5, x, y - 150, slider_length, 0.1, 1, 0.05, screen_radius_factor, 'size', handle_slider_update)
Slider(6, x, y - 180, screen_radius * 0.15, 0, 1, 1, 0, 'checkerboard', handle_slider_update)

draw()
