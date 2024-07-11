import math

# Source: https://algorithmtutor.com/Computational-Geometry/Area-of-a-polygon-given-a-set-of-points/
# Shoelace formula to calculate the area of a polygon
# the points must be sorted anticlockwise (or clockwise)
def polygon_area(vertices):
    psum = 0
    nsum = 0
    for i in range(len(vertices)):
        sindex = (i + 1) % len(vertices)
        prod = vertices[i][0] * vertices[sindex][1]
        psum += prod
    for i in range(len(vertices)):
        sindex = (i + 1) % len(vertices)
        prod = vertices[sindex][0] * vertices[i][1]
        nsum += prod
    return abs(1/2*(psum - nsum))

# get centroid of polygon
# Source: https://bell0bytes.eu/centroid-convex/
def get_polygon_centroid(polygon):
  centroidX = 0
  centroidY = 0
  det = 0
  j = 0
  nVertices = len(polygon)
  for i in range(nVertices):
    if (i + 1 == nVertices):
       j = 0
    else:
      j = i + 1
    x1, y1 = polygon[i]
    x2, y2 = polygon[j]
    tempDet = x1 * y2 - x2 * y1
    det += tempDet
    centroidX += (x1 + x2) * tempDet
    centroidY += (y1 + y2) * tempDet  

  centroidX = centroidX / (3 * det)
  centroidY = centroidY / (3 * det)
  return (centroidX, centroidY)

# draw polygon whirls recursively
def _draw_polygon_whirl(level, t, polygon, offset_factor, gradient, rgb_multiples):
  max_levels = 500 if gradient else 250
  # limit levels
  if level > max_levels:
    return
  min_area = 50 if gradient else 100
  # limit area
  if polygon_area(polygon) < min_area:
    return
  gap = 10 if gradient else 50
  # draw current polygon
  for i, v in enumerate(polygon):
    if i == 0:
      t.pu()
      if gradient:
        r = level * 1.05
        m1, m2, m3 = rgb_multiples
        t.color(r*m1, r*m2, r*m3)
    t.goto(v)
    if i == 0:
      t.pd()
  # create new polygon verties
  new_polygon = []
  for i, p0 in enumerate(polygon):
    if i == len(polygon) - 1:
      i = 0
    p1 = polygon[i + 1]
    x0, y0 = p0
    x1, y1 = p1
    D = math.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0))
    d = gap * offset_factor
    x2 = x0 + (d / D) * (x1 - x0)
    y2 = y0 + (d / D) * (y1 - y0)
    new_polygon.append((x2, y2))
  # recursively call with new polygon
  _draw_polygon_whirl(level + 1, t, new_polygon, offset_factor, gradient, rgb_multiples)

# draw polygon concentric recursively
def _draw_polygon_concentric(level, t, center, polygon, offset_factor, equidistant, gradient, rgb_multiples):
  max_levels = 1000 if gradient else 250
  # limit levels
  if level > max_levels:
    return
  min_area = 50 if gradient else 100
  # limit area
  if polygon_area(polygon) < min_area:
    return
  m = 1
  if equidistant:
    m = level
  # draw current polygon
  for i, v in enumerate(polygon):
    if i == 0:
      t.pu()
      if gradient:
        r = 10 + (level)*0.25
        m1, m2, m3 = rgb_multiples
        t.color(r*m1, r*m2, r*m3)
    t.goto(v)
    if i == 0:
      t.pd()
  # create new polygon verties
  new_polygon = []
  for i, p0 in enumerate(polygon):
    if i == len(polygon) - 1:
      i = 0
    p1 = center
    x0, y0 = p0
    x1, y1 = p1
    x2 = x0 + offset_factor * m * (x1 - x0)
    y2 = y0 + offset_factor * m * (y1 - y0)
    new_polygon.append((x2, y2))
  # recursively call with new polygon
  _draw_polygon_concentric(level + 1, t, center, new_polygon, offset_factor, equidistant, gradient, rgb_multiples)

def draw_polygon_whirl(t, polygon, offset_factor, gradient = False, rgb_multiples = (1, 2, 3)):
  _draw_polygon_whirl(0, t, polygon, offset_factor, gradient, rgb_multiples)

def draw_polygon_concentric(t, polygon, offset_factor, equidistant = False, gradient = False, rgb_multiples = (1, 2, 3)):
  center = get_polygon_centroid(polygon)
  if gradient:
    equidistant = True
    offset_factor = 0.00001
  _draw_polygon_concentric(0, t, center, polygon, offset_factor, equidistant, gradient, rgb_multiples)
