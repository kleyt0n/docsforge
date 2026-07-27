#!/usr/bin/env python3
"""Rename this template into your own project.

Run once, right after cloning:

    python scripts/init_template.py --dry-run    # preview every change
    python scripts/init_template.py              # apply

It rewrites the placeholder strings below across the whole tree, renames
``src/docsforge/`` to your package name, and swaps this README for a starter
one. Anything it cannot infer, it asks for.

Placeholders
------------
``docsforge``               package / import / crate name
``Docsforge``               display name — site title, headings, alt text
``my-org``                  GitHub org or user
``my-org/docsforge``        repository path
``Docsforge contributors``  copyright holder

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
    "target",  # Rust build artifacts
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
    ".rs",
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

    package = resolve(args.package, "Package (import) name", "docsforge")
    if not PACKAGE_RE.match(package):
        sys.exit(f"error: {package!r} is not a valid Python package name")

    display = resolve(
        args.name,
        "Display name (site title)",
        package.replace("_", " ").title(),
    )
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
    """Ordered (old, new) pairs. Longest/most specific patterns come first.

    Order matters: ``Docsforge contributors`` has to win over the bare
    ``Docsforge`` display-name pair, and both of the ``my-org/...`` URL forms
    have to win over the bare ``my-org``. :func:`rewrite` applies the whole
    table in one pass, so the first pattern that matches at a position wins and
    substituted text is never re-examined.
    """
    return [
        ("my-org.github.io/docsforge", f"{cfg['org']}.github.io/{cfg['repo']}"),
        ("my-org/docsforge", f"{cfg['org']}/{cfg['repo']}"),
        ("Docsforge contributors", cfg["author"]),
        ("Docsforge", cfg["display"]),
        ("my-org", cfg["org"]),
        ("docsforge", cfg["package"]),
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


def compile_pairs(pairs: list[tuple[str, str]]) -> tuple[re.Pattern[str], dict[str, str]]:
    """Compile ``pairs`` into one alternation pattern plus its lookup table.

    A single pass is what makes the substitution safe: applying the pairs one
    after another would let a later pattern match text an earlier one just
    inserted, so a display name of ``Docsforge Pro`` or an org named after the
    package would be rewritten twice.
    """
    table = {old: new for old, new in pairs if old != new}
    pattern = re.compile("|".join(re.escape(old) for old in table))
    return pattern, table


def rewrite(path: Path, compiled: tuple[re.Pattern[str], dict[str, str]], *, dry_run: bool) -> int:
    """Apply the compiled replacements to one file. Returns the match count."""
    pattern, table = compiled
    if not table:
        return 0

    try:
        original = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return 0

    updated, count = pattern.subn(lambda match: table[match.group(0)], original)

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
    """Rename ``src/docsforge`` to the chosen package name."""
    src = ROOT / "src" / "docsforge"
    dst = ROOT / "src" / cfg["package"]
    if src == dst or not src.exists():
        return
    print(f"  rename  src/docsforge -> src/{cfg['package']}")
    if not dry_run:
        src.rename(dst)


def install_project_readme(*, dry_run: bool) -> None:
    """Replace the template README with the starter project README.

    The banner goes with it: it illustrates the template's own README, which
    this overwrites, so keeping it would leave half a megabyte of unreferenced
    PNG in every project started from here.
    """
    starter = ROOT / "scripts" / "README.project.md"
    if not starter.exists():
        return
    print("  readme  scripts/README.project.md -> README.md")
    if not dry_run:
        shutil.copyfile(starter, ROOT / "README.md")
        starter.unlink()

    banner = ROOT / "banner.png"
    if banner.exists():
        print("  remove  banner.png")
        if not dry_run:
            banner.unlink()


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
    parser.add_argument("--package", help="package / import / crate name")
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
    compiled = compile_pairs(replacements(cfg))

    print()
    print(f"  package  {cfg['package']}")
    print(f"  display  {cfg['display']}")
    print(f"  repo     {cfg['org']}/{cfg['repo']}")
    print(f"  author   {cfg['author']}")
    print()

    total_files = 0
    for path in iter_files(ROOT):
        changed = rewrite(path, compiled, dry_run=args.dry_run)
        if changed:
            total_files += 1
            print(f"  {changed:>4}  {path.relative_to(ROOT)}")

    # Install the starter README first, so the tagline edit below lands on the
    # project's README rather than the template's.
    install_project_readme(dry_run=args.dry_run)
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
