# Installation

docsforge supports **Python 3.11, 3.12, and 3.13** on Linux, macOS, and Windows.

## Install

=== "uv"

    ```bash
    uv add docsforge
    ```

=== "pip"

    ```bash
    pip install docsforge
    ```

=== "From source"

    ```bash
    git clone https://github.com/my-org/docsforge
    cd docsforge
    uv sync --all-extras     # editable install + every optional extra
    ```

## Optional extras

Extras keep the base install small; add only what you use.

| Extra | Install | Pulls in | Needed for |
|---|---|---|---|
| `dev` | `uv sync --extra dev` | pytest, pytest-cov, ruff, mypy, pre-commit | Running the test suite and the linters |
| `docs` | `uv sync --extra docs` | mkdocs, mkdocs-material, mkdocstrings, pymdown-extensions | Building or serving this site |

Neither is needed to *use* the package — the runtime install has no
dependencies at all. `uv sync --all-extras` gets you both.

!!! note "Why extras instead of one big install"
    Every dependency you add is a dependency your users must resolve against
    their own environment. Keeping optional features behind extras means a
    conflict in a plotting library can never block someone who only needs the
    core. Add your own the same way, in `[project.optional-dependencies]`.

## Verify the install

```bash
python -c "import docsforge; print(docsforge.__version__)"
```

## Development install

Contributors need the dev toolchain as well:

```bash
git clone https://github.com/my-org/docsforge
cd docsforge
uv sync --all-extras
uv run pytest                  # test suite
uv run ruff check .            # lint
uv run mypy src                # type check
uv run mkdocs serve            # docs at http://127.0.0.1:8000/docsforge/
```

Open a pull request when the four commands above pass.

## Troubleshooting

??? failure "`ModuleNotFoundError: No module named 'docsforge'`"

    The most common cause is a shell pointing at a different interpreter than
    the one you installed into. Check which Python is being used:

    ```bash
    which python && python -c "import sys; print(sys.prefix)"
    ```

    Inside a uv project, prefer `uv run python` — it always resolves to the
    project environment.

??? failure "Version conflict while resolving dependencies"

    docsforge declares **lower bounds** on its dependencies and avoids
    speculative upper caps. If resolution still fails, share the output of
    `uv pip freeze` in an issue — a resolver trace is far more useful than the
    error message alone.
