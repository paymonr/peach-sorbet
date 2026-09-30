#!/usr/bin/env python3
"""Validator for the peach-sorbet CSS kit.

Checks the invariants the kit is built on:

  1. Every ``var(--x)`` consumed in either stylesheet resolves to a ``--x``
     defined in ``core.css``. A mistyped variable falls back to nothing in a
     browser, silently, so this is the check that matters most.
  2. ``core.css`` declares no raw colour outside its token blocks. Hex,
     ``rgb()``/``rgba()``, ``hsl()`` and ``oklch()`` with literal channels all
     count. Colour lives in the two token blocks and nowhere else.
  3. ``tint.css`` defines no custom properties, and every ``oklch()`` it writes
     takes each channel from a token or a calc() of tokens. It consumes core's
     values and adds none of its own, so the tier split cannot rot.
  4. Neither file uses ``!important``.
  5. Every class ``tint.css`` styles is one ``core.css`` already styles (apart
     from ``.tint`` itself). The tint layer recolours components; it never
     introduces one, so deleting it leaves nothing unstyled.
  6. Every ``data-scheme`` value in the stylesheets and the demo — in the
     attribute and in the script that sets it — is ``light`` or ``dark``. A
     typo renders as light in silence.
  7. Every ``border-radius`` in ``core.css`` comes off the ladder: a ``--r-*``
     token, ``50%`` for a circle, ``inherit``, or the blob's percentage quads.
  8. Every ``transition`` and ``animation`` duration is a ``--t-*`` or
     ``--glide-*`` token, so reduced-motion can zero them from one place.

Standard library only. Exits 0 on pass, 1 on failure.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORE = ROOT / "core.css"
TINT = ROOT / "tint.css"
INDEX = ROOT / "index.html"

SCHEMES = {"light", "dark"}
_VALUE = r"""(?:"([^"]*)"|'([^']*)'|([A-Za-z0-9_-]+))"""
SCHEME_USE = re.compile(
    r"data-scheme\s*=\s*" + _VALUE
    + r"""|dataset\.scheme\s*=\s*(?:"([^"]*)"|'([^']*)')"""
)

VAR_USE = re.compile(r"var\(\s*(--[\w-]+)")
VAR_DEF = re.compile(r"(--[\w-]+)\s*:")
RAW_COLOUR = re.compile(r"(?:#|%23)[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?)\s*\(")
OKLCH = re.compile(r"oklch\(([^()]*(?:\([^()]*\)[^()]*)*)\)")
COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
TOKEN_BLOCK = re.compile(
    r"(?:^|(?<=[}]))\s*(?::root|\[data-scheme[^\]]*\])(?:\s*,\s*(?::root|\[data-scheme[^\]]*\]))*\s*\{"
)
RULE = re.compile(r"([^{}]+)\{([^{}]*)\}")
CLASS_IN_SEL = re.compile(r"\.([a-z][a-z0-9-]*)")
RADIUS = re.compile(r"border-radius\s*:\s*([^;}]+)")
RADIUS_OK = re.compile(
    r"^(?:var\(--r-[a-z-]+\)|50%|inherit|(?:\d{1,2}%\s*){4}|(?:\d{1,2}%\s*){2})$"
)
DURATION = re.compile(r"\b(\d*\.?\d+)(m?s)\b")
MOTION = re.compile(r"(?:transition|animation)(?:-duration)?\s*:\s*([^;}]+)")


def strip_comments(text: str) -> str:
    """Blank out comments, keeping offsets and newlines so line numbers hold."""
    return COMMENT.sub(lambda m: "".join(c if c == "\n" else " " for c in m.group(0)), text)


def line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def token_spans(text: str) -> list[tuple[int, int]]:
    """Byte ranges of the :root and [data-scheme=...] blocks."""
    spans = []
    for m in TOKEN_BLOCK.finditer(text):
        depth = 0
        for i in range(m.end() - 1, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    spans.append((m.start(), i))
                    break
    return spans


def inside(spans: list[tuple[int, int]], offset: int) -> bool:
    return any(start <= offset <= end for start, end in spans)


def rules(text: str):
    """Yield (selector, body, offset) for every rule, at any depth."""
    for m in RULE.finditer(text):
        yield m.group(1), m.group(2), m.start()


def oklch_channels_are_tokens(args: str) -> bool:
    """Each of the three channels must be var(...) or calc(...) of vars."""
    parts = [p.strip() for p in re.split(r"\s+(?![^()]*\))", args.strip()) if p.strip()]
    if len(parts) != 3:
        return False
    for part in parts:
        if not (part.startswith("var(") or part.startswith("calc(")):
            return False
        if re.search(r"(?<![\w-])\d+(?:\.\d+)?%?", re.sub(r"var\([^)]*\)", "", part)) and not part.startswith("calc("):
            return False
    return True


def main() -> int:
    problems: list[str] = []

    if not CORE.exists():
        print("FAIL  core.css does not exist")
        return 1

    core = strip_comments(CORE.read_text())
    tint = strip_comments(TINT.read_text()) if TINT.exists() else ""

    # 1. every consumed variable is defined in core.css
    defined = {m.group(1) for m in VAR_DEF.finditer(core)}
    for name, text in (("core.css", core), ("tint.css", tint)):
        for m in VAR_USE.finditer(text):
            if m.group(1) not in defined:
                problems.append(f"{name}:{line_of(text, m.start())}  undefined variable {m.group(1)}")
    if not defined:
        problems.append("core.css  defines no custom properties at all")

    # 2. no raw colour in core.css outside the token blocks
    spans = token_spans(core)
    for m in RAW_COLOUR.finditer(core):
        if not inside(spans, m.start()):
            problems.append(
                f"core.css:{line_of(core, m.start())}  raw colour {m.group(0).strip()!r} "
                f"outside the token blocks — use a var() instead"
            )
    for m in OKLCH.finditer(core):
        if not inside(spans, m.start()):
            problems.append(
                f"core.css:{line_of(core, m.start())}  oklch() in a component — colour from data belongs in tint.css"
            )

    # 3. tint.css owns no tokens and writes oklch() from tokens only
    for m in VAR_DEF.finditer(tint):
        problems.append(f"tint.css:{line_of(tint, m.start())}  defines {m.group(1)} — tokens belong in core.css")
    for m in RAW_COLOUR.finditer(tint):
        problems.append(f"tint.css:{line_of(tint, m.start())}  raw colour {m.group(0).strip()!r}")
    for m in OKLCH.finditer(tint):
        if not oklch_channels_are_tokens(m.group(1)):
            problems.append(
                f"tint.css:{line_of(tint, m.start())}  oklch({m.group(1).strip()}) has a literal channel — "
                f"lightness comes from --tint-*, hue and chroma from the inputs"
            )

    # 4. no !important anywhere
    for name, text in (("core.css", core), ("tint.css", tint)):
        for m in re.finditer(r"!important", text):
            problems.append(f"{name}:{line_of(text, m.start())}  uses !important")

    # 5. tint.css only touches classes core.css defines
    core_classes = set()
    for sel, _, _ in rules(core):
        core_classes |= set(CLASS_IN_SEL.findall(sel))
    for sel, _, offset in rules(tint):
        for cls in CLASS_IN_SEL.findall(sel):
            if cls != "tint" and cls not in core_classes:
                problems.append(
                    f"tint.css:{line_of(tint, offset)}  .{cls} is not a core.css component — "
                    f"the tint layer recolours, it does not add"
                )

    # 6. every data-scheme names a scheme that exists
    sources = [("core.css", core), ("tint.css", tint)]
    if INDEX.exists():
        sources.append(("index.html", INDEX.read_text()))
    for name, text in sources:
        for m in SCHEME_USE.finditer(text):
            value = next((g for g in m.groups() if g is not None), "")
            if value not in SCHEMES:
                problems.append(
                    f"{name}:{line_of(text, m.start())}  unknown scheme {value!r} — expected light or dark"
                )

    # 7. every radius comes off the ladder
    for m in RADIUS.finditer(core):
        if inside(spans, m.start()):
            continue
        value = m.group(1).strip()
        if not RADIUS_OK.match(value):
            problems.append(
                f"core.css:{line_of(core, m.start())}  border-radius {value!r} is not on the ladder — use a --r-* token"
            )

    # 8. every duration is a token
    for name, text in (("core.css", core), ("tint.css", tint)):
        for m in MOTION.finditer(text):
            if inside(spans, m.start()) if name == "core.css" else False:
                continue
            if DURATION.search(m.group(1)):
                problems.append(
                    f"{name}:{line_of(text, m.start())}  literal duration in {m.group(0).strip()!r} — use --t-* "
                    f"so reduced-motion can zero it"
                )

    if problems:
        for p in problems:
            print(f"FAIL  {p}")
        print(f"\n{len(problems)} problem(s)")
        return 1

    print(f"PASS  {len(defined)} tokens defined, all references resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
