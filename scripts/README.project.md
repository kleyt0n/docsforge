<div align="center">

<img src="docs/logo.svg" alt="mypackage logo" width="120">

# mypackage

**A short, punchy description of mypackage — what it does and for whom.**

[![python](https://img.shields.io/badge/python-3.11+-3987e5?style=flat-square)](https://www.python.org)
[![docs](https://img.shields.io/badge/docs-latest-4f46e5?style=flat-square)](https://my-org.github.io/mypackage/)
[![license](https://img.shields.io/badge/MIT-c98500?style=flat-square)](LICENSE)

[Documentation](https://my-org.github.io/mypackage/) ·
[Quickstart](https://my-org.github.io/mypackage/getting-started/quickstart/) ·
[API reference](https://my-org.github.io/mypackage/reference/) ·
[Changelog](CHANGELOG.md)

</div>

---

## Why mypackage

Two or three sentences on the problem this solves, aimed at someone who has
never heard of it. Say what it *is*, then back the claim with the one detail
that makes it credible.

## Install

```bash
uv add mypackage      # or: pip install mypackage
```

## Quickstart

```python
import mypackage as mp

report = mp.summarize([3.0, 1.0, 4.0, 1.0, 5.0], label="demo")

print(report.mean)  # 2.8
print(report.to_row())
```

See the [documentation](https://my-org.github.io/mypackage/) for the full guide.

## Features

- **Uniform results** — every entry point returns the same `Report` type.
- **Extensible** — register your own method; it works everywhere the built-ins do.
- **Documented** — the API reference is generated from the source docstrings.

## Documentation

| | |
|---|---|
| [Installation](https://my-org.github.io/mypackage/getting-started/installation/) | Install, extras, and verification |
| [Quickstart](https://my-org.github.io/mypackage/getting-started/quickstart/) | End to end in under thirty lines |
| [Core concepts](https://my-org.github.io/mypackage/getting-started/concepts/) | The ideas that make the API predictable |
| [API reference](https://my-org.github.io/mypackage/reference/) | Generated from source docstrings |

## Development

```bash
git clone https://github.com/my-org/mypackage
cd mypackage
uv sync --all-extras
uv run pytest
uv run mkdocs serve
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow, and
[docs/guide/writing-docs.md](docs/guide/writing-docs.md) for the documentation
style guide.

## License

[MIT](LICENSE) © mypackage contributors
