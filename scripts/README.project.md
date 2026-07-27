<div align="center">

<img src="docs/logo.svg" alt="Docsforge logo" width="120">

# Docsforge

**A short, punchy description of docsforge — what it does and for whom.**

[![python](https://img.shields.io/badge/python-3.11+-495057?style=flat-square&labelColor=212529)](https://www.python.org)
[![docs](https://img.shields.io/badge/docs-latest-495057?style=flat-square&labelColor=212529)](https://my-org.github.io/docsforge/)
[![license](https://img.shields.io/badge/MIT-495057?style=flat-square&labelColor=212529)](LICENSE)

[Documentation](https://my-org.github.io/docsforge/) ·
[Quickstart](https://my-org.github.io/docsforge/getting-started/quickstart/) ·
[API reference](https://my-org.github.io/docsforge/reference/)

</div>

---

## Why Docsforge

Two or three sentences on the problem this solves, aimed at someone who has
never heard of it. Say what it *is*, then back the claim with the one detail
that makes it credible.

## Install

```bash
uv add docsforge      # or: pip install docsforge
```

## Quickstart

```python
import docsforge as mp

report = mp.summarize([3.0, 1.0, 4.0, 1.0, 5.0], label="demo")

print(report.mean)  # 2.8
print(report.to_row())
```

See the [documentation](https://my-org.github.io/docsforge/) for the full guide.

## Features

- **Uniform results** — every entry point returns the same `Report` type.
- **Extensible** — register your own method; it works everywhere the built-ins do.
- **Documented** — the API reference is generated from the source docstrings.

## Documentation

| | |
|---|---|
| [Installation](https://my-org.github.io/docsforge/getting-started/installation/) | Install, extras, and verification |
| [Quickstart](https://my-org.github.io/docsforge/getting-started/quickstart/) | End to end in under thirty lines |
| [Core concepts](https://my-org.github.io/docsforge/getting-started/concepts/) | The ideas that make the API predictable |
| [API reference](https://my-org.github.io/docsforge/reference/) | Generated from source docstrings |

## Development

```bash
git clone https://github.com/my-org/docsforge
cd docsforge
uv sync --all-extras
uv run pytest
cargo test --manifest-path rust/Cargo.toml   # if you kept the Rust crate
uv run mkdocs serve
```

See [docs/guide/writing-docs.md](docs/guide/writing-docs.md) for the
documentation style guide.

## License

[MIT](LICENSE) © Docsforge contributors
