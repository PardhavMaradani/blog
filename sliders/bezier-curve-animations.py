# https://pardhav-m.blogspot.com/2020/07/sliders.html
# Sliders
# Bézier curve animations
import turtle
from _slider import Slider
from _bezier_curve_animation import update_t, update_n_control_points

# handle slider updates
def handle_slider_update(id, value):
  if id == 0:
    update_t(value)
  elif id == 1:
    update_n_control_points(value)

screen = turtle.Screen()
wh = screen.window_height()
ww = 1.5 * wh
x = -ww/2 + 20
y = wh/2 - 20
screen_radius = wh / 2

default_t = 0.5
default_n_cps = 3
slider_length = screen_radius * 0.6

# create sliders
Slider(0, x, y, slider_length, 0, 1, 0.05, default_t, 't', handle_slider_update)
Slider(1, x, y - 30, slider_length, 3, 8, 1, default_n_cps, 'control_points', handle_slider_update)

# update with default slider values
update_t(default_t)
update_n_control_points(default_n_cps)
