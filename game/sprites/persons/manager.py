"""Manager Sprite."""
from pygame import image
from pygame.locals import RLEACCEL as RL
from pygame.sprite import Sprite

from game.sprites.shared.meters import Meter

# Define corner positions
corner_positions = [
    (100, 100),  # Top-left corner
    (600, 100),  # Top-right corner
    (600, 600),  # Bottom-right corner
    (100, 600),  # Bottom-left corner
]

# Object parameters
speed = 5  # Adjust speed as needed


class Manager(Sprite):
    """Player Sprite"""

    def __init__(self):
        super(Manager, self).__init__()
        self.surface = image.load("assets/jet.png").convert()
        self.surface.set_colorkey((255, 255, 255), RL)
        self.rect = self.surface.get_rect(center=(100, 100))  # starting position
        self.pseudo_rect = self.rect.scale_by(4, 4)
        self.is_frustrated = False
        self.meter = Meter()
        self.current_corner = 0

    def update(self):
        """Update manager sprite."""
        # Calculate the movement towards the current corner

        corner_x, corner_y = corner_positions[self.current_corner]
        dx = corner_x - self.rect.x
        dy = corner_y - self.rect.y
        distance = (dx**2 + dy**2) ** 0.5

        if distance > speed:
            # Normalize the direction vector
            direction = (dx / distance, dy / distance)
            # Move the rectangle
            self.rect.x += int(direction[0] * speed)
            self.rect.y += int(direction[1] * speed)
            self.pseudo_rect.center = self.rect.center
        else:
            # Move to the next corner
            self.current_corner = (self.current_corner + 1) % len(corner_positions)

        self.meter.update_position(self.rect.x, self.rect.y)
