# Basic usage

The everyday workflow, in the order you will actually meet it. Each section
answers one question and ends with a runnable snippet.

## Loading input

```python
import docsforge as mp

values = [3.0, 1.0, 4.0, 1.0, 5.0, 9.0, 2.0, 6.0]
report = mp.summarize(values, label="run-01")
```

Inputs may be any sequence of numbers — a list, a tuple, a NumPy array, or a
pandas `Series`. They are converted once, at the boundary.

## Choosing options

The options below are the ones worth knowing by name. Everything else has a
default that is right until you have a reason otherwise.

| Option | Default | What it controls |
|---|---|---|
| `label` | `None` | Name carried into tables and plots |
| `trim` | `0.0` | Fraction dropped from each tail before averaging |
| `precision` | `6` | Decimal places in reported figures |

```python
report = mp.summarize(values, label="run-01", trim=0.1, precision=3)
```

!!! note "Defaults are a promise"
    Changing a default changes results for every user who never passed the
    argument. Treat defaults as public API — see
    [API stability](../reference/stability.md).

## Comparing several inputs

```python
table = mp.compare(
    {
        "baseline": values,
        "treatment": [v * 1.2 for v in values],
    },
    trim=0.1,  # (1)!
)
```

1.  Options passed to `compare` apply to every series, which is what makes the
    comparison fair. Per-series overrides go in the mapping itself.

`compare` returns a list of `Report` objects in insertion order, so the output
of a comparison is stable across runs — safe to snapshot in a test.

## Reading results

```python
best = max(table, key=lambda r: r.mean)
print(f"{best.label}: mean={best.mean}, n={best.n}")
```

## Handling failures

Invalid input raises immediately, with the offending argument named:

```python
try:
    mp.summarize([], label="empty")
except ValueError as exc:
    print(exc)  # expected at least one value; got 0
```

??? question "Should I catch these, or let them propagate?"

    In a pipeline, let them propagate. The exceptions raised here indicate that
    the *inputs* are wrong, and continuing past that point produces numbers no
    one should trust. Catch them only at the boundary where you can report the
    problem to a human.

## A complete example

```python
--8<-- "examples/basic_usage.py"
```

The snippet above is included from `examples/basic_usage.py` with the
`--8<--` include syntax, so it is executed by the test suite and can never drift
out of sync with the docs. Prefer this over pasting code you have to maintain
twice — see [Writing docs](writing-docs.md#including-files).
