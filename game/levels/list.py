"""Level parameters List."""

from game.defs import Direction
from game.levels.parameters import (
    ConveyorBeltParameters,
    ElectricPanelParameters,
    EnvironmentParameters,
    LevelParameters,
    ManagerParameters,
    PlayerParameters,
    WorkerParameters,
)

levels: list[LevelParameters] = [
    LevelParameters(
        manager=ManagerParameters(
            walk_path=[
                (100, 100, Direction.up),  # Top-left corner
                (200, 100, Direction.right),  # Top-right corner
                (200, 150, Direction.down),  # Top-right corner
                (680, 150, Direction.right),  # Bottom-right corner
                (680, 300, Direction.down),  # Bottom-left corner
                (100, 300, Direction.left),  # Bottom-left corner
            ],
            walk_speed=5,
        ),
        environment=EnvironmentParameters(
            conveyor_belt=ConveyorBeltParameters(
                position=(400, 250), direction=Direction.right, speed=5
            ),
            workers=[
                WorkerParameters(position=(200, 250), worker_type=1),
                WorkerParameters(position=(350, 250), worker_type=2),
                WorkerParameters(position=(500, 250), worker_type=0),
            ],
            electric_panel=ElectricPanelParameters(position=(600, 80)),
        ),
        player=PlayerParameters(position=(600, 300)),
        timeout=90,
    )
]