# Contributing

Contributions are welcome — bug reports, documentation fixes, and features
alike. The full guide lives in
[`CONTRIBUTING.md`](https://github.com/my-org/mypackage/blob/main/CONTRIBUTING.md)
at the repository root; this page is the short version.

## Set up

```bash
git clone https://github.com/my-org/mypackage
cd mypackage
uv sync --all-extras
uv run pre-commit install
```

## Everyday commands

| Task | Command |
|---|---|
| Run tests | `uv run pytest` |
| Lint | `uv run ruff check .` |
| Format | `uv run ruff format .` |
| Preview docs | `uv run mkdocs serve` |
| Build docs like CI | `uv run mkdocs build --strict` |

## Documentation changes

Docs are as reviewable as code here. `mkdocs build --strict` runs in CI and
fails on broken links, missing nav entries, and unresolved includes — so a docs
PR that builds locally will pass.

New to the conventions? [Writing docs](../guide/writing-docs.md) is the house
style guide and component gallery.

## Before opening a pull request

- [ ] Tests pass, and new behavior has a test
- [ ] `ruff check` and `ruff format --check` pass
- [ ] `mkdocs build --strict` passes if docs changed
- [ ] Commits follow [Conventional Commits](https://www.conventionalcommits.org)
- [ ] The PR template is filled in and links its issue

## Code of conduct

Participation is governed by the
[Contributor Covenant](https://github.com/my-org/mypackage/blob/main/CODE_OF_CONDUCT.md).
Report concerns privately through the repository's **Security** tab.
