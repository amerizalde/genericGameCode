import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game_w, game_h, image_path, *groups):
        super(Player, self).__init__(*groups)
        self.img_path = image_path
        self.image = pygame.image.load(self.img_path)
        self.rect = pygame.rect.Rect((game_w, game_h), self.image.get_size())

    def update(self):
        key = pygame.key.get_pressed()
        if key[K_LEFT]:
            self.rect.x -= 10
        if key[K_RIGHT]:
            self.rect.x += 10
        if key[K_UP]:
            self.rect.y -= 10
        if key[K_DOWN]:
            self.rect.y += 10
