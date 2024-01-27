from game.defs import Direction
from game.sprites.persons.person import Person
from utils.loader import load_image


class Player(Person):
    def __init__(self):
        Person.__init__(self)
        self.surface, self.rect = load_image("star.png", -1, scale=0.03)
        self.isCaught = False
        self.velocity = 15
        self.direction = Direction.up
        self.rect.topleft = 10, 90

    def interact(self, allInteractables):
      for sprite in allInteractables:
        if sprite.canInteract:
            sprite.foo_action()