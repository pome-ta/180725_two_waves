from math import floor, sqrt
from random import random
from colorsys import hls_to_rgb
import ui


class Grad:
  def __init__(self, x, y, z):
    self.x, self.y, self.z = x, y, z
  
  def dot2(self, x, y):
    return self.x *x + self.y *y
  
  def dot3(self, x, y, z):
    return self.x *x + self.y *y + self.z *z


class Noise:
  def __init__(self):
    self.grad3 = [Grad(1, 1, 0), Grad(-1, 1, 0), Grad(1, -1, 0), Grad(-1, -1, 0), Grad(1, 0, 1), Grad(-1, 0, 1), Grad(1, 0, -1), Grad(-1, 0, -1), Grad(0, 1, 1), Grad(0, -1, 1), Grad(0, 1, -1), Grad(0, -1, -1)]
    
    self.p = [151, 160, 137, 91, 90, 15, 131, 13, 201, 95, 96, 53, 194, 233, 7, 225, 140, 36, 103, 30, 69, 142, 8, 99, 37, 240, 21, 10, 23, 190, 6, 148, 247, 120, 234, 75, 0, 26, 197, 62, 94, 252, 219, 203, 117, 35, 11, 32, 57, 177, 33, 88, 237, 149, 56, 87, 174, 20, 125, 136, 171, 168, 68, 175, 74, 165, 71, 134, 139, 48, 27, 166, 77, 146, 158, 231, 83, 111, 229, 122, 60, 211, 133, 230, 220, 105, 92, 41, 55, 46, 245, 40, 244, 102, 143, 54, 65, 25, 63, 161, 1, 216, 80, 73, 209, 76, 132, 187, 208, 89, 18, 169, 200, 196, 135, 130, 116, 188, 159, 86, 164, 100, 109, 198, 173, 186, 3, 64, 52, 217, 226, 250, 124, 123, 5, 202, 38, 147, 118, 126, 255, 82, 85, 212, 207, 206, 59, 227, 47, 16, 58, 17, 182, 189, 28, 42, 223, 183, 170, 213, 119, 248, 152, 2, 44, 154, 163, 70, 221, 153, 101, 155, 167, 43, 172, 9, 129, 22, 39, 253, 19, 98, 108, 110, 79, 113, 224, 232, 178, 185, 112, 104, 218, 246, 97, 228, 251, 34, 242, 193, 238, 210, 144, 12, 191, 179, 162, 241, 81, 51, 145, 235, 249, 14, 239, 107, 49, 192, 214, 31, 181, 199, 106, 157, 184, 84, 204, 176, 115, 121, 50, 45, 127, 4, 150, 254, 138, 236, 205, 93, 222, 114, 67, 29, 24, 72, 243, 141, 128, 195, 78, 66, 215, 61, 156, 180]
    
    self.perm = list([None] *512)
    self.gradP = list([None] *512)
    self.set_seed(0)
    self.f2 = 0.5 * (sqrt(3) - 1)
    self.g2 = (3 - sqrt(3)) / 6
    self.f3 = 1 / 3
    self.g3 = 1 / 6
    
  def set_seed(self, seed):
    if seed > 0 and seed < 1:
      seed *= 65536
    seed = floor(seed)
    if seed < 256:
      seed |= seed << 8
    for i in range(256):
      if i & 1:
        v = self.p[i] ^ (seed & 255)
      else:
        v = self.p[i] ^ ((seed >> 8) & 255)
      self.perm[i] = self.perm[i + 256] = v
      self.gradP[i] = self.gradP[i + 256] = self.grad3[v % 12]
  
  def fade(self, t):
    return t *t *t *(t *(t *6 - 15) + 10)
  
  def lerp(self, a, b, t):
    return (1 - t) *a + t *b
    
  def perlin2(self, x, y):
    X = floor(x)
    x = x - X
    X = X & 255
    Y = floor(y)
    y = y - Y
    Y = Y & 255
    n00 = self.gradP[X + self.perm[Y]].dot2(x, y)
    n01 = self.gradP[X + self.perm[Y + 1]].dot2(x, y - 1)
    n10 = self.gradP[X + 1 + self.perm[Y]].dot2(x - 1, y)
    n11 = self.gradP[X + 1 + self.perm[Y + 1]].dot2(x - 1, y - 1)
    u = self.fade(x)
    lerp = self.lerp(self.lerp(n00, n10, u), self.lerp(n01, n11, u), self.fade(y))
    return lerp


MAIN_COLOR = .256


class Sketch(ui.View):
  def __init__(self, parent):
    parent.add_subview(self)
    self.flex = 'WH'
    self.bg_color = 0
    self.time = 0
    self.time_div = 100
    self.update_interval = 1 / (self.time_div /4)
    self.noise = Noise()
    self.noise.set_seed(random())
    
  def draw(self):
    line_num = 80
    segment = 92
    amp = self.height/8
    for j in range(line_num):
      line = ui.Path()
      line.line_width = 1
      for i in range(segment):
        x = (i/(segment-1)) *self.width
        px = i/(32 + j)
        py = j/40 + (self.time / self.time_div)
        y = amp *self.noise.perlin2(px, py) + self.height / 2
        if i: line.line_to(x, y)
        else: line.move_to(x, y)
      h = j/line_num
      rgb = hls_to_rgb(h, h, 1)
      ui.set_color(rgb)
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

