"""Session-wide pytest fixtures.

Lives at the repo root rather than in ``tests/`` so it applies to the doctests
collected from ``src/`` as well — see ``testpaths`` in ``pyproject.toml``.
"""

from collections.abc import Iterator

import pytest

from docsforge import core


@pytest.fixture(autouse=True)
def isolate_registry() -> Iterator[None]:
    """Undo any method registration a test or doctest performs.

    ``register`` mutates a module-global, and the docstring examples for it
    register real methods. Without this fixture that state leaks into whatever
    runs next, so the suite passes or fails depending on collection order —
    ``pytest src tests`` and ``pytest tests src`` disagree. Snapshotting here
    keeps the examples honest (they show the real API, not a mocked one) and
    the suite order-independent.
    """
    snapshot = core._REGISTRY.copy()
    try:
        yield
    finally:
        core._REGISTRY.clear()
        core._REGISTRY.update(snapshot)
