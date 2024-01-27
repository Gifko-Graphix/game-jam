"""Meters for the game."""
from pygame import Rect, Surface, draw, time
from pygame.sprite import Sprite

from game.defs import MANAGER_METER_EVENT


class Meter(Sprite):
    """Base class for all meters."""

    def __init__(self, max_value: float = 100.0):
        super(Meter, self).__init__()
        self.max_width = max_value
        self.surface = Surface((self.max_width, 10))
        self.surface.fill((255, 255, 255))
        self.rect = self.surface.get_rect(center=(400, 300))
        time.set_timer(MANAGER_METER_EVENT, 100)
        self.progress = 0.0

    def update(self, positive: bool = False):
        """Update the meter's value."""
        if positive:
            factor: float = 0.01
        else:
            factor: float = 0.0005

        if positive:
            self.progress += factor
        else:
            self.progress -= factor
        
        if self.progress >= 1.0:
            self.progress = 1.0
        if self.progress <= 0.0:
            self.progress = 0.0

        draw.rect(
            self.surface, (255, 0, 0), Rect(0, 0, self.max_width * self.progress, 10)
        )

    def update_position(self, x: int, y: int):
        """Update the meter's position."""
        self.rect.x = x
        self.rect.y = y - 20

    @property
    def is_full(self):
        """Return True if the meter is full."""
        return self.progress * self.max_width >= self.max_width

    def draw_surface(self, surface: Surface):
        """Draw the meter on the surface."""
        draw.rect(surface, (255, 255, 255), self.rect)
        draw.rect(
            surface,
            (0, 255, 0),
            (self.rect.x, self.rect.y, self.max_width * self.progress, 10),
        )
