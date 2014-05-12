import pygame
import math
import random

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
        while n:
            try:
                self.grid[x, y] = tile
            except Exception as e:
                print e
                return
            x += random.choice(direction)
            y += random.choice(direction)
            print " {},{}  ".format(x, y)
            n -= 1

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
    dungeon.toImage("test_{}.png".format(random.randint(1000, 2000)))
