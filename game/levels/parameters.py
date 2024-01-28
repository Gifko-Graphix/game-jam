"""Level parameters."""

from dataclasses import dataclass

from game.defs import Direction

WalkPath = list[tuple[int, int, Direction]]

@dataclass
class ManagerParameters:
    """Manager parameters."""

    # manager walk path [list of (start, end, direction)]
    walk_path: WalkPath
    # manager walk speed
    walk_speed: int

@dataclass
class ConveyorBeltParameters:
    """Conveyor belt parameters."""

    # conveyor belt position
    position: tuple[int, int]
    # conveyor belt direction
    direction: Direction
    # conveyor belt speed
    speed: int

@dataclass
class WorkerParameters:
    """Worker parameters."""

    # position
    position: tuple[int, int]
    worker_type: int

@dataclass
class ElectricPanelParameters:
    """Electric panel parameters."""

    # position
    position: tuple[int, int]

@dataclass
class EnvironmentParameters:
    """Environment parameters."""

    # conveyor belt position
    conveyor_belt: ConveyorBeltParameters
    # worker positions
    workers: list[WorkerParameters]
    # electric panel position
    electric_panel: ElectricPanelParameters

@dataclass
class PlayerParameters:
    """Player parameters."""

    # position
    position: tuple[int, int]

@dataclass
class LevelParameters:
    """Level parameters."""

    # manager walk path [list of (start, end, direction)]
    manager: ManagerParameters
    # environment parameters
    environment: EnvironmentParameters
    # player start position
    player: PlayerParameters
    # level timeout
    timeout: int