import pygame as pg

from game.defs import Direction


class Person(pg.sprite.Sprite):
    """Abstract class for all person objects"""

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.area = pg.display.get_surface().get_rect()
        self.velocity = 1
        self.isInteracting = False
        self.canInteract = False

    def update(self):
        pass

    def walkLeft(self):
        if self.rect.left > self.area.left:
            self.rect.move_ip(-self.velocity, 0)

    def walkRight(self):
        if self.rect.right < self.area.right:
            self.rect.move_ip(self.velocity, 0)

    def walkUp(self):
        if self.rect.top > self.area.top:
            self.rect.move_ip(0, -self.velocity)

    def walkDown(self):
        if self.rect.bottom < self.area.bottom:
            self.rect.move_ip(0, self.velocity)

    def willCollide(self, direction: Direction, allsprites):
        if direction == Direction.left:
            nextPos = self.rect.move(-self.velocity, 0)
        if direction == Direction.right:
            nextPos = self.rect.move(self.velocity, 0)
        if direction == Direction.up:
            nextPos = self.rect.move(0, -self.velocity)
        if direction == Direction.down:
            nextPos = self.rect.move(0, self.velocity)

        allRects = [sprite.rect for sprite in allsprites]
        return nextPos.collidelist(allRects) != -1
