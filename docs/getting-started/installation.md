# Installation

mypackage supports **Python 3.11, 3.12, and 3.13** on Linux, macOS, and Windows.

## Install

=== "uv"

    ```bash
    uv add mypackage
    ```

=== "pip"

    ```bash
    pip install mypackage
    ```

=== "From source"

    ```bash
    git clone https://github.com/my-org/mypackage
    cd mypackage
    uv sync --all-extras     # editable install + every optional extra
    ```

## Optional extras

Extras keep the base install small; add only what you use.

| Extra | Install | Pulls in | Needed for |
|---|---|---|---|
| `data` | `uv add "mypackage[data]"` | `pyarrow` | Parquet and Arrow I/O |
| `viz` | `uv add "mypackage[viz]"` | `matplotlib` | The plotting helpers |
| `all` | `uv add "mypackage[all]"` | everything above | Trying things out |

!!! note "Why extras instead of one big install"
    Every dependency you add is a dependency your users must resolve against
    their own environment. Keeping optional features behind extras means a
    conflict in a plotting library can never block someone who only needs the
    core.

## Verify the install

```bash
python -c "import mypackage; print(mypackage.__version__)"
```

## Development install

Contributors need the dev toolchain as well:

```bash
git clone https://github.com/my-org/mypackage
cd mypackage
uv sync --all-extras
uv run pytest                  # test suite
uv run ruff check .            # lint
uv run mkdocs serve            # docs at http://127.0.0.1:8000
```

See [Contributing](../about/contributing.md) for the full workflow.

## Troubleshooting

??? failure "`ModuleNotFoundError: No module named 'mypackage'`"

    The most common cause is a shell pointing at a different interpreter than
    the one you installed into. Check which Python is being used:

    ```bash
    which python && python -c "import sys; print(sys.prefix)"
    ```

    Inside a uv project, prefer `uv run python` — it always resolves to the
    project environment.

??? failure "Version conflict while resolving dependencies"

    mypackage declares **lower bounds** on its dependencies and avoids
    speculative upper caps. If resolution still fails, share the output of
    `uv pip freeze` in an issue — a resolver trace is far more useful than the
    error message alone.
