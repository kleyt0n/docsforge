# Core concepts

A short page that pays for itself many times over: explain the *few* ideas that
make the rest of the API predictable, so readers can guess correctly instead of
looking everything up.

## One shape for every entry point

Every public entry point takes data and returns a `Report`:

```text
summarize(values, **options) ──▶ Report
compare(mapping,  **options) ──▶ list[Report]
```

That uniformity is the whole design. Because the output type never varies, the
things that consume a result — serialization, comparison, plotting — are written
once and work with every method, including ones you add yourself.

## The `Report` object

`Report` is a frozen dataclass. It carries the computed figures plus enough
provenance to reproduce them:

| Field | Meaning |
|---|---|
| `label` | Human-readable name, propagated into tables and plots |
| `mean` | The central estimate |
| `spread` | Dispersion of the input |
| `n` | Number of observations actually used, after trimming |
| `options` | The exact options the result was produced with |

Because `options` travels with the result, a `Report` read back from disk is
self-describing — you never have to guess which settings produced a number.

## Options are validated once, at the edge

Options are normalized and validated when they enter the public API, not deep in
a helper. Two consequences worth knowing:

- Errors surface immediately, pointing at the argument you passed, not at an
  internal frame ten calls down.
- Internal helpers may assume valid input. They are underscore-prefixed and not
  part of the public API — see [API stability](../reference/stability.md).

!!! warning "Public surface"
    The public API is what `docsforge.__all__` exports plus the documented
    submodules. Anything underscore-prefixed can change in any release.

## Extension is registration, not inheritance

Adding your own method means registering a function, not subclassing anything:

```python
@mp.register("median")
def median_summary(values, **options):
    ...
    return mp.Report(...)
```

Registered methods are indistinguishable from built-ins at every call site that
takes a method name. This is covered in [Advanced usage](../guide/advanced.md).

## A worked mental model

$$
\text{mean}_{\text{trimmed}} = \frac{1}{n - 2k} \sum_{i=k+1}^{n-k} x_{(i)}
$$

where \(x_{(i)}\) is the \(i\)-th order statistic and \(k = \lfloor \alpha n
\rfloor\) for a trim fraction \(\alpha\). Writing the formula down once, here,
means the API reference can simply say *"trimmed mean"* and be understood.

!!! tip "Rule of thumb for this page"
    If a reader can predict the signature of a function they have never seen
    after reading this page, it is doing its job.
