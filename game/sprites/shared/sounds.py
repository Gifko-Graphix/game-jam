"""Shared sounds for sprites."""

import pygame


def play_interaction_sound():
    """Play interaction sound."""
    pygame.mixer.music.load("assets/interaction.mp3")
    pygame.mixer.music.play()

def play_bg_music():
    """Play Background music."""
    pygame.mixer.music.load("assets/background_music.mp3")
    pygame.mixer.music.play()