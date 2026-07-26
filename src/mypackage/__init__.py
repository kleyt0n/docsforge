"""mypackage — a minimal, fully working example package for the docs template.

It exists so that the API reference, the doctested snippets, and the CI pipeline
all have something real to operate on. Replace it with your own code; the docs
configuration needs no changes beyond the module paths in
``docs/reference/*.md``.

Examples
--------
>>> import mypackage as mp
>>> mp.summarize([3.0, 1.0, 4.0, 1.0, 5.0], label="demo").mean
2.8
"""

from mypackage.core import Report, compare, register, summarize

__version__ = "0.1.0"

__all__ = [
    "Report",
    "compare",
    "register",
    "summarize",
]
