# Quickstart

This page takes you from a fresh install to a real result. Every snippet runs as
written — copy the whole thing into a file and execute it.

!!! info "Prerequisite"
    Install the package first — see [Installation](installation.md).

## 1. Summarize a series

```python
import mypackage as mp

report = mp.summarize([3.0, 1.0, 4.0, 1.0, 5.0], label="demo")  # (1)!

print(report.mean)  # 2.8
print(report.spread)  # 4.0
```

1.  `label` is optional, but naming a result pays off the moment you have more
    than one of them — it shows up in `to_row()` and in every comparison table.

Every entry point returns a [`Report`][mypackage.core.Report], a small frozen
object. Because the return type is uniform, anything that consumes one result
consumes all of them.

## 2. Compare several inputs

```python
series = {
    "baseline": [3.0, 1.0, 4.0, 1.0, 5.0],
    "treatment": [9.0, 2.0, 6.0, 5.0, 3.0],
}

table = mp.compare(series)

for row in table:
    print(row)
```

## 3. Tune the behavior

```python
report = mp.summarize(
    [3.0, 1.0, 4.0, 1.0, 5.0],
    label="trimmed",
    trim=0.2,  # drop the tails before averaging
    precision=3,  # rounding applied to the reported figures
)
```

The three parameters above cover most real usage. The full set is documented in
the [API reference](../reference/core.md).

## 4. Persist the result

=== "As a dict"

    ```python
    payload = report.to_row()
    ```

=== "As JSON"

    ```python
    import json
    from pathlib import Path

    Path("report.json").write_text(json.dumps(report.to_row(), indent=2))
    ```

=== "As a DataFrame"

    ```python
    import pandas as pd

    df = pd.DataFrame(mp.compare(series))
    ```

## Where to next

<div class="site-grid" markdown>

<div class="site-card" markdown>
### [Core concepts](concepts.md)
Why every entry point has the same shape, and what that buys you.
</div>

<div class="site-card" markdown>
### [Basic usage](../guide/basic-usage.md)
The everyday workflow in depth, parameter by parameter.
</div>

<div class="site-card" markdown>
### [API reference](../reference/index.md)
Every public function and class, generated from the source.
</div>

</div>
