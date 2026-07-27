"""Run every script in `examples/` and require a clean exit.

The docs include these files verbatim with the `--8<--` syntax, so a snippet on
the site is only as trustworthy as the script behind it. Executing them here is
what makes "the examples cannot drift" a fact rather than an intention.

Scripts are discovered, not listed: drop a new one into `examples/` and it is
covered from the next run.
"""

import subprocess
import sys
from pathlib import Path

import pytest

EXAMPLES = sorted((Path(__file__).resolve().parent.parent / "examples").glob("*.py"))


@pytest.mark.parametrize("script", EXAMPLES, ids=lambda path: path.name)
def test_example_runs_clean(script: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"{script.name} exited {result.returncode}:\n{result.stderr}"
    assert result.stdout, f"{script.name} produced no output"


def test_examples_directory_is_not_empty() -> None:
    # Guards the parametrization above: a bad glob would silently collect
    # nothing and report a green run that tested no examples at all.
    assert EXAMPLES
