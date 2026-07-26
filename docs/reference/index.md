# API reference

This reference is generated directly from the source docstrings, so it always
matches the installed version. It is organized by module; the top-level
`mypackage` namespace re-exports the most common entry points.

<div class="site-grid" markdown>

<div class="site-card" markdown>
### [Core](core.md)
The primary entry points and the `Report` type they all return.
</div>

<div class="site-card" markdown>
### [Utilities](utils.md)
Building blocks for composing your own methods.
</div>

</div>

## Top-level namespace

The following are importable directly as `mypackage.<name>`:

```python
import mypackage as mp
```

::: mypackage
    options:
      members: false
      show_root_heading: false
      show_source: false

| Name | Kind | Summary |
|---|---|---|
| [`summarize`][mypackage.core.summarize] | function | Summarize one series into a `Report` |
| [`compare`][mypackage.core.compare] | function | Summarize several series on equal footing |
| [`register`][mypackage.core.register] | decorator | Add a method to the registry |
| [`Report`][mypackage.core.Report] | class | The uniform result type |

!!! note "How to read these pages"
    Signatures show the annotations from the source. Parameters, returns, and
    raises come from NumPy-style docstring sections — the same text you get from
    `help()` in a REPL. Click **source** on any entry to see the implementation.
