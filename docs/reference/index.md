# API reference

This reference is generated directly from the source docstrings, so it always
matches the installed version. It is organized by module; the top-level
`docsforge` namespace re-exports the most common entry points.

<div class="site-grid" markdown>

<div class="site-card" markdown>
### [Core](core.md)
The primary entry points and the `Report` type they all return.
</div>

<div class="site-card" markdown>
### [Utilities](utils.md)
Building blocks for composing your own methods.
</div>

<div class="site-card" markdown>
### [Rust API](rust.md)
rustdoc-generated reference for the companion crate in `rust/`.
</div>

</div>

## Top-level namespace

The following are importable directly as `docsforge.<name>`:

```python
import docsforge as mp
```

::: docsforge
    options:
      members: false
      show_root_heading: false
      show_source: false

| Name | Kind | Summary |
|---|---|---|
| [`summarize`][docsforge.core.summarize] | function | Summarize one series into a `Report` |
| [`compare`][docsforge.core.compare] | function | Summarize several series on equal footing |
| [`register`][docsforge.core.register] | decorator | Add a method to the registry |
| [`Report`][docsforge.core.Report] | class | The uniform result type |

!!! note "How to read these pages"
    Signatures show the annotations from the source. Parameters, returns, and
    raises come from NumPy-style docstring sections — the same text you get from
    `help()` in a REPL. Click **source** on any entry to see the implementation.
