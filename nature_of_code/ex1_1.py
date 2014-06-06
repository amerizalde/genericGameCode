import random, pygame, os, sys, threading
import vector
from pygame.locals import *


class Ball(object):
    size = 20
    xspeed = 1.
    yspeed = 3.3
    bounce_x = False
    bounce_y = False
    color = (
        random.randint(20, 255),
        random.randint(20, 255),
        255)
    def __init__(self, x, y, xspeed=None, yspeed=None):
        self.vector = vector.Vector(x, y)
        self.xspeed = xspeed or self.xspeed
        self.yspeed = yspeed or self.yspeed

    def move(self, dx, dy):
        self.vector.attract(vector.Vector(dx, dy))

    def run(self):
        if self.bounce_x:
            self.xspeed *= -1       # reverse direction...
            self.bounce_x = False   # ...and reset state
        if self.bounce_y:
            self.yspeed *= -1       # reverse direction...
            self.bounce_y = False   # ...and reset state
        # update position
        self.move(self.xspeed, self.yspeed)

class Game(object):

    SPACING = 20
    title = "Bouncing Ball"
    cwd = os.getcwd()  # this is the folder the script is run from
    # change this to the folder your art and such is in
    assets = "../assets"

    def __init__(self, width=(16 * 40), height=(10 * 40), fps=30):
        pygame.init()
        pygame.display.set_caption(self.title)
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height),
            DOUBLEBUF)
        self.background = pygame.Surface(
            self.display.get_size()).convert_alpha()
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.Font(
        self.assets + '/Fonts/kenpixel_future.ttf', 10)
        # an object containing useful info about the display
        self.info = pygame.display.Info()
        self.balls = []

    def run(self):
        for i in xrange(2):
            x = random.randint(20, self.info.current_w - 20)
            y = random.randint(20, self.info.current_h - 20)
            xspeed = random.random() * 2
            yspeed = random.random() * 6
            self.balls.append(Ball(x, y, xspeed, yspeed))
        while True:
            self.display.blit(self.background, (0, 0))  # clear screen

            # EVENT LOGIC
            for event in pygame.event.get():
                self._event_manager(event)
            # GAME LOGIC
            for ball in self.balls:
                if ball.vector.x < 1:
                    ball.bounce_x = True
                if ball.vector.x > (self.info.current_w - ball.size - 1):
                    ball.bounce_x = True
                if ball.vector.y < 1:
                    ball.bounce_y = True
                if ball.vector.y > (self.info.current_h - ball.size - 1):
                    ball.bounce_y = True
                # DRAW
                try:
                    pygame.draw.ellipse(
                        self.display,
                        ball.color,
                        (ball.vector.x, ball.vector.y, ball.size, ball.size))
                except TypeError:
                    print (ball.vector.x, ball.vector.y, ball.size, ball.size)
                    continue

            self.show_fps()
            pygame.display.flip()

    def show_fps(self):
        milliseconds = self.clock.tick(self.fps)
        self.playtime += milliseconds / 1000.
        self.draw_text("FPS: {:1g}".format(self.clock.get_fps()),
            (10, self.height - 20))
        self.draw_text("PLAYTIME: {:1g} SECONDS".format(self.playtime),
            (10, self.height))

    def draw_text(self, text, pos):
        """ Helper method for drawing text on the screen"""
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, (0, 255, 0))
        self.display.blit(surface, ((pos[0]) / 2, (pos[1] - fh)))

    def quit(self):
        pygame.quit()
        sys.exit()

    def _event_manager(self, event):
        if event.type == QUIT:
            self.quit()
        elif event.type == KEYDOWN:
            self._key_event(event)
        elif event.type == MOUSEBUTTONDOWN:
            self._mouse_event(event)

    def _key_event(self, event):
        if event.key == K_ESCAPE:
            self.quit()

    def _mouse_event(self, event):
        pass

if __name__ == "__main__":
    Game().run()
