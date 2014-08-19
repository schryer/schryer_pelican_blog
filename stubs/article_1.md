Title: First steps with Pelican
Date: 2014-05-22 22:00
Tags: pelican, python
Category: Blog
Slug: 1
Author: David Schryer
Summary: First steps with Pelican

These are thoughts about my first steps with [Pelican] and hosting a
blog on [GitHub pages].

## Installation

Installing [Pelican] itself was pretty straightforward. More time was
spent choosing a theme that worked without any kind of tinkering.

## Use of two repositories 

To avoid the need for [GitHub Pages] to regenerate the static pages
after reload, I split this project into two nested repositories with
the [parent] housing the [generated content] in its `output`
directory. To avoid deleting the contents of the `.git` directory in
the [generated content] repository, the `output` directory was put in
the `.gitignore` file in the parent repository and the `clean` option
was changed in the Pelican `Makefile` (see below).

## Conversion of my resume

As a test, I converted my [resume](pages/resume) from [reST] to
[Markdown] using [pandoc], however, some changes were required to
render subscripts and superscripts using the [render_math] plugin for
[Pelican].

## Adding a common external links file

Because [Markdown] does not have a built in mechanism for including
content from other files, I decided to build a simple [Python] script
that reads all files contained in `stubs/` and `stubs/pages/`, and
generates new files in `contents/` and `contents/pages/` with all
links contained in `external_links.md` appended to the end of each.

The `Makefile` was altered to include a single [Python] command before
each type of build:

```shell
python add_links.py
```

The `clean` function within the `Makefile` was changed to:

```shell
python add_links.py --clean
```

which removes all generated files. The generated files replace `.md`
with `_GENERATED_by_add_links.md` to ensure other `.md` files created
by users in `content/` are not removed. 

## Typesetting mathematics

Let us start with Bayes' theorem:

$$
P(\mu~|~D) = \frac{P(D~|~\mu)P(\mu)}{P(D)}
$$

We'll use a flat prior on $\mu$ (i.e. $P(\mu) \propto 1$ over the region of interest) and use the likelihood

$$
P(D~|~\mu) = \prod_{i=1}^N \frac{1}{\sqrt{2\pi\sigma_x^2}}\exp\left[\frac{(\mu - x_i)^2}{2\sigma_x^2}\right]
$$

Computing this product and manipulating the terms, it's straightforward to show that this gives

$$
P(\mu~|~D) \propto \exp\left[\frac{-(\mu - \bar{x})^2}{2\sigma_\mu^2}\right]
$$

which is recognizable as a normal distribution with mean $\bar{x}$ and standard deviation $\sigma_\mu$.
That is, **the Bayesian posterior on $\mu$ in this case is exactly equal to the frequentist sampling distribution for $\mu$**.

## Next steps

In future posts I will try to include [IPython notebook] files inline.


[parent]: https://github.com/schryer/schryer_pelican_blog "parent"
[generated content]: http://schryer.github.io/ "generated content"
