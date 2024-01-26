"""App module"""
from game.runner import Runner


def run() -> None:
    """Run the app."""
    runner = Runner()
    runner.start()
