"""Unit tests for mars_rover.py. Standard library only: run with

    python3 -m unittest test_mars_rover

Loaded via its exact file path rather than `import mars_rover` because a
same-named `mars_rover/` package also lives at the project root -- a plain
import would silently resolve to that package instead of this script.
"""

import importlib.util
import pathlib
import unittest

_SPEC = importlib.util.spec_from_file_location(
    "mars_rover_script", pathlib.Path(__file__).parent / "mars_rover.py"
)
mars_rover_script = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(mars_rover_script)

Rover = mars_rover_script.Rover
parse_obstacle = mars_rover_script.parse_obstacle
parse_size = mars_rover_script.parse_size


class TestTurning(unittest.TestCase):
    def test_turn_left_from_north_faces_west(self):
        rover = Rover(5, 5, set())
        rover.turn_left()
        self.assertEqual(rover.heading, "W")

    def test_turn_right_from_north_faces_east(self):
        rover = Rover(5, 5, set())
        rover.turn_right()
        self.assertEqual(rover.heading, "E")

    def test_four_right_turns_return_to_start(self):
        rover = Rover(5, 5, set())
        for _ in range(4):
            rover.turn_right()
        self.assertEqual(rover.heading, "N")


class TestMoveForward(unittest.TestCase):
    def test_moves_north_by_default(self):
        rover = Rover(5, 5, set())
        rover.move_forward()
        self.assertEqual((rover.x, rover.y), (0, 1))

    def test_blocked_by_obstacle_reports_message_and_stays_put(self):
        rover = Rover(5, 5, {(0, 1)})
        message = rover.move_forward()
        self.assertEqual(message, "OBSTACLE: movement blocked at (0, 1)")
        self.assertEqual((rover.x, rover.y), (0, 0))

    def test_blocked_by_edge_reports_message_and_stays_put(self):
        rover = Rover(1, 1, set())
        rover.turn_right()  # now heading E, edge is one step away
        message = rover.move_forward()
        self.assertEqual(message, "EDGE: movement blocked at (1, 0)")
        self.assertEqual((rover.x, rover.y), (0, 0))

    def test_open_move_returns_none_and_updates_position(self):
        rover = Rover(5, 5, set())
        self.assertIsNone(rover.move_forward())
        self.assertEqual((rover.x, rover.y), (0, 1))


class TestStatusAndMap(unittest.TestCase):
    def test_status_format(self):
        rover = Rover(5, 5, set())
        self.assertEqual(rover.status(), "Position: (0, 0)  Heading: N")

    def test_map_places_rover_and_obstacle_glyphs(self):
        rover = Rover(5, 5, {(2, 2)})
        rover.x, rover.y, rover.heading = 1, 2, "E"
        rendered = rover.render_map()
        row_two = rendered.splitlines()[2]  # y=4,3,2,1,0 -> row index 2 is y=2
        self.assertIn(">", row_two)
        self.assertIn("#", row_two)


class TestParseSize(unittest.TestCase):
    def test_parses_valid_size(self):
        self.assertEqual(parse_size("5x5"), (5, 5))

    def test_rejects_malformed_size(self):
        with self.assertRaises(Exception):
            parse_size("bogus")

    def test_rejects_oversized_grid(self):
        with self.assertRaises(Exception):
            parse_size("1000000x1000000")


class TestParseObstacle(unittest.TestCase):
    def test_parses_valid_obstacle(self):
        self.assertEqual(parse_obstacle("2,2"), (2, 2))

    def test_tolerates_whitespace_after_comma(self):
        self.assertEqual(parse_obstacle("2, 2"), (2, 2))

    def test_rejects_double_sign(self):
        with self.assertRaises(Exception):
            parse_obstacle("--2,3")


if __name__ == "__main__":
    unittest.main()
