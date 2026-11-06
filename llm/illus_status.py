"""Show, for every "Picture it" box of a book, whether it has a scene (prompt) and an image.

Usage: python3 illus_status.py <book_dir> [page.html ...]          one line per page (counts)
       python3 illus_status.py <book_dir> page.html --boxes         one line per box: index, scene name, image, text
"""
import glob, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from illus_insert import BOX, norm, strip, image_file


def status(book, page):
    illus = os.path.join(book, "illus")
    scenes = [s for f in sorted(glob.glob(os.path.join(illus, "scenes*.json")))
              for s in json.load(open(f, encoding="utf-8")) if s["page"] == page]
    html = strip(open(os.path.join(book, page), encoding="utf-8").read())
    rows = []
    for i, m in enumerate(BOX.finditer(html)):
        text = norm(m.group(2))
        hit = [s for s in scenes if s["key"] in text]
        name = hit[0]["name"] if hit else None
        rows.append((i, name, image_file(illus, name) if name else None, text.split("\n")[0]))
    return rows


if __name__ == "__main__":
    book = sys.argv[1]
    pages = [a for a in sys.argv[2:] if a.endswith(".html")] or sorted(
        os.path.basename(p) for p in glob.glob(os.path.join(book, "ch*.html")))
    for page in pages:
        rows = status(book, page)
        if "--boxes" in sys.argv:
            for i, name, img, text in rows:
                print(f"{page} [{i:2d}] {name or '-':40s} {img or 'NO IMAGE':45s} {text[:70]}")
        else:
            print(f"{page:52s} boxes {len(rows):3d}  with scene {sum(1 for r in rows if r[1]):3d}  "
                  f"with image {sum(1 for r in rows if r[2]):3d}")
