import pygame as pg

from game.defs import Direction


class Person(pg.sprite.Sprite):
    """Abstract class for all person objects"""

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.area = pg.display.get_surface().get_rect()
        self.velocity = 1
        self.canInteract = False

    def update(self):
        pass

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
