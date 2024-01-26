"""Manager Sprite."""
from pygame import image
from pygame.locals import RLEACCEL as RL
from pygame.sprite import Sprite


class Manager(Sprite):
    """Player Sprite"""

    def __init__(self):
        super(Manager, self).__init__()
        self.surface = image.load("assets/jet.png").convert()
        self.surface.set_colorkey((255, 255, 255), RL)
        self.rect = self.surface.get_rect()
        self.frustration_level = 0
