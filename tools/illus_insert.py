"""Put the AI illustrations into the "Picture it" boxes of a book's pages (idempotent).

Each book keeps its illustrations in <book>/illus/: NAME.webp (Gemini art) or NAME.svg (hand-drawn
fallback when Gemini is not available; the .webp wins when both exist) plus scenes*.json, a list of
{"page", "key", "name", "alt", "scene"}. `key` is a substring of the box's normalised text
(tags stripped, entities unescaped, whitespace collapsed) that picks exactly one box on the page.
Scenes with no image yet are skipped, so this can run while images are still coming.

Usage: python3 illus_insert.py <book_dir> [...]
"""
import glob, html as htmllib, json, os, re, struct, sys

FIG_START, FIG_END = "<!-- illus -->", "<!-- /illus -->"
CSS_START, CSS_END = "<!-- illus-css:start -->", "<!-- illus-css:end -->"
BOX = re.compile(r'(<div class="box picture"[^>]*>\s*<b>Picture it\b.*?</b>)(.*?)(</div>)', re.S)

# The art has an opaque off-white ground, so it sits on a matching card that reads well in both themes.
CSS = CSS_START + """<style>
figure.illus { margin: 6px 0 10px; background: #f6f1e7; border: 1px solid var(--rule); border-radius: 12px; padding: 6px; }
figure.illus img { display: block; width: 100%; height: auto; border-radius: 8px; }
</style>""" + CSS_END


def norm(fragment):
    # Both spellings of "tags removed": dropped outright ("card.") and replaced by a space ("card .").
    texts = (re.sub(r"<[^>]+>", sep, fragment) for sep in ("", " "))
    return "\n".join(re.sub(r"\s+", " ", htmllib.unescape(t)).strip() for t in texts)


def webp_size(path):
    with open(path, "rb") as f:
        head = f.read(30)
    kind = head[12:16]
    if kind == b"VP8 ":
        w, h = struct.unpack("<HH", head[26:30])
        return w & 0x3FFF, h & 0x3FFF
    if kind == b"VP8L":
        b = int.from_bytes(head[21:25], "little")
        return (b & 0x3FFF) + 1, ((b >> 14) & 0x3FFF) + 1
    if kind == b"VP8X":
        return int.from_bytes(head[24:27], "little") + 1, int.from_bytes(head[27:30], "little") + 1
    raise ValueError(f"unknown webp chunk {kind} in {path}")


def svg_size(path):
    head = open(path, encoding="utf-8").read(2000)
    m = re.search(r'viewBox="\s*[-\d.]+[ ,]+[-\d.]+[ ,]+([\d.]+)[ ,]+([\d.]+)', head)
    return round(float(m.group(1))), round(float(m.group(2)))


def image_file(illus_dir, name):
    for ext in (".webp", ".svg"):
        if os.path.exists(os.path.join(illus_dir, name + ext)):
            return name + ext
    return None


def strip(page_html):
    page_html = re.sub(re.escape(FIG_START) + r".*?" + re.escape(FIG_END), "", page_html, flags=re.S)
    return re.sub(r"\n?" + re.escape(CSS_START) + r".*?" + re.escape(CSS_END), "", page_html, flags=re.S)


def figure(scene, illus_dir):
    fname = image_file(illus_dir, scene["name"])
    path = os.path.join(illus_dir, fname)
    w, h = webp_size(path) if fname.endswith(".webp") else svg_size(path)
    alt = htmllib.escape(scene["alt"], quote=True)
    return (f'{FIG_START}<figure class="illus"><img src="illus/{fname}" alt="{alt}" '
            f'width="{w}" height="{h}" loading="lazy" decoding="async"></figure>{FIG_END}')


def illustrate(book):
    illus_dir = os.path.join(book, "illus")
    scenes = [s for f in sorted(glob.glob(os.path.join(illus_dir, "scenes*.json")))
              for s in json.load(open(f, encoding="utf-8"))]
    by_page = {}
    for s in scenes:
        by_page.setdefault(s["page"], []).append(s)
    total = 0
    for page, items in sorted(by_page.items()):
        path = os.path.join(book, page)
        src = open(path, encoding="utf-8").read()
        out = strip(src)
        ready = [s for s in items if image_file(illus_dir, s["name"])]
        for s in ready:
            hits = [m for m in BOX.finditer(out) if s["key"] in norm(m.group(2))]
            if len(hits) != 1:
                sys.exit(f"{page}: key {s['key']!r} matches {len(hits)} boxes")
            m = hits[0]
            out = out[:m.end(1)] + figure(s, illus_dir) + out[m.end(1):]
        if ready:
            out = out.replace("</head>", CSS + "\n</head>", 1)
        if out != src:
            open(path, "w", encoding="utf-8").write(out)
        total += len(ready)
        print(f"  {page}: {len(ready)}/{len(items)} illustrations")
    print(f"{book}: {total} illustrations placed")


if __name__ == "__main__":
    for book in sys.argv[1:]:
        illustrate(book)
