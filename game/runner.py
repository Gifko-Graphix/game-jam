# Example file showing a circle moving on screen
import pygame


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
        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # fill the screen with a color to wipe away anything from last frame
            screen.fill("purple")

            pygame.draw.circle(screen, "red", player_pos, 40)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and keys[pygame.K_s]:
                player_pos.y += 300 * dt * 0.707
                player_pos.x -= 300 * dt * 0.707
            elif keys[pygame.K_a] and keys[pygame.K_w]:
                player_pos.y -= 300 * dt * 0.707
                player_pos.x -= 300 * dt * 0.707
            elif keys[pygame.K_d] and keys[pygame.K_w]:
                player_pos.y -= 300 * dt * 0.707
                player_pos.x += 300 * dt * 0.707
            elif keys[pygame.K_d] and keys[pygame.K_s]:
                player_pos.y += 300 * dt * 0.707
                player_pos.x += 300 * dt * 0.707
            elif keys[pygame.K_w]:
                player_pos.y -= 300 * dt
            elif keys[pygame.K_s]:
                player_pos.y += 300 * dt
            elif keys[pygame.K_a]:
                player_pos.x -= 300 * dt
            elif keys[pygame.K_d]:
                player_pos.x += 300 * dt

            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            dt = clock.tick(60) / 1000

    def stop(self) -> None:
        pygame.quit()