import turtle

# register square thumb shape
thumb_size = 7
screen = turtle.Screen()
screen.register_shape('thumb', ((-thumb_size, -thumb_size), (thumb_size, -thumb_size), (thumb_size, thumb_size), (-thumb_size, thumb_size)))

# Slider Class
class Slider(turtle.Turtle):
  def __init__(self, id, x, y, length, min, max, step, initial_value, label, callback):
    turtle.Turtle.__init__(self)
    self.shape('thumb')
    self.speed(0)
    self.id = id
    self.x = x
    self.y = y
    self.length = length
    self.min = min
    self.step = step
    self.label = label
    self.callback = callback
    self.clicked = False
    self.dragging = False
    self.steps = (max - min) / step
    # draw slider line
    self.pu()
    self.goto(x, y)
    self.pd()
    self.fd(length)
    # turtle to write label text and value
    self.lt = turtle.Turtle()
    self.lt.speed(0)
    self.lt.pu()
    self.lt.goto(self.pos())
    self.lt.fd(20)
    self.lt.right(90)
    self.lt.fd(thumb_size/2)
    self.lt.ht()
    # move thumb to initial position
    self.bk(length)
    initial_length = length * ((initial_value - min) / (max - min))
    self.fd(initial_length)
    self.value = initial_value
    # update label
    self.update_label()
    # register mouse handlers
    self.onclick(self.onclick_handler)
    self.onrelease(self.onrelease_handler)
    self.ondrag(self.ondrag_handler)

  # write label text and value    
  def update_label(self):
    self.lt.clear()
    self.lt.write(self.label + ' = ' + str(self.value), font=("Arial", 10, "normal"))
  
  # get value based on slider position
  def get_value(self, x):
    unit_value = (x - self.x) / self.length
    v1 = unit_value * self.steps * self.step
    v1 = int(v1 / self.step) * self.step
    return self.min + v1

  # onclick handler
  def onclick_handler(self, x, y):
    self.clicked = True

  # onrelease handler
  def onrelease_handler(self, x, y):
    self.clicked = False

  # ondrag handler
  def ondrag_handler(self, x, y):
    if not self.clicked:
      return
    if self.dragging:
      return
    # stop drag if mouse moves away in y direction
    if abs(y - self.y) > 20:
      self.clicked = False
      self.dragging = False
      self.callback(self.id, self.value)
      return
    self.dragging = True
    # limit drag within the slider
    if x < self.x:
      x = self.x
    if x > self.x + self.length:
      x = self.x + self.length
    # move thumb to new position
    self.goto(x, self.y)
    new_value = self.get_value(x)
    # call the callback function if value changes
    if new_value != self.value:
      self.value = new_value
      self.update_label()
      self.callback(self.id, self.value)
    self.update()
    self.dragging = False
