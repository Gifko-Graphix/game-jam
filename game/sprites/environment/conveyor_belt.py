"""Conveyor belt sprite class."""
from pygame import Surface
from pygame.sprite import Sprite

from game.defs import Direction


class ConveyorBelt(Sprite):
    """Conveyor belt sprite."""

    def __init__(self, x: int = 500, y: int = 500, direction: Direction = Direction.right) -> None:
        """Initialize conveyor belt sprite."""
        super(ConveyorBelt, self).__init__()
        # self.surface = image.load("assets/conveyor_belt.png").convert()
        # self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        self.surface = Surface((500, 50))
        self.surface.fill((255, 255, 255))
        self.rect = self.surface.get_rect(center=(x, y))
        self.direction = direction

    def update(self) -> None:
        """Update conveyor belt sprite."""
        if self.direction == Direction.left:
            self.rect.move_ip(-1, 0)
        elif self.direction == Direction.right:
            self.rect.move_ip(1, 0)
        elif self.direction == Direction.up:
            self.rect.move_ip(0, -1)
        elif self.direction == Direction.down:
            self.rect.move_ip(0, 1)