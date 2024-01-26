"""Cloud Sprite."""
from pygame.sprite import Sprite
from pygame import image
from pygame.locals import RLEACCEL as RL
import random

from game.defs import SCREEN_HEIGHT, SCREEN_WIDTH


class Cloud(Sprite):
    """Cloud Sprite"""

    def __init__(self):
        super(Cloud, self).__init__()
        self.surface = image.load("assets/cloud.png").convert()
        self.surface.set_colorkey((0, 0, 0), RL)
        self.rect = self.surface.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()
