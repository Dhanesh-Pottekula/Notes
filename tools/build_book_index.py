#!/usr/bin/env python3
"""Build index.html for the book folders that have no hand-made one, so every chapter's "all chapters" link works.

    python3 Notes/tools/build_book_index.py          # rebuild all of BOOKS; rerun after adding a chapter

- Books: BOOKS below (folders from the Notes root). Title and one-line description come from the book's entry in
  tools/build_home.py SECTIONS, so each book is described in one place only.
- Chapters are found on disk (chNN_*.html) and titled by their <h1>, like the home page does.
- Safety: a page this script wrote carries the MARK comment. An index.html WITHOUT it is hand-made
  (DDIA, Carnegie, the LLM books) and is never overwritten.
- Same look as the other index pages (DDIA index styles, light/dark switch, highlights).
"""
import html, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_home as home                        # noqa: E402  (SECTIONS, chapters(), STYLE, FONTS; builds nothing on import)
from theme_toggle import add_theme               # noqa: E402
from annotate_inject import add_annotate         # noqa: E402

BOOKS = ["system_design/database_internals/", "trading/murphy/", "trading/grimes/", "trading/carter/"]
MARK = "<!-- built by tools/build_book_index.py -->"


def entry(folder):
    for _, _, entries in home.SECTIONS:
        for path, title, desc in entries:
            if path == folder:
                return title, desc
    raise SystemExit(f"{folder} is not in SECTIONS of build_home.py; add it there first")


def build(folder):
    out = os.path.join(NOTES, folder, "index.html")
    if os.path.exists(out) and MARK not in open(out, encoding="utf-8").read():
        print(f"  kept (hand-made): {folder}index.html")
        return
    title, desc = entry(folder)
    e = html.escape
    chs = home.chapters(folder)
    items = "\n".join(
        f'      <li><a href="{e(os.path.basename(href))}"><span class="num">{num}</span><span class="t">{e(t)}</span></a></li>'
        for num, href, t in chs)
    up = os.path.relpath(os.path.join(NOTES, "index.html"), os.path.join(NOTES, folder)).replace(os.sep, "/")
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)} · study pages</title>
{home.FONTS}
{home.STYLE}
</head>
<body>
{MARK}
<div class="wrap">
  <header>
    <nav class="kicker"><a href="{up}" style="color:inherit">← All notes</a></nav>
    <div class="kicker">{len(chs)} study pages</div>
    <h1>{e(title)}</h1>
    <p>{e(desc)}</p>
    <p>One study page per chapter, in the book's order.</p>
  </header>
  <section class="plate">
    <h2>The chapters</h2>
    <ol class="chapters">
{items}
    </ol>
  </section>
</div>
</body>
</html>
"""
    with open(out, "w", encoding="utf-8") as f:
        f.write(add_annotate(add_theme(page), out))
    print(f"  built {folder}index.html: {len(chs)} chapters")


if __name__ == "__main__":
    for b in BOOKS:
        build(b)
