#!/usr/bin/env python3
"""Pack the public website from Notes: only pages to read and what they load.

    python3 Notes/tools/build_site.py [out_dir]        # default out_dir: Notes/_site (git-ignored)

The site is the home page (index.html) plus every study page and note page, with their pictures, the
highlight script and the downloadable practice scripts. It is what GitHub Pages serves
(.github/workflows/pages.yml runs this on every push to main).

Left OUT of the site on purpose:
- career/profile, career/job-search, career/sources   (profile text, application logs, raw sources)
- PRIVATE_PAGES below (the behavioural interview page: salary, notice period); a stub page takes its place
- working files: *.md sources, AGENTS.md / BRIEF.md, tools/, build sources (src/), *.py, scenes*.json,
  figure manifests, *.notes.json, PDFs
Note: the Notes repository itself is public, so these files are still visible on GitHub; they are only
kept off the website.

After copying, every link and image of every page is checked; a link from a page on the site to a file
that is not on the site is reported, and the build fails if there is any.
"""
import html, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(NOTES, "_site")

SKIP_DIRS = {".git", ".github", "_site", "tools", "src", "node_modules", "__pycache__"}
SKIP_PATHS = {"career/profile", "career/job-search", "career/sources"}       # from the Notes root
# Pages that stay private: the site gets a short "kept private" page at the same address, so links to it still work.
PRIVATE_PAGES = {"career/interview-topics/12-behavioral.html"}       # salary, notice period, reasons for leaving
STUB = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Private page</title>
<style>body{font-family:system-ui,sans-serif;max-width:560px;margin:18vh auto;padding:0 20px;line-height:1.6;
color:#1d2433;background:#f6f3ec}@media (prefers-color-scheme:dark){body{color:#e6e9ef;background:#12161d}a{color:#7db8ff}}</style>
</head><body><h1>This page is private</h1>
<p>It is part of the notes but is not published on the website. Open it from the local copy of Notes.</p>
<p><a href="HOME">&larr; Notes home</a></p></body></html>
"""
WEB_EXT = {".html", ".css", ".js", ".svg", ".png", ".webp", ".jpg", ".jpeg", ".gif", ".ico", ".woff2"}
WHOLE_DIRS = ("vlsi/tcl_perl_pv/scripts/", "vlsi/tcl_perl_pv/fixtures/")     # practice files linked from the pages


def wanted(rel):
    if rel.startswith(WHOLE_DIRS):
        return not rel.endswith(".DS_Store")
    return os.path.splitext(rel)[1].lower() in WEB_EXT


def copy_site():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    n = 0
    for root, dirs, files in os.walk(NOTES):
        rel_root = os.path.relpath(root, NOTES).replace(os.sep, "/")
        rel_root = "" if rel_root == "." else rel_root + "/"
        dirs[:] = sorted(d for d in dirs if (d not in SKIP_DIRS or (rel_root + d + "/").startswith(WHOLE_DIRS))
                         and (rel_root + d) not in SKIP_PATHS and not d.startswith(".")
                         and os.path.abspath(os.path.join(root, d)) != OUT)
        for name in files:
            rel = rel_root + name
            if wanted(rel):
                dst = os.path.join(OUT, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                if rel in PRIVATE_PAGES:
                    with open(dst, "w", encoding="utf-8") as f:
                        f.write(STUB.replace("HOME", "../" * rel.count("/") + "index.html"))
                    continue
                shutil.copy2(os.path.join(root, name), dst)
                n += 1
    open(os.path.join(OUT, ".nojekyll"), "w").close()            # serve files as they are
    return n


def check_links():
    """Every relative href/src of every page must exist in the site."""
    broken, pages = [], 0
    # exact names, so a wrong-case link fails here as it would on the (case-sensitive) web server
    have = {os.path.join(r, f) for r, _d, fs in os.walk(OUT) for f in fs}
    for root, _dirs, files in os.walk(OUT):
        for name in files:
            if not name.endswith(".html"):
                continue
            pages += 1
            path = os.path.join(root, name)
            text = open(path, encoding="utf-8", errors="replace").read()
            text = re.sub(r"<script\b.*?</script>|<pre\b.*?</pre>|<code\b.*?</code>", "", text, flags=re.S | re.I)
            for target in set(re.findall(r'<(?:a|img|link|script|source|iframe)\b[^>]*?\b(?:href|src)="([^"]+)"', text, flags=re.I)):
                target = html.unescape(target)
                if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:|//|#", target):
                    continue
                file = target.split("#")[0].split("?")[0]
                if not file:
                    continue
                full = os.path.normpath(os.path.join(root, file))
                if full not in have and os.path.join(full, "index.html") in have:
                    full = os.path.join(full, "index.html")
                if full not in have:
                    broken.append((os.path.relpath(path, OUT), target))
    return pages, broken


def main():
    n = copy_site()
    pages, broken = check_links()
    size = sum(os.path.getsize(os.path.join(r, f)) for r, _d, fs in os.walk(OUT) for f in fs)
    print(f"site: {n} files, {pages} pages, {size / 1e6:.0f} MB -> {OUT}")
    fatal = 0
    for page, target in sorted(broken):
        dest = os.path.normpath(os.path.join(os.path.dirname(page), target.split("#")[0])).replace(os.sep, "/")
        if any(dest.startswith(p + "/") for p in SKIP_PATHS):
            print(f"  note    {page}  ->  {target}   (kept off the site on purpose)")
        elif re.match(r"ch\d+[a-z]?_.*\.html$", os.path.basename(dest)):
            print(f"  note    {page}  ->  {target}   (chapter page not written yet)")
        else:
            fatal += 1
            print(f"  BROKEN  {page}  ->  {target}")
    if fatal:
        sys.exit(f"{fatal} broken link(s): fix the page, or add the file to the site rules above")


if __name__ == "__main__":
    main()
