import math, time

class Vector2d(object):

	def __init__(self, x, y, z=0):
		self._x = x
		self._y = y
		self._z = z

	@property  # vec.length
	def length(self):
		return math.sqrt(self._x ** 2 + self._y ** 2)

	@property  # vec.length_comparison
	def length_comparison(self):
		return (self._x ** 2 + self._y ** 2)

	@property  # vec.x
	def x(self):
		return self._x

	@x.setter
	def x(self, value):
		assert type(value) in (int, float)
		return Vector2d(value, self._y)

	@property  # vec.y
	def y(self):
		return self._y

	@y.setter
	def y(self, value):
		assert type(value) in (int, float)
		return Vector2d(self._x, value)

	def __eq__(self, other):
		if self.x == other.x and self.y == other.y:
			return True
		else:
			return False

	def __add__(self, other):
		if type(other) is Vector2d:
			return Vector2d(self.x + other.x, self.y + other.y)
		else:
			assert type(other) in (int, float)
			return Vector2d(self.x + other, self.y + other)

	def __sub__(self, other):
		if type(other) is Vector2d:
			return Vector2d(self.x - other.x, self.y - other.y)
		else:
			assert type(other) in (int, float)
			return Vector2d(self.x - other, self.y - other)

	def __repr__(self):
		return "Vector2d({}, {})".format(self.x, self.y)

	def __mul__(self, scalar):
		return Vector2d(self.x * scalar, self.y * scalar)

	def __truediv__(self, scalar):
		return Vector2d(self.x / scalar, self.y / scalar)


class EulerAngle(object):

	def __init__(self, pitch, yaw, roll):
		self._pitch = pitch
		self._yaw = yaw
		self._roll = roll

	@property
	def pitch(self):
		return self._pitch

	@pitch.setter
	def pitch(self, value):
		assert type(value) in (int, float)
		return EulerAngle(value, self.yaw, self.roll)

	@property
	def yaw(self):
		return self._yaw

	@yaw.setter
	def yaw(self, value):
		assert type(value) in (int, float)
		return EulerAngle(self.pitch, value, self.roll)

	@property
	def roll(self):
		return self._roll

	@roll.setter
	def roll(self, value):
		assert type(value) in (int, float)
		return EulerAngle(self.pitch, self.yaw, value)

	def __eq__(self, other):
		assert type(other) is EulerAngle, "Comparison with types other than EulerAngle not supported."
		if self.pitch == other.pitch and self.yaw == other.yaw and self.roll == other.roll:
			return True
		else:
			return False

	def to_vector(self):
		""" obtain a vector from this EulerAngle. """
		return Vector2d(
			# Vx = cos(yaw) * cos(pitch)
			math.cos(self.yaw) * math.cos(self.pitch),
			# Vy = sin(pitch)
			math.sin(self.pitch),
			# Vz = sin(yaw) * cos(pitch) -- unused in 2D
			math.sin(self.yaw) * math.cos(self.pitch))

	def normalize(self):
		if self.pitch > 89.:
			self.pitch = 89.
		if self.pitch < -89.:
			self.pitch = -89.

		while self.yaw < -180.:
			self.yaw += 360.
		while self.yaw > 180.:
			self.yaw -= 360.


GRAVITY = Vector2d(0, -2)
TIME = time.clock()

def closest(a, opfor):
	"""
	Returns the next closest point in opfor to a.

	param a: a Vector2d object
	param opfor: a list of Vector2d objects to compare to `a`
	"""
	assert type(a) is Vector2d, "arg `a` MUST be a Vector2d."
	assert hasattr(opfor, '__contains__'), "arg2 MUST be an iterable of Vector2d objects."
	target = min([((a - i).length_comparison, i) for i in opfor])
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

def cross_product(a, b):
	assert type(a) is Vector2d, "arg `a` MUST be a Vector2d."
	assert type(b) is Vector2d, "arg `b` MUST be a Vector2d."
	return Vector2d(
		a.y * b.z - a.z * b.y,
		a.z * b.x - a.x * b.z,
		a.x * b.y - a.y * b.x)

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

def delta_time():
	global TIME
	newTime = time.clock()
	dt = newTime - TIME
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

def lerp(goal, current, dt):
	""" move to goal from current, by a distance of delta time."""
	diff = (goal - current).length
	if diff > dt:
		return current + dt
	if diff < -dt:
		return current - dt
	return goal
