# Example file showing a circle moving on screen
import pygame
from game.sprites.persons.player import Player


class Runner:
    """Runner for the Game"""
    def __init__(self) -> None:
        pass
        
    def start(self) -> None:
        # pygame setup
        # pygame.init()
        screen = pygame.display.set_mode((500, 500))
        clock = pygame.time.Clock()
        running = True
        dt = 0

        player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        print("Started")
        player = Player()

        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # fill the screen with a color to wipe away anything from last frame
            screen.fill("cyan")
            allsprites = pygame.sprite.RenderPlain((player))


            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                player.walkUp()
            if keys[pygame.K_DOWN]:
                player.walkDown()
            if keys[pygame.K_LEFT]:
                player.walkLeft()
            if keys[pygame.K_RIGHT]:
                player.walkRight()

            # flip() the display to put your work on screen
            allsprites.draw(screen)
            pygame.display.flip()

    def stop(self) -> None:
        pygame.quit()