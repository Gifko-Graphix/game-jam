import pygame as pg

from game.defs import ELECTRIC_PANEL_TIMER_EVENT
from game.sprites.persons.player import Player
from utils.loader import load_image

OFF_TIME_SECONDS = 70


class ElectricPanel(pg.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.surface, self.rect = load_image("star.png", -1, 0.025)
        self.isOn = True
        self.canInteract = False
        self.rect.topleft = (900, 200)
        self.hitbox = self.rect.scale_by(2,2)
        self.countdownTimerValue = OFF_TIME_SECONDS
        self.hitbox = self.rect.scale_by(2, 2)

    def update(self) -> None:
        pass

    def detectPlayer(self, player: Player) -> None:
        if self.hitbox.colliderect(player.rect):
            self.canInteract = True
        else:
            self.canInteract = False

    def foo_action(self):
        self.isOn = False
        self.countdownTimerValue = OFF_TIME_SECONDS
        pg.time.set_timer(ELECTRIC_PANEL_TIMER_EVENT, 100)

    def countdown_timer(self):
        self.countdownTimerValue -= 1
        if self.countdownTimerValue <= 0:
            pg.time.set_timer(ELECTRIC_PANEL_TIMER_EVENT, 0)
            self.isOn = True
