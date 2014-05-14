# Game showing off random level generation and save states
import pygame
import os, sys
import visualaid_2dmaps as mapgen

from pygame.locals import *


def getPixelArray(filename):
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        print "Cannot load image:", filename
        raise SystemExit, message
    return pygame.surfarray.array3d(image)


class NewGame(object):
    """ Start a game using procedurally-generated, reusable maps."""

    map_n = 0
    resolution = (256, 256)

    def __init__(self, path, resolution=None):
        """ Looks for a /save directory, indicating that there are
        already maps generated.
        """
        self.path = path
        self.view = os.listdir(path)
        if resolution and type(resolution) == tuple:
            self.resolution = resolution
        if 'save' not in self.view:
            self.create()
        self.build()

    def create(self):
        """ generate a new /save folder and populate it with 32 maps."""
        try:
            os.mkdir(self.path + '/save')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        for i in xrange(2):
            dungeon = mapgen.Dungeon(resolution[0], resolution[1])
            dungeon.walk(32768)
            dungeon.rule_four_five(2)
            dungeon.toImage("save/level_{}.jpg".format(i))

    def build(self):
        try:
            self.level = getPixelArray("save/level_{}.jpg".format(self.map_n))
        except:
            print "Out of maps!"
            self._quit()

    def next(self):
        self.map_n += 1
        pygame.display.set_caption("Level {}".format(self.map_n))
        self.build()

    def previous(self):
        self.map_n -= 1
        pygame.display.set_caption("Level {}".format(self.map_n))
        self.build()

    def show(self):
        w, h, _ = self.level.shape
        display = pygame.display.set_mode((w, h), 0, 32)
        pygame.display.set_caption("Level {}".format(self.map_n))

        while True:
            # EVENT LOGIC
            for event in pygame.event.get():
                self._event_manager(event)

            # GAME LOGIC

            # DRAWING LOGIC
            pygame.surfarray.blit_array(display, self.level)
            pygame.display.flip()

    def _event_manager(self, event):
        if event.type == QUIT:
            self._quit()
        elif event.type == KEYDOWN:
            self._key_event(event)
        elif event.type == MOUSEBUTTONDOWN:
            self._mouse_event(event)

    def _key_event(self, event):
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif event.key == K_PAGEUP:
            self.next()
        elif event.key == K_PAGEDOWN:
            self.previous()

    def _mouse_event(self, event):
        pass

    def _quit(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    path = os.getcwd()
    game = NewGame(path)
    game.show()
