---
title: "Pandoc Markdown CSS Theme"
subtitle: "Starter files for generating HTML from Pandoc Markdown"
author: "@jez"
author-url: 'https://github.com/jez'
date: "2021-06-20"
---

This project provides CSS files and a template for using Pandoc[^pandoc] to
generate standalone HTML files. It supports most features Pandoc Markdown has to
offer, and some extras. The default look can be tweaked via CSS variables, and
it does not need JavaScript, even for side notes.

# Features

A short list of headline features:

[^pandoc]:
  {-} [Pandoc] is a "universal document converter." It is particularly good at
  generating HTML and \(\LaTeX\) from Markdown.

- [Code blocks](features/#code-blocks), including:
  - Syntax themes
  - Line numbers and line highlights
  - Extra wide and full-width options
  - Captions
- [Images and tables](features/#images-tables-and-captioned-code-blocks),
  including:
  - Extra wide and full-width options
  - Captions
- [Side notes and margin notes](features/#side-notes-and-margin-notes)
- [Floating table of contents](features/#table-of-contents)
- [\(\LaTeX\) math](features/#math), rendered via [\(\KaTeX\)][KaTeX] in
  the browser
- Dark mode, based on the user's default color scheme preference

For the complete feature set, see the documentation. You might also want to
view the "kitchen sink" page that is useful when developing, or the source code:

[→ Documentation](features/)\
[→ Kitchen Sink](kitchen-sink/)\
[→ Source on GitHub](https://github.com/jez/pandoc-markdown-css-theme)

The theme is fully responsive, including phones, tablets, laptops, and wide
desktop screens. Side notes and the table of contents display inline on small
screen sizes, and in the margins on wide enough screens. Extra wide images,
tables, and code blocks shrink when space isn't available. CSS `@media print`
styles declare first-class print styles.

:::{.wide .extra-wide .only-light-mode}

![Only right margin at tablet width, and no margins on mobile](img/light-mobile-responsive.png)

:::

:::{.wide .extra-wide .only-dark-mode}

![Only right margin at tablet width, and no margins on mobile](img/dark-mobile-responsive.png)

:::

The source code is extremely tweakable.[^tweakable] A small set of CSS variables
control a large number of font and color settings: you don't have to hunt down
all the places that need to be changed to tweak the design. As a proof of
concept, see [this page](paper/), which tweaks the default theme slightly. These
same CSS variables power the light- and dark-mode versions of the theme. Of
course, the code is open source and you're welcome to copy the theme files and
completely overhaul them if desired.

[^tweakable]:
  {-} When changing things like the font family or font size, the thing that
  matters is to pay special attention to alignment. Different fonts have
  different x-heights and widths. Most layouting can be agnostic of these
  things, but there are explicit variables for places where it matters.


And finally, there's basically only HTML and CSS. The theme doesn't use custom
fonts by default, and only uses JavaScript for two things:

- Rendering math (via [\(\KaTeX\)][KaTeX]), only if used.
- Slightly tweaking the appearance of checklist items. (Pandoc emits them as
  disabled, but they look better when enabled in my opinion.) This is entirely
  presentational.

Placement of side notes, the table of contents, and code block line highlights
are all controlled with CSS. See the [credits](#credits) below for more
background on the techniques used.

# Usage

This project merely provides a CSS files and a standalone HTML template to give
to Pandoc.  The imporant files that you might want to copy out to start your own
project:

- [`public/css/theme.css`], the core CSS implementing theme
- [`template.html5`], the Pandoc template that renders Markdown to HTML
- [`Makefile`], showcasing the Pandoc flags required to get things to build
- [`src/index.md`], the source code for this page

[`public/css/theme.css`]: https://github.com/jez/pandoc-markdown-css-theme/blob/master/public/css/theme.css
[`template.html5`]: https://github.com/jez/pandoc-markdown-css-theme/blob/master/template.html5
[`Makefile`]: https://github.com/jez/pandoc-markdown-css-theme/blob/master/Makefile
[`src/index.md`]: https://github.com/jez/pandoc-markdown-css-theme/blob/master/src/index.md

To see things in action, try rebuilding this site locally. First, you'll need a
few command line programs:

- [ ] [Pandoc]
- [ ] [`pandoc-sidenote`]
- [ ] `realpath` from [GNU coreutils]
- [ ] (optional) [`watchman`], for rebuilding when files change

Follow the installation instructions for your platform. If you're using macOS,
installation is as easy as:

```{.numberLines}
brew install pandoc coreutils
brew tap jez/formulae
brew install pandoc-sidenote
```

Then you can clone this project and run `make watch`:

```{.bash .numberLines .hl-7 .hl-10}
git clone https://github.com/jez/pandoc-markdown-css-theme
cd pandoc-markdown-css-theme

# Test everything by forcing a clean build
# (the generated comes with the clone)
make clean
make

# If you installed watchman
make watch
```

Running `make` will build everything in the site.

Running `make watch` will start a webserver at <http://127.0.0.1:8000/>, open
that URL in a web browser, and watch files for changes in the background.

## Usage with Jekyll

While the core theme is just a handful of static files that can be copied into
any project, using this theme with [Jekyll] is as easy as installing a theme:

→ [Pandoc Markdown Jekyll Theme][`pandoc-markdown-jekyll-theme`]

Check the project above for installation and usage instructions with Jekyll.

# Credits

First, thanks to [Pandoc], by John MacFarlane, for being an all-around awesome
tool, especially for Markdown.

The core technique for laying out side notes[^gwern] I learned from [Tufte CSS],
by Dave Liepmann. The technique is [described in detail
here][tufte-css-sidenotes]. Tufte CSS suggests writing the HTML for sidenotes by
hand, but I wanted to use Markdown. I wrote [`pandoc-sidenote`], a [Pandoc
filter] that traverses Pandoc's internal AST and converts footnote nodes into
the HTML side note markup for Tufte CSS-style side notes.

[^gwern]:
  {-} Gwern has a great survey post that discusses [Sidenotes In Web Design],
  covering the techniques in Tufte CSS as well as the limitations, and many
  alternatives.

[tufte-css-sidenotes]: https://edwardtufte.github.io/tufte-css/#sidenotes
[Sidenotes In Web Design]: https://www.gwern.net/Sidenotes

While the idea for side notes comes entirely from Tufte CSS, the implementation
at this point is almost completely different. Tufte CSS uses relative widths
everywhere, but I wanted a body with a constant width at all but the smallest
screen sizes. Tufte CSS renders the main body off center. Rendering centered
when possible and off center when not adds complexity in the implementation.

The inspiration for code block line highlights comes from a change I contributed
to [`pandoc-emphasize-code`], by Oskar Wickström (another Pandoc filter). I
decided against using it for this project because it forces a choice of either
line highlights or syntax highlighting per code block (unless you tack on a
JavaScript-based syntax highlighter, like Highlight.js). I thought of a [clever
technique](features/#line-highlight-limit) using CSS clases to avoid this.

[`pandoc-emphasize-code`]: https://github.com/owickstrom/pandoc-emphasize-code

Considerable design inspiration comes from [Dropbox Paper], a gorgeous and
powerful tool. (In fact, the theme is customizable enough to [recreate the
look of Paper](paper/). This is provided for educational purposes only, under
Fair Use.)

Z
[Pandoc]: https://pandoc.org/
[Pandoc filter]: https://pandoc.org/filters.html
[`pandoc-sidenote`]: https://github.com/jez/pandoc-sidenote
[GNU coreutils]: https://www.gnu.org/software/coreutils/coreutils.html
[`watchman`]: https://facebook.github.io/watchman/
[KaTeX]: https://katex.org/
[Tufte CSS]: https://edwardtufte.github.io/tufte-css/
[Dropbox Paper]: https://www.dropbox.com/paper
[`pandoc-markdown-jekyll-theme`]: https://github.com/jez/pandoc-markdown-jekyll-theme
[Jekyll]: https://jekyllrb.com
