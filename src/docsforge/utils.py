"""Small, composable helpers shared by the built-in methods.

These are public on purpose: anyone writing their own method should be able to
reuse the parts that are easy to get subtly wrong, rather than reimplementing
them.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover - import cycle only exists for type checkers
    from docsforge.core import Report

__all__ = ["describe", "normalize", "trim"]


def normalize(values: Iterable[float]) -> tuple[float, ...]:
    """Coerce an arbitrary sequence of numbers into a validated tuple.

    Conversion happens once, at the public boundary, so that internal helpers
    may assume valid input and errors point at the argument the caller passed.

    Parameters
    ----------
    values : iterable of float
        Any iterable of real numbers — list, tuple, NumPy array, or pandas
        ``Series``.

    Returns
    -------
    tuple of float
        The observations as plain floats.

    Raises
    ------
    ValueError
        If ``values`` is empty, or contains a value that is not finite.
    TypeError
        If a value cannot be interpreted as a number.

    Examples
    --------
    >>> normalize([3, 1, 4])
    (3.0, 1.0, 4.0)
    """
    observations = tuple(float(value) for value in values)

    if not observations:
        raise ValueError("expected at least one value; got 0")

    for value in observations:
        if not math.isfinite(value):
            raise ValueError(f"values must be finite; got {value!r}")

    return observations


def trim(values: Sequence[float], *, fraction: float = 0.0) -> tuple[float, ...]:
    r"""Drop ``fraction`` of the observations from each tail.

    Uses the standard convention: :math:`k = \lfloor \alpha n \rfloor` values
    are removed from each end of the sorted input.

    Parameters
    ----------
    values : sequence of float
        Observations, in any order. Sorted internally when ``fraction > 0``.
    fraction : float, optional
        Fraction removed per tail, in ``[0, 0.5)``. Zero returns the input
        unchanged, without sorting.

    Returns
    -------
    tuple of float
        The retained observations, sorted when trimming occurred.

    Raises
    ------
    ValueError
        If ``fraction`` is outside ``[0, 0.5)``.

    Examples
    --------
    >>> trim([3.0, 1.0, 4.0, 1.0, 5.0], fraction=0.2)
    (1.0, 3.0, 4.0)
    """
    if not 0.0 <= fraction < 0.5:
        raise ValueError(f"fraction must be in [0, 0.5); got {fraction!r}")

    if fraction == 0.0:
        return tuple(values)

    ordered = sorted(values)
    k = math.floor(fraction * len(ordered))
    return tuple(ordered[k : len(ordered) - k])


def describe(reports: Iterable[Report]) -> list[dict[str, Any]]:
    """Turn reports into printable rows.

    Parameters
    ----------
    reports : iterable of Report
        Typically the output of :func:`docsforge.core.compare`.

    Returns
    -------
    list of dict
        One row per report, ready for ``pandas.DataFrame`` or a plain
        ``csv.DictWriter``.

    Examples
    --------
    >>> from docsforge import compare
    >>> describe(compare({"a": [1.0, 2.0, 3.0]}))
    [{'label': 'a', 'mean': 2.0, 'spread': 2.0, 'n': 3}]
    """
    return [report.to_row() for report in reports]
