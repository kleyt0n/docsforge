# Support

Need help with mypackage? Here's where to go.

## Getting help

- **Documentation** — start with the [docs site](https://my-org.github.io/mypackage/):
  getting-started guides, per-topic guides, and the full API reference.
- **Questions & discussion** — open a
  [GitHub Discussion](https://github.com/my-org/mypackage/discussions) (or an
  issue if Discussions are disabled) for "how do I…" questions and usage help.
- **Bug reports & feature requests** — open a
  [GitHub Issue](https://github.com/my-org/mypackage/issues) using the provided
  templates.
- **Security issues** — follow the private process in [SECURITY.md](SECURITY.md);
  do **not** file them as public issues.

Please search existing issues and discussions before opening a new one.

## Version & compatibility policy

### Python

Supported Python versions: **3.11, 3.12, and 3.13**, exercised in CI on Ubuntu,
macOS, and Windows. New CPython releases are added once stable; a version is
dropped only after it reaches end-of-life, in a minor release with a changelog
note.

### Dependencies

- Runtime dependencies specify **minimum** versions and avoid speculative upper
  bounds, so the package composes cleanly in larger environments. Upper bounds
  are added only when a specific newer major is known to break us, with the
  rationale recorded inline in `pyproject.toml`.
- For **reproducible** installs, commit `uv.lock` and use `uv sync --frozen`.

### API stability

Public API and deprecation guarantees are documented in
[docs/reference/stability.md](docs/reference/stability.md).

## Commercial / formal support

mypackage is provided under the MIT License with no warranty (see
[GOVERNANCE.md](GOVERNANCE.md) for the maintenance commitment). There is no paid
support tier at this time.
