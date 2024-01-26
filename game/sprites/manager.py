"""Manager Sprite."""
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, RLEACCEL as RL
from pygame import image
from pygame.sprite import Sprite

from game.defs import SCREEN_WIDTH, SCREEN_HEIGHT


class Manager(Sprite):
    """Player Sprite"""

    def __init__(self):
        super(Manager, self).__init__()
        self.surface = image.load("assets/jet.png").convert()
        self.surface.set_colorkey((255, 255, 255), RL)
        self.rect = self.surface.get_rect()
        self.frustration_level = 0