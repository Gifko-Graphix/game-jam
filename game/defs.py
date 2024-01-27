"""Constants for the game."""

import pygame
from enum import Enum


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
LEVEL_TIMER_EVENT = pygame.USEREVENT + 1
WORKER_TIMER_EVENT = pygame.USEREVENT + 2
PLAYER_TRIGGER_INTERACTION = pygame.USEREVENT + 3

# Timer values
LEVEL_TIMER_VALUE = 90


WorkerState = Enum("WorkerState", ["working", "distracted"])
Direction = Enum("Direction", ["up", "down", "left", "right"])