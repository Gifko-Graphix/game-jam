import pygame

from pygame import display, event, key, time
from pygame.sprite import Group as SpriteGroup, spritecollideany

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
)
from game.sprites.cloud import Cloud
from game.sprites.enemy import Enemy
from game.sprites.player import Player
from game.defs import SCREEN_WIDTH, SCREEN_HEIGHT


class Runner:
    """Runner for the Game"""

    def __init__(self) -> None:
        pass

    def start(self) -> None:
        # pygame setup
        pygame.init()  # do not call unless necessary, because it takes a while to load
        screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        clock = time.Clock()
        player = Player()

        # Create a custom event for adding a new enemy
        ADDENMEY = pygame.USEREVENT + 1
        time.set_timer(ADDENMEY, 250)
        ADDCLOUD = pygame.USEREVENT + 2
        time.set_timer(ADDCLOUD, 2000)

        # one group for all sprites
        all_sprites = SpriteGroup()
        all_sprites.add(player)

        # one group for enemies
        enemies = SpriteGroup()

        # one group for clouds
        clouds = SpriteGroup()

        running = True

        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for e in event.get():
                if e.type == pygame.QUIT:
                    running = False
                elif e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        running = False
                elif e.type == ADDENMEY:
                    new_enemy = Enemy()
                    enemies.add(new_enemy)
                    all_sprites.add(new_enemy)
                elif e.type == ADDCLOUD:
                    new_cloud = Cloud()
                    clouds.add(new_cloud)
                    all_sprites.add(new_cloud)

            pressed_keys = key.get_pressed()
            player.update(pressed_keys)

            # update enemies' position
            enemies.update()

            # update clouds' position
            clouds.update()

            # Fill the screen with black
            screen.fill((135, 205, 245))

            # draw all sprites
            for entity in all_sprites:
                screen.blit(entity.surface, entity.rect)

            if spritecollideany(player, enemies):
                player.kill()
                running = False

            # refresh display
            display.flip()

            # ensure program maintains a rate of 30 frames per second
            clock.tick(30)

    def stop(self) -> None:
        pygame.quit()
