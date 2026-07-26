"""Primary entry points and the uniform result type they all return.

Every public entry point has the same shape — data in, :class:`Report` out — so
that everything which consumes a result (serialization, comparison, plotting)
is written once and works with every method, including user-registered ones.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any

from mypackage.utils import normalize
from mypackage.utils import trim as trim_tails

__all__ = ["Report", "compare", "register", "summarize"]

# Name -> method. Populated at import time by the `register` decorator.
_REGISTRY: dict[str, Callable[..., Report]] = {}


@dataclass(frozen=True)
class Report:
    """A summary of one series, carrying its own provenance.

    A ``Report`` is immutable and self-describing: because ``options`` travels
    with the numbers, a result read back from disk can always be traced to the
    settings that produced it.

    Parameters
    ----------
    label : str or None
        Human-readable name, propagated into comparison tables and plots.
    mean : float
        The central estimate.
    spread : float
        Dispersion of the input, measured as ``max - min``.
    n : int
        Number of observations actually used, *after* any trimming.
    options : dict
        The normalized options this result was produced with.

    Examples
    --------
    >>> Report(label="demo", mean=2.8, spread=4.0, n=5).to_row()
    {'label': 'demo', 'mean': 2.8, 'spread': 4.0, 'n': 5}
    """

    label: str | None
    mean: float
    spread: float
    n: int
    options: dict[str, Any] = field(default_factory=dict)

    def to_row(self) -> dict[str, Any]:
        """Return a flat, JSON-serializable mapping of the reported figures.

        Returns
        -------
        dict
            Keys ``label``, ``mean``, ``spread``, and ``n``. Suitable for
            ``json.dumps`` or ``pandas.DataFrame``.
        """
        return {
            "label": self.label,
            "mean": self.mean,
            "spread": self.spread,
            "n": self.n,
        }


def register(name: str) -> Callable[[Callable[..., Report]], Callable[..., Report]]:
    """Register a summary method under ``name``.

    Registered methods are indistinguishable from the built-ins at every call
    site that accepts a method name. The entire contract is the return type:
    the callable must return a :class:`Report`.

    Parameters
    ----------
    name : str
        The name users pass as ``method=``. Must not already be registered.

    Returns
    -------
    callable
        A decorator that registers the function and returns it unchanged.

    Raises
    ------
    ValueError
        If ``name`` is already registered.

    Examples
    --------
    >>> @register("first")
    ... def first_value(values, *, label=None, **options):
    ...     values = list(values)
    ...     return Report(label=label, mean=values[0], spread=0.0, n=len(values))
    >>> summarize([3.0, 1.0], method="first").mean
    3.0
    """

    def decorator(func: Callable[..., Report]) -> Callable[..., Report]:
        if name in _REGISTRY:
            raise ValueError(f"method {name!r} is already registered")
        _REGISTRY[name] = func
        return func

    return decorator


def summarize(
    values: Iterable[float],
    *,
    label: str | None = None,
    method: str = "mean",
    trim: float = 0.0,
    precision: int = 6,
) -> Report:
    """Summarize one series.

    Parameters
    ----------
    values : iterable of float
        The observations. Any sequence of numbers works — list, tuple, NumPy
        array, or pandas ``Series``; it is converted once, at this boundary.
    label : str or None, optional
        Name carried into tables and plots. Naming results pays off as soon as
        you have more than one.
    method : str, optional
        Which registered method to use. Defaults to the arithmetic mean.
    trim : float, optional
        Fraction dropped from *each* tail before averaging, in ``[0, 0.5)``.
        Non-zero values sort the input, making the call ``O(n log n)``.
    precision : int, optional
        Decimal places applied to the reported figures.

    Returns
    -------
    Report
        The summary, with ``n`` reflecting the observations actually used.

    Raises
    ------
    ValueError
        If ``values`` is empty, ``method`` is unknown, or ``trim`` is
        outside ``[0, 0.5)``.

    See Also
    --------
    compare : Summarize several series on equal footing.

    Examples
    --------
    >>> summarize([3.0, 1.0, 4.0, 1.0, 5.0], label="demo").mean
    2.8
    >>> summarize([3.0, 1.0, 4.0, 1.0, 5.0], trim=0.2).n
    3
    """
    if method not in _REGISTRY:
        known = ", ".join(sorted(_REGISTRY)) or "<none>"
        raise ValueError(f"unknown method {method!r}; registered methods: {known}")

    return _REGISTRY[method](
        values,
        label=label,
        trim=trim,
        precision=precision,
    )


def compare(
    series: Mapping[str, Iterable[float]],
    **options: Any,
) -> list[Report]:
    """Summarize several series under identical options.

    Passing the options once, here, is what makes the comparison fair — it is
    not possible to accidentally trim one series and not another.

    Parameters
    ----------
    series : mapping of str to iterable of float
        Label-to-observations mapping. Insertion order is preserved, so the
        output is stable across runs and safe to snapshot in a test.
    **options
        Forwarded to :func:`summarize` for every series.

    Returns
    -------
    list of Report
        One report per series, in insertion order.

    Examples
    --------
    >>> table = compare({"a": [1.0, 2.0, 3.0], "b": [2.0, 4.0, 6.0]})
    >>> [r.mean for r in table]
    [2.0, 4.0]
    """
    return [summarize(values, label=label, **options) for label, values in series.items()]


@register("mean")
def _mean_summary(
    values: Iterable[float],
    *,
    label: str | None = None,
    trim: float = 0.0,
    precision: int = 6,
) -> Report:
    """Built-in arithmetic-mean method (optionally trimmed)."""
    observations = trim_tails(normalize(values), fraction=trim)
    if not observations:
        raise ValueError("summarize() requires at least one value after trimming; got 0")

    return Report(
        label=label,
        mean=round(sum(observations) / len(observations), precision),
        spread=round(max(observations) - min(observations), precision),
        n=len(observations),
        options={"trim": trim, "precision": precision},
    )
