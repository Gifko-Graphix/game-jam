from pygame.sprite import Sprite
from pygame import Surface, Rect, Color, font
from pygame import display

class CanInteractIndicator(Sprite):
  def __init__(self):
    super().__init__()
    self.isActive = False
    self.text = "Press SPACE to interact"
    self.displayText = self.text
    self.surface = Surface((100, 20))
    self.surface.fill((100, 200, 100))
    self.font = font.SysFont("Roboto", 24)
    screen = display.get_surface()
    self.rect = self.surface.get_rect(center=(screen.get_width()/2 - 50, screen.get_height() - 50))
  
  def update(self, text=None):
    if self.isActive:
      self.surface = self.font.render(self.displayText, True, (255, 255, 255))
    else:
      self.surface = self.font.render(self.displayText, True, (200, 200, 200))

  def checkForAnyPossibleInteract(self, sprites, player):
    if player.isInteracting:
      self.displayText = "performing action..."
    else:
      for sprite in sprites:
        if sprite.canInteract:
          self.isActive = True
          self.displayText = sprite.interactDisplayText
          return
      self.isActive = False
      self.displayText = self.text
      return