<!-- =================================================================
     HOME PAGE
     The hero below is plain HTML + the `.site-*` classes defined in
     docs/stylesheets/extra.css. Keep the structure; swap the words.

     It is deliberately spare: mark, name, one sentence, two links.
     Badges live in the README, where they answer a stranger's first
     questions; here they would only compete with the tagline.
     ================================================================= -->

<div class="site-hero" markdown>

<img class="site-hero__logo" src="logo.svg" alt="Docsforge logo">

<h1 class="site-hero__title">Docsforge</h1>

<p class="site-hero__tagline">
One sentence that says what this is and why it exists. Concrete beats clever —
name the thing it does and the thing it replaces.
</p>

[Get started](getting-started/installation.md){ .md-button .md-button--primary }
[View on GitHub](https://github.com/my-org/docsforge){ .md-button }

</div>

## Why Docsforge

Open with the *problem*, not the feature list. Two or three short paragraphs
that a reader who has never heard of this project can follow: what is hard
today, why the existing options do not solve it, and what changes if they adopt
this.

Say what it *is* in one bolded sentence — **docsforge turns X into Y** — and
then back that claim with the one detail that makes it credible: the algorithm,
the guarantee, the benchmark, the integration. Avoid adjectives that carry no
information ("powerful", "seamless", "blazing fast"); a number or a mechanism
persuades where an adjective does not.

Close the section by telling the reader where to go next. Every other page on
this site is one click from here.

<figure markdown>
  ![Placeholder screenshot](img/placeholder.svg)
  <figcaption>A representative output, rendered with <code>docsforge.summarize</code>.</figcaption>
</figure>

## What is inside

<div class="site-grid" markdown>

<div class="site-card" markdown>
### [Installation](getting-started/installation.md)
Install with uv or pip, plus the optional extras and how to verify the install.
</div>

<div class="site-card" markdown>
### [Quickstart](getting-started/quickstart.md)
An end-to-end example in under thirty lines, runnable as written.
</div>

<div class="site-card" markdown>
### [Core concepts](getting-started/concepts.md)
The handful of ideas that make the rest of the API predictable.
</div>

<div class="site-card" markdown>
### [Basic usage](guide/basic-usage.md)
The everyday workflow, with the parameters that actually matter.
</div>

<div class="site-card" markdown>
### [Advanced usage](guide/advanced.md)
Extension points, performance notes, and the sharp edges worth knowing.
</div>

<div class="site-card" markdown>
### [API reference](reference/index.md)
Generated from source docstrings, so it always matches the installed version.
</div>

</div>

## Quickstart

```python
import docsforge as mp

report = mp.summarize([3.0, 1.0, 4.0, 1.0, 5.0], label="demo")

print(report.mean)  # 2.8
print(report.to_row())
```

## Capabilities at a glance

| Area | What you get |
|---|---|
| **Core** | The one-line summary of your primary abstraction |
| **Extensibility** | How users plug in their own behavior |
| **Performance** | The claim you can defend with a benchmark |
| **Integrations** | The formats, services, or libraries you interoperate with |
| **Support** | Python versions and platforms exercised in CI |

!!! tip "New here?"
    Start with [Installation](getting-started/installation.md), then the
    [Quickstart](getting-started/quickstart.md). To understand *how* the pieces
    fit together before reaching for the API reference, read
    [Core concepts](getting-started/concepts.md).
