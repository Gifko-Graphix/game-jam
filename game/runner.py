# Example file showing a circle moving on screen
import pygame
from game.sprites.persons.player import Player
from game.sprites.persons.worker import Worker



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

        print("Started")
        player = Player()
        worker = Worker()

        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # fill the screen with a color to wipe away anything from last frame
            screen.fill("cyan")
            allsprites = pygame.sprite.RenderPlain((player, worker))
            workers = pygame.sprite.Group(worker)
            allsprites.draw(screen)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                if not player.willCollide("Up", workers):
                    player.walkUp()
            if keys[pygame.K_DOWN]:
                if not player.willCollide("Down", workers):
                    player.walkDown()
            if keys[pygame.K_LEFT]:
                if not player.willCollide("Left", workers):
                    player.walkLeft()
            if keys[pygame.K_RIGHT]:
                if not player.willCollide("Right", workers):
                    player.walkRight()
            
            worker.detectPlayer(player)

            # flip() the display to put your work on screen
            
            allsprites.update()
            pygame.display.flip()

    def stop(self) -> None:
        pygame.quit()