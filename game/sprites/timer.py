from pygame import font, time
from pygame.sprite import Sprite

from game.defs import LEVEL_TIMER_EVENT, LEVEL_TIMER_VALUE, SCREEN_WIDTH


class Timer(Sprite):
    """Timer Sprite."""

    def __init__(self):
        """Initialize the timer sprite."""
        super(Timer, self).__init__()
        self.value = LEVEL_TIMER_VALUE
        self.font = font.SysFont("Roboto", 30)
        time.set_timer(LEVEL_TIMER_EVENT, 1000)

        self.surface = self.font.render(str(self.value), True, (255, 255, 255))
        self.rect = self.surface.get_rect(center=(SCREEN_WIDTH / 2, 50))

    def update(self):
        """Update the timer sprite."""
        self.surface = self.font.render(str(self.value), True, (255, 255, 255))
        self.rect = self.surface.get_rect(center=(SCREEN_WIDTH / 2, 50))
