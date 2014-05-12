import pygame
import os
from PIL import Image
from pprint import pprint
from pygame.locals import *
from sys import argv

try:
    pygame.init()
except Exception as e:
    print '''*******************************************************************
    ERROR: {}

    Make sure you have PyGame installed before running this module.
    http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame

*******************************************************************'''.format((e,))

try:
    _, folder = argv
except ValueError as e:
    print '''*******************************************************************
    ERROR: {}

    If the folder name has spaces in it, like My Pictures,
    enclose it in double-quotes, i.e. "My Documents/My Pictures".

*******************************************************************'''.format((e,))

def is_image(path_to_file):
    try:
        im = pygame.image.load(path_to_file)
        return (im, path_to_file)  # retain the path to the orig image
    except pygame.error:
        pass

# CHOOSING FOLDER #
path = os.path.join(os.path.expanduser("~"), folder)
contents = os.listdir(path)
# END #

# GETTING ALL IMAGES #
files = []
for f in contents:
    sub_path = "{}/{}".format(path, f)
    if os.path.isfile(sub_path):
        im = is_image(sub_path)
        if im is not None:
            files.append(im)
# END #

# how big does the initial sprite sheet need to be? #
w = sum([f[0].get_width() for f in files])
h = sum([f[0].get_height() for f in files])
print w, h

sheets = []
w, h = 4000, 4000
surf = pygame.Surface((w, h))
surf.fill((128, 128, 128))
spacer = 2 # 2px
cursor_x, cursor_y = 0, 0
for f in files:
    f_w, f_h = f[0].get_width(), f[0].get_height()
    if cursor_x + f_w < w:
        surf.blit(f[0], (cursor_x, cursor_y))
    else:
        cursor_x = 0
        cursor_y += f_h + spacer
        if cursor_y >= h:
            break
        else:
            surf.blit(f[0], (cursor_x, cursor_y))
    cursor_x += f_w + spacer

pygame.image.save(surf, path + "/test.jpg")
