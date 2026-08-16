# bmad-first-project

Two independent implementations of the Mars Rover kata, built via [BMad Method](https://docs.bmad-method.org) skills in Claude Code.

## `mars_rover/` — classic batch kata

A `uv`-managed package. Reads a full mission from stdin (plateau size, then position + command lines per rover), moves with `L`/`R`/`M`, and wraps around the grid edges.

```bash
uv run pytest
printf '5 5\n1 2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM\n' | uv run mars-rover
```

## `mars_rover.py` — interactive tutorial CLI

A standalone, standard-library-only script matching the [BMad getting-started tutorial](https://docs.bmad-method.org/tutorials/getting-started/) example exactly. Interactive REPL with a bounded grid and obstacles instead of wrap-around.

```bash
python3 -m unittest test_mars_rover
python3 mars_rover.py --size 5x5 --obstacle 2,2
```

Commands at the `>` prompt: `F` (forward), `L`/`R` (turn), `MAP` (print the grid), `QUIT` (exit). Movement letters can be chained on one line, e.g. `FFRFF`.

## Project layout

- `mars_rover/`, `tests/` — the batch kata package and its pytest suite
- `mars_rover.py`, `test_mars_rover.py` — the standalone tutorial CLI and its unittest suite
- `_bmad/`, `.claude/skills/` — BMad Method skill library and render engine (tooling, not project code)
- `_bmad-output/implementation-artifacts/` — spec traces generated for each build
