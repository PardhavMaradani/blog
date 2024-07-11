import turtle

# Interactive Seed Class
class Seed(turtle.Turtle):
  def __init__(self, id = 0, x = 0, y = 0, bounding_box = None, callback = None):
    turtle.Turtle.__init__(self)
    self.id = id
    self.clicked = False
    self.dragging = False
    self.is_playing = None
    self.bounding_box = bounding_box
    self.callback = callback
    self.speed(0)
    self.pu()
    self.goto(x, y)
    # self.fd(10)
    # self.write("s" + str(self.id))
    # self.bk(10)
    # click/release/drag handlers
    self.onclick(self.onclick_handler)
    self.onrelease(self.onrelease_handler)
    self.ondrag(self.ondrag_handler)
    self.update()

  # handle click
  def onclick_handler(self, x, y):
    if not self.isvisible():
      return
    self.clicked = True

  # handle release
  def onrelease_handler(self, x, y):
    self.clicked = False

  # handle drag
  def ondrag_handler(self, x, y):
    if not self.clicked or self.dragging:
      return
    gap = 6
    (bb_minx, bb_miny, bb_maxx, bb_maxy) = self.bounding_box
    if not (x >= bb_minx + gap and x <= bb_maxx - gap and y >= bb_miny + gap and y <= bb_maxy - gap):
      self.clicked = False      
      return
    self.dragging = True
    self.clear()
    self.goto(x, y)
    # self.fd(10)
    # self.write("s" + str(self.id))
    # self.bk(10)
    if self.callback:
      self.callback(self.id)
    self.update()
    self.dragging = False

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
