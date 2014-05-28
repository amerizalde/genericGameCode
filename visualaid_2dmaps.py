import pygame
import math
import random
import datetime
import progress_tracker

from sys import argv
from pygame.locals import *
pygame.init()


# generate the map
class Dungeon(object):

    def __init__(self, w, h):
        self.surface = pygame.Surface((w, h))
        self.grid = pygame.surfarray.array3d(self.surface)

    def walk(self, n):
        """ starting from the midpoint of grid, carve out a path for N steps"""
        direction = [0, -1, 1]
        w, h, _ = self.grid.shape
        x, y = math.floor(w / 2), math.floor(h / 2)
        tile = [1, 128, 255]
        start_time = datetime.datetime.now()
        while n:
            try:
                # wrap around at edges
                if x >= w:
                    x = 0
                if x < 0:
                    x = w - 1
                if y >= h:
                    y = 0
                if y < 0:
                    y = h - 1
                self.grid[x, y] = tile
            except Exception as e:
                print e
                return
            x += random.choice(direction)
            y += random.choice(direction)

            # progress tracker
            progress_tracker.report(start_time)

            n -= 1

    def rule_four_five(self, n):
        """ Use after performing a .walk() or .visualize() to smooth
        out the noise. Increase N for more open space.
        """
        w, h, _ = self.grid.shape
        tile = [1, 128, 255]
        wall = [0, 0, 0]
        start_time = datetime.datetime.now()
        while n:
            for i in xrange(w - 1):
                # progress tracker
                iter_i = i
                progress_tracker.report(start_time)
                for j in xrange(h - 1):
                    iter_j = j
                    neighbors = self.num_walls(iter_i, iter_j, w, h)
                    if neighbors <= 3:
                        self.grid[iter_i, iter_j] = tile
                    elif neighbors > 5:
                        self.grid[iter_i, iter_j] = wall

            # iterate
            n -= 1

    def num_walls(self, i, j, w, h):
        """ determine the number of neighbors that are a wall.
                WARNING: WALL OF TEXT INCOMING
        """
        # nw
        def northw(grid, i, j):
            cell = grid[i - 1, j - 1]
            return True if cell.all() == False else False
        # n
        def north(grid, i, j):
            cell = grid[i, j - 1]
            return True if cell.all() == False else False
        # ne
        def northe(grid, i, j):
            cell = grid[i + 1, j - 1]
            return True if cell.all() == False else False
        # e
        def east(grid, i, j):
            cell = grid[i + 1, j]
            return True if cell.all() == False else False
        # se
        def southe(grid, i, j):
            cell = grid[i + 1, j + 1]
            return True if cell.all() == False else False
        # s
        def south(grid, i, j):
            cell = grid[i, j + 1]
            return True if cell.all() == False else False
        # sw
        def southw(grid, i, j):
            cell = grid[i - 1, j + 1]
            return True if cell.all() == False else False
        # w
        def west(grid, i, j):
            cell = grid[i - 1, j]
            return True if cell.all() == False else False

        count = 0

        # edge cases
        if i == 0 and j == 0:
            # TOP LEFT CORNER has 3 possible neighbors
            # e
            if east(self.grid, i, j): count += 1
            # se
            if southe(self.grid, i, j): count += 1
            # s
            if south(self.grid, i, j): count += 1
        elif i == 0 and j == h:
            # BOTTOM LEFT CORNER has 3 possible neighbors
            # e
            if east(self.grid, i, j): count += 1
            # ne
            if northe(self.grid, i, j): count += 1
            # n
            if north(self.grid, i, j): count += 1
        elif i == w and j == 0:
            # TOP RIGHT CORNER has 3 possible neighbors
            # w
            if west(self.grid, i, j): count += 1
            # sw
            if southw(self.grid, i, j): count += 1
            # s
            if south(self.grid, i, j): count += 1
        elif i == w and j == h:
            # BOTTOM RIGHT CORNER has 3 possible neighbors
            # w
            if west(self.grid, i, j): count += 1
            # nw
            if northw(self.grid, i, j): count += 1
            # n
            if north(self.grid, i, j): count += 1
        elif i == 0:
            # LEFT SIDE has 5 possible neighbors
            if north(self.grid, i, j): count += 1
            if northe(self.grid, i, j): count += 1
            if east(self.grid, i, j): count += 1
            if southe(self.grid, i, j): count += 1
            if south(self.grid, i, j): count += 1
        elif i == w:
            # RIGHT SIDE has 5 possible neighbors
            if north(self.grid, i, j): count += 1
            if northw(self.grid, i, j): count += 1
            if west(self.grid, i, j): count += 1
            if southw(self.grid, i, j): count += 1
            if south(self.grid, i, j): count += 1
            pass
        elif j == 0:
            # TOP SIDE has 5 possible neighbors
            if west(self.grid, i, j): count += 1
            if southw(self.grid, i, j): count += 1
            if south(self.grid, i, j): count += 1
            if southe(self.grid, i, j): count += 1
            if east(self.grid, i, j): count += 1
        elif j == h:
            # BOTTOM SIDE has 5 possible neighbors
            if west(self.grid, i, j): count += 1
            if northw(self.grid, i, j): count += 1
            if north(self.grid, i, j): count += 1
            if northe(self.grid, i, j): count += 1
            if east(self.grid, i, j): count += 1
        else:
            # everything else has 8 possible neighbors
            if north(self.grid, i, j): count += 1
            if northw(self.grid, i, j): count += 1
            if west(self.grid, i, j): count += 1
            if southw(self.grid, i, j): count += 1
            if south(self.grid, i, j): count += 1
            if southe(self.grid, i, j): count += 1
            if east(self.grid, i, j): count += 1
            if northe(self.grid, i, j): count += 1
        return count

    def toImage(self, filename):
        try:
            self.surface = pygame.surfarray.make_surface(self.grid)
        except IndexError:
            width, height, _ = self.grid.shape
            self.surface = pygame.display.set_mode((width, height))
            pygame.surfarray.blit_array(self.surface, self.grid)

        pygame.image.save(self.surface, filename)


    def visualize(self, n):
        """ show the walking process on-screen. """
        direction = [0, -1, 1]
        w, h, _ = self.grid.shape
        x, y = math.floor(w / 2), math.floor(h / 2)
        tile = [1, 128, 255]

        display = pygame.display.set_mode((w, h), 0, 32)
        pygame.display.set_caption("Generating the dungeon...")
        display.fill((0, 0, 0))
        while n:
            # EVENT LOGIC
            for event in pygame.event.get():
                self._event_manager(event)

            # GAME LOGIC
            try:
                # wrap around at edges
                if x >= w:
                    x = 0
                if x < 0:
                    x = w - 1
                if y >= h:
                    y = 0
                if y < 0:
                    y = h - 1
                self.grid[x, y] = tile
            except Exception as e:
                print "Walked out of bounds,\n{}".format(e)
                return
            x += random.choice(direction)
            y += random.choice(direction)

            # DRAWING LOGIC
            pygame.surfarray.blit_array(display, self.grid)
            pygame.display.flip()

            # iterate
            n -= 1

    def _event_manager(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            self._key_event(event)
        elif event.type == MOUSEBUTTONDOWN:
            self._mouse_event(event)

    def _key_event(self, event):
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()

    def _mouse_event(self, event):
        pass


if __name__ == "__main__":
    _, w, h = argv
    w, h = int(w), int(h)
    dungeon = Dungeon(w, h)
    dungeon.visualize(32768)
    n = random.randint(1000, 2000)
    dungeon.toImage("test_{}.png".format(n))
    dungeon.rule_four_five(2)
    dungeon.toImage("test_{}_smooth.png".format(n))
