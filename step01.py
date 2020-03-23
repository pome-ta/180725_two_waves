import ui


MAIN_COLOR = .256


class Sketch(ui.View):
  def __init__(self, parent):
    parent.add_subview(self)
    self.flex = 'WH'
    self.bg_color = 0
    
  def draw(self):
    ui.set_color(1)
    line = ui.Path()
    line.line_width = 8
    line.move_to(0, self.height / 2)
    line.line_to(self.width, self.height / 2)
    line.stroke()
  
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

