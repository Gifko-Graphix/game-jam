import pygame as pg

from game.defs import PLAYER_TRIGGER_INTERACTION, Direction
from game.levels.parameters import PlayerParameters
from game.sprites.persons.person import Person
from game.sprites.shared.sounds import play_bg_music, play_interaction_sound
from utils.loader import load_image

walkUpFiles = [
    "PlayerB1.png",
    "PlayerB2.png",
    "PlayerB3.png",
    "PlayerB4.png",
    "PlayerB5.png",
    "PlayerB6.png",
    "PlayerB7.png",
    "PlayerB8.png",
]
walkDownFiles = [
    "PlayerF1.png",
    "PlayerF2.png",
    "PlayerF3.png",
    "PlayerF4.png",
    "PlayerF5.png",
    "PlayerF6.png",
    "PlayerF7.png",
    "PlayerF8.png",
]
walkLeftFiles = [
    "PlayerL1.png",
    "PlayerL2.png",
    "PlayerL3.png",
    "PlayerL4.png",
    "PlayerL5.png",
    "PlayerL6.png",
    "PlayerL7.png",
    "PlayerL8.png",
]
walkRightFiles = [
    "PlayerR1.png",
    "PlayerR2.png",
    "PlayerR3.png",
    "PlayerR4.png",
    "PlayerR5.png",
    "PlayerR6.png",
    "PlayerR7.png",
    "PlayerR8.png",
]

interactionFiles = [
    "PlayerSC1.png",
    "PlayerSC2.png",
    "PlayerSC3.png",
    "PlayerSC4.png",
    "PlayerSC5.png",
    "PlayerSC6.png",
]
PLAYER_TIME_TO_INTERACT = 2


class Player(Person):
    def __init__(self, params: PlayerParameters):
        Person.__init__(self)
        self.surface, self.rect = load_image("PlayerL.png", -1, scale=1)
        self.walkUpAnim = [load_image(file, -1, 1) for file in walkUpFiles]
        self.walkDownAnim = [load_image(file, -1, 1) for file in walkDownFiles]
        self.walkLeftAnim = [load_image(file, -1, 1) for file in walkLeftFiles]
        self.walkRightAnim = [load_image(file, -1, 1) for file in walkRightFiles]
        self.interactionAnim = [load_image(file, -1, 1) for file in interactionFiles]

        self.area = pg.Rect(100, 100, 600, 300)

        self.idleUp = load_image("PlayerB.png", -1, 1)
        self.idleDown = load_image("PlayerF.png", -1, 1)
        self.idleLeft = load_image("PlayerL.png", -1, 1)
        self.idleRight = load_image("PlayerR.png", -1, 1)
        self.isInteracting = False
        self.interactWith = None
        self.allInteractables = None
        self.timeToInteract = PLAYER_TIME_TO_INTERACT
        self.isWalking = False
        self.walkCount = 8
        self.isCaught = False
        self.velocity = 5
        self.direction = Direction.up
        self.rect.topleft = params.position
        self.animSpeed = 10
        self.interactCount = len(self.interactionAnim) * self.animSpeed

    def interact(self, sprite: Person):
        if hasattr(sprite, "isBroken"):
            sprite.foo_action(self.allInteractables)
        else:
            sprite.foo_action()

    def walkLeft(self):
        if not self.isInteracting:
            self.isWalking = True
            self.direction = Direction.left
            self.surface = self.walkLeftAnim[self.walkCount % 8][0]
            self.walkCount -= 1
            if self.rect.left > self.area.left:
                self.rect.move_ip(-self.velocity, 0)

    def walkRight(self):
        if not self.isInteracting:
            self.isWalking = True
            self.direction = Direction.right
            self.surface = self.walkRightAnim[self.walkCount % 8][0]
            self.walkCount -= 1
            if self.rect.right < self.area.right:
                self.rect.move_ip(self.velocity, 0)

    def walkUp(self):
        if not self.isInteracting:
            self.isWalking = True
            self.direction = Direction.up
            self.surface = self.walkUpAnim[self.walkCount % 8][0]
            self.walkCount -= 1
            if self.rect.top < self.area.top:
                self.rect.move_ip(0, self.velocity)
            if self.rect.top > self.area.top:
                self.rect.move_ip(0, -self.velocity)

    def walkDown(self):
        if not self.isInteracting:
            self.isWalking = True
            self.direction = Direction.down
            self.surface = self.walkDownAnim[self.walkCount % 8][0]
            self.walkCount -= 1
            if self.rect.bottom < self.area.bottom:
                self.rect.move_ip(0, self.velocity)

    def update(self):
        if self.isInteracting and not self.isWalking:
            if self.interactCount <= 0:
                self.interactCount = len(self.interactionAnim) * self.animSpeed
            self.surface = self.interactionAnim[(self.interactCount // self.animSpeed) % len(self.interactionAnim)][0]
            self.interactCount -= 1
        elif self.isWalking and not self.isInteracting:
            if self.walkCount == 0:
                self.walkCount = 8
        elif not self.isWalking and not self.isInteracting:
            if self.direction == Direction.up:
                self.surface = self.idleUp[0]
            if self.direction == Direction.down:
                self.surface = self.idleDown[0]
            if self.direction == Direction.left:
                self.surface = self.idleLeft[0]
            if self.direction == Direction.right:
                self.surface = self.idleRight[0]

    def triggerInteractionDelay(self, allInteractables):
        self.allInteractables = allInteractables
        for sprite in allInteractables:
            if sprite.canInteract:
                pg.time.set_timer(PLAYER_TRIGGER_INTERACTION, 1000)
                play_interaction_sound()
                self.isInteracting = True
                self.interactWith = sprite
                self.timeToInteract = 3 if hasattr(sprite, "isOneTime") else PLAYER_TIME_TO_INTERACT

    def checkInteractTimer(self):
        if self.isInteracting:
            if self.timeToInteract == 0:
                pg.time.set_timer(PLAYER_TRIGGER_INTERACTION, 0)
                self.isInteracting = False
                self.timeToInteract = PLAYER_TIME_TO_INTERACT
                self.interact(self.interactWith)
                play_bg_music()
            else:
                self.timeToInteract -= 1
