"""Add highlights + margin notes (Notes/assets/annotate/) to every study page (idempotent).

Each page gets one tag loading the shared script by a relative path, so one change to annotate.js reaches
every page. Notes are saved per page by Notes/serve_notes.py (see annotate.js for storage).
build_index.py calls add_annotate() too, so rebuilt index pages keep the tag.

Usage: python3 annotate_inject.py [folder ...]
  (updates every .html under the given folders; default: all of Notes, skipping illus/ folders)
"""
import glob, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
SCRIPT = os.path.join(NOTES, "assets", "annotate", "annotate.js")
START, END = "<!-- annotate:start -->", "<!-- annotate:end -->"


def strip(html):
    return re.sub(r"\n*" + re.escape(START) + r".*?" + re.escape(END) + r"\n?", "\n", html, flags=re.S)


def add_annotate(html, page_file):
    src = os.path.relpath(SCRIPT, os.path.dirname(os.path.abspath(page_file))).replace(os.sep, "/")
    tag = f'{START}<script src="{src}" defer></script>{END}'
    html = strip(html)
    i = html.rfind("</body>")
    if i < 0:
        return html.rstrip("\n") + "\n" + tag + "\n"
    return html[:i] + tag + "\n" + html[i:]


if __name__ == "__main__":
    import sys
    roots = sys.argv[1:] or [NOTES]
    files = sorted(f for r in roots for f in glob.glob(os.path.join(r, "**", "*.html"), recursive=True)
                   if f"{os.sep}illus{os.sep}" not in f)
    changed = 0
    for f in files:
        src = open(f, encoding="utf-8").read()
        out = add_annotate(src, f)
        if out != src:
            open(f, "w", encoding="utf-8").write(out)
            changed += 1
    print(f"{changed} of {len(files)} pages updated")
