import pytest

from mars_rover.rover import Direction, Plateau, Rover, UnknownCommandError, run_mission


@pytest.fixture
def plateau() -> Plateau:
    return Plateau(max_x=5, max_y=5)


class TestTurning:
    def test_left_turn_cycles_counterclockwise(self, plateau: Plateau) -> None:
        rover = Rover(1, 2, Direction.N, plateau)
        rover.execute("L")
        assert rover.direction == Direction.W

    def test_right_turn_cycles_clockwise(self, plateau: Plateau) -> None:
        rover = Rover(1, 2, Direction.N, plateau)
        rover.execute("R")
        assert rover.direction == Direction.E

    def test_four_left_turns_return_to_start(self, plateau: Plateau) -> None:
        rover = Rover(1, 2, Direction.N, plateau)
        rover.execute("LLLL")
        assert rover.direction == Direction.N

    def test_four_right_turns_return_to_start(self, plateau: Plateau) -> None:
        rover = Rover(1, 2, Direction.N, plateau)
        rover.execute("RRRR")
        assert rover.direction == Direction.N


class TestMoving:
    @pytest.mark.parametrize(
        "direction,expected",
        [
            (Direction.N, (1, 3)),
            (Direction.S, (1, 1)),
            (Direction.E, (2, 2)),
            (Direction.W, (0, 2)),
        ],
    )
    def test_move_forward_in_each_direction(
        self, plateau: Plateau, direction: Direction, expected: tuple[int, int]
    ) -> None:
        rover = Rover(1, 2, direction, plateau)
        rover.execute("M")
        assert (rover.x, rover.y) == expected


class TestWrapAround:
    def test_moving_north_past_top_edge_wraps_to_bottom(self, plateau: Plateau) -> None:
        rover = Rover(0, 5, Direction.N, plateau)
        rover.execute("M")
        assert (rover.x, rover.y) == (0, 0)

    def test_moving_south_past_bottom_edge_wraps_to_top(self, plateau: Plateau) -> None:
        rover = Rover(0, 0, Direction.S, plateau)
        rover.execute("M")
        assert (rover.x, rover.y) == (0, 5)

    def test_moving_east_past_right_edge_wraps_to_left(self, plateau: Plateau) -> None:
        rover = Rover(5, 0, Direction.E, plateau)
        rover.execute("M")
        assert (rover.x, rover.y) == (0, 0)

    def test_moving_west_past_left_edge_wraps_to_right(self, plateau: Plateau) -> None:
        rover = Rover(0, 0, Direction.W, plateau)
        rover.execute("M")
        assert (rover.x, rover.y) == (5, 0)


class TestUnknownCommand:
    def test_raises_on_unrecognized_command(self, plateau: Plateau) -> None:
        rover = Rover(0, 0, Direction.N, plateau)
        with pytest.raises(UnknownCommandError):
            rover.execute("X")

    def test_invalid_command_leaves_rover_unmoved(self, plateau: Plateau) -> None:
        rover = Rover(0, 0, Direction.N, plateau)
        with pytest.raises(UnknownCommandError):
            rover.execute("MMX")
        assert (rover.x, rover.y, rover.direction) == (0, 0, Direction.N)


class TestStartingPositionValidation:
    def test_rejects_x_outside_plateau(self, plateau: Plateau) -> None:
        with pytest.raises(ValueError):
            Rover(6, 0, Direction.N, plateau)

    def test_rejects_negative_y(self, plateau: Plateau) -> None:
        with pytest.raises(ValueError):
            Rover(0, -1, Direction.N, plateau)


class TestPlateauWrap:
    def test_wrap_is_a_no_op_within_bounds(self, plateau: Plateau) -> None:
        assert plateau.wrap(2, 3) == (2, 3)

    def test_wrap_carries_multiple_edge_crossings(self, plateau: Plateau) -> None:
        assert plateau.wrap(7, -2) == (1, 4)


class TestRoverReport:
    def test_report_formats_position_and_heading(self, plateau: Plateau) -> None:
        rover = Rover(3, 4, Direction.E, plateau)
        assert rover.report() == "3 4 E"


class TestClassicKataExample:
    def test_two_rover_mission_matches_kata_spec(self) -> None:
        input_text = "5 5\n1 2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM\n"
        assert run_mission(input_text) == "1 3 N\n5 1 E"

    def test_empty_input_returns_empty_output(self) -> None:
        assert run_mission("") == ""


class TestMalformedMissionInput:
    def test_rejects_malformed_header(self) -> None:
        with pytest.raises(ValueError):
            run_mission("not a header\n1 2 N\nM\n")

    def test_rejects_unknown_direction(self) -> None:
        with pytest.raises(ValueError):
            run_mission("5 5\n1 2 Q\nM\n")

    def test_rejects_missing_command_line(self) -> None:
        with pytest.raises(ValueError):
            run_mission("5 5\n1 2 N\n")

    def test_rejects_malformed_position_line(self) -> None:
        with pytest.raises(ValueError):
            run_mission("5 5\n1 2\nM\n")

    def test_accepts_zero_dimension_plateau(self) -> None:
        assert run_mission("0 0\n0 0 N\nM\n") == "0 0 N"
