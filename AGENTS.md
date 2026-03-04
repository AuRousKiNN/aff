# Repository Guidelines

## Project Language
- The project language is Chinese
- Use Chinese to response User

## Project Structure & Module Organization
- `aff/core.py` holds every AFF domain object plus serialization helpers; extend its dataclasses when the format grows.
- `aff/__init__.py` defines the public API, while `pyproject.toml` carries packaging, typing, and build metadata.
- Root-level tests (`test_aff_objects.py`, `test_real_chart.py`) use the bundled charts `test.aff` and `real.aff`; reference docs live in `USAGE.md`, `FORMAT_REF.md`, and `GEMINI.md`.

## Build, Test, and Development Commands
- `python -m pip install -e .` sets up an editable install inside `.venv` so local scripts resolve `aff` consistently.
- `python -m pytest` runs the regression suite and will fail fast on serialization drift.
- `python test_real_chart.py` is a lightweight smoke test that guarantees `real.aff` parses and round-trips exactly.
- `python -m mypy aff` enforces the strict typing contract; treat warnings as blockers.
- `python -m build` (after tests pass) emits sdist/wheel artifacts to `build/` for distribution.

## Coding Style & Naming Conventions
- Follow PEP 8 with four-space indentation, `snake_case` for helpers, and `UpperCamelCase` for AFF entities (`AffHeader`, `TimingGroup`).
- Keep dataclasses small and descriptive, prefer explicit floats/ints, and format serialized floats with two decimals to match existing output.
- Every exported helper must carry type hints that satisfy strict mypy; avoid `Any`, and document new attributes inline the way `core.py` already does.

## Testing Guidelines
- Add pytest coverage whenever parser logic changes: assert object counts, key field values, and `.serialize()` equality.
- Use fixture charts stored next to the tests; name new samples after the scenario (`timing_group_overlap.aff`).
- Target edge cases (custom easing, hitsounds, timing groups) and keep round-trip assertions for any new object type.

## Commit & Pull Request Guidelines
- Follow the existing log style—concise, imperative subjects such as “Add aff core, package metadata, and usage docs”.
- Reference related issues or charts in the body, list the commands you ran (pytest, mypy, sample scripts), and describe expected side effects.
- Open PRs only after lint/tests succeed; include a one-paragraph summary, reproduction steps, and before/after serialization snippets when behavior shifts.
- Request review promptly and flag any skipped tests or outstanding TODOs so reviewers can gauge remaining risk.

## Security & Configuration Tips
- Do not commit proprietary charts; keep large samples out of the repo and document how to obtain them.
- When sharing reproduction files, scrub player identifiers and store them outside version control, referencing paths such as `charts/local/secret.aff` in the PR notes.
