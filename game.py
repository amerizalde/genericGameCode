# Game showing off random level generation and save states
import pygame
import os
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
    def __init__(self, path):
        """ Looks for a /save directory, indicating that there are
        already maps generated.
        """
        self.path = path
        self.view = os.listdir(path)
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
            dungeon = mapgen.Dungeon(256, 256)
            dungeon.walk(32768)
            dungeon.rule_four_five(2)
            dungeon.toImage("save/level_{}.jpg".format(i))

    def build(self):
        self.level = getPixelArray("save/level_{}.jpg".format(self.map_n))

    def next(self):
        self.map_n += 1
        self.build()

    def previous(self):
        self.map_n -= 1
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
    path = os.getcwd()
    game = NewGame(path)
