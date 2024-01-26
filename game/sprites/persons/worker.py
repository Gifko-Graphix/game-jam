import pygame as pg
from game.sprites.persons.person import Person
from game.sprites.persons.player import Player
from utils.loader import load_image


INTERACT_DISTANCE = 0.1

class Worker(Person):
  def __init__(self) -> None:
    super().__init__()
    self.image, self.rect = load_image("temp_worker.png", -1, scale=1)
    self.isWorking = True
    self.isFacing = "Forward"
    self.initial_rect = self.rect
    self.rect.topleft = (200, 200)

  def update(self) -> None:
    if self.canInteract:
      self.isWorking = False
    else:
      self.rect = self.initial_rect
      self.isWorking = True

  def detectPlayer(self, player: Player) -> None:
    if(self.rect.inflate(INTERACT_DISTANCE,INTERACT_DISTANCE).colliderect(player.rect)):
      self.canInteract = True
    else:
      self.canInteract = False
