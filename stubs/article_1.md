Title: First steps with Pelican
Date: 2014-05-22 22:00
Tags: pelican, python
Category: pelican
Slug: pelican
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

## Next steps

In future posts I will try to include [IPython notebook] files inline.


[parent]: https://github.com/schryer/schryer_pelican_blog "parent"
[generated content]: http://schryer.github.io/ "generated content"
