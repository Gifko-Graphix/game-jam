"""Manager Sprite."""
import pygame as pg

from pygame import image
from pygame.locals import RLEACCEL as RL
from pygame.sprite import Sprite
from game.defs import Direction
from game.sprites.persons.person import Person

from utils.loader import load_image
from game.sprites.shared.meters import Meter

# Define corner positions
corner_positions: list[tuple[int, int, Direction]] = [
    (100, 100, Direction.up),  # Top-left corner
    (600, 100, Direction.right),  # Top-right corner
    (600, 600, Direction.down),  # Bottom-right corner
    (100, 600, Direction.left),  # Bottom-left corner
]

# Object parameters
speed = 5  # Adjust speed as needed

M_walkUpFiles = [
    "ManagerB1.png",
    "ManagerB2.png",
    "ManagerB3.png",
    "ManagerB4.png",
    "ManagerB5.png",
    "ManagerB6.png",
    "ManagerB7.png",
    "ManagerB8.png",
]
M_walkDownFiles = [
    "ManagerF1.png",
    "ManagerF2.png",
    "ManagerF3.png",
    "ManagerF4.png",
    "ManagerF5.png",
    "ManagerF6.png",
    "ManagerF7.png",
    "ManagerF8.png",
]
M_walkLeftFiles = [
    "ManagerL1.png",
    "ManagerL2.png",
    "ManagerL3.png",
    "ManagerL4.png",
    "ManagerL5.png",
    "ManagerL6.png",
    "ManagerL7.png",
    "ManagerL8.png",
]
M_walkRightFiles = [
    "ManagerR1.png",
    "ManagerR2.png",
    "ManagerR3.png",
    "ManagerR4.png",
    "ManagerR5.png",
    "ManagerR6.png",
    "ManagerR7.png",
    "ManagerR8.png",
]

class Manager(Person):
    """Player Sprite"""

    def __init__(self):
        super(Manager, self).__init__()
        self.surface, self.rect = load_image("ManagerR.png", -1, 1)
        self.pseudo_rect = self.rect.scale_by(4, 4)
        self.walkUpAnim = [load_image(file, -1, 1) for file in M_walkUpFiles]
        self.walkDownAnim = [load_image(file, -1, 1) for file in M_walkDownFiles]
        self.walkLeftAnim = [load_image(file, -1, 1) for file in M_walkLeftFiles]
        self.walkRightAnim = [load_image(file, -1, 1) for file in M_walkRightFiles]

        self.idleUp = load_image("ManagerB.png", -1, 1)
        self.idleDown = load_image("ManagerF.png", -1, 1)
        self.idleLeft = load_image("ManagerL.png", -1, 1)
        self.idleRight = load_image("ManagerR.png", -1, 1)
        self.isWalking = False
        self.walkCount = 8
        self.velocity = 5
        self.is_frustrated = False
        self.meter = Meter()
        self.current_corner = 0
        self.direction = Direction.up

    def update(self):
        """Update manager sprite."""
        # Calculate the movement towards the current corner
        self.isWalking = True
        if self.isWalking:
            
            if self.walkCount == 0:
                self.walkCount = 8
            elif self.direction == Direction.up:
                print("up")
                self.surface = self.walkUpAnim[self.walkCount % 8][0]
            elif self.direction == Direction.down:
                print("down")
                self.surface = self.walkDownAnim[self.walkCount % 8][0]
            elif self.direction == Direction.left:
                print("left")
                self.surface = self.walkLeftAnim[self.walkCount % 8][0]
            elif self.direction == Direction.right:
                print("right")
                self.surface = self.walkRightAnim[self.walkCount % 8][0]
            corner_x, corner_y, direction = corner_positions[self.current_corner]
            self.direction = direction
            dx = corner_x - self.rect.x
            dy = corner_y - self.rect.y
            distance = (dx**2 + dy**2) ** 0.5
            self.walkCount -=1
        else:
            if self.direction == Direction.up:
                self.surface = self.idleUp[0]
            if self.direction == Direction.down:
                self.surface = self.idleDown[0]
            if self.direction == Direction.left:
                self.surface = self.idleLeft[0]
            if self.direction == Direction.right:
                self.surface = self.idleRight[0]

        

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
