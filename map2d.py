import debug_print, pprint, math, random


def Map(size, tile):
	""" 
		Create a two dimensional level of size x size.
		The key to the contents of each tile is a tuple.
	"""
	level = {}
	i = 0
	while i < size:
		j = 0
		while j < size:
			level[i, j] = tile  # change to a Tile class default later
			j += 1
		i += 1
	return level

def DrunkWalk(level, position=(0, 0), stepsToWalk=0, drop=0):
	"""
		Drunkard Walk algorithm.
		Starting at "position", walk around "level" for
		"stepsToWalk", and change tile to == "drop".
	"""
	# bounds = [0, math.sqrt(len(level))]
	bowl = [0, -1, 1]
	# don't wanna be walking around forever!
	if stepsToWalk >= len(level):
		print "Too many steps, not enough tiles! Reducing steps to 1 below level size."
		stepsToWalk = len(level) - 1

	while stepsToWalk > 0:
		level[position] = drop
		# make two choices, 1 for x, 1 for y.
		x = random.choice(bowl)
		y = random.choice(bowl)
		new_position = (position[0] + x, position[1] + y)
		if new_position in level:
			position = new_position
		stepsToWalk -= 1

def TipsyWalk(level, position=(0, 0), stepsToWalk=0, drop=0):
	"""
		Modified Drunkard Walk algorithm.
		Starting at "position", walk around "level" for
		"stepsToWalk", and change tile to == "drop". This
		version does not walk over tiles that are already
		 == to "drop".
	"""
	bounds = int(math.sqrt(len(level)))
	# print "Steps left: {}".format(stepsToWalk)
	bowl = [0, -1, 1]

	# don't wanna be walking around forever!
	if stepsToWalk >= len(level):
		print "Too many steps, not enough tiles! Reducing steps to 5 below level size."
		stepsToWalk = len(level) - 5

	# 0 - are we done walking?
	if stepsToWalk > 0:
		# 1 - change tile to floor
		level[position] = drop
		# 2 - make two choices, 1 for x, 1 for y.
		x = random.choice(bowl)
		y = random.choice(bowl)
		new_position = (position[0] + x, position[1] + y)
		# 3a - check if position to move to is valid
		if new_position in level:
			# 4 - have we already walked here?
			if level[new_position] != drop:
				position = new_position
				TipsyWalk(level, position, stepsToWalk - 1, drop)
			else:
				TipsyWalk(level, (random.randint(0, bounds - 1), random.randint(0, bounds - 1)), stepsToWalk - 1, drop)
		# 3b - wasn't valid
		else:
			TipsyWalk(level, (random.randint(0, bounds - 1), random.randint(0, bounds - 1)), stepsToWalk - 1, drop)
		

if __name__ == "__main__":
	import time

	level = Map(50, "wall")
	drop = "floor"
	steps = 50

	startTime = time.clock()
	TipsyWalk(level, stepsToWalk=steps, drop=drop)
	endTime = time.clock()
	print "Execution Time: {}".format(endTime - startTime)
	pprint.pprint(level)

	count = 0
	for tile in level:
		if level[tile] == "floor":
			count +=1
	print "Level Size = {}".format(len(level))
	print "Tiles Carved = {}".format(count)
