from typing import Optional

import pygame
from pygame import display, event, font, time
from pygame.locals import K_ESCAPE, KEYDOWN
from pygame.sprite import Group as SpriteGroup
from pygame.locals import *
from pygame import mixer

import game.colors as colors
from game.defs import (
    ELECTRIC_PANEL_TIMER_EVENT,
    LEVEL_TIMER_EVENT,
    MANAGER_METER_EVENT,
    PLAYER_TRIGGER_INTERACTION,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WORKER_TIMER_EVENT,
    Direction,
    WorkerState,
)
from game.levels.list import levels
from game.levels.parameters import LevelParameters
from game.sprites.environment.conveyor_belt import ConveyorBelt
from game.sprites.environment.electricPanel import ElectricPanel
from game.sprites.interaction_indicator import InteractionIndicator
from game.sprites.persons.manager import Manager
from game.sprites.persons.player import Player
from game.sprites.persons.worker import Worker
from game.sprites.timer import Timer


class Runner:
    """Runner for the Game"""

    def __init__(self) -> None:
        """Initialize the game."""
        # pygame setup
        pygame.init()
        font.init()
        pygame.display.set_caption("Agents of Chaos")
        self.screen = display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
        )
        self.clock = time.Clock()
        self.running: bool = False
        self.player: Optional[Player] = None
        self.electricPanel: Optional[ElectricPanel] = None
        self.all_sprites = SpriteGroup()
        self.workers = SpriteGroup()
        self.playerInteractables = SpriteGroup()
        self.managers = SpriteGroup()
        self.meters = SpriteGroup()
        self.level_timer = Timer()
        self.player_win = False
        self.game_over = False
        self.CanInteractIndicator = None
        mixer.init()
        mixer.music.load('assets/background_music.mp3')
        mixer.music.play()

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
            elif e.type == WORKER_TIMER_EVENT:
                workers: list[Worker] = self.workers.sprites()
                managers: list[Manager] = self.managers.sprites()
                for worker in workers:
                    if worker.state == WorkerState.distracted:
                        worker.countdown_distraction()
                distracted_workers = [
                    w for w in workers if w.state == WorkerState.distracted
                ]
                if distracted_workers:
                    for m in managers:
                        m.meter.update(positive=True)

            elif e.type == PLAYER_TRIGGER_INTERACTION:
                self.player.checkInteractTimer()
            elif e.type == MANAGER_METER_EVENT:
                managers: list[Manager] = self.managers.sprites()
                for m in managers:
                    m.meter.update(positive=m.is_frustrated)
            elif e.type == ELECTRIC_PANEL_TIMER_EVENT:
                managers: list[Manager] = self.managers.sprites()
                self.electricPanel.countdown_timer()
                if not self.electricPanel.isOn:
                    for m in managers:
                        m.meter.update(positive=True)

    def check_win_state(self) -> None:
        """Check if the player has won."""
        if self.level_timer.value == 0:
            self.game_over = True
            # check the manager's frustration level
            for m in self.managers.sprites():
                if m.meter.is_full:
                    self.player_win = False
        else:
            managers: list[Manager] = self.managers.sprites()
            for m in managers:
                if m.meter.is_full:
                    print("game over")
                    self.player_win = True
                    self.game_over = True

        # final check of the player's win state
        if self.game_over:
            # stop the level timer
            time.set_timer(LEVEL_TIMER_EVENT, 0)

            # stop the game
            self.running = False

    def check_collisions(self) -> None:
        """Check if the player has collided with a manager."""
        managers = self.managers.sprites()
        for m in managers:
            if m.pseudo_rect.colliderect(self.player.rect):
                self.player_win = False
                self.game_over = True
                self.running = False

    def start(self) -> None:
        """Show the start Screen."""
        font = pygame.font.SysFont("Roboto Bold", 50)
        surface = font.render("Agents of Chaos", True, colors.WHITE)
        rect = surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100))
        self.screen.fill((135, 205, 245))
        self.screen.blit(surface, rect)

        font = pygame.font.SysFont("Roboto Bold", 30)
        surface = font.render("Press ENTER to start", True, colors.WHITE)
        rect = surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.screen.blit(surface, rect)
        display.flip()
        while True:
            for e in event.get():
                if e.type == pygame.QUIT:
                    self.end()
            keys = pygame.key.get_pressed()

            if keys[pygame.K_RETURN]:
                self.info_screen_story()
            if keys[pygame.K_ESCAPE]:
                self.end()

    def info_screen_controls(self) -> None:
        """Show the info Screen."""
        font = pygame.font.SysFont("Roboto Bold", 44)
        surface = font.render("Agents of Chaos", True, colors.WHITE)
        rect = surface.get_rect(center=(SCREEN_WIDTH / 2, 50))
        self.screen.fill((135, 205, 245))
        self.screen.blit(surface, rect)

        # add game instructions
        font = pygame.font.SysFont("Roboto", 28)
        surface = font.render("Controls", True, colors.WHITE)
        rect = surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 120))
        self.screen.blit(surface, rect)
        # movement instructions (Up/down/left/right)
        controls = """
        Arrow keys (Up/Down/Left/Right) =  Movement
        Space Bar = Interact with objects/People in the level to cause chaos
        ESC = Quit Game
        """

        font = pygame.font.SysFont("Roboto", 28)
        for idx, line in enumerate(controls.splitlines()):
            surface = font.render(line, True, colors.WHITE)
            rect = surface.get_rect(topleft=(50, 120+ idx*30))
            self.screen.blit(surface, rect)

        win_lose_cond = """
        Fill up the Manager's frustration meter to win the game.
        You lose when the timer runs out or when the Manager catches you.
        """

        font = pygame.font.SysFont("Roboto", 28)
        for idx, line in enumerate(win_lose_cond.splitlines()):
            surface = font.render(line, True, colors.WHITE)
            rect = surface.get_rect(topleft=(50, 120+ idx*30))
            self.screen.blit(surface, rect)

        # win condition (manager frustration)
        # lose condition (timer, get caught by manager)
        # electric panel (works only once, takes longest to activate)
        # workers when distracted have varying effects on manager frustration

        font = pygame.font.SysFont("Roboto Bold", 30)
        surface = font.render("Press ENTER to continue", True, colors.WHITE)
        rect = surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 200))
        self.screen.blit(surface, rect)
        display.flip()
        while True:
            for e in event.get():
                if e.type == pygame.QUIT:
                    self.end()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        self.start_round()
                    if e.key == pygame.K_ESCAPE:
                        self.end()
    
    def info_screen_story(self) -> None:
        """Show the info Screen."""
        font = pygame.font.SysFont("Roboto Bold", 44)
        surface = font.render("Agents of Chaos", True, colors.WHITE)
        rect = surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150))
        self.screen.fill((135, 205, 245))
        self.screen.blit(surface, rect)

        # story
        instructions = """
       We are Agents of Chaos. We are here to cause chaos in the factory.
       Interact with the workers and the electric panel to cause chaos.
        """

        font = pygame.font.SysFont("Roboto", 28)
        for idx, line in enumerate(instructions.splitlines()):
            surface = font.render(line, True, colors.WHITE)
            rect = surface.get_rect(topleft=(50, SCREEN_HEIGHT / 2 - 100+ idx*30))
            self.screen.blit(surface, rect)

        font = pygame.font.SysFont("Roboto Bold", 30)
        surface = font.render("Press ENTER to continue", True, colors.WHITE)
        rect = surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 200))
        self.screen.blit(surface, rect)
        display.flip()
        while True:
            for e in event.get():
                if e.type == pygame.QUIT:
                    self.end()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        self.info_screen_controls()
                    if e.key == pygame.K_ESCAPE:
                        self.end()


    def start_round(self):
        self.init(levels[0])
        self.game_over = False
        self.running = True
        self.player_win = None
        self.main_loop()

    def end(self, player_won: Optional[bool] = None) -> None:
        """Show the stop Screen."""
        if player_won is None:
            message = "Quit Game?"
        else:
            message = "You Win!" if player_won else "You Lose!"
        font = pygame.font.SysFont("Roboto Bold", 50)
        surface = font.render(message, True, colors.WHITE)
        rect = surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100))
        self.screen.fill((135, 205, 245))
        self.screen.blit(surface, rect)

        font = pygame.font.SysFont("Roboto Bold", 30)
        surface = font.render(
            "Press ENTER to play again, or Q to quit", True, colors.WHITE
        )
        rect = surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.screen.blit(surface, rect)
        display.flip()
        showEndScreen = True
        while showEndScreen:
            for e in event.get():
                if e.type == pygame.QUIT:
                    showEndScreen = False
                    self.stop()
            keys = pygame.key.get_pressed()

            if keys[pygame.K_RETURN]:
                showEndScreen = False
                self.all_sprites.empty()
                self.workers.empty()
                self.playerInteractables.empty()
                self.managers.empty()
                self.meters.empty()
                self.start_round()
                self.init(level_params=levels[0])
                self.main_loop()
            if keys[pygame.K_q]:
                showEndScreen = False
                self.stop()

    def run(self) -> None:
        """Start the game."""
        self.start()

        self.init(level_params=levels[0])
        self.main_loop()
        self.end()

    def init(self, level_params: LevelParameters):
        """Initialize the game."""
        self.player = Player(level_params.player)
        manager = Manager(level_params.manager)
        self.electricPanel = ElectricPanel(level_params.environment.electric_panel)
        self.CanInteractIndicator = InteractionIndicator()
        conveyor_belt = ConveyorBelt(level_params.environment.conveyor_belt)
        self.all_sprites.add(conveyor_belt)
        self.all_sprites.add(self.CanInteractIndicator)

        for params in level_params.environment.workers:
            worker = Worker(params)
            self.all_sprites.add(worker)
            self.workers.add(worker)
            self.playerInteractables.add(worker)

        self.meters.add(manager.meter)

        self.all_sprites.add(self.level_timer)
        self.all_sprites.add(self.player)
        self.all_sprites.add(manager.meter)
        self.all_sprites.add(self.electricPanel)
        self.playerInteractables.add(self.electricPanel)
        self.playerInteractables.add(conveyor_belt)
        self.all_sprites.add(worker)
        self.all_sprites.add(manager)

        self.managers.add(manager)

    def main_loop(self) -> None:
        """Main loop for the game."""
        self.running = True
        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            self.check_events()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                if not self.player.willCollide(Direction.up, self.playerInteractables):
                    self.player.walkUp()
            elif keys[pygame.K_DOWN]:
                if not self.player.willCollide(
                    Direction.down, self.playerInteractables
                ):
                    self.player.walkDown()
            elif keys[pygame.K_LEFT]:
                if not self.player.willCollide(
                    Direction.left, self.playerInteractables
                ):
                    self.player.walkLeft()
            elif keys[pygame.K_RIGHT]:
                if not self.player.willCollide(
                    Direction.right, self.playerInteractables
                ):
                    self.player.walkRight()
            else:
                self.player.isWalking = False
            if keys[pygame.K_SPACE]:
                self.player.triggerInteractionDelay(self.playerInteractables)

            if keys[pygame.K_ESCAPE]:
                self.end()

            if keys[pygame.K_q]:
                self.end()

            # update all sprites
            self.player.update()
            self.workers.update([self.player])
            workers: list[Worker] = self.workers.sprites()
            for worker in workers:
                worker.detectPlayer(self.player)
            self.electricPanel.detectPlayer(self.player)
            self.managers.update()
            self.CanInteractIndicator.checkForAnyPossibleInteract(
                self.playerInteractables, self.player
            )
            self.CanInteractIndicator.update()

            # check for collisions
            self.check_collisions()

            # check if the player has won
            self.check_win_state()

            # bg color
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
            self.end(self.player_win)

    def stop(self) -> None:
        try:
            pygame.quit()
        except pygame.error:
            pass
