import pygame
import os
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
    _, folder, saveas = argv
except ValueError as e:
    print '''*******************************************************************
    Usage:
        python|pypy sprite_tools.py <path_to_directory> <name>

        <path_to_directory> -- the relative path of the folder
        <name> -- name to give the sprite-sheet

*******************************************************************'''.format((e,))

def is_image(path_to_file):
    if os.path.isfile(path_to_file):
        try:
            im = pygame.image.load(path_to_file)
            return (im, path_to_file)  # retain the path to the orig image
        except pygame.error:
            pass
    else:
        pass

def get_images(directory, contents):
    """ Return all image files (according to pygame),
        ignoring sub-directories.

        <directory> -- the valid path to search
        <contents> -- a list of strings returned from os.listdir()"""
    images = []
    for f in contents:
        path = "{}/{}".format(directory, f)
        im = is_image(path)
        if im is not None:
            images.append(im)
    return images

# CHOOSING FOLDER #
path = os.path.join(os.getcwd(), folder)
contents = os.listdir(path)

# GETTING ALL IMAGES #
files = get_images(path, contents)

# how big does the initial sprite sheet need to be? #
if len(files) % 2 == 0:
    split = len(files) / 2
else:
    split = (len(files) + 1) / 2
w = sum([f[0].get_width() for f in files])
h = sum([f[0].get_height() for f in files])
print split
perimeter = files[0][0].get_width() * split
print perimeter  ###
surf = pygame.Surface((perimeter, perimeter))
color_key = (0, 0, 0)
surf.fill(color_key)
spacer = 2 # 2px
cursor_x, cursor_y = 0, 0
for f in files:
    # get image dimensions
    f_w, f_h = f[0].get_width(), f[0].get_height()
    # check if there is room in this column for the image
    if cursor_x + f_w < perimeter - f_w:
        surf.blit(f[0], (cursor_x, cursor_y))
    # else drop to the next row, first column
    else:
        cursor_x = 0
        cursor_y += f_h + spacer
        # this should never run, but just in case...
        if cursor_y >= perimeter - f_h:
            break
        else:
            surf.blit(f[0], (cursor_x, cursor_y))
    cursor_x += f_w + spacer

# save the surface to disk.
pygame.image.save(surf, path + "/{}.png".format(saveas))
