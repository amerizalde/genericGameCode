import random
import game_math as gm
from nose.tools import *

def setup():
	print("Setup!")

def teardown():
	print("Tear down!")

def test_basic():
	print("I ran!")

def test_addition():
	a = gm.Vector2d(1, 2)
	b = gm.Vector2d(2, 3)
	c = a + b
	assert_equal(c, gm.Vector2d(3, 5))

def test_subtraction():
	a = gm.Vector2d(1, 2)
	b = gm.Vector2d(2, 3)
	c = a - b
	assert_equal(c, gm.Vector2d(-1, -1))

def test_scalar():
	a = gm.Vector2d(1, 2)
	c = a * 5
	assert_equal(c, gm.Vector2d(5, 10))
	assert_equal(c.length, a.length * 5)

	a = gm.Vector2d(10, 20)
	c = a / 5
	assert_equal(c, gm.Vector2d(2.0, 4.0))
	assert_equal(c.length, a.length / 5)

def test_look():
	a = gm.Vector2d(1, 2)
	b = gm.Vector2d(2, 3)
	normal = gm.look(a, b)
	assert_true(-1 <= normal.x <= 1, normal.x)
	assert_true(-1 <= normal.y <= 1, normal.y)
	assert_equal(round(normal.length), 1, normal.length)

def test_closest():
	# Unfinished test
	a = gm.Vector2d(1, 2)
	ops = []
	for i in range(100):
		ops.append(gm.Vector2d(random.randint(0, 100), random.randint(0, 100)))
	winner = gm.closest(a, ops)

def test_lerp():
	start = gm.Vector2d(0, 1.)
	goal = gm.Vector2d(100, 100)

	def approach(steps):
		move = gm.lerp(goal, start, gm.delta_time())
		while steps:
			move = gm.lerp(goal, move, gm.delta_time())
			steps -= 1
		return move

	current = approach(5)
	assert_not_equal(current, start)
	assert current.length_comparison > start.length_comparison

	start, goal = goal, start
	current = approach(5)
	assert_not_equal(current, start)
	assert current.length_comparison > start.length_comparison
