import threading
import random
import pygame
import math

from pygame.locals import *


#  -- CONSTANTS --
NUM_WORMS =         24
CELL_SIZE =         20
CELLS_WIDE =        40
CELLS_HIGH =        32
BGCOLOR =           color.THECOLORS["black"]
GRID_LINES_COLOR =  color.THECOLORS["darkslategray"]
SURFACEWIDTH =      CELL_SIZE * CELLS_WIDE
SURFACEHEIGHT =     CELL_SIZE * CELLS_WIDE
UP =    'up'
DOWN =  'down'
LEFT =  'left'
RIGHT = 'right'
HEAD =  0

# -- SHARED DATA --
GRID = [[None] * CELLS_HIGH for i in xrange(CELLS_WIDE)]
GRID_LOCK = threading.Lock()
GAME_OVER = False

class Mobile(threading.Thread):
    """
    [name] -- to identify a specific thread 
    [color] -- the color to represent a specialization
    [speed] -- how many turns per X does this get?
    [ai] -- how does it move, act, and react?
    [archetype] -- what does it specialize in?
    [team] -- which side is it on?
    """

    def __init__(self, name=None, color=None, speed=None, ai=None,
        archetype=None, team=None):
        global GRID, GRID_LOCK, CELLS_WIDE, CELLS_HIGH, UP, DOWN, LEFT, RIGHT
        super(Worm, self).__init__()
        self.name = name

        if color is None:
            self.color = (random.randint(60, 255),
                random.randint(60, 255),
                random.randint(60, 255))
        else:
            self.color = color

        if speed is None:
            self.speed = random.randint(200, 500) # .02 - .5 secs
        else:
            self.speed = speed

        self.ai = ai
        self.archetype = archetype
        self.team = team

        # ACQUIRE LOCK-ON .. PEW PEW!
        GRID_LOCK.acquire()

        # Find a valid spawn point
        while True:
            startx = random.randint(0, CELLS_WIDE - 1)
            starty = random.randint(0, CELLS_HIGH - 1)
            if GRID[startx][starty] is None:
                break  # we've found an unoccupied cell in the grid

        # Modifying the shared data Grid.
        # Changing the color of the cell to this Worm's color
        GRID[startx][starty] = self.color

        # done modifying.. RELEASE
        GRID_LOCK.release()

        self.body = [{'x': startx, 'y': starty}]
        self.direction = random.choice((UP, DOWN, LEFT, RIGHT))
        self.target = None
        self.dead = False

    def run(self):
        """ if self.target.dead or None: 
                Acquire a valid target.
                if no valid targets:
                    GAME_OVER = True

            Move into attack range. Attack.
        """
        global GRID, GRID_LOCK, CELLS_WIDE, CELLS_HIGH, GAME_OVER
        while True:
            if GAME_OVER or self.dead:
                return

            if self.archetype:
                # FIND TARGET
                if self.target.dead or self.target is None:
                    self.find_target()
                # ATTACKING
                if self.archetype.in_range():
                    self.archetype.attack(self.target)
                else:
                    # MOVING
                    self.move()

            # speed is governed by sleeping for the length of self.speed
            pygame.time.wait(self.speed)

    def move(self):
        global GRID, GRID_LOCK, CELLS_WIDE, CELLS_HIGH, UP, DOWN, LEFT, RIGHT

        GRID_LOCK.acquire()
        nextx, nexty = self.getNextPosition()
        # if Grid[nextx][nexty] is occupied or out of bounds...
        if nextx in (-1, CELLS_WIDE) or nexty in (
            -1, CELLS_HIGH) or GRID[nextx][nexty] is not None:
            # try going a different way...
            self.direction = self.getNewDirection()

            # that didn't work so...
            if self.direction is None:
                # self.body.reverse()  # Being a list means reversing
                #                      # direction is built-in!
                self.direction = self.getNewDirection()

            # that worked!
            if self.direction is not None:
                nextx, nexty = self.getNextPosition()
        # if Grid[nextx][nexty] is NOT occupied, and in the Grid...
        if self.direction is not None:
            GRID[nextx][nexty] = self.color
            self.body[0]["x"] = nextx
            self.body[0]["y"] = nexty
        else:
            # can't move there, so try a new direction
            self.direction = random.choice((UP, DOWN, LEFT, RIGHT))
        GRID_LOCK.release()

    def target_bearing(self):
        """ find distance to target and return a normalized vector"""
        dx = self.target.body['x'] - self.body['x']
        dy = self.target.body['y'] - self.body['y']
        distance = math.sqrt(dx ** 2 + dy ** 2)
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        return dx, dy

    def move_to(self, pos):
        """ for mouse movement """
        dx = pos[0] - self.body['x']
        dy = pos[1] - self.body['y']
        distance = math.sqrt(dx ** 2 + dy ** 2)
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        return dx, dy

    def getNextPosition(self):
        """ Return the x, y values of self.direction"""
        global UP, DOWN, LEFT, RIGHT, HEAD
        if self.direction == UP:
            nextx = self.body[HEAD]['x']
            nexty = self.body[HEAD]['y'] - 1
        elif self.direction == DOWN:
            nextx = self.body[HEAD]['x']
            nexty = self.body[HEAD]['y'] + 1
        elif self.direction == LEFT:
            nextx = self.body[HEAD]['x'] - 1
            nexty = self.body[HEAD]['y']
        elif self.direction == RIGHT:
            nextx = self.body[HEAD]['x'] + 1
            nexty = self.body[HEAD]['y']
        else:
            assert False, 'Bad value for self.direction: {}'.format(
                self.direction)
        return nextx, nexty

    def getNewDirection(self):
        """ when bearing to target changes,
            this will be used to find the next best move. """
        global GRID, GRID_LOCK, CELLS_HIGH, CELLS_WIDE, HEAD
        t_x, t_y = self.target_bearing()
        x = self.body[HEAD]['x']
        y = self.body[HEAD]['y']
        # holds the possible directions to move
        newDirection = []
        borderY = (-1, CELLS_HIGH)
        borderX = (-1, CELLS_WIDE)
        # determine valid exits
        if t_y == 1:
            if y - 1 not in borderY and GRID[x][y - 1] is None:
                newDirection.append(UP)
        if t_y == -1:
            if y + 1 not in borderY and GRID[x][y + 1] is None:
                newDirection.append(DOWN)
        if t_x == -1:
            if x - 1 not in borderX and GRID[x - 1][y] is None:
                newDirection.append(LEFT)
        if t_x == 1:
            if x + 1 not in borderX and GRID[x + 1][y] is None:
                newDirection.append(RIGHT)

        # if there are no valid exits, return None
        if newDirection == []:
            return None
        # otherwise, pick an exit at random and return it.
        # TODO: add a weight to the choices?
        else:
            return random.choice(newDirection)

    def find_target(self, targets):
        targets = [t for t in targets if t.team != self.team]
        self.target = random.choice(targets)
