# peach-sorbet — a portable style guideline

**Date:** 2026-09-30
**Status:** implemented

> This document is the source of truth for every value in the kit. Change a colour, a
> radius or a size here first, then in `core.css`. Where the prose here disagrees with
> the built code, **[STYLE-GUIDE.md](../STYLE-GUIDE.md) is authoritative.**

## Purpose

Extract the visual system of a self-hosted music recommender's web app into a
standalone, publicly shareable, **general-purpose** CSS kit: tokens, components, a
written guideline, a living demo. It is the second kit in a series; the first,
kawaii-meadow, came from a status page. Same shape — two files, no build step, a
validator, a demo served from the repo root — different look.

The look: a peach ground, white and pastel cards with no borders, blob-shaped covers,
one purple accent, Fredoka for display and Figtree for text, and a way of colouring a
card from its content. The source app used that to tint each recommendation from its
album art; the kit generalises it to "any hue, from anywhere".

The goal is **portable but not prescriptive**. Nothing in the source app has to adopt
it back. It should be *droppable*: link `core.css` and a new page is substantially
styled with no hand-written CSS.

It is explicitly **not** a framework: no grid system, no utility classes, no JavaScript
in the kit. Three behaviours need a few lines of script on the page (a measured
marquee, a row that folds open, a dialog); the guide gives them.

## Deliverable

```
README.md        what it is, quickstart, link to the live demo
LICENSE          MIT
CLAUDE.md        orientation for future sessions opened in this repo
STYLE-GUIDE.md   the full guideline
core.css         tokens and components, light and dark
tint.css         the optional layer: colour from content
index.html       living demo, served by GitHub Pages
tools/check.py   validator, standard library only
docs/design.md   this document
```

**Out of scope:** no changes to the source app. No conformance section; nothing is
obliged to adopt this.

## Source analysis

The source stylesheet is about 600 lines with 30 custom properties already declared at
`:root` and redefined for dark mode, so unlike its sibling kit the colours were named
from the start. What the source did *not* name: its radius ladder (eleven distinct
values), its type scale (sixteen sizes, all literals), its two transition durations,
or the boundaries between components, since most rules are page-specific
(recommendation cards, a clip player, artist tags, an activity log). Naming those, and
renaming the music out of the class names, is most of the work.

Three patterns carry the design:

1. **A peach ground, white surfaces, no borders.** Cards, bars and chips separate from
   the page by colour alone. The only lines in the app are table rules, input borders
   and one rule beside a list of steps.
2. **Six pastels on rotation, one accent.** Tiles rotate through four pastels by
   position; the original design mockup rotated cards through all six. A single purple
   is the only saturated colour, used for links, the primary button, the active tab and
   the focus ring.
3. **Colour from content.** A recommendation card takes its hue and chroma from its
   cover in OKLCH; the stylesheet sets the lightness, one value per scheme, so the same
   numbers read correctly in light and dark. A nearly grey cover falls back to the hue
   of the artist's category, and an artist with no category gets a warm stone.

Dark mode is a second full set of tokens on `[data-scheme="dark"]`, and it is opt-in:
light is the default for everyone, and following the device is a choice the user makes.
That decision is kept.

## Two tiers

### Tier 1: `core.css`

Tokens and every component, in both schemes. Renders a complete, coherent page by
itself. Without `tint.css`, media cards rotate through the six pastels, blobs are
lavender, meters and dots are purple.

### Tier 2: `tint.css`

Colour from content. Put `.tint` on an element and four numbers inline. A card, a
media card or a chip paints its own surface with the hue; any element with `.tint`
passes it to its blob, meter, pill, dot, progress bar and primary button. It defines
no tokens and styles no class `core.css` does not already style, so deleting it leaves
nothing unstyled; the validator enforces both.

## Tokens

### Ground, ink, accent, states

| Token | Light | Dark | Used by |
| --- | --- | --- | --- |
| `--bg` | `#fff4ec` | `#1b1624` | the page, code, meters' empty part |
| `--surface` | `#ffffff` | `#262033` | cards, bars, chips, inputs, the info panel on a card |
| `--text` | `#2d2640` | `#f3eefc` | body ink |
| `--muted` | `#5b5068` | `#b9aecb` | secondary ink, table headers, ledes |
| `--line` | `#eadde3` | `#3a3248` | table rules, input borders, the steps' left rule |
| `--button` | `#ffffff` | `#3a3248` | the round icon buttons on a card |
| `--accent` | `#6c4ce0` | `#b7a5ff` | links, primary button, active tab, focus ring |
| `--accent-ink` | `#ffffff` | `#1b1624` | ink on the accent |
| `--accent-soft` | `#e7e0ff` | `#342a55` | secondary button, badges, hover fills |
| `--warn` | `#8a5300` | `#f2c35b` | warning ink |
| `--warn-soft` | `#fff1b8` | `#3a3020` | warning badge |
| `--bad` | `#b3261e` | `#ff9aa8` | error ink |
| `--bad-soft` | `#ffd6e0` | `#43222f` | error card and badge |
| `--good-soft` | `#d7f5e7` | `#1f3a31` | done badge, added chip |
| `--chart-1` | `#6c4ce0` | `#b7a5ff` | main chart series |
| `--chart-2` | `#ffb3c6` | `#6b4a66` | second chart series |
| `--shadow` | `0 6px 20px rgba(45, 38, 64, 0.12)` | `0 6px 20px rgba(0, 0, 0, 0.45)` | the floating bars |
| `--scrim` | `rgba(45, 38, 64, 0.40)` | `rgba(0, 0, 0, 0.60)` | dialog backdrop (derived) |

There is no `--good` ink. The source never needed one: a done badge is `--text` on
`--good-soft`, and the kit keeps that rather than inventing a green.

### The six pastels

| Token | Light | Dark |
| --- | --- | --- |
| `--lavender` | `#e7e0ff` | `#2f2848` |
| `--mint` | `#d7f5e7` | `#1f3a31` |
| `--butter` | `#fff1b8` | `#3a3420` |
| `--pink` | `#ffd6e0` | `#40263a` |
| `--blue` | `#dbeafe` | `#22304a` |
| `--peach` | `#ffe4cc` | `#3d2c22` |

**The trap.** In light mode `--accent-soft` equals `--lavender`, `--good-soft` equals
`--mint`, `--warn-soft` equals `--butter` and `--bad-soft` equals `--pink`. In dark mode
all four pairs differ (`#342a55` against `#2f2848`, `#3a3020` against `#3a3420`,
`#43222f` against `#40263a`). A component that reads a pastel where it means a state
looks right in light and subtly wrong in dark, and nothing fails. Read the state token.

### Tint layer

| Token | Light | Dark | Meaning |
| --- | --- | --- | --- |
| `--tint-l` | `93%` | `29%` | lightness of a tinted surface |
| `--tint-blob-l` | `80%` | `44%` | lightness of the blob |
| `--tint-accent-l` | `52%` | `82%` | lightness of the primary button, meter, dot, ring |
| `--tint-ink` | `#ffffff` | `#1b1624` | ink on the primary button |

And the four **inputs**, defaulting at `:root` to "stone", a warm near-grey:

| Input | Default | Meaning |
| --- | --- | --- |
| `--h` | `70` | hue, degrees |
| `--c` | `0.012` | chroma of the surface |
| `--blob-c` | `0.015` | chroma of the blob |
| `--accent-c` | `0.02` | chroma of the button, meter, dot and ring |

The scheme owns lightness; the element brings hue and chroma. Dark **inverts the
ramp**: a deep card, a mid-tone blob, a pale button with dark ink. That is why the
inputs are chroma only. The source let a category nudge blob and button lightness by up
to three percent; the kit drops that, so one theme value applies to every tint.

### Two recipes for the inputs

**From an image** (the source's cover reader). Shrink the image to 64 pixels square,
cut it to eight colours, and score each by how much of the image it covers times its
chroma to the 1.2, with near-white and near-black (lightness outside 0.25 to 0.92)
counting for a fifth. Take the winner's hue and chroma, then:

```
if chroma < 0.03:  stone (the defaults above)
else:              --h = hue;  --c = 0.045
                   --blob-c   = clamp(chroma, 0.05, 0.10)
                   --accent-c = clamp(chroma × 1.15, 0.07, 0.15)
```

A dull picture gives a quiet card; a vivid one a stronger blob and button; the card
itself stays pastel. The demo ships a browser port.

**From a category.** Spread the categories around the wheel and tune chroma by hand.
The source app's twelve, for reference; the names are its own, the numbers are what
matter:

| Category | `--h` | `--c` | `--blob-c` | `--accent-c` |
| --- | --- | --- | --- | --- |
| rock | 20 | 0.045 | 0.10 | 0.15 |
| hip-hop | 55 | 0.045 | 0.10 | 0.14 |
| R&B | 78 | 0.045 | 0.10 | 0.11 |
| pop | 100 | 0.05 | 0.11 | 0.10 |
| folk | 155 | 0.045 | 0.09 | 0.11 |
| indie | 185 | 0.045 | 0.08 | 0.09 |
| Persian | 208 | 0.045 | 0.09 | 0.10 |
| lo-fi | 232 | 0.04 | 0.08 | 0.10 |
| electronic | 255 | 0.045 | 0.09 | 0.13 |
| synth | 285 | 0.04 | 0.09 | 0.14 |
| J-pop | 315 | 0.045 | 0.10 | 0.15 |
| K-pop | 350 | 0.045 | 0.10 | 0.15 |
| *(none)* | 70 | 0.012 | 0.015 | 0.02 |

Chroma varies with hue on purpose: yellows and greens (100, 155, 185) look garish at the
chroma that pinks and purples need, so their buttons sit at 0.09 to 0.11 where K-pop's
sits at 0.15.

## Type

Two families. **Fredoka** at weight 600 for display: headings, the brand, tile values,
media card titles. **Figtree** for everything else, at 400 for body, 500 for check
labels, 600 for labels, chips and meta, 650 for a name in a table, 700 for buttons,
badges, titles and action labels.

Both are loaded from Google Fonts in the quickstart; both are under the SIL Open Font
Licence, so self-hosting two `woff2` files each (as the source app does) is fine.

| Token | Size | Used by |
| --- | --- | --- |
| `--fs-h1` | 2.1rem | page heading |
| `--fs-value` | 1.9rem | the number on a tile |
| `--fs-brand` | 1.5rem | the brand in the sidebar |
| `--fs-h2` | 1.35rem | section heading, the brand in the phone header |
| `--fs-title` | 1.3rem | media card title, card-head heading |
| `--fs-h3` | 1.1rem | h3, lede, avatar initial, the chip's × |
| `--fs-row-title` | 1.05rem | media row title |
| `--fs-base` | 1rem | body, sidebar tabs |
| `--fs-table` | 0.95rem | tables, facts |
| `--fs-ui` | 0.925rem | chips, labels, segmented control, the info panel |
| `--fs-note` | 0.9rem | tile labels, the divider, bars on a phone |
| `--fs-small` | 0.875rem | `.small`, notes, steps, the small button |
| `--fs-meta` | 0.85rem | tags line, dock link, facts' terms, `pre` |
| `--fs-label` | 0.8rem | table headers, eyebrows, row numbers |
| `--fs-tiny` | 0.75rem | badges, action labels, pills |
| `--fs-tab` | 0.72rem | phone tab bar labels |

Sixteen rungs is more than a kit designed from scratch would have. They are what the
source uses, and folding them would move the look; two sizes were folded (see
Deviations) because they were within a tenth of a rem of a neighbour.

## Radius ladder

| Token | Value | Used by |
| --- | --- | --- |
| `--r-pill` | 999px | buttons, chips, tabs, badges, meters, nav tabs |
| `--r-bar` | 32px | the floating bars: phone tab bar, dock, search bar |
| `--r-feature` | 28px | media cards, the sidebar |
| `--r-card` | 24px | cards, tiles, gallery items, strips, dialogs |
| `--r-row` | 20px | media rows, entries |
| `--r-control` | 16px | inputs, the info panel on a card, gallery covers, `pre` |
| `--r-tight` | 12px | action buttons' focus box, the note over a row |
| `--r-hair` | 6px | inline code |

Circles are `50%`. The blob is seven percentage quads, rotating by position in a grid
so neighbours never share a silhouette, on media cards and on cards with a card-head:

| # | Corners | In the mockups | In the source app |
| --- | --- | --- | --- |
| 1 | `42% 58% 55% 45%` | yes | yes |
| 2 | `55% 45% 50% 50%` | yes | yes |
| 3 | `50% 50% 45% 55%` | yes | yes |
| 4 | `45% 55% 58% 42%` | yes | yes |
| 5 | `55% 45% 42% 58%` | yes | no |
| 6 | `48% 52% 55% 45%` | yes | no |
| 7 | `45% 55% 50% 50%` | yes | no |

The design mockups used all seven across their four boards; the app kept the first
four. The kit carries the full set, since it is the record of the design rather than
of one build of it (see Deviations).

## Spacing

Pixels on a four-pixel grid, no tokens: 4, 6, 8, 10, 12, 14, 16, 18, 20, 32, 36, 48.
The source has no spacing scale and tokenising one would have meant re-deriving every
padding; the kit states the grid instead and leaves the literals.

## Motion

| Token | Value | Used by |
| --- | --- | --- |
| `--t-fast` | 0.1s | the icon's press and hover scale |
| `--t-base` | 0.2s | a card dimming or gaining its ring |
| `--glide-duration` | 8s | the marquee, set per line by the script |
| `--glide-shift` | 0px | the marquee, set per line by the script |

`prefers-reduced-motion` sets both `--t-*` tokens to `0s` at `:root`. The source did
this with `* { transition: none !important }`; the kit forbids `!important`, so every
transition takes its duration from a token, and the validator checks that no literal
duration exists.

**The marquee keeps gliding under Reduce Motion, by decision.** A line that does not
fit is unreadable if it does not move, and the source's owner, who has Reduce Motion
on, asked for the glide. It runs slower there (12 px/s against 25) with longer rests
at each end. The kit carries that decision and documents it rather than second-guessing
it.

Press feedback: the round icon scales to 0.96 on press and 1.06 on hover; pill buttons
brighten by 6%.

## Layout and breakpoints

The shell is a sidebar on wide screens and a floating tab bar on phones, from one
`<nav>`. `.shell` on `<body>` makes the grid at 900px; below it the nav is fixed to the
bottom, the phone header shows, and the main column gets 120px of bottom padding to
clear the bar.

| Width | What changes |
| --- | --- |
| ≥ 900px | sidebar; media rows go single-line; dock docks bottom-right |
| ≥ 640px | tiles four across; facts two columns |
| ≤ 480px | bars narrow their name column; the dock's link hides |
| ≤ 420px | media cards shrink their blob to 64px and their icons to 42px |

## Component set

Two provenances, marked in the guide and on every entry in the demo.

**Extracted, proven in the source app.** Shell (main, top, brand, avatar, skip link),
nav and nav tabs, headings, lede, muted, small, eyebrow, code and pre, card and its four
tints, solo card, cards list, section head, divider, card head with a blob, strip, tiles,
chips and tag chips, tabs with tint dots, segmented control, badge in four states,
buttons (accent, secondary, link, small), inputs, select, checkbox, radio, choices,
stacked form, search bar with modes, action buttons, table, facts, schedule, bars,
progress, list, lines, dot, blob, media card, media list and rows, marquee, dock,
entries with steps, gallery, visually-hidden.

**Designed, added here.** Textarea, the danger button, the `.grid` helper, and the
native dialog dressed as a card. Four items; the source page was a whole app, so it had
already needed most of what a kit wants.

**Rules the designed components follow**, so they read as native:

1. Surfaces are `--surface` on the `--bg` ground and carry no border. Lines are for
   table rules, input borders and the steps rule only, always `--line`.
2. Radius comes off the ladder by role. Anything small and interactive is a pill.
3. Colour is the accent or one of the six pastels, never a new hue. Colour from data
   goes through `tint.css`.
4. States read their own tokens even where a pastel would look the same in light.
5. Display type is Fredoka 600 for headings, the brand, values and titles only; the
   rest is Figtree, and weight carries hierarchy.
6. Interactive things are 44px tall on touch, focus is a 3px `--accent` outline offset
   2px (or `--text` on a tinted part), press scales the icon, and every transition
   uses a `--t-*` token.

### Renamed for portability

| Source | Kit |
| --- | --- |
| `body.signed-in` | `.shell` |
| `main` | `.main` |
| `.nav a.tab` | `.nav-tab` |
| `.nav-settings` | `.nav-tab.wide` |
| `.login` | `.card.solo` |
| `.playlist-line` | `.strip` |
| `.view-toggle` | `.segmented` |
| `.badge.state-done` / `.state-warning` / `.state-failed` | `.badge.ok` / `.warn` / `.bad` |
| `.entry.state-running` / `.state-warning` / `.state-failed` | `.entry.busy` / `.warn` / `.bad` |
| `.steps .level-warning` / `.level-error` | `.steps .warn` / `.bad` |
| `h3.day` | `.eyebrow` |
| `.track-name` | `.name` |
| `.recent-searches` | `.list` |
| `.artist-hit` | `.lines` |
| `.edits` | `.cards` |
| `.genre-head` | `.card-head` |
| `.genre-dot` | `.dot.mini` |
| `.genre-bars` / `.genre-name` | `.bars` / `.bar-name` |
| `.genre-pill` | `.pill` |
| `.genre-chip.tint` | `.chip.tint` |
| `.recs` / `.recs.list` | `.media-grid` / `.media-list` |
| `.rec` / `.rec.row` | `.media` / `.media.row` |
| `.rec-body` / `.rec-info` / `.rec-actions` | `.media-body` / `.media-info` / `.media-actions` |
| `.artists` / `.open-spotify` | `.subtitle` / `.media-link` |
| `.genres` (line) / `.card-note` | `.tags` / `.note` |
| `.row-genres` / `.row-genres-inline` | `.row-tags` / `.row-tags-inline` |
| `.act.play` | `.act.primary` |
| `.rec.playing` | `.media.selected` |
| `.player-bar` / `.now` | `.dock` / `.dock-body` |
| `.np-button` / `.np-next` | `.dock-button.primary` / `.dock-button.soft` |
| `.np-progress` | `.progress` |
| `#np-spotify` | `.dock-link` |
| `.playlists` / `.playlist` / `.playlist-cover` / `.playlist-body` / `.playlist-name` | `.gallery` / `.gallery-item` / `.gallery-cover` / `.gallery-body` / `.gallery-name` |
| `--card-l` / `--card-ink` / `--card-blob-l` / `--card-accent-l` | `--tint-l` / `--tint-ink` / `--tint-blob-l` / `--tint-accent-l` |
| `--card-c` | `--c` |
| `--duration` / `--shift` | `--glide-duration` / `--glide-shift` |

### Where the kit deviates

Faithful everywhere except these, each a deliberate call:

1. **Radii are tokens.** The source's player bar was 34px; the kit's dock is
   `--r-bar` (32px), two pixels off, so the three floating bars share one rung.
   Nav tabs were 26px and 24px on boxes 52px and 48px tall, which is a pill either way;
   they are `--r-pill`. Meters were 7px and 3px on 14px and 6px bars: pills again.
2. **Two type sizes folded.** The card-head heading was 1.25rem and is `--fs-title`
   (1.3rem). The gallery cover is `--r-control`. Everything else is the source's size.
3. **Tint lightness is the scheme's alone.** The source let each category nudge blob
   and button lightness by up to 3%; the kit reads one value per scheme.
4. **Reduced motion through tokens**, not `!important` (see Motion).
5. **`.media` rotates through the six pastels without `tint.css`.** The source always
   tinted, so it had no untinted card. The rotation is the original mockup's, and it
   gives `core.css` a coherent card on its own.
6. **The media row's external-link action is not carried over.** It was specific to
   the source's provider; a row's actions are plain `.act` buttons.
7. **`--scrim` is derived.** The source has no dialog.
9. **Seven blob silhouettes, not four.** The design mockups had seven; the app shipped
   four of them. The kit restores the three the app dropped and rotates through all
   seven. The app can adopt the same set when it is next touched.
8. **`[data-scheme]` works on any wrapper**, not only `:root`, and in both directions:
   the light tokens are declared for `:root, [data-scheme="light"]`, so a light panel
   can sit on a dark page as well as the reverse. The source only ever set it on
   `<html>`.

## Living demo

Self-contained, served by GitHub Pages from the repo root. It is the kit's own shell,
so the sidebar and tab bar are demonstrated by the page itself. It shows every token
in both schemes as a swatch pair read off the stylesheet, the radius ladder, the type
scale, every component in every state with its provenance tag, the tint layer with a
hue slider, twelve hues around the wheel and an image-to-hue reader, a switch between
light, dark and "match my device", a switch that disables `tint.css` to prove the
fallback, and an assembled page built from kit classes only.

## Accessibility

Measured, WCAG 2 contrast, in both schemes:

| Pair | Light | Dark |
| --- | --- | --- |
| `--text` on `--bg` | 13.3:1 | 15.5:1 |
| `--text` on `--surface` | 14.4:1 | 13.8:1 |
| `--text` on the six pastels | 10.9 to 12.7:1 | 10.8 to 12.2:1 |
| `--muted` on `--surface` | 7.5:1 | 7.5:1 |
| `--muted` on the six pastels | 5.7 to 6.6:1 | 5.8 to 6.6:1 |
| `--accent` on `--surface` (a link) | 5.6:1 | 7.4:1 |
| `--accent-ink` on `--accent` (a button) | 5.6:1 | 8.3:1 |
| `--warn` on `--warn-soft` | 5.6:1 | 7.5:1 |
| `--bad` on `--bad-soft` | 5.0:1 | 6.9:1 |
| `--text` on a tinted card, any hue | 11.3 to 11.9:1 | 12.2 to 12.6:1 |
| `--muted` on a tinted card, any hue | 5.9 to 6.2:1 | 6.6 to 6.8:1 |
| `--tint-ink` on a tinted button, any hue | 4.8 to 6.0:1 | 9.1 to 10.7:1 |

Every pair clears AA. **One does not:** `--accent` on `--accent-soft`, a link inside a
lavender notice card, is **4.4:1** in light mode (6.1:1 in dark). It is kept because
the notice card is the source's look and the link is still underlined; if the link
carries the only way forward, put it on a plain card instead.

The tinted button's white ink is the tightest pass, at 4.8:1 around hue 185 to 208
(teal), where a 52% lightness button is at its brightest. Every other hue is above 5:1.

Everything is keyboard-reachable: real buttons, real inputs, real links, a skip link,
`aria-current` on the active tab, `aria-pressed` on toggles, `aria-expanded` on the
row's chevron, and a focus ring on everything.

## Public-repo hygiene

- No hostnames, IPs, container names or private details in any file, including commit
  messages.
- Provenance stated generically: extracted from a self-hosted music recommender's web
  app. The demo's content is written fresh and is not about music.
- Fonts loaded from Google Fonts in the quickstart; both are OFL, so self-hosting is
  allowed and the guide shows the `@font-face` for it.

## Verification

- `python3 tools/check.py` passes: every `var()` resolves, no raw colour outside the
  token blocks, `tint.css` defines no tokens and touches only core classes, no
  `!important`, every radius is on the ladder, every duration is a token, every
  `data-scheme` value exists.
- Feed the validator a deliberately broken copy and confirm every rule fires. Done
  before the first commit: ten planted faults, ten reports.
- Render `index.html` headlessly at 1280px and 390px, light and dark, and look.
- Disable `tint.css` and confirm nothing is unstyled.
- The assembled page at the bottom of the demo needs no bespoke CSS. If it ever does,
  that is a missing component and the fix goes in `core.css`.
