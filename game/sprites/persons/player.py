import pygame as pg
from game.sprites.persons.person import Person

class Player(Person):
  def __init__(self):
    Person.__init__(self)
    self.isCaught = False
    self.velocity = 2
    self.rect.topleft = 10, 90

