# CLAUDE.md

Guidance for Claude Code (claude.ai/code) when working in this repository.

## What this repo is

A small, opinionated CSS kit, not a framework. It packages the visual system of a
self-hosted music recommender's web app into something droppable and general-purpose:
link two stylesheets and a new page is substantially styled with no hand-written CSS.
It is the sibling of kawaii-meadow, with the same shape and a different look.

Plain CSS. No build step, no dependencies, no preprocessor, no JS in the kit. Files are
usable by `<link>` alone, and the demo is served by GitHub Pages from the repo root.

## Layout

```
core.css         tokens + components, light and dark — stands alone
tint.css         opt-in layer: colour from content
index.html       living demo, also the GitHub Pages site
STYLE-GUIDE.md   the written guideline
tools/check.py   validator, stdlib only
docs/design.md   design rationale — SOURCE OF TRUTH for every value
```

## The two-tier rule

`core.css` must render a complete, coherent page **on its own**. `tint.css` recolours
components from four inputs, consumes core's tokens, defines none of its own, and styles
only classes `core.css` already styles. Deleting `tint.css` must never leave anything
unstyled: without it, media cards rotate through the six pastels and accented parts are
purple. The validator enforces both halves.

If you find yourself adding a colour or a new component to `tint.css`, it belongs in
`core.css`.

## Scheme

Light is `:root, [data-scheme="light"]` and the default for everyone. Dark is
`[data-scheme="dark"]`, a full second set of tokens. Either goes on `<html>` or on any
wrapper, so panels can nest in both directions. Nothing follows the device by itself;
the guide gives the six-line script for pages that want to. Every `data-scheme` value in
the repo must be `light` or `dark`; the validator checks, because a typo renders as
light in silence.

## The tint contract

An element with `.tint` reads four inputs set inline: `--h` (hue), `--c` (surface
chroma), `--blob-c`, `--accent-c`. `.tint` carries the hue: only a card, a media card
or a chip paints its own surface with it; the parts inside any `.tint` element (blob,
meter, pill, dot, progress, primary button) take it. The scheme owns lightness (`--tint-l`,
`--tint-blob-l`, `--tint-accent-l`) and ink (`--tint-ink`), and dark inverts the ramp.
The defaults at `:root` are "stone", a warm near-grey. `tint.css` may only write
`oklch()` whose channels are tokens or `calc()` of tokens; a literal channel is a bug.

## Extracted vs designed

Every component is one or the other, marked in `STYLE-GUIDE.md` and on each entry in
the demo:

- **extracted**: lifted from the source app, proven in production.
- **designed**: added for this kit because the source never needed it. Four so far:
  textarea, the danger button, `.grid`, `dialog`.

Keep the tags accurate when adding components.

## The six rules for new components

Anything added must be buildable from these. If it can't be, the kit is being stretched
past what it is; say so rather than inventing new primitives.

1. Surfaces are `--surface` on the `--bg` ground and carry no border. Lines are for
   table rules, input borders and the steps rule only, always `--line`.
2. Radius comes off the ladder by role, never an arbitrary value. Anything small and
   interactive is a pill. The validator rejects a literal radius.
3. Colour is `--accent` or one of the six pastels, never a new hue. Colour from data
   goes through `tint.css`.
4. States read their state token (`--good-soft`, `--warn-soft`, `--bad-soft`,
   `--accent-soft`) even where a pastel looks identical in light mode; in dark mode
   the pairs differ.
5. Display type (Fredoka 600) is for headings, the brand, values and card titles only;
   everything else is Figtree, and weight carries hierarchy.
6. Interactive things are 44px tall, focus is a 3px `--accent` outline offset 2px,
   press scales the icon, and every transition takes its duration from `--t-fast` or
   `--t-base`. Reduced motion zeroes those tokens; the validator rejects a literal
   duration, and `!important` is forbidden.

## Verifying

```bash
python3 tools/check.py
```

Then open `index.html` in a browser, and once more with `data-scheme="dark"` on
`<html>`, and once with `tint.css` disabled (the demo has buttons for both). There is no
test runner and no CI; the validator plus the demo is the whole verification story. The
demo's assembled page at the bottom is built only from kit classes; if it ever needs
bespoke CSS, that's a missing component, and the fix goes in `core.css`, not the demo.

No local browser? Render headlessly (Chrome `--headless=new --screenshot`) at 1280px and
390px and inspect the images rather than assuming.

## Conventions

- `docs/design.md` holds every value. Change it there first, then the CSS.
- This repo is public. No hostnames, IPs, container names, or private infrastructure
  details in any file, including commit messages.
- The demo's content is not about music; keep it that way. The kit is general-purpose
  and its provenance is stated once, generically.
- Commit tightly scoped changes; stage by path.
