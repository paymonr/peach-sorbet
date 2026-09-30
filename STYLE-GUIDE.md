# Style guide

A small CSS kit with a soft look: a peach ground, white and pastel cards with no
borders, blob-shaped covers, one purple accent, and an optional layer that colours a
card from its content.

Two files, no build step, no dependencies.

- **`core.css`**: tokens and components, light and dark. Stands alone.
- **`tint.css`**: colour from content. Optional, deletable, breaks nothing.

---

## Quickstart

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
    <p>Nothing yet. <a href="/discover">Get your first batch</a>.</p>
  </div>
</main>
```

That is the whole install. Load the fonts: Fredoka is the display face and Figtree the
text face, and the kit falls back to `system-ui` but stops looking like itself.

To self-host instead, both fonts are under the SIL Open Font Licence. Two `woff2` files
each (latin and latin-ext) and this, before `core.css`:

```css
@font-face { font-family: Fredoka; font-weight: 300 700; font-display: swap; src: url(fonts/fredoka-latin.woff2) format("woff2"); }
@font-face { font-family: Figtree; font-weight: 300 900; font-display: swap; src: url(fonts/figtree-latin.woff2) format("woff2"); }
```

---

## Tiers

`core.css` renders a complete page by itself: without `tint.css`, media cards rotate
through the six pastels, blobs are lavender, and meters, dots and primary buttons are
purple.

`tint.css` recolours those parts from four numbers on the element. It consumes core's
tokens and defines none of its own, and it styles only classes core already styles. If
you find yourself adding a colour or a component to it, that belongs in `core.css`.

---

## Scheme

Light is the default for everyone. Dark is an attribute:

```html
<html data-scheme="dark">
```

The attribute works on any wrapper, in either direction: a dark panel can sit on a
light page, and `data-scheme="light"` puts a light panel on a dark one. Nothing
follows the device by itself; that is a choice the page makes, with six lines:

```html
<script>
  const root = document.documentElement, dark = matchMedia("(prefers-color-scheme: dark)");
  const apply = () => { root.dataset.scheme = dark.matches ? "dark" : "light"; };
  apply(); dark.addEventListener("change", apply);
</script>
```

Set `<meta name="theme-color">` to `#fff4ec` for light and `#1b1624` for dark so the
browser chrome matches the ground.

---

## Tokens

Every colour in the kit, light and dark. Components read these and nothing else.

| Token | Light | Dark | Used by |
| --- | --- | --- | --- |
| `--bg` | `#fff4ec` | `#1b1624` | the page, code, the empty part of a meter |
| `--surface` | `#ffffff` | `#262033` | cards, bars, chips, inputs, the info panel on a card |
| `--text` | `#2d2640` | `#f3eefc` | body ink |
| `--muted` | `#5b5068` | `#b9aecb` | secondary ink |
| `--line` | `#eadde3` | `#3a3248` | table rules, input borders, the steps' rule |
| `--button` | `#ffffff` | `#3a3248` | round icon buttons on a card |
| `--accent` | `#6c4ce0` | `#b7a5ff` | links, primary button, active tab, focus |
| `--accent-ink` | `#ffffff` | `#1b1624` | ink on the accent |
| `--accent-soft` | `#e7e0ff` | `#342a55` | secondary button, badges, hover fills |
| `--warn` / `--warn-soft` | `#8a5300` / `#fff1b8` | `#f2c35b` / `#3a3020` | warning ink and badge |
| `--bad` / `--bad-soft` | `#b3261e` / `#ffd6e0` | `#ff9aa8` / `#43222f` | error ink, card and badge |
| `--good-soft` | `#d7f5e7` | `#1f3a31` | done badge, added chip |
| `--chart-1` / `--chart-2` | `#6c4ce0` / `#ffb3c6` | `#b7a5ff` / `#6b4a66` | chart series |
| `--shadow` | `0 6px 20px rgba(45,38,64,.12)` | `0 6px 20px rgba(0,0,0,.45)` | the floating bars |
| `--scrim` | `rgba(45,38,64,.40)` | `rgba(0,0,0,.60)` | dialog backdrop |

### The six pastels

| Token | Light | Dark |
| --- | --- | --- |
| `--lavender` | `#e7e0ff` | `#2f2848` |
| `--mint` | `#d7f5e7` | `#1f3a31` |
| `--butter` | `#fff1b8` | `#3a3420` |
| `--pink` | `#ffd6e0` | `#40263a` |
| `--blue` | `#dbeafe` | `#22304a` |
| `--peach` | `#ffe4cc` | `#3d2c22` |

Tiles rotate through the first four by position; media cards through all six. The
avatar and an empty gallery cover are lavender; the "who" pill in an entry is peach.

> **The trap.** In light mode four state tints equal a pastel: `--accent-soft` is
> `--lavender`, `--good-soft` is `--mint`, `--warn-soft` is `--butter`, `--bad-soft` is
> `--pink`. In dark mode every pair differs. A badge built on `--mint` looks right in
> light and slightly off in dark, and nothing errors. A state reads its state token.

### Charts

`--chart-1` and `--chart-2` exist so a chart library can read them with
`getComputedStyle` and follow the scheme. Axis ink is `--muted`, grid lines `--line`.

---

## Tint: colour from content

Put `.tint` on an element and give it four numbers inline:

```html
<article class="media tint" style="--h: 340; --c: .045; --blob-c: .10; --accent-c: .14">
```

`.tint` carries the hue. A card, a media card or a chip paints its own surface with
it; any element with `.tint` passes it to the parts inside: `.blob`, the `.bar` meter,
`.pill`, `.dot`, `.progress`, and the `.act.primary` or `.dock-button.primary` button.
`.tint.selected` draws the ring in the same accent. A bar's `li` or the dock carries
`.tint` without changing its own background, which is what the source does. The scheme
owns lightness and ink:

| Token | Light | Dark |
| --- | --- | --- |
| `--tint-l` (surface) | 93% | 29% |
| `--tint-blob-l` | 80% | 44% |
| `--tint-accent-l` (button, meter, dot, ring) | 52% | 82% |
| `--tint-ink` | `#ffffff` | `#1b1624` |

Dark inverts the ramp: deep card, mid blob, pale button with dark ink. That is why the
inputs are chroma only. Leave them out and an element is **stone**: `--h: 70`,
`--c: .012`, `--blob-c: .015`, `--accent-c: .02`, a warm near-grey for anything with no
colour of its own.

Small parts can carry `.tint` themselves when the parent should not: a `.tab-dot.tint`
inside a tab, a `.dot.mini.tint` beside a name, a `.chip.tint`.

### Where the four numbers come from

**From an image.** Shrink it, cut it to a few colours, score each by coverage × chroma
to the 1.2 with near-white and near-black counting for a fifth, take the winner, then:
if chroma is under 0.03 the picture is grey, so use stone; otherwise `--c` is 0.045,
`--blob-c` is the chroma clamped to 0.05–0.10, and `--accent-c` is 1.15 × chroma
clamped to 0.07–0.15. The demo has a browser port; the source app does it server-side
in Python with Pillow.

**From a category.** Spread your categories around the wheel and tune chroma by hand.
Yellows and greens (hues 100–185) want a quieter button (0.09–0.11) than pinks and
purples (0.14–0.15). `docs/design.md` has the source's twelve as a worked example.

---

## Radius ladder

Pick by the role of the box, never an arbitrary value. Anything small and interactive is
a pill.

| Token | Value | Used by |
| --- | --- | --- |
| `--r-pill` | 999px | buttons, chips, tabs, badges, meters, nav tabs |
| `--r-bar` | 32px | phone tab bar, dock, search bar |
| `--r-feature` | 28px | media cards, the sidebar |
| `--r-card` | 24px | cards, tiles, gallery items, strips, dialogs |
| `--r-row` | 20px | media rows, entries |
| `--r-control` | 16px | inputs, the info panel, gallery covers, `pre` |
| `--r-tight` | 12px | an action's focus box, the note over a row |
| `--r-hair` | 6px | inline code |

Circles are `50%`. The blob is seven percentage quads that rotate with position in a
grid, so two neighbours never share a silhouette: `42% 58% 55% 45%`, `55% 45% 50% 50%`,
`50% 50% 45% 55%`, `45% 55% 58% 42%`, `55% 45% 42% 58%`, `48% 52% 55% 45%`,
`45% 55% 50% 50%`.

---

## Type

Fredoka at weight 600 for display: `h1`–`h3`, `.brand`, `.tile .value`, `.media .title`
and `.card-head h2`. Figtree for everything else; weight carries hierarchy, not size.

| Token | Size | Used by |
| --- | --- | --- |
| `--fs-h1` | 2.1rem | page heading |
| `--fs-value` | 1.9rem | tile value |
| `--fs-brand` | 1.5rem | brand in the sidebar |
| `--fs-h2` | 1.35rem | section heading, brand on a phone |
| `--fs-title` | 1.3rem | media card title, card-head heading |
| `--fs-h3` | 1.1rem | h3, lede, avatar |
| `--fs-row-title` | 1.05rem | media row title |
| `--fs-base` | 1rem | body |
| `--fs-table` | .95rem | tables, facts |
| `--fs-ui` | .925rem | chips, labels, segmented control, info panel |
| `--fs-note` | .9rem | tile label, divider |
| `--fs-small` | .875rem | `.small`, notes, steps |
| `--fs-meta` | .85rem | tags line, dock link, `pre` |
| `--fs-label` | .8rem | table headers, `.eyebrow` |
| `--fs-tiny` | .75rem | badges, action labels, pills |
| `--fs-tab` | .72rem | phone tab labels |

The **eyebrow** is the one uppercase style: `.8rem`, weight 700, `.05em` tracking, in
`--muted`. Use it for a day in a timeline or a heading over a sub-list.

---

## Spacing, motion, focus

- Spacing is pixels on a four-pixel grid. There is no spacing scale; the values are
  4, 6, 8, 10, 12, 14, 16, 18, 20, 32, 36, 48.
- Cards have no borders. The only lines are table rules (1px), input borders (2px) and
  the rule beside a list of steps (2px), always in `--line`.
- Motion: `--t-fast` (.1s) for the icon's press and hover scale, `--t-base` (.2s) for a
  card dimming or gaining its ring. `prefers-reduced-motion` sets both to `0s`, which is
  why no transition may carry a literal duration.
- The marquee keeps gliding under Reduce Motion, on purpose: a line that does not fit
  is unreadable still. It runs slower there. See Scripts below.
- Focus is a 3px `--accent` outline, offset 2px, on everything; an action's round icon
  uses `--text` instead, since it sits on a tinted card.
- Touch targets: buttons are 44px tall, inputs 48px, the round icon 46px.

---

## Components

Every component is **extracted** (from the source app, proven in production) or
**designed** (added here). The demo carries the same tags.

### Shell · extracted

```html
<body class="shell">
  <a class="skip" href="#main">Skip to content</a>
  <header class="top"><a class="brand" href="/">brand</a><a class="avatar" href="/settings">S</a></header>
  <nav class="nav" aria-label="Main">
    <a class="brand" href="/">brand</a>
    <a class="nav-tab" href="/" aria-current="page"><svg …></svg><span>Home</span></a>
    <a class="nav-tab" href="/discover"><svg …></svg><span>Discover</span></a>
    <a class="nav-tab wide" href="/settings"><svg …></svg><span>Settings</span></a>
    <div class="nav-foot"><button class="link">Sign out</button></div>
  </nav>
  <main class="main" id="main">…</main>
</body>
```

One nav, two shapes. Below 900px it is a floating tab bar at the bottom with icon over
label, and the `.top` header shows the brand and avatar; `.wide` tabs and `.nav-foot`
hide. From 900px `.shell` becomes a two-column grid, the nav is a sticky sidebar, and
`.top` hides. `.main` alone (without `.shell`) is a centred column, for a sign-in page.

### Text · extracted

`h1` `h2` `h3` `.lede` `.muted` `.small` `.name` `.eyebrow` `.error` `.warn-text`
`code` `pre` `.visually-hidden`. Headings are Fredoka. `.lede` sits under an `h1` with a
negative top margin.

### Cards · extracted

| Class | Notes |
| --- | --- |
| `.card` | White, 24px radius, 20px padding. First child loses its top margin. |
| `.card.notice` `.card.warning` `.card.error` | Lavender, butter, pink. A `p.card.notice` inside a card works too. |
| `.card.solo` | A lone card centred on the page: sign-in, setup, an error. |
| `.cards` | A `ul` of cards. |
| `.card-head` | A blob beside a heading at the top of a card; `.dot` inside the blob. |
| `.strip` | A one-line card with a button and a link on the right. |
| `.section-head` | Heading on the left, an action on the right. |
| `.divider` | Centred "or". |

### Tiles · extracted

```html
<div class="tiles">
  <div class="tile"><div class="value">1,284</div><div class="label">plays</div></div>
</div>
```

Two across, four from 640px, rotating lavender, mint, butter, pink.

### Chips, tabs, badges · extracted

| Class | Notes |
| --- | --- |
| `.chips` + `.chip` | Filters. `.active` fills with the accent. Works on `ul` and `div`. |
| `.chip.tag` | Holds a value, a weight and a `.chip-x` remove button. `.added` is mint, `.removed` an outline with the value struck through. |
| `.tabs` + `a.active` | A pill strip that scrolls sideways. A `.tab-dot` before the label takes a tint. |
| `.segmented` | Two or three options; `a[aria-current]` or `button[aria-pressed="true"]` is the current one. |
| `.badge` | Small pill. Bare is accent-soft (queued, made here); `.ok` mint, `.warn` butter, `.bad` pink. |

### Buttons · extracted

`button` and `.button` are pills, 44px tall, accent-filled. `.secondary` is accent-soft
with dark ink. `.link` is a text button in `--muted`. `.small-button` is 36px. `.inline`
on a form keeps a button in a line of text. `.row` lays buttons out with 10px gaps.
`.danger` (designed) is `--bad` on `--bad-soft`.

### Actions · extracted

```html
<div class="media-actions">
  <button class="act primary"><span class="icon"><svg …></svg></span><span>Play</span></button>
  <button class="act" aria-pressed="false"><span class="icon"><svg …></svg></span><span>Love</span></button>
</div>
```

Stacked icon-and-label. The icon is a 46px round in `--button`; `.primary` fills it with
the accent (or the card's tint); `aria-pressed="true"` or `.on` inverts it to `--text`.

### Forms · extracted, textarea designed

Text, password, search, number, email and url inputs, `select` and `textarea` share one
style: 48px tall, a 2px `--line` border that turns accent on focus. `label` stacks its
text over the control. `.check` puts a checkbox or radio beside its text; native
controls, `accent-color` set. `fieldset.choices` lays radios out in a row. `form.stack`
is a 12px-gapped column capped at 440px.

`.search-form` is a pill bar holding a search input and its button; `.search-modes`
underneath holds radio options.

### Data · extracted

| Class | Notes |
| --- | --- |
| `table` in `.card.scroll` | Rules in `--line`, headers in `--muted`. `td.num` right-aligns with tabular figures. `.name` for the strong first line of a cell. |
| `dl.facts` | Terms in `--muted`, two columns from 640px. |
| `ul.schedule` | Times in a fixed-width column. |
| `ul.bars` | Name, meter, number. Each `li` can carry `.tint`. |
| `.progress` | A 6px meter. |
| `ul.list` | Rows in a card with hairlines between. `.lines` for a two-line cell. |
| `.dot` / `.dot.mini` | A 22px colour swatch, or a 10px inline one before a name. |
| `.chart-box` | A 240px box for a canvas. |

### Blob · extracted

A 76px organic shape with `overflow: hidden`; put an `img.cover` inside or leave it as a
colour. Seven silhouettes rotate with position, on `.media` cards and on `.card`s with
a card-head, so neighbours in a grid never match.

### Media card · extracted

```html
<div class="media-grid">
  <article class="media">
    <div class="blob"><img class="cover" src="…" alt=""></div>
    <div class="media-body">
      <h3 class="title marquee"><span>Title</span></h3>
      <p class="subtitle marquee"><span>Subtitle</span></p>
      <a class="media-link" href="…">Open</a>
    </div>
    <div class="media-info">
      <p class="line marquee"><span>Why this one</span></p>
      <p class="line tags marquee"><span>Tag · Tag</span></p>
    </div>
    <div class="media-actions">…</div>
  </article>
</div>
```

Blob, title and subtitle up top, a white info panel with two lines, actions along the
bottom. Cards in a grid are all the same height because the info panel is two lines and
long lines glide instead of wrapping. `.dimmed` fades a card to 60%; `.selected` draws a
3px ring; a `p.note` inside `.media-info` lays a message over the panel.

### Media list · extracted

The same card as a row, in `.media-list`:

```html
<article class="media row">
  <span class="row-num">1</span>
  <div class="blob">…</div>
  <div class="media-body">
    <h3 class="title marquee"><span>Title</span></h3>
    <p class="subtitle marquee"><span>Subtitle<span class="row-tags-inline"> · Tag</span></span></p>
  </div>
  <div class="media-info"><p class="line marquee"><span>Why</span></p></div>
  <div class="row-tags"><span><span class="pill">Tag</span></span></div>
  <button class="act primary" aria-label="Play">…</button>
  <div class="media-actions">…</div>
  <button class="row-toggle" aria-expanded="false" aria-label="More">…</button>
</article>
```

On a phone the row shows the blob, the title and the primary action; the chevron toggles
`.open`, which folds the info and the other actions out below. From 900px it is one
line: number, blob, body, info, tags, primary, actions, and the chevron hides.

### Marquee · extracted

`.marquee > span` on any one-line element. A script measures each line and adds
`.scrolling` with `--glide-shift` and `--glide-duration`; the line glides to the end and
back, pausing under the pointer or when the card has focus.

### Dock · extracted

```html
<div class="dock">
  <button class="dock-button primary" aria-label="Pause">…</button>
  <div class="dock-body">
    <div class="name">Title</div>
    <div class="muted small">0:12 of 0:30</div>
    <div class="progress"><div style="width: 40%"></div></div>
  </div>
  <a class="dock-link" href="…">Open</a>
  <button class="dock-button soft" aria-label="Next">…</button>
</div>
```

A floating bar for whatever is playing, running or selected. On a phone it floats above
the tab bar; from 900px it docks bottom-right at up to 560px. `hidden` hides it. Put
`.tint` on it with the current item's hue to colour its main button and meter.

### Entries · extracted

```html
<h3 class="eyebrow">Today</h3>
<div class="entries">
  <article class="entry busy">
    <div class="entry-head"><time>09:41</time><span class="entry-title">Refreshing</span><span class="who small">Sam</span><span class="badge">Running</span></div>
    <p class="entry-summary">…</p>
    <ol class="steps"><li><time>09:41:02</time> Started</li><li class="warn"><time>09:41:33</time> Slow</li></ol>
    <p class="entry-meta muted small">Queued 09:40</p>
  </article>
</div>
```

A timeline. `.busy`, `.warn` and `.bad` draw a 4px inset rule on the left in the accent,
warn or bad colour. `.steps` is a log with a 2px rule; a `details` can hold the long
version.

### Gallery · extracted

`ul.gallery` of `.gallery-item`: a 64px `.gallery-cover` (image or lavender placeholder)
beside `.gallery-body` with a `.gallery-name` link, a meta line and a badge.

### Dialog and grid · designed

`dialog` is a card with a scrim; open it with `showModal()`. `.grid` is the auto-filling
300px grid the media grid and gallery use, for anything else.

---

## Scripts the kit expects

The kit ships no JavaScript. Three components need a class toggled or a value measured;
these are the whole of it.

**Marquee.** Measure every `.marquee` after fonts load and on resize:

```js
const reduce = matchMedia("(prefers-reduced-motion: reduce)");
function measure() {
  document.querySelectorAll(".marquee").forEach(line => {
    const text = line.firstElementChild; if (!text) return;
    line.classList.remove("scrolling");
    const overflow = text.offsetWidth - line.clientWidth;
    if (overflow > 2) {
      const speed = reduce.matches ? 12 : 25;                       // px per second
      line.style.setProperty("--glide-shift", -overflow + "px");
      line.style.setProperty("--glide-duration", Math.max(reduce.matches ? 12 : 7, 5 + overflow / speed) + "s");
      line.classList.add("scrolling");
    }
  });
}
addEventListener("resize", () => setTimeout(measure, 120));
if (document.fonts) document.fonts.ready.then(measure); else measure();
```

**Row toggle.** Toggle `.open` on the row and `aria-expanded` on the chevron, then
re-measure the lines that just appeared:

```js
document.addEventListener("click", e => {
  const toggle = e.target.closest(".row-toggle"); if (!toggle) return;
  const row = toggle.closest(".media.row"), open = !row.classList.contains("open");
  row.classList.toggle("open", open); toggle.setAttribute("aria-expanded", String(open));
  if (open) measure();
});
```

**Dialog.** `dialog.showModal()` and `dialog.close()`.

**Match my device.** The six lines under Scheme above.

---

## Extending

Anything you add must be buildable from these six rules. If it cannot be, the kit is
being stretched past what it is; say so rather than inventing new primitives.

1. Surfaces are `--surface` on the `--bg` ground and carry no border. Lines are for
   table rules, input borders and the steps rule only, always in `--line`.
2. Radius comes off the ladder by role. Anything small and interactive is a pill.
3. Colour is the accent or one of the six pastels, never a new hue. Colour from data
   goes through `tint.css`.
4. States read their own tokens even where a pastel would look the same in light.
5. Display type is Fredoka 600 for headings, the brand, values and titles only; the
   rest is Figtree, and weight carries hierarchy.
6. Interactive things are 44px tall, focus is a 3px `--accent` outline offset 2px (or
   `--text` on a tinted part), press scales the icon, and every transition takes its
   duration from a `--t-*` token.

Run `python3 tools/check.py` afterwards. It fails if a component hardcodes a colour, a
`var()` does not resolve, `tint.css` defines a token or styles a class core does not,
anything uses `!important`, a radius is off the ladder, a duration is a literal, or a
`data-scheme` value is misspelt. Then look at the component in dark mode.

---

## Accessibility

Measured, WCAG 2 contrast. Every pair below clears AA in both schemes:

| Pair | Light | Dark |
| --- | --- | --- |
| `--text` on `--surface` | 14.4:1 | 13.8:1 |
| `--text` on the pastels | ≥ 10.9:1 | ≥ 10.8:1 |
| `--muted` on `--surface` | 7.5:1 | 7.5:1 |
| `--muted` on the pastels | ≥ 5.7:1 | ≥ 5.8:1 |
| `--accent` on `--surface` (links) | 5.6:1 | 7.4:1 |
| `--accent-ink` on `--accent` (buttons) | 5.6:1 | 8.3:1 |
| `--bad` on `--bad-soft` | 5.0:1 | 6.9:1 |
| `--text` on a tinted card, any hue | ≥ 11.3:1 | ≥ 12.2:1 |
| `--tint-ink` on a tinted button, any hue | ≥ 4.8:1 | ≥ 9.1:1 |

**One pair does not.** A link (`--accent`) inside a `.card.notice` (`--accent-soft`) is
4.4:1 in light mode. It is kept because the lavender notice is the look and the link is
underlined; if that link is the only way forward, put it on a plain card.

The tightest pass is the white ink on a tinted button around hue 185 to 208 (teal),
at 4.8:1. Above 5:1 everywhere else.

Everything is reachable by keyboard and has a visible focus ring. The marquee runs under
Reduce Motion by decision (see Spacing, motion, focus); transitions do not.

---

## Provenance

Extracted from a self-hosted music recommender's web app: a Discover board of
recommendation cards, a clip player, listening insights, an activity log, artist tags.

### Renamed for portability

| Source | Kit |
| --- | --- |
| `body.signed-in` | `.shell` |
| `.nav a.tab` | `.nav-tab` |
| `.login` | `.card.solo` |
| `.playlist-line` | `.strip` |
| `.view-toggle` | `.segmented` |
| `.badge.state-done` / `.state-failed` | `.badge.ok` / `.bad` |
| `.entry.state-running` / `.state-failed` | `.entry.busy` / `.bad` |
| `h3.day` | `.eyebrow` |
| `.track-name` | `.name` |
| `.recent-searches` | `.list` |
| `.rec` / `.recs` | `.media` / `.media-grid` |
| `.artists` / `.open-spotify` / `.card-note` | `.subtitle` / `.media-link` / `.note` |
| `.act.play` / `.rec.playing` | `.act.primary` / `.media.selected` |
| `.player-bar` / `.np-button` / `.np-progress` | `.dock` / `.dock-button` / `.progress` |
| `.playlists` / `.playlist` | `.gallery` / `.gallery-item` |
| `.genre-bars` / `.genre-pill` / `.genre-dot` | `.bars` / `.pill` / `.dot.mini` |
| `--card-l` / `--card-ink` | `--tint-l` / `--tint-ink` |

The full table is in [docs/design.md](docs/design.md#renamed-for-portability).

### Where the kit deviates

1. **Radii are tokens.** The dock was 34px and is `--r-bar` (32px); nav tabs and meters
   were half their height and are pills.
2. **Two type sizes folded.** The card-head heading was 1.25rem and is `--fs-title`.
3. **Tint lightness is the scheme's alone.** The source let a category nudge it by 3%.
4. **Reduced motion through tokens**, not `!important`.
5. **Untinted media cards rotate through the pastels.** The source always tinted.
6. **The row's external-link action is not carried over.**
7. **`--scrim` is derived**; the source has no dialog.
8. **`[data-scheme]` works on any wrapper**, not only `<html>`, in both directions.
9. **Seven blob silhouettes.** The mockups had seven; the app shipped four. The kit
   carries all seven.

---

## What this is not

Not a framework. No grid system, no utility classes, no JavaScript in the kit, no
theming build. One soft look, about forty components, and two files you can read in a
sitting.

If you need a framework, use a framework.
