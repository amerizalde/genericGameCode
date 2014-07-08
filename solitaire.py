import pygame
import sys
import os
import math

from pygame.locals import *


class Peg(pygame.sprite.DirtySprite):

    def __init__(self, image_path, *groups):
        super(Peg, self).__init__(*groups)
        self.image = pygame.image.load(image_path)
        # color = self.image.get_at((0,0))
        # self.image.set_colorkey(color)

    def set_position(self, (x, y)):
        self.x, self.y = x, y

    def show(self):
        self.w, self.h = self.image.get_size()
        self.rect = pygame.rect.Rect(
            (self.x + self.w, self.y + self.h),  # position of top-left corner
            (self.w, self.h))  # size

    def update(self, surface):
        self.image = self.image.convert_alpha(surface)


class Game(object):

    def __init__(self):
        self.pegs = pygame.sprite.Group()
        self.setup()
        im = self.pegs.sprites()[0]
        self.w, self.h = im.w * 9, im.h * 9

    def run(self):
        w, h = self.w, self.h
        x, y = math.floor(w / 2), math.floor(h / 2)

        self.display = pygame.display.set_mode((w, h), 0, 32)
        pygame.display.set_caption("Solitaire v0.01")
        self.display.fill((0, 0, 0))

        while True:
            # EVENT LOGIC
            for event in pygame.event.get():
                self._event_manager(event)

            # GAME LOGIC

            # DRAWING LOGIC
            self.pegs.update(self.display)
            self.pegs.draw(self.display)
            pygame.display.flip()

    def setup(self):
        print "in setup()"
        path = os.getcwd()
        path += "/assets/peg.png"
        board =                 [(3, 0), (4, 0), (5, 0),
                                (3, 1), (4, 1), (5, 1),
                                (3, 2), (4, 2), (5, 2),
        (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3),
        (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4),
        (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5),
                                (3, 6), (4, 6), (5, 6),
                                (3, 7), (4, 7), (5, 7),
                                (3, 8), (4, 8), (5, 8)]
        for p in board:
            peg = Peg(path, self.pegs)
            peg.set_position(p)
            peg.show()
        print "setup() complete"

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
    game = Game()
    game.run()
