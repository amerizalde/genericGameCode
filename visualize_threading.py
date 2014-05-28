import random, pygame, os, sys, threading

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
# the worm is stored as a list with the HEAD being the first element.
HEAD =  0
BUTT = -1

# -- SHARED DATA --
GRID = [[None] * CELLS_HIGH for i in xrange(CELLS_WIDE)]
GRID_LOCK = threading.Lock()
# global var that the Worm threads check to see if they should exit
WORMS_RUNNING = True



class Worm(threading.Thread):
    """ Just an abstract idea of a worm/snake to learn about Threads.

            [name] -- to identify a specific Thread. debugging purposes.
            [maxsize] -- how long can the worm be?
            [color] -- duh
            [speed] -- what you see is an arg for defining how fast the worm
                        can move. In reality, it is a governer limiting
                        how often this thread will run. Less is more.
    """
    global GRID, GRID_LOCK, CELLS_HIGH, CELLS_WIDE, WORMS_RUNNING, HEAD, BUTT
    
    def __init__(self, name="Worm", maxsize=None, color=None, speed=None):
        global GRID, GRID_LOCK, CELLS_HIGH, CELLS_WIDE, WORMS_RUNNING, HEAD, BUTT
        super(Worm, self).__init__()
        # Thread Identifier
        self.name = name

        if maxsize is None:
            self.maxsize = random.randint(10, 20)
        else:
            self.maxsize = maxsize

        if color is None:
            self.color = (random.randint(60, 255),
                random.randint(60, 255),
                random.randint(60, 255))
        else:
            self.color = color

        if speed is None:
            self.speed = random.randint(20, 500) # .02 - .5 secs
        else:
            self.speed = speed

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

        # life as a worm starts as a single cell organism.
        # This is you cell. There are many like it but this one is yours.
        self.body = [{'x': startx, 'y': starty}]

        # Which direction will you grow in?
        self.direction = random.choice((UP, DOWN, LEFT, RIGHT))

    def run(self):
        global GRID, GRID_LOCK, CELLS_HIGH, CELLS_WIDE, WORMS_RUNNING, HEAD, BUTT
        while True:
            # WORMS_RUNNING is a global boolean that all the threads can look up.
            if not WORMS_RUNNING:
                return
            # 20% chance to change direction
            if random.randint(0, 100) < 20:
                self.direction = random.choice((UP, DOWN, LEFT, RIGHT))

            # time to read/write to the Grid again.
            GRID_LOCK.acquire()

            nextx, nexty = self.getNextPosition()
            # if Grid[nextx][nexty] is occupied...
            if nextx in (-1, CELLS_WIDE) or nexty in (
                -1, CELLS_HIGH) or GRID[nextx][nexty] is not None:
                # try going a different way...
                self.direction = self.getNewDirection()

                # that didn't work so...
                if self.direction is None:
                    self.body.reverse()  # Being a list means reversing
                                         # direction is built-in!
                    self.direction = self.getNewDirection()

                # that worked!
                if self.direction is not None:
                    nextx, nexty = self.getNextPosition()
            # if Grid[nextx][nexty] is NOT occupied, and in the Grid...
            if self.direction is not None:
                GRID[nextx][nexty] = self.color
                # the HEAD moves first
                self.body.insert(HEAD, {'x': nextx, 'y': nexty})

                # the worm should never be longer than it's maxsize
                # (the worm is represented as a list of dicts)
                if len(self.body) > self.maxsize:
                    # this removes the color from the GRID cell
                    GRID[self.body[BUTT]['x']][self.body[BUTT]['y']] = None
                    # this shortens the list
                    del self.body[BUTT]
            else:
                # can't move there, so try a new direction
                self.direction = random.choice((UP, DOWN, LEFT, RIGHT))

            # done modifying Grid
            GRID_LOCK.release()

            # speed is governed by sleeping for the length of self.speed
            pygame.time.wait(self.speed)

    def getNextPosition(self):
        """ Return the x, y values of self.direction"""
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
        global GRID, GRID_LOCK, CELLS_HIGH, CELLS_WIDE, WORMS_RUNNING, HEAD, BUTT
        x = self.body[HEAD]['x']
        y = self.body[HEAD]['y']
        # holds the possible directions to move
        newDirection = []
        borderY = (-1, CELLS_HIGH)
        borderX = (-1, CELLS_WIDE)
        # determine valid exits
        if y - 1 not in borderY and GRID[x][y - 1] is None:
            newDirection.append(UP)
        if y + 1 not in borderY and GRID[x][y + 1] is None:
            newDirection.append(DOWN)
        if x - 1 not in borderX and GRID[x - 1][y] is None:
            newDirection.append(LEFT)
        if x + 1 not in borderX and GRID[x + 1][y] is None:
            newDirection.append(RIGHT)

        # if there are no valid exits, return None
        if newDirection == []:
            return None
        # otherwise, pick an exit at random and return it.
        # TODO: add a weight to the choices?
        else:
            return random.choice(newDirection)


class Game(object):
    SPACING = 20
    title = "Threadworms"
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

        self.worms = []

    def run(self):
        global NUM_WORMS
        # add some walls to the GRID
        if self.levels:
            self.setGridSquares(self.levels[self.current_level], color=(255, 128, 255))
        for i in xrange(NUM_WORMS):
            # create the threads, and add to self.worms
            self.worms.append(Worm(maxsize=4))
            # start the worm code in its own thread,
            # after it is added to the list
            self.worms[-1].start()
        while True:
            # screen is already cleared in the call to .drawGrid()
            # self.display.blit(self.background, (0, 0))  # clear screen

            # EVENT LOGIC
            for event in pygame.event.get():
                self._event_manager(event)
            # GAME LOGIC
            # the threads are handling their own logic.

            # DRAW
            self.drawGrid()
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
        global WORMS_RUNNING
        if event.type == QUIT:
            WORMS_RUNNING = False
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            self._key_event(event)
        elif event.type == MOUSEBUTTONDOWN:
            self._mouse_event(event)

    def _key_event(self, event):
        """ Handle all key events. """
        global WORMS_RUNNING
        if event.key == K_ESCAPE:
            WORMS_RUNNING = False
            pygame.quit()
            sys.exit()

    def _mouse_event(self, event):
        """ Handle all mouse events. """
        pass

    def drawGrid(self):
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
