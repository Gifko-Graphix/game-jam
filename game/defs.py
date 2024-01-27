"""Constants for the game."""

from enum import Enum

import pygame

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
LEVEL_TIMER_EVENT = pygame.USEREVENT + 1
WORKER_TIMER_EVENT = pygame.USEREVENT + 2
PLAYER_TRIGGER_INTERACTION = pygame.USEREVENT + 3
MANAGER_METER_EVENT = pygame.USEREVENT + 4
ELECTRIC_PANEL_TIMER_EVENT = pygame.USEREVENT + 5

# Timer values
LEVEL_TIMER_VALUE = 90

class WorkerState(Enum):
    working = 1
    distracted = 2
    idle = 3


class Direction(Enum):
    up = 1
    down = 2
    left = 3
    right = 4
