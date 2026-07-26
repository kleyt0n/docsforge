# Contributing to mypackage

Thanks for your interest in improving mypackage! This guide covers everything
you need to make a change — from setting up the environment to getting a pull
request merged.

By participating you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## Development setup

This project uses [uv](https://docs.astral.sh/uv/) for environment and
dependency management.

```bash
git clone https://github.com/my-org/mypackage
cd mypackage
uv sync --all-extras          # package + dev + docs
```

That installs the package in editable mode along with every optional extra, so
the test suite and the docs build both work out of the box.

## Everyday commands

```bash
uv run pytest                              # run the test suite (incl. doctests)
uv run pytest --cov=mypackage              # with coverage (must stay above the floor)
uv run ruff check .                        # lint
uv run ruff format .                       # auto-format
uv run ruff format --check .               # verify formatting (what CI runs)
uv run mkdocs serve                        # preview docs at localhost:8000
uv run mkdocs build --strict               # build docs the way CI does
```

### Pre-commit

A [pre-commit](https://pre-commit.com/) config runs Ruff and a few hygiene hooks
before each commit:

```bash
uv run pre-commit install       # one-time, installs the git hook
uv run pre-commit run --all-files
```

## Coding conventions

- **Style & linting** are enforced by Ruff (`line-length = 100`; rule set in
  `pyproject.toml`). Run `ruff format` before committing.
- **Docstrings use the NumPy style** (`Parameters` / `Returns` sections). The
  docs site renders the public API from these via mkdocstrings, so every public
  function or class needs at least a one-line summary, and non-trivial ones need
  full `Parameters` / `Returns`.
- **Examples in docstrings are tested.** `pytest` runs with `--doctest-modules`,
  so a doctest that drifts from the code fails CI.
- **Public vs. private surface.** The public API is what `__all__` exports plus
  the documented submodules. Underscore-prefixed names are internal and may
  change without notice — see [API stability](docs/reference/stability.md).

## Documentation

Documentation changes go through the same review as code.

- Conventions, components, and the house style live in
  [docs/guide/writing-docs.md](docs/guide/writing-docs.md).
- New pages must be added to `nav:` in `mkdocs.yml`.
- `mkdocs build --strict` fails on broken links, unresolved includes, and pages
  missing from the nav — run it before pushing.

## Tests

- Every bug fix and feature needs a test.
- Keep tests deterministic. Snapshot the output of comparison helpers rather
  than asserting on floating-point noise.
- **Coverage floor.** CI enforces a minimum via `fail_under` in
  `pyproject.toml`. Ratchet it *up* when coverage improves; never lower it to
  make a PR pass — add tests instead.

## Commits & changelog

This project follows [Conventional Commits](https://www.conventionalcommits.org)
(`feat:`, `fix:`, `docs:`, `chore:`, `perf:`, `refactor:`, `test:`). Add an entry
to `CHANGELOG.md` under **Unreleased** for anything user-visible; the docs site
includes that file directly, so the entry ships with the release.

## Pull requests

1. Branch from `main` (e.g. `feat/trimmed-mean`, `fix/empty-input`).
2. Keep PRs focused; open an issue first for large or cross-cutting changes.
3. Ensure `ruff check`, `ruff format --check`, `pytest`, and
   `mkdocs build --strict` all pass locally — CI runs the same.
4. Fill out the PR template and link the issue it closes.

## Questions

See [SUPPORT.md](SUPPORT.md) for where to ask questions. Security issues follow
a private process — see [SECURITY.md](SECURITY.md).
