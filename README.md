genericGameCode
===============

Experimentation with procedural algorithms, image processing, and manipulation.

_visualaid_2dmaps.py_
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

    .rule_four_five(smoothing)
a cellular automata algorithm I read about at http://www.pixelenvy.ca/wa/ca_cave.html. Slow, but works.

> I use the 4-5 rule for adjusting squares. This means that for any given square, if it has 3 or fewer adjacent wall squares (counting all 8 cardinal compass points), the square 'starves' and becomes a floor. If it has greater than 5 adjacent wall squares, the square becomes a wall. Otherwise, leave it as is. 

