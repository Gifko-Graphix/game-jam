import pygame
from pygame import display, event, time
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
)
from pygame.sprite import Group as SpriteGroup

from game.defs import LEVEL_TIMER_EVENT, SCREEN_HEIGHT, SCREEN_WIDTH
from game.sprites.manager import Manager
from game.sprites.persons.player import Player
from game.sprites.persons.worker import Worker

# from game.sprites.cloud import Cloud
# from game.sprites.enemy import Enemy
# from game.sprites.player import Player
from game.sprites.timer import Timer


class Runner:
    """Runner for the Game"""

    def __init__(self) -> None:
        """Initialize the game."""
        # pygame setup
        pygame.init()
        self.screen = display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED
        )
        self.clock = time.Clock()
        self.running: bool = False
        self.all_sprites = SpriteGroup()
        self.workers = SpriteGroup()

        self.managers = SpriteGroup()
        self.managers.add(Manager())
        self.level_timer = Timer()
        self.all_sprites.add(self.level_timer)
        self.player_win = False
        self.game_over = False

    def _update_level_timer(self) -> None:
        """Update the level timer."""
        self.level_timer.value -= 1
        self.level_timer.update()
        if self.level_timer.value == 0:
            time.set_timer(LEVEL_TIMER_EVENT, 0)
            self.running = False

    def check_events(self) -> None:
        """Check for events."""
        for e in event.get():
            if e.type == pygame.QUIT:
                self.running = False
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    self.running = False
            elif e.type == LEVEL_TIMER_EVENT:
                self._update_level_timer()

    def check_win_state(self) -> None:
        """Check if the player has won."""
        if self.level_timer.value == 0:
            self.game_over = True
            # check the manager's frustration level
            for m in self.managers.sprites():
                if m.frustration_level < 100:
                    self.player_win = False
        else:
            for m in self.managers.sprites():
                if m.frustration_level >= 100:
                    self.player_win = True
                    self.game_over = True

        # final check of the player's win state
        if self.game_over:
            # stop the level timer
            time.set_timer(LEVEL_TIMER_EVENT, 0)

            # stop the game
            self.running = False

    def start(self) -> None:
        player = Player()
        worker = Worker()

        self.running = True

        # one group for all sprites
        self.all_sprites.add(player)
        self.all_sprites.add(worker)
        self.workers.add(worker)

        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            self.check_events()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                if not player.willCollide("Up", self.workers):
                    player.walkUp()
            if keys[pygame.K_DOWN]:
                if not player.willCollide("Down", self.workers):
                    player.walkDown()
            if keys[pygame.K_LEFT]:
                if not player.willCollide("Left", self.workers):
                    player.walkLeft()
            if keys[pygame.K_RIGHT]:
                if not player.willCollide("Right", self.workers):
                    player.walkRight()

            self.all_sprites.update()
            worker.detectPlayer(player)

            self.check_win_state()

            # Fill the screen with black
            self.screen.fill((135, 205, 245))

            # draw all sprites
            for entity in self.all_sprites:
                self.screen.blit(entity.surface, entity.rect)

            # refresh display
            display.flip()

            # ensure program maintains a rate of 30 frames per second
            self.clock.tick(30)

        # after loop ends check what state the game is in and whether the player won or lost
        if self.game_over:
            if self.player_win:
                print("You win!")
                # render win screen & play win sound
                # play next level?
            else:
                print("You lose!")
                # render lose screen & play lose sound
                # play again?

    def stop(self) -> None:
        pygame.quit()
