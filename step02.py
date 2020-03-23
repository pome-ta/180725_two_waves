from math import sin, pi
import ui


MAIN_COLOR = .256


class Sketch(ui.View):
  def __init__(self, parent):
    parent.add_subview(self)
    self.flex = 'WH'
    self.bg_color = 0
    self.time = 0
    self.time_div = 100
    self.update_interval = 1 / self.time_div
    
  def draw(self):
    ui.set_color(1)
    line = ui.Path()
    line.line_width = 8
    segment = 8
    amp = self.height/8
    for i in range(segment):
      x = (i/(segment-1)) *self.width
      radian = (i/segment) *pi + (self.time / self.time_div)
      y = amp *sin(radian) + self.height / 2
      if i: line.line_to(x, y)
      else: line.move_to(x, y)
    line.stroke()
  
  def update(self):
    self.set_needs_display()
    self.time += 1
  
  def get_size(self, frame):
    self.width = frame[2]
    self.height = frame[3]
    

class View(ui.View):
  def __init__(self):
    self.bg_color = MAIN_COLOR
    self.tint_color = MAIN_COLOR
    self.sketch = Sketch(self)
    
  def draw(self):
    self.sketch.get_size(self.frame)
    
  def layout(self):
    self.sketch.x = self.width / 2 - self.sketch.width / 2
    self.sketch.y = self.height / 2 - self.sketch.height / 2


v = View()
v.present(style='fullscreen')

