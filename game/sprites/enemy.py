"""Enemy Sprite."""

import random
from pygame import image
from pygame.sprite import Sprite
from pygame.locals import RLEACCEL as RL

from game.defs import SCREEN_HEIGHT, SCREEN_WIDTH


class Enemy(Sprite):
    """Enemy Sprite"""

    def __init__(self):
        super(Enemy, self).__init__()
        self.surface = image.load("assets/missile.png").convert()
        self.surface.set_colorkey((255, 255, 255), RL)
        self.rect = self.surface.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
