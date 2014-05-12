genericGameCode
===============

Experimentation with procedural algorithms, image processing, and manipulation.

_visualaid___2dmaps.py_
---
requires pygame http://www.pygame.org/

    dungeon = Dungeon(width, height)
creates a Dungeon object containing a .surface and a .grid

    .walk(steps)
applies my interpretation of the drunkard walk algorithm to the .grid

    .visualize(steps)
displays the walk until complete, then closes.

    .toImage(filename)
saves the .grid as an image to disk.
