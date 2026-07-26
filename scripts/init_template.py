#!/usr/bin/env python3
"""Rename this template into your own project.

Run once, right after cloning:

    python scripts/init_template.py --dry-run    # preview every change
    python scripts/init_template.py              # apply

It rewrites the placeholder strings below across the whole tree, renames
``src/mypackage/`` to your package name, and swaps this README for a starter
one. Anything it cannot infer, it asks for.

Placeholders
------------
``mypackage``               package / import name, and the default display name
``my-org``                  GitHub org or user
``my-org/mypackage``        repository path
``mypackage contributors``  copyright holder

The script only edits text files, and never touches ``.git/``.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Directories that are never rewritten.
SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "site",
    "dist",
    "build",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
}

# Extensions treated as text. Anything else is left alone.
TEXT_SUFFIXES = {
    "",
    ".cfg",
    ".css",
    ".ini",
    ".js",
    ".json",
    ".lock",
    ".md",
    ".py",
    ".svg",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}

PACKAGE_RE = re.compile(r"^[a-z][a-z0-9_]*$")


def ask(prompt: str, default: str) -> str:
    """Prompt for a value, falling back to ``default`` on an empty answer."""
    reply = input(f"{prompt} [{default}]: ").strip()
    return reply or default


def collect(args: argparse.Namespace) -> dict[str, str]:
    """Resolve every setting from flags, prompting for whatever is missing."""
    interactive = sys.stdin.isatty()

    def resolve(value: str | None, prompt: str, default: str) -> str:
        if value:
            return value
        if not interactive:
            return default
        return ask(prompt, default)

    package = resolve(args.package, "Package (import) name", "mypackage")
    if not PACKAGE_RE.match(package):
        sys.exit(f"error: {package!r} is not a valid Python package name")

    display = resolve(args.name, "Display name (site title)", package)
    org = resolve(args.org, "GitHub org or user", "my-org")
    repo = resolve(args.repo, "Repository name", package)
    author = resolve(args.author, "Copyright holder", f"{display} contributors")
    tagline = resolve(
        args.tagline,
        "One-line description",
        f"A short, punchy description of {display}.",
    )

    return {
        "package": package,
        "display": display,
        "org": org,
        "repo": repo,
        "author": author,
        "tagline": tagline,
    }


def replacements(cfg: dict[str, str]) -> list[tuple[str, str]]:
    """Ordered (old, new) pairs. Longest/most specific patterns come first."""
    return [
        ("my-org.github.io/mypackage", f"{cfg['org']}.github.io/{cfg['repo']}"),
        ("my-org/mypackage", f"{cfg['org']}/{cfg['repo']}"),
        ("mypackage contributors", cfg["author"]),
        ("my-org", cfg["org"]),
        ("mypackage", cfg["package"]),
    ]


def is_text_file(path: Path) -> bool:
    """Return True for files the rewriter should open."""
    return path.suffix.lower() in TEXT_SUFFIXES


def iter_files(root: Path):
    """Yield every candidate file below ``root``, skipping build/VCS dirs."""
    this_file = Path(__file__).resolve()
    for path in sorted(root.rglob("*")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.resolve() == this_file:  # never rewrite the rewriter
            continue
        if path.is_file() and is_text_file(path):
            yield path


def rewrite(path: Path, pairs: list[tuple[str, str]], *, dry_run: bool) -> int:
    """Apply ``pairs`` to one file. Returns the number of substitutions."""
    try:
        original = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return 0

    updated = original
    count = 0
    for old, new in pairs:
        if old == new:
            continue
        count += updated.count(old)
        updated = updated.replace(old, new)

    if count and not dry_run:
        path.write_text(updated, encoding="utf-8")

    return count


def _apply_edits(edits: dict[Path, list[tuple[str, str]]], *, dry_run: bool) -> None:
    """Apply an exact-string edit list to specific files, skipping missing ones."""
    for path, pairs in edits.items():
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for old, new in pairs:
            text = text.replace(old, new)
        if not dry_run:
            path.write_text(text, encoding="utf-8")


def apply_display_name(cfg: dict[str, str], *, dry_run: bool) -> None:
    """Fix the few places that want the display name, not the package name."""
    pkg, display = cfg["package"], cfg["display"]
    if display == pkg:
        return

    edits = {
        ROOT / "mkdocs.yml": [(f"site_name: {pkg}", f"site_name: {display}")],
        ROOT / "docs" / "index.md": [
            (
                f'<h1 class="site-hero__title">{pkg}</h1>',
                f'<h1 class="site-hero__title">{display}</h1>',
            ),
            (f"## Why {pkg}", f"## Why {display}"),
        ],
        ROOT / "README.md": [
            (f"# {pkg}\n", f"# {display}\n"),
            (f"## Why {pkg}", f"## Why {display}"),
            (f'alt="{pkg} logo"', f'alt="{display} logo"'),
        ],
    }

    _apply_edits(edits, dry_run=dry_run)


def apply_tagline(cfg: dict[str, str], *, dry_run: bool) -> None:
    """Drop the one-line description into every place that shows it."""
    pkg, tagline = cfg["package"], cfg["tagline"]
    if tagline == f"A short, punchy description of {pkg}.":
        return

    boilerplate = f"A short, punchy description of {pkg} — what it does and for whom."

    edits = {
        ROOT / "docs" / "index.md": [
            (
                "One sentence that says what this is and why it exists. "
                "Concrete beats clever —\nname the thing it does and the thing it replaces.",
                tagline,
            ),
        ],
        ROOT / "README.md": [(f"**{boilerplate}**", f"**{tagline}**")],
        ROOT / "pyproject.toml": [(f'description = "{boilerplate}"', f'description = "{tagline}"')],
        ROOT / "mkdocs.yml": [
            (
                f"  A short, punchy description of {pkg} — what it does, for whom, and\n"
                "  what makes it different. Two lines at most; it lands in search results.",
                f"  {tagline}",
            ),
        ],
    }

    _apply_edits(edits, dry_run=dry_run)


def rename_package(cfg: dict[str, str], *, dry_run: bool) -> None:
    """Rename ``src/mypackage`` to the chosen package name."""
    src = ROOT / "src" / "mypackage"
    dst = ROOT / "src" / cfg["package"]
    if src == dst or not src.exists():
        return
    print(f"  rename  src/mypackage -> src/{cfg['package']}")
    if not dry_run:
        src.rename(dst)


def install_project_readme(*, dry_run: bool) -> None:
    """Replace the template README with the starter project README."""
    starter = ROOT / "scripts" / "README.project.md"
    if not starter.exists():
        return
    print("  readme  scripts/README.project.md -> README.md")
    if not dry_run:
        shutil.copyfile(starter, ROOT / "README.md")
        starter.unlink()


def stamp_license(cfg: dict[str, str], *, dry_run: bool) -> None:
    """Set the current year on the MIT license."""
    path = ROOT / "LICENSE"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"Copyright \(c\) \d{4}", f"Copyright (c) {date.today().year}", text)
    if not dry_run:
        path.write_text(text, encoding="utf-8")


def main() -> int:
    """Entry point."""
    parser = argparse.ArgumentParser(
        description="Rename this docs template into your own project.",
    )
    parser.add_argument("--name", help="display name shown as the site title")
    parser.add_argument("--package", help="Python package / import name")
    parser.add_argument("--org", help="GitHub org or user")
    parser.add_argument("--repo", help="repository name")
    parser.add_argument("--author", help="copyright holder")
    parser.add_argument("--tagline", help="one-line description for the hero")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show what would change without writing anything",
    )
    parser.add_argument(
        "--keep-script",
        action="store_true",
        help="do not delete this script when finished",
    )
    args = parser.parse_args()

    cfg = collect(args)
    pairs = replacements(cfg)

    print()
    print(f"  package  {cfg['package']}")
    print(f"  display  {cfg['display']}")
    print(f"  repo     {cfg['org']}/{cfg['repo']}")
    print(f"  author   {cfg['author']}")
    print()

    total_files = 0
    for path in iter_files(ROOT):
        changed = rewrite(path, pairs, dry_run=args.dry_run)
        if changed:
            total_files += 1
            print(f"  {changed:>4}  {path.relative_to(ROOT)}")

    # Install the starter README first, so the display name and tagline edits
    # below land on the project's README rather than the template's.
    install_project_readme(dry_run=args.dry_run)
    apply_display_name(cfg, dry_run=args.dry_run)
    apply_tagline(cfg, dry_run=args.dry_run)
    stamp_license(cfg, dry_run=args.dry_run)
    rename_package(cfg, dry_run=args.dry_run)

    print()
    if args.dry_run:
        print(f"dry run: {total_files} files would change. Re-run without --dry-run.")
        return 0

    print(f"done: {total_files} files updated.")
    print("next:")
    print("  uv sync --all-extras")
    print("  uv run mkdocs serve")

    if not args.keep_script:
        Path(__file__).unlink()
        print("\n(this script deleted itself; --keep-script keeps it)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
