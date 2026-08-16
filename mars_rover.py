#!/usr/bin/env python3
"""Mars Rover -- interactive terminal simulator.

Standard-library only, no dependencies. Run:

    python3 mars_rover.py --size 5x5 --obstacle 2,2

Then type commands at the prompt (case-insensitive, chainable on one line):

    F        move forward one cell
    L        turn left 90 degrees
    R        turn right 90 degrees
    MAP      print the grid
    QUIT     exit

The rover starts at (0, 0) heading N. The origin is the bottom-left corner,
x increases to the right, y increases upward. Driving into an obstacle or
off the edge of the grid halts the rest of that command line and reports
why.
"""

from __future__ import annotations

import argparse

_HEADINGS = ["N", "E", "S", "W"]
_DELTAS = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}
_ROVER_GLYPH = {"N": "^", "E": ">", "S": "v", "W": "<"}
_VALID_MOVE_COMMANDS = frozenset("FLR")
_MAX_CELLS = 10_000  # sanity cap so a typo like --size 1000000x1000000 fails fast


def parse_size(text: str) -> tuple[int, int]:
    parts = text.lower().split("x")
    if len(parts) != 2 or not all(p.isdigit() for p in parts):
        raise argparse.ArgumentTypeError(f"Invalid --size {text!r} (expected WIDTHxHEIGHT, e.g. 5x5)")
    width, height = int(parts[0]), int(parts[1])
    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError(f"--size dimensions must be positive: {text!r}")
    if width * height > _MAX_CELLS:
        raise argparse.ArgumentTypeError(f"--size {text!r} exceeds the maximum of {_MAX_CELLS} cells")
    return width, height


def parse_obstacle(text: str) -> tuple[int, int]:
    parts = [p.strip() for p in text.split(",")]
    if len(parts) != 2:
        raise argparse.ArgumentTypeError(f"Invalid --obstacle {text!r} (expected X,Y, e.g. 2,2)")
    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid --obstacle {text!r} (expected X,Y, e.g. 2,2)") from None


class Rover:
    def __init__(self, width: int, height: int, obstacles: set[tuple[int, int]]):
        self.width = width
        self.height = height
        self.obstacles = obstacles
        self.x = 0
        self.y = 0
        self.heading = "N"

    def turn_left(self) -> None:
        self.heading = _HEADINGS[(_HEADINGS.index(self.heading) - 1) % len(_HEADINGS)]

    def turn_right(self) -> None:
        self.heading = _HEADINGS[(_HEADINGS.index(self.heading) + 1) % len(_HEADINGS)]

    def move_forward(self) -> str | None:
        dx, dy = _DELTAS[self.heading]
        nx, ny = self.x + dx, self.y + dy
        if (nx, ny) in self.obstacles:
            return f"OBSTACLE: movement blocked at ({nx}, {ny})"
        if not (0 <= nx < self.width and 0 <= ny < self.height):
            return f"EDGE: movement blocked at ({nx}, {ny})"
        self.x, self.y = nx, ny
        return None

    def status(self) -> str:
        return f"Position: ({self.x}, {self.y})  Heading: {self.heading}"

    def render_map(self) -> str:
        row_label_width = len(str(self.height - 1))
        col_width = len(str(self.width - 1))
        rows = []
        for y in range(self.height - 1, -1, -1):
            cells = []
            for x in range(self.width):
                if (x, y) == (self.x, self.y):
                    glyph = _ROVER_GLYPH[self.heading]
                elif (x, y) in self.obstacles:
                    glyph = "#"
                else:
                    glyph = "."
                cells.append(f"{glyph:>{col_width}}")
            rows.append(f"{y:>{row_label_width}} " + " ".join(cells))
        header = " " * (row_label_width + 1) + " ".join(f"{x:>{col_width}}" for x in range(self.width))
        rows.append(header)
        return "\n".join(rows)


def run_repl(rover: Rover) -> None:
    print(f"Mars Rover ready on a {rover.width}x{rover.height} grid.")
    print(rover.status())
    print("Commands: F(orward) L(eft) R(ight), MAP, QUIT")
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            print("Mission control signing off.")
            break
        if not line:
            continue
        command = line.upper()
        if command == "QUIT":
            print("Mission control signing off.")
            break
        if command == "MAP":
            print(rover.render_map())
            continue
        unknown = set(command) - _VALID_MOVE_COMMANDS
        if unknown:
            print(f"Unknown command(s): {', '.join(sorted(unknown))}")
            continue
        blocked_message = None
        for char in command:
            if char == "F":
                blocked_message = rover.move_forward()
                if blocked_message:
                    break
            elif char == "L":
                rover.turn_left()
            else:
                rover.turn_right()
        print(rover.status())
        if blocked_message:
            print(blocked_message)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Interactive Mars Rover terminal simulator.")
    parser.add_argument("--size", required=True, type=parse_size, help="Grid size as WIDTHxHEIGHT, e.g. 5x5")
    parser.add_argument(
        "--obstacle",
        action="append",
        type=parse_obstacle,
        default=[],
        metavar="X,Y",
        help="Obstacle coordinates as X,Y; repeatable for multiple obstacles",
    )
    args = parser.parse_args(argv)

    width, height = args.size
    obstacles = set(args.obstacle)
    for ox, oy in obstacles:
        if not (0 <= ox < width and 0 <= oy < height):
            parser.error(f"--obstacle ({ox}, {oy}) is outside the {width}x{height} grid")
    if (0, 0) in obstacles:
        parser.error("--obstacle (0, 0) coincides with the rover's starting position")

    run_repl(Rover(width, height, obstacles))


if __name__ == "__main__":
    main()
