"""End-to-end example, included verbatim into docs/guide/basic-usage.md.

Because the docs pull this file in with the `--8<--` include syntax, and CI runs
it, the snippet on the site can never drift away from working code.
"""

import docsforge as mp
from docsforge.utils import describe

series = {
    "baseline": [3.0, 1.0, 4.0, 1.0, 5.0, 9.0, 2.0, 6.0],
    "treatment": [4.0, 2.0, 5.0, 2.0, 6.0, 9.0, 3.0, 7.0],
}

table = mp.compare(series, trim=0.125, precision=3)

for row in describe(table):
    print(f"{row['label']:>10}  mean={row['mean']:>6}  n={row['n']}")

best = max(table, key=lambda report: report.mean)
print(f"\nhighest mean: {best.label} ({best.mean})")
