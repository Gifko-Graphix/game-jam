from game.sprites.persons.person import Person
from utils.loader import load_image


class Player(Person):
    def __init__(self):
        Person.__init__(self)
        self.surface, self.rect = load_image("star.png", -1, scale=0.05)
        self.isCaught = False
        self.velocity = 1
        self.rect.topleft = 10, 90