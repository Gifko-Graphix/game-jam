"""Conveyor belt sprite class."""
from pygame import Surface, time
from pygame.sprite import Sprite

from game.defs import ELECTRIC_PANEL_TIMER_EVENT
from game.levels.parameters import ConveyorBeltParameters
from game.sprites.environment.electricPanel import OFF_TIME_SECONDS
from game.sprites.persons.player import Player
from utils.loader import load_image

ConveyorBeltFiles = [
    "LL5.png",
    "LL4.png",
    "LL3.png",
    "LL2.png",
    "LL1.png",
]

class ConveyorBelt(Sprite):
    """Conveyor belt sprite."""

    # x: int = 500, y: int = 500, direction: Direction = Direction.right
    def __init__(self, params: ConveyorBeltParameters) -> None:
        """Initialize conveyor belt sprite."""
        super(ConveyorBelt, self).__init__()
        # self.surface = image.load("assets/conveyor_belt.png").convert()
        # self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        self.canInteract = False
        self.surface = Surface((500, 50))
        self.surfaces = [load_image(file,(0, 0, 0), 0.25)[0] for file in ConveyorBeltFiles]
        self.surface = load_image("LL5.png",(0, 0, 0), 0.25)[0]
        self.rect = self.surface.get_rect(center=params.position)
        self.direction = params.direction
        self.animSpeed = 10
        self.animCount = len(self.surfaces) * self.animSpeed

    def update(self) -> None:
        """Update conveyor belt sprite."""
        if self.animCount <= 0:
            self.animCount = len(self.surfaces) * self.animSpeed
        self.surface = self.surfaces[(self.animCount // self.animSpeed) % len(self.surfaces)]
        self.animCount -= 1

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
