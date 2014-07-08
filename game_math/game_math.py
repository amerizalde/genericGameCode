import math, time

class Vector2d(object):

	def __init__(self, x, y):
		self._x = x
		self._y = y

	@property  # vec.length
	def length(self):
		return math.sqrt(self._x ** 2 + self._y ** 2)

	@property  # vec.length2
	def length2(self):
		return (self._x ** 2 + self._y ** 2)

	@property
	def x(self):
		return self._x

	@x.setter
	def x(self, value):
		return Vector2d(value, self._y)

	@property
	def y(self):
		return self._y

	@y.setter
	def y(self, value):
		return Vector2d(self._x, value)

	def __eq__(self, other):
		if self.x == other.x and self.y == other.y:
			return True

	def __add__(self, other):
		return Vector2d(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return Vector2d(self.x - other.x, self.y - other.y)

	def __repr__(self):
		return "Vector2d({}, {})".format(self.x, self.y)

	def __mul__(self, scalar):
		return Vector2d(self.x * scalar, self.y * scalar)

	def __truediv__(self, scalar):
		return Vector2d(self.x / scalar, self.y / scalar)


GRAVITY = Vector2d(0, -2)
TIME = time.time()

def closest(a, opfor):
	"""
	Returns the next closest point in opfor to a.

	param a: a Vector2d object
	param opfor: a list of Vector2d objects to compare to `a`
	"""
	assert type(a) is Vector2d, "arg `a` MUST be a Vector2d."
	assert hasattr(opfor, '__contains__'), "arg2 MUST be an iterable of Vector2d objects."
	target = min([((a - i).length2, i) for i in opfor])
	return target[1]

def look(a, b):
	""" make `a` look at `b`. returns the normalized vector.
	param a: a Vector2d object
	param b: a Vector2d object
	"""
	assert type(a) is Vector2d, "arg `a` MUST be a Vector2d."
	assert type(b) is Vector2d, "arg `b` MUST be a Vector2d."
	c = b - a
	return c / c.length

def dot_product(a, b):
	"""
	param a: a Vector2d object
	param b: a Vector2d object
	"""
	assert type(a) is Vector2d, "arg `a` MUST be a Vector2d."
	assert type(b) is Vector2d, "arg `b` MUST be a Vector2d."
	# length of a * length of b * cos(theta)
	# (a.x * b.x) + (a.y * b.y)
	return a.x * b.x + a.y * b.y

def is_behind(a, b):
	""" is `a` behind `b`?
	param a: a Vector2d object
	param b: a Vector2d object
	"""
	assert type(a) is Vector2d, "arg `a` MUST be a Vector2d."
	assert type(b) is Vector2d, "arg `b` MUST be a Vector2d."
	normal = look(a, b)
	dotp = dot_product(a, normal)
	if dotp < -0.5:
		return True

def deltaTime():
	global TIME
	newTime = time.time()
	dt, TIME = newTime - TIME, newTime
	return .15 if dt > .15 else dt

def verlet(a, b, damper=1):
	""" verlet integration.
	Return a new Vector2d.
	"""
	assert type(a) is Vector2d, "arg `a` MUST be a Vector2d."
	assert type(b) is Vector2d, "arg `b` MUST be a Vector2d."
	assert 0 <= damper <= 1, "damper must be in 0..1 range."
	return (a - b) * damper

def attract(a, b):
	assert type(a) is Vector2d, "arg `a` MUST be a Vector2d."
	assert type(b) is Vector2d, "arg `b` MUST be a Vector2d."
	d = b - a
	x = d.x / d.length
	y = d.y / d.length
	verlet(a, Vector2d(x, y), .001)
