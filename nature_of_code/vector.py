import math

class Vector(object):
    damping = 0.001
    def __init__(self, x=None, y=None):
        self.x = x or 0
        self.y = y or 0

    def integrate(self, vector):
        """ verlet integration """
        self.x += (self.x - vector.x) * self.damping
        self.y += (self.y - vector.y) * self.damping

    def attract(self, vector):
        """ attraction """
        vx, vy = vector.x, vector.y
        dx = vector.x - self.x
        dy = vector.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        vx += dx / distance
        vy += dx / distance
        self.integrate(Vector(vx, vy))
