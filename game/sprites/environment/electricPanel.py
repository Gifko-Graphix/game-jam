import pygame as pg

from game.defs import ELECTRIC_PANEL_TIMER_EVENT
from game.levels.parameters import ElectricPanelParameters
from game.sprites.persons.player import Player
from utils.loader import load_image

OFF_TIME_SECONDS = 50


class ElectricPanel(pg.sprite.Sprite):
    def __init__(self, params: ElectricPanelParameters) -> None:
        super().__init__()
        self.surface, self.rect = load_image("star.png", -1, 0.025)
        self.isOn = True
        self.isOneTime = True
        self.isBroken = False
        self.canInteract = False
        self.rect.topleft = params.position
        self.hitbox = self.rect.scale_by(2, 2)
        self.countdownTimerValue = OFF_TIME_SECONDS
        self.hitbox = self.rect.scale_by(2, 2)
        self.interactDisplayText = "press SPACE to switch off Panel"

    def update(self) -> None:
        pass

    def detectPlayer(self, player: Player) -> None:
        if self.hitbox.colliderect(player.rect) and not self.isBroken:
            self.canInteract = True
        else:
            self.canInteract = False

    def foo_action(self, allworkers):
        self.isOn = False
        self.isBroken = True
        self.countdownTimerValue = OFF_TIME_SECONDS
        workers = allworkers.sprites()
        for worker in workers:
            if hasattr(worker, "change_animation_speed_factor"):
                worker.change_animation_speed_factor(6)
        pg.time.set_timer(ELECTRIC_PANEL_TIMER_EVENT, 100)

    def countdown_timer(self):
        self.countdownTimerValue -= 1
        if self.countdownTimerValue <= 0:
            pg.time.set_timer(ELECTRIC_PANEL_TIMER_EVENT, 0)
            self.isOn = True
