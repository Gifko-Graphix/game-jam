import pygame as pg

from game.defs import WORKER_TIMER_EVENT, Direction, WorkerState
from game.sprites.persons.person import Person
from game.sprites.persons.player import Player
from utils.loader import load_image

DISTRACTION_TIME_SECONDS = 40


class Worker(Person):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.surface, self.rect = load_image("temp_worker.png", -1)
        self.isWorking = True
        self.interactDisplayText = "press SPACE to distract worker"
        self.state = WorkerState.working
        self.direction = Direction.up
        self.velocity = 10
        self.rect.topleft = (x, y)
        self.distractedTimerValue = DISTRACTION_TIME_SECONDS
        self.hitbox = self.rect.scale_by(2, 2)

    def update(self, all_sprites) -> None:
        pass

    def detectPlayer(self, player: Player) -> None:
        if self.hitbox.colliderect(player.rect):
            self.canInteract = True
        else:
            self.canInteract = False

    def walk(self):
        newpos = self.rect.move((self.velocity, 0))
        if not self.area.contains(newpos):
            if self.rect.left <= self.area.left or self.rect.right >= self.area.right:
                self.velocity *= -1
                newpos = self.rect.move((self.velocity, 0))
                self.surface = pg.transform.flip(self.surface, True, False)
        self.rect = newpos
        self.hitbox = self.rect.scale_by(2, 2)

    def foo_action(self):
        self.state = WorkerState.distracted
        self.distractedTimerValue = DISTRACTION_TIME_SECONDS
        pg.time.set_timer(WORKER_TIMER_EVENT, 100)

    def countdown_distraction(self):
        self.distractedTimerValue -= 1
        if self.distractedTimerValue <= 0:
            pg.time.set_timer(WORKER_TIMER_EVENT, 0)
            self.state = WorkerState.working
