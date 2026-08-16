"""Mars Rover kata.

Rovers move on a rectangular plateau addressed by (x, y) in [0, max_x] x
[0, max_y]. Driving a rover past an edge wraps it to the opposite edge
(a torus, not a hard boundary) -- the plateau has no "off the map" state.

Commands: L (turn left), R (turn right), M (move forward one grid point).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

_VALID_COMMANDS = frozenset("LRM")


class Direction(Enum):
    N = (0, 1)
    E = (1, 0)
    S = (0, -1)
    W = (-1, 0)

    @property
    def delta(self) -> tuple[int, int]:
        return self.value


_ORDER = [Direction.N, Direction.E, Direction.S, Direction.W]


def _turn_left(direction: Direction) -> Direction:
    return _ORDER[(_ORDER.index(direction) - 1) % len(_ORDER)]


def _turn_right(direction: Direction) -> Direction:
    return _ORDER[(_ORDER.index(direction) + 1) % len(_ORDER)]


@dataclass(frozen=True)
class Plateau:
    max_x: int
    max_y: int

    def wrap(self, x: int, y: int) -> tuple[int, int]:
        return x % (self.max_x + 1), y % (self.max_y + 1)

    def contains(self, x: int, y: int) -> bool:
        return 0 <= x <= self.max_x and 0 <= y <= self.max_y


class UnknownCommandError(ValueError):
    pass


class Rover:
    def __init__(self, x: int, y: int, direction: Direction, plateau: Plateau):
        if not plateau.contains(x, y):
            raise ValueError(
                f"Starting position ({x}, {y}) is outside the plateau "
                f"(0..{plateau.max_x}, 0..{plateau.max_y})"
            )
        self.x = x
        self.y = y
        self.direction = direction
        self.plateau = plateau

    def execute(self, commands: str) -> None:
        unknown = set(commands) - _VALID_COMMANDS
        if unknown:
            raise UnknownCommandError(f"Unknown command(s): {sorted(unknown)!r}")
        for command in commands:
            self._execute_one(command)

    def _execute_one(self, command: str) -> None:
        if command == "L":
            self.direction = _turn_left(self.direction)
        elif command == "R":
            self.direction = _turn_right(self.direction)
        else:
            dx, dy = self.direction.delta
            self.x, self.y = self.plateau.wrap(self.x + dx, self.y + dy)

    def report(self) -> str:
        return f"{self.x} {self.y} {self.direction.name}"


def run_mission(input_text: str) -> str:
    lines = [line.strip() for line in input_text.strip().splitlines() if line.strip()]
    if not lines:
        return ""

    header = lines[0].split()
    if len(header) != 2 or not all(n.lstrip("-").isdigit() for n in header):
        raise ValueError(f"Malformed plateau header: {lines[0]!r} (expected 'MAX_X MAX_Y')")
    plateau = Plateau(int(header[0]), int(header[1]))

    if len(lines) % 2 == 0:
        raise ValueError("Malformed mission: each rover needs both a position and a command line")

    reports = []
    for i in range(1, len(lines), 2):
        position = lines[i].split()
        if len(position) != 3:
            raise ValueError(f"Malformed rover position: {lines[i]!r} (expected 'X Y DIRECTION')")
        x_str, y_str, dir_str = position
        try:
            direction = Direction[dir_str]
        except KeyError as exc:
            raise ValueError(f"Unknown direction: {dir_str!r} (expected one of N, E, S, W)") from exc
        rover = Rover(int(x_str), int(y_str), direction, plateau)
        rover.execute(lines[i + 1])
        reports.append(rover.report())

    return "\n".join(reports)


def main() -> None:
    import sys

    print(run_mission(sys.stdin.read()))


if __name__ == "__main__":
    main()
