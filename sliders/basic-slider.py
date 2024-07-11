# https://pardhav-m.blogspot.com/2020/07/sliders.html
# sliders
# Basic Slider
import turtle
from _slider import Slider

# screen setup
screen = turtle.Screen()
wh = screen.window_height()  # window height
ww = 1.5 * wh  # window width
# trinket returns the same window width and height (hence square)
# set it to a rectangular area
screen.setup(ww, wh)
screen.tracer(0)
screen_radius = wh / 2

def handle_slider_update(id, value):
  print(id, value)

x = -ww/2 + 20
y = wh/2 - 20

slider_length = screen_radius * 0.8
Slider(0, x, y, slider_length, 5, 50, 5, 25, 'value 1', handle_slider_update)
Slider(1, x, y - 30, slider_length, 0, 1, 0.05, 0.25, 'value 2', handle_slider_update)

screen.update()
