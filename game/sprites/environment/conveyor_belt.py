"""Conveyor belt sprite class."""
from pygame import Surface, time
from pygame.sprite import Sprite

from game.defs import ELECTRIC_PANEL_TIMER_EVENT, Direction
from game.sprites.environment.electricPanel import OFF_TIME_SECONDS
from game.sprites.persons.player import Player


class ConveyorBelt(Sprite):
    """Conveyor belt sprite."""

    def __init__(self, x: int = 500, y: int = 500, direction: Direction = Direction.right) -> None:
        """Initialize conveyor belt sprite."""
        super(ConveyorBelt, self).__init__()
        # self.surface = image.load("assets/conveyor_belt.png").convert()
        # self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        self.canInteract = False
        self.surface = Surface((500, 50))
        self.surface.fill((255, 255, 255))
        self.rect = self.surface.get_rect(center=(x, y))
        self.direction = direction

    def update(self) -> None:
        """Update conveyor belt sprite."""

    def detectPlayer(self, player: Player) -> None:
        if self.hitbox.colliderect(player.rect):
            self.canInteract = True
        else:
            self.canInteract = False

    def foo_action(self):
        self.isOn = False
        self.countdownTimerValue = OFF_TIME_SECONDS
        time.set_timer(ELECTRIC_PANEL_TIMER_EVENT, 100)

    def countdown_timer(self):
        self.countdownTimerValue -= 1
        if self.countdownTimerValue <= 0:
            time.set_timer(ELECTRIC_PANEL_TIMER_EVENT, 0)
            self.isOn = True