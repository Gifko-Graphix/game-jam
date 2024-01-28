from typing import Any
import pygame as pg

from game.defs import ELECTRIC_PANEL_TIMER_EVENT
from game.levels.parameters import ElectricPanelParameters
from game.sprites.persons.player import Player
from utils.loader import load_image

OFF_TIME_SECONDS = 50

panelFiles = [
    "electric_panel1.png",
    "electric_panel2.png",
    "electric_panel3.png",
    "electric_panel4.png",
    "electric_panel5.png",
    "electric_panel6.png",
    "electric_panel7.png",
    "electric_panel8.png",
]

panelActiveFiles = [
    "electric_panel1.png",
    "electric_panel2.png",
    "electric_panel3.png",
]

panelBrokenFiles = [
    "electric_panel4.png",
    "electric_panel6.png",
    "electric_panel8.png",
]

class ElectricPanel(pg.sprite.Sprite):
    def __init__(self, params: ElectricPanelParameters) -> None:
        super().__init__()
        self.surface, self.rect = load_image("electric_panel1.png", -1, 5)
        self.activeAnim = [load_image(file,-1, 5)[0] for file in panelActiveFiles]
        self.brokenAnim = [load_image(file,-1, 5)[0] for file in panelBrokenFiles]

        self.isOn = True
        self.isOneTime = True
        self.isBroken = False
        self.canInteract = False
        self.rect.topleft = params.position
        self.hitbox = self.rect.scale_by(2, 2)
        self.countdownTimerValue = OFF_TIME_SECONDS
        self.hitbox = self.rect.scale_by(2, 2)
        self.interactDisplayText = "press SPACE to switch off Panel"
        self.animSpeed = 10
        self.animCount = len(self.activeAnim) * self.animSpeed
    
    def update(self) -> None:
        if self.animCount <= 0:
            self.animCount = len(self.activeAnim) * self.animSpeed
        if self.isBroken or not self.isOn:
            self.surface = self.brokenAnim[(self.animCount // self.animSpeed) % len(self.activeAnim)]
        else:
            self.surface = self.activeAnim[(self.animCount // self.animSpeed) % len(self.activeAnim)]
        self.animCount -= 1

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
