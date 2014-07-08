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
	a = gm.Vector2d(1, 2)
	ops = []
	for i in range(100):
		ops.append(gm.Vector2d(random.randint(0, 100), random.randint(0, 100)))
	winner = gm.closest(a, ops)

def test_lerp():
	current = gm.Vector2d(0, 0)
	goal = gm.Vector2d(100, 100)

	move = gm.lerp(goal, current, gm.delta_time())
	assert_not_equal(move, current)
	assert_not_equal(move, goal)
	assert move.length_comparison > current.length_comparison
	assert move.length_comparison < goal.length_comparison
