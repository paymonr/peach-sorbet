# peach-sorbet

A small CSS kit with a soft look: a peach ground, white and pastel cards with no
borders, blob-shaped covers, one purple accent, and a way of colouring a card from its
content. Light and dark, switched with one attribute.

Two files, no build step, no dependencies.

Open `index.html` for the living demo: every token in both schemes, every component in
every state, the tint layer with a hue slider and an image-to-hue reader, and a page
assembled from kit classes only. It is self-contained, so GitHub Pages serves it from
the repo root: **<https://paymonr.github.io/peach-sorbet/>**.

---

## Quickstart

Copy `core.css` (and optionally `tint.css`) next to your page:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@300..700&family=Figtree:wght@300..900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="core.css">
<link rel="stylesheet" href="tint.css">   <!-- optional -->

<main class="main">
  <h1>Hey Sam</h1>
  <p class="lede">1,284 plays this week.</p>
  <div class="tiles">
    <div class="tile"><div class="value">1,284</div><div class="label">plays, last 7 days</div></div>
    <div class="tile"><div class="value">96</div><div class="label">hours</div></div>
  </div>
  <div class="card">
    <h2>Recommendations</h2>
    <p>Nothing yet. <a href="#">Get your first batch</a>.</p>
  </div>
</main>
```

That's the whole install. Load the fonts: Fredoka for display, Figtree for text. Both
are OFL, so self-hosting is fine; the style guide shows how.

## Dark mode

```html
<html data-scheme="dark">
```

Light is the default for everyone. Dark is an attribute on `<html>`, or on any wrapper.
Following the device is six lines of script, given in the guide, and a choice the page
makes rather than something the kit does by itself.

## Two tiers

| File | What it is |
| --- | --- |
| `core.css` | Tokens and about forty components, light and dark. Stands alone. |
| `tint.css` | Colour from content. Optional; deleting it breaks nothing. |

Without `tint.css`, cards rotate through six pastels and everything accented is purple.
With it, four numbers on an element colour its surface, blob, meter, pill and primary
button:

```html
<article class="media tint" style="--h: 340; --c: .045; --blob-c: .10; --accent-c: .14">
```

The scheme owns lightness and ink, so the same numbers read correctly in light and dark.
The source app read the numbers from album art; the guide gives that recipe and one for
categories.

## What's in it

A shell that is a sidebar on wide screens and a floating tab bar on phones. Cards,
tiles, chips, tabs, a segmented control, badges, buttons, form controls, a search bar,
tables, key–value facts, bars, a progress meter, lists, blobs, media cards and rows, a
marquee for lines that don't fit, a dock for whatever is playing, a timeline of entries
with steps, a gallery, and a dialog.

Every component is marked **extracted** (lifted from the app this came from, proven in
production) or **designed** (added here because that app never needed it). The demo
shows the tag next to each one.

## What it isn't

Not Bootstrap. No grid system, no utility classes, no JavaScript in the kit, no build
tooling. Three components need a few lines of script on the page (a measured marquee,
a row that folds open, a dialog); the guide gives them.

If you need a framework, use a framework.

## Accessibility, honestly

Every measured text pair clears WCAG AA in both schemes, most by a wide margin: body ink
is above 10:1 on every surface, muted ink above 5.7:1. One pair does not: a link inside a
lavender notice card is 4.4:1 in light mode, kept because that card is the look and the
link is underlined. The marquee keeps gliding under Reduce Motion by decision, since a
line that doesn't fit is unreadable otherwise; transitions do stop.
[Full detail in the style guide.](STYLE-GUIDE.md#accessibility)

## Docs

- **[STYLE-GUIDE.md](STYLE-GUIDE.md)**: tokens, the tint layer, components, the six
  rules for extending it, the scripts, and where the kit deviates from its source.
- **[docs/design.md](docs/design.md)**: the design rationale and the source of truth for
  every value.

## Verifying changes

```bash
python3 tools/check.py
```

Fails if a component hardcodes a colour, a `var()` doesn't resolve, `tint.css` defines a
token or styles a class core doesn't, anything uses `!important`, a radius is off the
ladder, a transition has a literal duration, or a `data-scheme` value is misspelt.
Standard library only.

## Sibling

[kawaii-meadow](https://github.com/paymonr/kawaii-meadow) is the same idea with a
different look: hairline borders, heavy uppercase micro-labels, a night meadow.

## Licence

MIT
