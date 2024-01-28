import pygame as pg

from game.defs import WORKER_TIMER_EVENT, Direction, WorkerState
from game.sprites.persons.person import Person
from game.sprites.persons.player import Player
from utils.loader import load_image
import random

DISTRACTION_TIME_SECONDS = 40
WORKER_DISTRACTION_TIMES = [40, 60, 20]

Worker1WorkingFiles = [
    "Worker1BS.png",
    "Worker1BS1.png",
    "Worker1BS2.png",
    "Worker1BS3.png",
    "Worker1BS4.png",
    "Worker1BS5.png",
]

Worker1DistractedFiles = [
    "Worker1SC.png",
    "Worker1SC1.png",
    "Worker1SC2.png",
    "Worker1SC3.png",
    "Worker1SC4.png",
    "Worker1SC5.png",
]

# Worker2WorkingFiles = [
#     "Worker2BS.png",
#     "Worker2BS1.png",
#     "Worker2BS2.png",
#     "Worker2BS3.png",
#     "Worker2BS4.png",
#     "Worker2BS5.png",
# ]

# Worker2BusyFiles = [
#     "Worker2SC.png",
#     "Worker2SC1.png",
#     "Worker2SC2.png",
#     "Worker2SC3.png",
#     "Worker2SC4.png",
#     "Worker2SC5.png",
# ]

# Worker3WorkingFiles = [
#     "Worker3BS.png",
#     "Worker3BS1.png",
#     "Worker3BS2.png",
#     "Worker3BS3.png",
#     "Worker3BS4.png",
#     "Worker3BS5.png",
# ]

# Worker3BusyFiles = [
#     "Worker3SC.png",
#     "Worker3SC1.png",
#     "Worker3SC2.png",
#     "Worker3SC3.png",
#     "Worker3SC4.png",
#     "Worker3SC5.png",
# ]


class Worker(Person):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.surface, self.rect = load_image("Worker1BS.png", -1)
        self.isWorking = True
        self.interactDisplayText = "press SPACE to distract worker"
        self.state = WorkerState.working
        self.direction = Direction.up
        self.velocity = 10
        # self.workerType = random.choice([0,1,2])
        self.workerType = 0
        self.workerBusyAnim = [load_image(file, -1, 1) for file in Worker1WorkingFiles]
        self.workerDistractedAnim = [load_image(file, -1, 1) for file in Worker1DistractedFiles]
        self.rect.topleft = (x, y)
        self.distractedTimerValue = WORKER_DISTRACTION_TIMES[self.workerType]
        self.hitbox = self.rect.scale_by(2, 2)
        self.animCount = 18

    def update(self, all_sprites) -> None:
        if self.animCount <= 0:
            self.animCount = 18
        if self.state == WorkerState.working:
            self.surface = self.workerBusyAnim[(self.animCount // 3) % 6][0]
        elif self.state == WorkerState.distracted:
            self.surface = self.workerDistractedAnim[(self.animCount // 3) % 6][0]
        self.animCount -= 1


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
        self.distractedTimerValue = WORKER_DISTRACTION_TIMES[self.workerType]
        pg.time.set_timer(WORKER_TIMER_EVENT, 100)

    def countdown_distraction(self):
        self.distractedTimerValue -= 1
        if self.distractedTimerValue <= 0:
            pg.time.set_timer(WORKER_TIMER_EVENT, 0)
            self.state = WorkerState.working
