"""Tests for the demo package.

They exist mainly to prove the CI pipeline in this template works end to end.
Replace them along with `src/docsforge/`.
"""

import pytest

import docsforge as mp
from docsforge.utils import describe, normalize, trim


def test_summarize_reports_mean_and_spread() -> None:
    report = mp.summarize([3.0, 1.0, 4.0, 1.0, 5.0], label="demo")

    assert report.label == "demo"
    assert report.mean == 2.8
    assert report.spread == 4.0
    assert report.n == 5


def test_trimming_reduces_n() -> None:
    assert mp.summarize([3.0, 1.0, 4.0, 1.0, 5.0], trim=0.2).n == 3


def test_options_travel_with_the_result() -> None:
    report = mp.summarize([1.0, 2.0], trim=0.0, precision=3)

    assert report.options == {"trim": 0.0, "precision": 3}


def test_compare_preserves_insertion_order() -> None:
    table = mp.compare({"a": [1.0, 2.0, 3.0], "b": [2.0, 4.0, 6.0]})

    assert [report.label for report in table] == ["a", "b"]
    assert [report.mean for report in table] == [2.0, 4.0]


def test_describe_returns_flat_rows() -> None:
    rows = describe(mp.compare({"a": [1.0, 2.0, 3.0]}))

    assert rows == [{"label": "a", "mean": 2.0, "spread": 2.0, "n": 3}]


def test_register_rejects_duplicate_names() -> None:
    with pytest.raises(ValueError, match="already registered"):
        # Deliberately the wrong return type: the point is that `register`
        # rejects the *name* before anything ever calls the function.
        mp.register("mean")(lambda values, **options: None)  # type: ignore[arg-type]


def test_unknown_method_names_the_registered_ones() -> None:
    with pytest.raises(ValueError, match="registered methods: mean"):
        mp.summarize([1.0], method="nope")


@pytest.mark.parametrize("values", [[], ()])
def test_empty_input_raises(values: list[float] | tuple[float, ...]) -> None:
    with pytest.raises(ValueError, match="at least one value"):
        mp.summarize(values)


def test_non_finite_input_raises() -> None:
    with pytest.raises(ValueError, match="finite"):
        normalize([1.0, float("nan")])


@pytest.mark.parametrize("fraction", [-0.1, 0.5, 1.0])
def test_out_of_range_trim_raises(fraction: float) -> None:
    with pytest.raises(ValueError, match=r"\[0, 0.5\)"):
        trim([1.0, 2.0, 3.0], fraction=fraction)
