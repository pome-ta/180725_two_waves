from math import floor, sqrt
from random import random
import ui


class Grad:
 def __init__(self, x, y, z):
   self.x, self.y, self.z = x, y, z

 def dot2(self, x, y):
   return (self.x * x) + (self.y * y)

 def dot3(self, x, y, z):
   return (self.x * x) + (self.y * y) + (self.z * z)


class Noise:
 def __init__(self):
   self.grad3 = [Grad(1, 1, 0), Grad(-1, 1, 0), Grad(1, -1, 0),
Grad(-1, -1, 0),
                 Grad(1, 0, 1), Grad(-1, 0, 1), Grad(1, 0, -1),
Grad(-1, 0, -1),
                 Grad(0, 1, 1), Grad(0, -1, 1), Grad(0, 1, -1),
Grad(0, -1, -1)]

   self.p = [151, 160, 137, 91, 90, 15, 131, 13, 201, 95, 96, 53,
194, 233, 7, 225, 140, 36, 103, 30, 69, 142, 8, 99,
             37, 240, 21, 10, 23, 190, 6, 148, 247, 120, 234, 75, 0,
26, 197, 62, 94, 252, 219, 203, 117, 35, 11, 32,
             57, 177, 33, 88, 237, 149, 56, 87, 174, 20, 125, 136,
171, 168, 68, 175, 74, 165, 71, 134, 139, 48, 27,
             166, 77, 146, 158, 231, 83, 111, 229, 122, 60, 211, 133,
230, 220, 105, 92, 41, 55, 46, 245, 40, 244, 102,
             143, 54, 65, 25, 63, 161, 1, 216, 80, 73, 209, 76, 132,
187, 208, 89, 18, 169, 200, 196, 135, 130, 116,
             188, 159, 86, 164, 100, 109, 198, 173, 186, 3, 64, 52,
217, 226, 250, 124, 123, 5, 202, 38, 147, 118, 126,
             255, 82, 85, 212, 207, 206, 59, 227, 47, 16, 58, 17,
182, 189, 28, 42, 223, 183, 170, 213, 119, 248, 152,
             2, 44, 154, 163, 70, 221, 153, 101, 155, 167, 43, 172,
9, 129, 22, 39, 253, 19, 98, 108, 110, 79, 113,
             224, 232, 178, 185, 112, 104, 218, 246, 97, 228, 251,
34, 242, 193, 238, 210, 144, 12, 191, 179, 162, 241,
             81, 51, 145, 235, 249, 14, 239, 107, 49, 192, 214, 31,
181, 199, 106, 157, 184, 84, 204, 176, 115, 121,
             50, 45, 127, 4, 150, 254, 138, 236, 205, 93, 222, 114,
67, 29, 24, 72, 243, 141, 128, 195, 78, 66, 215,
             61, 156, 180]

   self.perm = list([None] * 512)
   self.gradP = list([None] * 512)
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

 def simplex2(self, xin, yin):
   s = (xin + yin) * self.f2
   i = floor(xin + s)
   j = floor(yin + s)
   t = (i + j) * self.g2
   x0 = xin - i + t
   y0 = yin - j + t
   if x0 > y0:
     i1 = 1
     j1 = 0
   else:
     i1 = 0
     j1 = 1
   x1 = x0 - i1 + self.g2
   y1 = y0 - j1 + self.g2
   x2 = x0 - 1 + 2 * self.g2
   y2 = y0 - 1 + 2 * self.g2
   i &= 255
   j &= 255
   gi0 = self.gradP[i + self.perm[j]]
   gi1 = self.gradP[i + i1 + self.perm[j + j1]]
   gi2 = self.gradP[i + 1 + self.perm[j + 1]]
   t0 = 0.5 - (x0 * x0) - (y0 * y0)
   if t0 < 0:
     n0 = 0
   else:
     t0 *= t0
     n0 = t0 * t0 * gi0.dot2(x0, y0)
   t1 = 0.5 - (x1 * x1) - (y1 * y1)
   if t1 < 0:
     n1 = 0
   else:
     t1 *= t1
     n1 = t1 * t1 * gi1.dot2(x1, y1)
   t2 = 0.5 - (x2 * x2) - (y2 * y2)
   if t2 < 0:
     n2 = 0
   else:
     t2 *= t2
     n2 = t2 * t2 * gi2.dot2(x2, y2)
   return 70 * (n0 + n1 + n2)

 def simplex3(self, xin, yin, zin):
   s = (xin + yin + zin) * self.f3
   i = floor(xin + s)
   j = floor(yin + s)
   k = floor(zin + s)
   t = (i + j + k) * self.g3
   x0 = xin - i + t
   y0 = yin - j + t
   z0 = zin - k + t
   if x0 >= y0:
     if y0 >= z0:
       i1, j1, k1 = 1, 0, 0
       i2, j2, k2 = 1, 1, 0
     elif x0 >= z0:
       i1, j1, k1 = 1, 0, 0
       i2, j2, k2 = 1, 0, 1
     else:
       i1, j1, k1 = 0, 0, 1
       i2, j2, k2 = 1, 0, 1
   else:
     if y0 < z0:
       i1, j1, k1 = 0, 0, 1
       i2, j2, k2 = 0, 1, 1
     elif x0 < z0:
       i1, j1, k1 = 0, 1, 0
       i2, j2, k2 = 0, 1, 1
     else:
       i1, j1, k1 = 0, 1, 0
       i2, j2, k2 = 1, 1, 0
   x1 = x0 - i1 + self.g3
   y1 = y0 - j1 + self.g3
   z1 = z0 - k1 + self.g3
   x2 = x0 - i2 + 2 * self.g3
   y2 = y0 - j2 + 2 * self.g3
   z2 = z0 - k2 + 2 * self.g3
   x3 = x0 - 1 + 3 * self.g3
   y3 = y0 - 1 + 3 * self.g3
   z3 = z0 - 1 + 3 * self.g3
   i &= 255
   j &= 255
   k &= 255
   gi0 = self.gradP[i + self.perm[j + self.perm[k]]]
   gi1 = self.gradP[i + i1 + self.perm[j + j1 + self.perm[k + k1]]]
   gi2 = self.gradP[i + i2 + self.perm[j + j2 + self.perm[k + k2]]]
   gi3 = self.gradP[i + 1 + self.perm[j + 1 + self.perm[k + 1]]]
   t0 = 0.6 - x0 * x0 - y0 * y0 - z0 * z0
   if t0 < 0:
     n0 = 0
   else:
     t0 *= t0
     n0 = t0 * t0 * gi0.dot3(x0, y0, z0)
   t1 = 0.6 - x1 * x1 - y1 * y1 - z1 * z1
   if t1 < 0:
     n1 = 0
   else:
     t1 *= t1
     n1 = t1 * t1 * gi1.dot3(x1, y1, z1)
   t2 = 0.6 - x2 * x2 - y2 * y2 - z2 * z2
   if t2 < 0:
     n2 = 0
   else:
     t2 *= t2
     n2 = t2 * t2 * gi2.dot3(x2, y2, z2)
   t3 = 0.6 - x3 * x3 - y3 * y3 - z3 * z3
   if t3 < 0:
     n3 = 0
   else:
     t3 *= t3
     n3 = t3 * t3 * gi3.dot3(x3, y3, z3)
   return 32 * (n0 + n1 + n2 + n3)

 def fade(self, t):
   return t * t * t * (t * (t * 6 - 15) + 10)

 def lerp(self, a, b, t):
   return (1 - t) * a + t * b

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
   lerp = self.lerp(self.lerp(n00, n10, u), self.lerp(n01, n11, u),
self.fade(y))
   return lerp

 def perlin3(self, x, y, z):
   X = floor(x)
   x = x - X
   X = X & 255
   Y = floor(y)
   y = y - Y
   Y = Y & 255
   Z = floor(z)
   z = z - Z
   Z = Z & 255
   n000 = self.gradP[X + self.perm[Y + self.perm[Z]]].dot3(x, y, z)
   n001 = self.gradP[X + self.perm[Y + self.perm[Z + 1]]].dot3(x, y, z - 1)
   n010 = self.gradP[X + self.perm[Y + 1 + self.perm[Z]]].dot3(x, y - 1, z)
   n011 = self.gradP[X + self.perm[Y + 1 + self.perm[Z + 1]]].dot3(x,
y - 1, z - 1)
   n100 = self.gradP[X + 1 + self.perm[Y + self.perm[Z]]].dot3(x - 1, y, z)
   n101 = self.gradP[X + 1 + self.perm[Y + self.perm[Z + 1]]].dot3(x
- 1, y, z - 1)
   n110 = self.gradP[X + 1 + self.perm[Y + 1 + self.perm[Z]]].dot3(x
- 1, y - 1, z);
   n111 = self.gradP[X + 1 + self.perm[Y + 1 + self.perm[Z +
1]]].dot3(x - 1, y - 1, z - 1)
   u = self.fade(x)
   v = self.fade(y)
   w = self.fade(z)
   lerp = self.lerp(self.lerp(self.lerp(n000, n100, u),
self.lerp(n001, n101, u), w),
                    self.lerp(self.lerp(n010, n110, u),
self.lerp(n011, n111, u), w), v)
   return lerp


MAIN_COLOR = .256


class Sketch(ui.View):
  def __init__(self, parent):
    parent.add_subview(self)
    self.flex = 'WH'
    self.bg_color = 0
    self.time = 0
    self.time_div = 400
    self.update_interval = 1 / (self.time_div /4)
    self.noise = Noise()
    self.noise.set_seed(random())
    
  def draw(self):
    self.set_needs_display()
    ui.set_color(1)
    line = ui.Path()
    line.line_width = 8
    segment = 128
    amp = self.height/8
    for i in range(segment):
      x = (i/(segment-1)) *self.width
      px = i/32
      py = self.time / self.time_div
      y = amp *self.noise.perlin2(px, py) + self.height / 2
      if i: line.line_to(x, y)
      else: line.move_to(x, y)
    line.stroke()
  
  def update(self):
    self.draw()
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

