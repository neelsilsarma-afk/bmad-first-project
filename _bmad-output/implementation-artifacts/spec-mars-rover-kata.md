---
title: 'Mars Rover Kata Implementation'
type: 'feature'
created: '2026-08-16'
status: 'done'
route: 'one-shot'
---

## Intent

**Problem:** No Mars Rover kata implementation exists in this project.

**Approach:** Implement the classic kata in Python — plateau grid, L/R/M command execution, edge wrap-around — with a full pytest test suite and a stdin-driven CLI.

## Suggested Review Order

**Core rover mechanics**

- Turning, moving, and starting-position validation gathered in one class.
  [`rover.py:56`](../../mars_rover/rover.py#L56)

- Commands are pre-validated before any are applied, so execution is atomic.
  [`rover.py:68`](../../mars_rover/rover.py#L68)

- Fixed N/E/S/W order list drives left/right turning.
  [`rover.py:32`](../../mars_rover/rover.py#L32)

- Modulo arithmetic implements edge wrap-around (a torus, not a hard boundary).
  [`rover.py:45`](../../mars_rover/rover.py#L45)

**Mission parsing (multi-rover input)**

- Parses the classic two-line-per-rover format with defensive validation and clear error messages.
  [`rover.py:88`](../../mars_rover/rover.py#L88)

- Stdin-driven CLI entry point, wired to the `mars-rover` console script.
  [`rover.py:118`](../../mars_rover/rover.py#L118)

**Public API**

- Package exports: `Direction`, `Plateau`, `Rover`, `UnknownCommandError`, `run_mission`.
  [`__init__.py:1`](../../mars_rover/__init__.py#L1)

**Tests and config (peripherals)**

- Full pytest suite: turning, movement, wrap-around, validation, malformed input, and the canonical two-rover kata example.
  [`test_rover.py:1`](../../tests/test_rover.py#L1)

- Pytest dev dependency and `mars-rover` console script.
  [`pyproject.toml:1`](../../pyproject.toml#L1)
