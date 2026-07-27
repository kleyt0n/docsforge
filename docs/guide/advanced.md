# Advanced usage

Extension points, performance characteristics, and the sharp edges. This page
assumes you have read [Core concepts](../getting-started/concepts.md).

## Registering your own method

Register a callable that returns a `Report` and it becomes a first-class
citizen everywhere a method name is accepted:

```python
import statistics
import docsforge as mp


@mp.register("median")  # (1)!
def median_summary(values, *, label=None, **options):
    values = list(values)
    return mp.Report(  # (2)!
        label=label,
        mean=statistics.median(values),
        spread=max(values) - min(values),
        n=len(values),
        options=options,
    )


mp.summarize(values, method="median")  # (3)!
```

1.  The name is what users type. Registering a name twice raises — pick
    something unlikely to collide.
2.  Return the same type the built-ins return. That is the entire contract.
3.  From here on, your method is indistinguishable from a built-in: it works in
    `compare`, in serialization, and in the plotting helpers.

!!! warning "The contract is the return type"
    A registered method that returns something other than a `Report` will fail
    later, in code far from your function. Construct the `Report` explicitly
    rather than returning a dict that "looks close enough".

## Composing with the building blocks

Public helpers exist so you do not have to reimplement the parts that are easy
to get subtly wrong:

| Helper | Use it for |
|---|---|
| `docsforge.utils.normalize` | Coercing any iterable of numbers to a validated tuple of floats |
| `docsforge.utils.trim` | Symmetric tail trimming with the standard convention |
| `docsforge.utils.describe` | Turning an iterable of `Report` into printable rows |

```python
from docsforge.utils import normalize, trim

clean = trim(normalize(raw_values), fraction=0.1)
```

## Performance notes

State the shape of the cost, not a vague claim:

- `summarize` is $O(n \log n)$ when `trim > 0` (it sorts) and $O(n)$ otherwise.
- `compare` is linear in the number of series; the series themselves are
  independent, so it parallelizes trivially if you need it to.
- Memory is dominated by one copy of the input, made during normalization.

<figure markdown>
  ![Placeholder benchmark](../img/placeholder.svg)
  <figcaption>Replace with a real benchmark — a chart with a reproducible script beats a paragraph of adjectives.</figcaption>
</figure>

!!! tip "Benchmarks belong in the repo"
    Ship the script that produced the chart (`examples/benchmark.py`) and say so
    in the caption. A benchmark nobody can rerun is marketing, not evidence.

## Sharp edges

??? danger "Trimming changes `n`"

    After trimming, `report.n` reflects the number of observations actually
    used, not the number passed in. Comparing an untrimmed and a trimmed report
    on `n` alone will mislead you.

??? danger "Options are compared by value"

    Two reports are equal only when their `options` are equal. A float that
    round-trips through JSON as `0.30000000000000004` will not compare equal to
    `0.3`. Use `precision` to normalize before serializing.

??? question "Is any of this thread-safe?"

    Reading is. The registry is mutated at import time by decorators; register
    your methods at module scope rather than inside a worker.

## Reproducibility checklist

- [x] Pin your environment (`uv.lock`, or an equivalent lockfile)
- [x] Record `report.options` alongside the numbers you publish
- [x] Set `precision` explicitly when results cross a process boundary
- [ ] Add a regression test that snapshots `compare()` output
