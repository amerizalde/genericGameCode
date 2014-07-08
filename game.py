import threading
import random
import pygame
import math
import sys
import os

from pygame.locals import *

# TODO -- A* for bots. Target change upon reaching target.

#  -- CONSTANTS --
NUM_BOTS =          24
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
TARGETS = []
GRID_LOCK = threading.Lock()
TARGET_LOCK = threading.Lock()
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
        super(Mobile, self).__init__()
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
        global GAME_OVER, TARGETS, TARGET_LOCK
        while True:
            if GAME_OVER or self.dead:
                return

            # TARGETING
            if self.target is None or self.target.dead:
                TARGET_LOCK.acquire()
                self.find_target(TARGETS)
                TARGET_LOCK.release()
            # ATTACKING
            if self.archetype and self.archetype.in_range():
                self.archetype.attack(self.target)
            # MOVING
            else:
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
            GRID[self.body[HEAD]["x"]][self.body[HEAD]["y"]] = None
            GRID[nextx][nexty] = self.color
            self.body[HEAD]["x"] = nextx
            self.body[HEAD]["y"] = nexty
        else:
            # can't move there, so try a new direction
            self.direction = random.choice((UP, DOWN, LEFT, RIGHT))
        GRID_LOCK.release()

    def target_bearing(self):
        """ find distance to target and return a normalized vector"""
        dx = self.target.body[HEAD]['x'] - self.body[HEAD]['x']
        dy = self.target.body[HEAD]['y'] - self.body[HEAD]['y']
        distance = math.sqrt(dx ** 2 + dy ** 2)
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        return dx, dy

    def move_to(self, pos):
        """ for mouse movement """
        dx = pos[HEAD] - self.body[HEAD]['x']
        dy = pos[1] - self.body[HEAD]['y']
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
        if t_y == -1:
            if y - 1 not in borderY and GRID[x][y - 1] is None:
                newDirection.append(UP)
        if t_y == 1:
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
        global GAME_OVER
        targets = [t for t in targets if t.team != self.team]
        if targets:
            self.target = random.choice(targets)
        else:
            GAME_OVER = True


class Game(object):
    SPACING = 20
    title = "ThreadBOTS"
    cwd = os.getcwd()  # this is the folder the script is run from
    # change this to the folder your art and such is in
    assets = cwd + "/assets"
    current_level = -1

    def __init__(self, width=640, height=480, fps=30, levels=None):
        # BEGIN boilerplate
        pygame.init()
        pygame.display.set_caption(self.title)
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height),
            DOUBLEBUF)
        self.background = pygame.Surface(
            self.display.get_size()).convert_alpha()
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.Font(
        self.assets + '/Fonts/kenpixel_future.ttf', 12)
        # an object containing useful info about the display
        self.info = pygame.display.Info()
        self.levels = levels
        # END boilerplate

        self.bots = []

    def run(self):
        global NUM_BOTS
        # add some walls to the GRID
        if self.levels:
            self.setGridSquares(self.levels[self.current_level], color=(255, 128, 255))
        for i in xrange(NUM_BOTS):
            # create the threads, and add to self.bots and TARGETS
            team = random.choice((0, 1))
            bot = Mobile(team=team)
            self.bots.append(bot)
            TARGET_LOCK.acquire()
            TARGETS.append(bot)
            TARGET_LOCK.release()
        for i in self.bots:
            i.start()
        while True:
            # screen is already cleared in the call to .draw_grid()
            # self.display.blit(self.background, (0, 0))  # clear screen

            # EVENT LOGIC
            for event in pygame.event.get():
                self._event_manager(event)
            # GAME LOGIC
            # the threads are handling their own logic.

            # DRAW
            self.draw_grid()
            self.show_fps()
            pygame.display.flip()

    def show_fps(self):
        """ Display current FPS, and PLAYTIME. """
        milliseconds = self.clock.tick(self.fps)
        self.playtime += milliseconds / 1000.
        self.draw_text("FPS: {:1g}".format(self.clock.get_fps()),
            (10, self.height - 20))
        self.draw_text("PLAYTIME: {:1g} SECONDS".format(self.playtime),
            (10, self.height))

    def draw_text(self, text, pos):
        """ Helper method for drawing text on the screen
            <text> -- the string to show on screen.
            <pos> -- where to place the text, based on the top-left corner. """
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, (0, 255, 0))
        self.display.blit(surface, ((pos[0]) / 2, (pos[1] - fh)))

    def _event_manager(self, event):
        """ My attempt to simplify event handling. """
        global GAME_OVER
        if event.type == QUIT:
            GAME_OVER = True
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            self._key_event(event)
        elif event.type == MOUSEBUTTONDOWN:
            self._mouse_event(event)

    def _key_event(self, event):
        """ Handle all key events. """
        global GAME_OVER
        if event.key == K_ESCAPE:
            GAME_OVER = True
            pygame.quit()
            sys.exit()

    def _mouse_event(self, event):
        """ Handle all mouse events. """
        pass

    def draw_grid(self):
        """ Draw the grid and then fill the appropriate cells. """
        global GRID, GRID_LOCK, CELLS_HIGH, CELLS_WIDE, BGCOLOR, GRID_LINES_COLOR
        self.display.fill(BGCOLOR)

        # draw a grid of lines covering the extent of the window
        map(
            lambda pos: pygame.draw.line(
                self.display,
                GRID_LINES_COLOR,
                (pos, 0),
                (pos, self.info.current_h)),
            range(0, self.info.current_w, CELL_SIZE))
        map(
            lambda pos: pygame.draw.line(
                self.display,
                GRID_LINES_COLOR,
                (0, pos),
                (self.info.current_w, pos)),
            range(0, self.info.current_h, CELL_SIZE))

        GRID_LOCK.acquire()
        # determine what color each cell should be this frame
        # and draw a rect representing that cell.
        for x in xrange(0, CELLS_WIDE):
            i_x = x
            for y in xrange(0, CELLS_HIGH):
                i_y = y
                # if None, dont draw anything and move on
                if GRID[i_x][i_y] is None:
                    continue
                # the inner cell color
                color = GRID[i_x][i_y]
                # the outer cell color
                darkerColor = (max(color[0] - 50, 0),
                    max(color[1] - 50, 0),
                    max(color[2] - 50, 0))
                # draw two rects, one of full CELL_SIZE but slightly darker
                # color to create a border effect...
                pygame.draw.rect(
                    self.display,
                    darkerColor,
                    (i_x * CELL_SIZE, i_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                # ...another of normal color but slightly smaller CELL_SIZE
                pygame.draw.rect(
                    self.display,
                    color,
                    (i_x * CELL_SIZE + 4, i_y * CELL_SIZE + 4,
                        CELL_SIZE - 8, CELL_SIZE - 8))

        GRID_LOCK.release()

    def setGridSquares(self, squares, color=(192, 192, 192)):
        """ Draw walls based on input string.
            [color] -- the wall color.
        """
        global GRID, GRID_LOCK, CELLS_HIGH, CELLS_WIDE
        squares = squares.split('\n')
        if squares[0] == '':
            del squares[0]
        if squares[-1] == '':
            del squares[-1]

        GRID_LOCK.acquire()
        for y in xrange(min(len(squares), CELLS_HIGH)):
            i_y = y
            for x in xrange(min(len(squares[i_y]), CELLS_WIDE)):
                i_x = x
                if squares[i_y][i_x] == " ":
                    GRID[i_x][i_y] = None
                elif squares[i_y][i_x] == ".":
                    pass
                else:
                    GRID[i_x][i_y] = color
        GRID_LOCK.release()


if __name__ == "__main__":
    level = ["""
    ...........................
    ...........................
    ...........................
    .H..H..EEE..L....L.....OO..
    .H..H..E....L....L....O..O.
    .HHHH..EE...L....L....O..O.
    .H..H..E....L....L....O..O.
    .H..H..EEE..LLL..LLL...OO..
    ...........................
    .W.....W...OO...RRR..MM.MM.
    .W.....W..O..O..R.R..M.M.M.
    .W..W..W..O..O..RR...M.M.M.
    .W..W..W..O..O..R.R..M...M.
    ..WW.WW....OO...R.R..M...M.
    ...........................
    ...........................
    """,]
    Game(800, 600, levels=level).run()
