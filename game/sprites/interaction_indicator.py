from pygame import Surface, display, font
from pygame.sprite import Sprite


class InteractionIndicator(Sprite):
    def __init__(self):
        super().__init__()
        self.isActive = False
        self.text = "Go cause Chaos!"
        self.displayText = self.text
        self.surface = Surface((100, 20))
        self.surface.fill((100, 200, 100))
        self.font = font.SysFont("Daydream", 10)
        screen = display.get_surface()
        self.rect = self.surface.get_rect(
            center=(screen.get_width() / 2 - 50, screen.get_height() - 50)
        )

    def update(self):
        self.surface = self.font.render(self.displayText, True, (255, 255, 255))

    def checkForAnyPossibleInteract(self, sprites, player):
        if player.isInteracting:
            self.displayText = "casting spell..."
        else:
            for sprite in sprites:
                if sprite.canInteract:
                    self.isActive = True
                    self.displayText = sprite.interactDisplayText
                    return
            self.isActive = False
            self.displayText = self.text
            return
