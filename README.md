<div align="center">

<img src="docs/logo.svg" alt="Template logo" width="120">

# Professional docs template

**A batteries-included documentation setup for Python projects — Material for
MkDocs with a flat, monospace, terminal-styled theme, an auto-generated API
reference, and CI that publishes to GitHub Pages.**

[![python](https://img.shields.io/badge/python-3.11+-3987e5?style=flat-square)](https://www.python.org)
[![mkdocs-material](https://img.shields.io/badge/mkdocs--material-9.5+-4f46e5?style=flat-square)](https://squidfunk.github.io/mkdocs-material/)
[![license](https://img.shields.io/badge/MIT-c98500?style=flat-square)](LICENSE)

</div>

---

> **You are reading the template's README.** `scripts/init_template.py` replaces
> it with a starter README for your project.

## Use it

```bash
# 1. Start from this template (GitHub: "Use this template"), then clone it
git clone https://github.com/my-org/professional-docs-template myproject
cd myproject

# 2. Rename everything — preview first, then apply
python scripts/init_template.py --dry-run
python scripts/init_template.py

# 3. Install and preview
uv sync --all-extras
uv run mkdocs serve            # http://127.0.0.1:8000
```

The init script is non-interactive too:

```bash
python scripts/init_template.py \
  --name "MyProject" --package myproject \
  --org my-org --repo myproject \
  --author "MyProject contributors" \
  --tagline "Differentiable widgets for people who hate widgets."
```

It rewrites the placeholders (`mypackage`, `my-org`, `my-org/mypackage`,
`mypackage contributors`) across every text file, renames `src/mypackage/`,
stamps the license year, installs the starter README, and then deletes itself.

## What you get

| | |
|---|---|
| **Theme** | Material for MkDocs, flat/monospace/terminal styling, true-black dark mode, light+dark palettes with a toggle |
| **Home page** | Hero with logo, badges, and CTA buttons; auto-fitting feature-card grid |
| **Content** | Admonitions, collapsible details, synced content tabs, code annotations, math (MathJax + instant-nav hookup), footnotes, keyboard keys, task lists |
| **API reference** | mkdocstrings renders NumPy-style docstrings straight from `src/`; nothing to keep in sync by hand |
| **Docs-as-code** | `--8<--` includes pull code and the changelog in from the repo, so snippets cannot drift |
| **Strict builds** | `validation:` in `mkdocs.yml` turns broken links, bad anchors, and pages missing from the nav into build failures |
| **CI** | `docs.yml` publishes to GitHub Pages; `ci.yml` runs lint, tests (3.11–3.13 × Linux/macOS/Windows), and the same strict docs build on every PR |
| **Repo hygiene** | Contributing, code of conduct, security, support, governance, API-stability policy, issue/PR templates, CODEOWNERS, pre-commit |
| **Working example** | A tiny real package (`src/mypackage/`) with tested doctests, so the whole pipeline is green from the first commit |

## Layout

```text
.
├── mkdocs.yml                  # theme, extensions, plugins, nav
├── docs/
│   ├── index.md                # home page + hero
│   ├── logo.svg                # placeholder mark (swap for yours)
│   ├── stylesheets/extra.css   # the entire visual identity, `--site-*` vars
│   ├── javascripts/mathjax.js  # math, wired to instant navigation
│   ├── getting-started/        # installation · quickstart · concepts
│   ├── guide/                  # basic · advanced · writing-docs (style guide)
│   ├── reference/              # generated API reference + stability policy
│   └── about/                  # contributing · changelog (included from root)
├── src/mypackage/              # example package the API reference renders
├── examples/basic_usage.py     # included verbatim into the docs
├── tests/                      # proves the CI pipeline works end to end
├── scripts/init_template.py    # the renamer
└── .github/                    # workflows, issue/PR templates, CODEOWNERS
```

## Publishing to GitHub Pages

One-time setup after your first push: **Settings → Pages → Build and deployment
→ Source: GitHub Actions**. From then on, `.github/workflows/docs.yml` builds
and deploys on every push to `main` that touches `docs/`, `mkdocs.yml`, `src/`,
or `CHANGELOG.md`.

For a project site the default `site_url` is
`https://<org>.github.io/<repo>/`; the init script sets it for you.

## Customizing

**Colors.** One variable drives the accent: `--md-accent-fg-color` at the top of
`docs/stylesheets/extra.css`. The dark background ramp sits just below it, under
`[data-md-color-scheme="slate"]`.

**Logo.** Replace `docs/logo.svg`. Keep it single-color so it reads against the
black header; the hero applies a subtle glow that suits line art.

**Fonts.** `theme.font` in `mkdocs.yml`. The mono-everywhere look is deliberate
— switch `text` to a sans (e.g. `Inter`) if you want a more conventional feel;
nothing in the CSS assumes monospace.

**Not a Python project?** Delete the `mkdocstrings` block from `mkdocs.yml`,
drop `docs/reference/`, `src/`, and `tests/`, and remove the `test` job from
`ci.yml`. Everything else is language-agnostic.

**Adding pages.** Create the `.md` file, add it to `nav:` in `mkdocs.yml`, link
to it with a relative `.md` path. `mkdocs build --strict` catches all three if
you miss one.

## Conventions

The [Writing docs](docs/guide/writing-docs.md) page is both the house style
guide and a live gallery of every component, with source shown next to the
rendered result. It is the one page worth reading before writing any others —
and worth keeping in your project so contributors have the same reference.

## License

[MIT](LICENSE) — use it for anything, no attribution required.
