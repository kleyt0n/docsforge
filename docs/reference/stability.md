# API stability

What we promise not to break, and how we break it when we must. Adapt the
specifics; keep the structure — users cannot depend on a library whose stability
policy is unwritten.

## Versioning

docsforge follows [Semantic Versioning](https://semver.org). Every release is
described in the [GitHub release notes](https://github.com/my-org/docsforge/releases),
which are the changelog — one place, generated from the tags, impossible to
forget to update:

| Change | Version bump |
|---|---|
| Bug fix, no behavior change to documented API | patch (`0.1.0 → 0.1.1`) |
| New feature, backward compatible | minor (`0.1.0 → 0.2.0`) |
| Breaking change to public API | major (`1.0.0 → 2.0.0`) |

!!! warning "Pre-1.0"
    While the version is below `1.0`, minor releases may contain breaking
    changes. They will always be listed under **Breaking changes** in the
    release notes. Pin an exact version if you need stability today.

## What counts as public API

**Public** — covered by the guarantees above:

- Everything exported in `docsforge.__all__`.
- The documented submodules on this site (`docsforge.core`, `docsforge.utils`).
- The fields of `Report`, and the shape of `to_row()`.
- Documented default values. Changing a default is a behavior change.

**Not public** — may change in any release, without notice:

- Anything whose name starts with an underscore.
- Modules not listed in the [API reference](index.md).
- Exception *messages* (the exception *types* are public).
- The exact contents of `repr()` output.

## Deprecation policy

1. **Announce.** The replacement ships first, in a minor release, and the old
   name starts emitting a `DeprecationWarning` naming its replacement.
2. **Document.** The release notes record it under **Deprecations**, and the
   docstring gains a `.. deprecated::` note.
3. **Wait.** A deprecated name lives for at least **two minor releases** or
   **six months**, whichever is longer.
4. **Remove.** Removal happens only in a major release (or, pre-1.0, a minor
   release that says so in its release notes).

```python
import warnings


def old_name(*args, **kwargs):
    """Deprecated alias for :func:`new_name`.

    .. deprecated:: 0.3.0
        Use :func:`new_name`; ``old_name`` is removed in 1.0.
    """
    warnings.warn(
        "old_name() is deprecated and will be removed in 1.0; use new_name()",
        DeprecationWarning,
        stacklevel=2,
    )
    return new_name(*args, **kwargs)
```

!!! tip "Surface deprecations in your own CI"
    Run your test suite with `-W error::DeprecationWarning` to find out about a
    removal on the release that announces it, not the one that ships it.

## Supported Python versions

We support all Python versions that upstream has not end-of-lifed, currently
**3.11–3.13**, and test each of them in CI. A new CPython release is added once
it is stable; an old one is dropped only after EOL, in a minor release that
says so in its release notes.

## Numerical results

Numbers can change without the API changing. Any change to a computed result
that is not a bug fix is treated as **breaking** and documented in the release
notes with the reason and the expected magnitude of the difference.
