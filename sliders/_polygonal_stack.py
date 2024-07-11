import turtle
import math

# screen setup
screen = turtle.Screen()
wh = screen.window_height()  # window height
ww = 1.5 * wh                # window width
# trinket returns the same window width and height (hence square)
# set it to a rectangular area
screen.setup(ww, wh)
screen_radius = wh / 2
top_clip_window = [(-ww/2, wh/2), (-ww/2, 0), (ww/2, 0), (ww/2, wh/2)]      # top half
bottom_clip_window = [(-ww/2, 0), (-ww/2, -wh/2), (ww/2, -wh/2), (ww/2, 0)] # bottom half

# turtle setup
t = turtle.Turtle()
t.ht()
t.speed(0)
t.tracer(0)

# draw a border
def draw_border():
  t = turtle.Turtle()
  t.ht()
  t.speed(0)
  t.pu()
  t.goto(-ww/2, -wh/2)
  t.pd()
  t.goto(ww/2, -wh/2)
  t.goto(ww/2, wh/2)
  t.goto(-ww/2, wh/2)
  t.goto(-ww/2, -wh/2)

# regular polygon shape functions from https://www.mathsisfun.com/geometry/regular-polygons.html
def shape_radius(sides, length):
  return length / (2 * math.sin(math.pi / sides))

def shape_apothem(sides, length):
  return shape_radius(sides, length) * math.cos(math.pi / sides)

def shape_length(sides, radius):
  return 2 * radius * math.sin(math.pi / sides)

# get inner polygon to draw
# sides - number of sides
# cx, cy - center
# length - length of side
# xangle - angle wrt x axis
def get_polygon(sides, cx, cy, length, xangle):
  radius = shape_radius(sides, length)
  t.pu()
  t.goto(cx, cy)
  t.seth(270)  # point down
  t.right(math.degrees(math.pi / sides))
  t.fd(radius)
  sx, sy = t.pos()  # left most starting point
  # get the rotated starting point
  # see https://stackoverflow.com/questions/2259476/rotating-a-point-about-another-point-2d
  sx -= cx
  sy -= cy
  s = math.sin(math.radians(xangle))
  c = math.cos(math.radians(xangle))
  rsx = cx + (sx * c - sy * s)
  rsy = cy + (sx * s + sy * c)
  t.goto(rsx, rsy)  # goto rotated starting point
  t.seth(xangle)  # rotate turtle to start angle
  # draw each side
  polygon = []
  for s in range(sides):
    polygon.append(t.pos())
    t.fd(length)
    t.left(360 / sides)
  t.goto(cx, cy)
  t.pd()
  return polygon

# fill a polygon
# polygon - vertices of polygon to fill
# color - fill color
# pen_size - pen size to draw outline
# index - polygon index
# checkerboard - whether to fill alternatively
def fill_polygon(polygon, color, pen_size):
  # first fill white  
  t.pensize(1)
  t.color(color)
  for i, v in enumerate(polygon):
    if i == 0:
      t.pu()
      t.goto(v)
      t.pd()
      t.begin_fill()
    else:
      t.goto(v)
  t.end_fill()
  # now draw outline except intersecting line on x axis
  t.pensize(pen_size)
  t.color('black')
  for i, v1 in enumerate(polygon):
    v2 = polygon[(i + 1) % len(polygon)]
    if i == 0:
      t.pu()
      t.goto(v1)
      t.pd()
    _, y1 = v1  
    _, y2 = v2  
    if y1 == 0 and y2 == 0:
      t.pu()
    t.goto(v1)
    t.goto(v2)
    if y1 == 0 and y2 == 0:
      t.pd()

# get intersecting polygon
# Code from: https://rosettacode.org/wiki/Sutherland-Hodgman_polygon_clipping#Python
# Referred from: https://stackoverflow.com/questions/37555770/control-shape-overlap-in-pythons-turtle
# subjectPolygon - polygon to be clipped
# clipPolygon - clipping window
def clip(subjectPolygon, clipPolygon):
  def inside(p):
    return(cp2[0]-cp1[0])*(p[1]-cp1[1]) > (cp2[1]-cp1[1])*(p[0]-cp1[0])
 
  def computeIntersection():
    dc = [ cp1[0] - cp2[0], cp1[1] - cp2[1] ]
    dp = [ s[0] - e[0], s[1] - e[1] ]
    n1 = cp1[0] * cp2[1] - cp1[1] * cp2[0]
    n2 = s[0] * e[1] - s[1] * e[0] 
    n3 = 1.0 / (dc[0] * dp[1] - dc[1] * dp[0])
    return ((n1*dp[0] - n2*dc[0]) * n3, (n1*dp[1] - n2*dc[1]) * n3)
 
  outputList = subjectPolygon
  cp1 = clipPolygon[-1]

  for clipVertex in clipPolygon:
    cp2 = clipVertex
    inputList = outputList
    outputList = []
    s = inputList[-1]
 
    for subjectVertex in inputList:
      e = subjectVertex
      if inside(e):
        if not inside(s):
          outputList.append(computeIntersection())
        outputList.append(e)
      elif inside(s):
        outputList.append(computeIntersection())
      s = e
    cp1 = cp2
  return(outputList)

# draw on outer polygon
# half - which half of the screen
# o_sides - outer sides
# o_length - outer side length
# i_sides - inner sides
# i_length - inner side length
# i_p_m - inner polygons multiple
# twists - number of twists
# ra - base rotate angle wrt x axis
# pen_size - pen size
# checkerboard - whether to fill alternatively
def draw_on_outer_polygon(half, o_sides, o_length, i_sides, i_length, i_p_m, twists, ra, pen_size, checkerboard):
  o_radius = shape_radius(o_sides, o_length)
  i_radius = shape_radius(i_sides, i_length)
  t.pu()
  t.goto(ww/6, 0)
  t.seth(270)  # point down
  t.right(math.degrees(math.pi / o_sides))
  t.fd(o_radius)
  t.seth(0)  # rotate turtle to start angle
  # skip so we start on correct side
  skip = 0 if half == 'top' else math.ceil(o_sides / 2)
  for i in range(skip):
    t.fd(o_length)
    t.left(360 / o_sides)
  t.pd()
  # draw along each side of outer polygon
  for s in range(o_sides):
    delta = o_length / i_p_m
    delta_angle = ((360 / i_sides) / i_p_m) * twists
    # draw each inner polygon
    for i in range(i_p_m):
      t.pu()
      t.fd(delta)
      t.pd()
      fillcolor = 'white'
      if checkerboard:
        fillcolor = 'white' if i % 2 == 0 else 'gray'
      # save starting center
      cx, cy = t.pos()
      sh = t.heading()
      # check if this polygon will be visible or needs intersection
      visible = False
      should_check_intersection = False
      if half == 'top':
        if cy > i_radius:
          visible = True
        elif cy >= -i_radius:
          should_check_intersection = True          
      else:
        if cy < -i_radius:
          visible = True
        elif cy <= i_radius:
          should_check_intersection = True
      # get the polygon only if will be drawn
      if visible or should_check_intersection:
        polygon = get_polygon(i_sides, cx, cy, i_length, ra + (delta_angle * i))
      else:
        continue
      # draw and fill inner polygon
      if visible:
        fill_polygon(polygon, fillcolor, pen_size)
      elif should_check_intersection:
        ip = None
        try:
          clip_window = top_clip_window if half == 'top' else bottom_clip_window
          ip = clip(polygon, clip_window)
        except (IndexError, ZeroDivisionError):
          pass
        if ip is not None:
          fill_polygon(ip, fillcolor, pen_size)
      # go back to starting center
      t.pu()
      t.goto(cx, cy)
      t.seth(sh)
      t.pd()
    t.left(360 / o_sides)

# draw polygonal stack
def draw_polygonal_stack(
  outer_sides,
  inner_sides,
  inner_polygons_multiple,
  inner_length_factor,
  twists,
  pen_size,
  screen_radius_factor,
  checkerboard):
  # calculate radius and lengths wrt screen size
  outer_radius = (screen_radius * screen_radius_factor) /  (1 + inner_length_factor * math.cos(math.pi / outer_sides))
  outer_length = shape_length(outer_sides, outer_radius)
  inner_radius = shape_apothem(outer_sides, outer_length)
  inner_length = shape_length(inner_sides, inner_radius) * inner_length_factor
  # draw stack
  t.clear()
  # draw top half
  draw_on_outer_polygon('top', outer_sides, outer_length, inner_sides, inner_length, inner_polygons_multiple, twists, 0, pen_size, checkerboard)
  # draw bottom half
  draw_on_outer_polygon('bottom', outer_sides, outer_length, inner_sides, inner_length, inner_polygons_multiple, twists, 0, pen_size, checkerboard)
  t.update()

# main

draw_border()
