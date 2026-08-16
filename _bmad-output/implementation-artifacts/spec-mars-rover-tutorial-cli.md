---
title: 'Mars Rover Tutorial CLI (Interactive Standalone Script)'
type: 'feature'
created: '2026-08-16'
status: 'done'
route: 'one-shot'
---

## Intent

**Problem:** The BMad getting-started tutorial demonstrates a specific interactive Mars Rover CLI (`python3 mars_rover.py --size 5x5 --obstacle 2,2`, then `F`/`L`/`R`/`MAP`/`QUIT` commands) that didn't exist in this project — only a different, previously-built batch-style kata package did.

**Approach:** Implement the tutorial's exact interface as a standalone, standard-library-only script (`mars_rover.py`) at the project root, independent of the existing `mars_rover/` package, reproducing its documented output byte-for-byte.

## Suggested Review Order

**Interactive rover mechanics (entry point)**

- Turning, moving, and obstacle-vs-edge blocking gathered in one class.
  [`mars_rover.py:55`](../../mars_rover.py#L55)

- Obstacle and edge blocking are distinguished with different messages; the rover doesn't move on either.
  [`mars_rover.py:70`](../../mars_rover.py#L70)

**REPL and CLI**

- Command dispatch: `MAP`/`QUIT` handled first, then move/turn letters; hitting an obstacle or edge halts the rest of that line.
  [`mars_rover.py:103`](../../mars_rover.py#L103)

- `--size`/`--obstacle` parsing with a cell-count sanity cap and a guard against an obstacle sitting on the rover's spawn point.
  [`mars_rover.py:142`](../../mars_rover.py#L142)

**Map rendering**

- Column/row label widths are computed from grid size so alignment holds for grids beyond single-digit dimensions.
  [`mars_rover.py:83`](../../mars_rover.py#L83)

**Tests (peripherals)**

- Stdlib `unittest` suite, loaded via `importlib` by file path — `mars_rover.py` and the sibling `mars_rover/` package share a name, so a plain `import mars_rover` would silently resolve to the wrong one.
  [`test_mars_rover.py:1`](../../test_mars_rover.py#L1)
