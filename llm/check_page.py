#!/usr/bin/env python3
"""Check one study page: python3 check_page.py <book_dir> <page.html> <chapter_number>

Verifies: every figure of the chapter (from figs/MANIFEST.tsv) is used exactly once, every <img src> exists,
no external scripts/styles except Google Fonts, each inline <script> parses (node --check), and prints size.
Exit code 1 on any problem.
"""
import os, re, subprocess, sys, tempfile

book, page, ch = sys.argv[1], sys.argv[2], sys.argv[3]
path = os.path.join(book, page)
html = open(path, encoding="utf-8").read()
problems = []

ids = []
for line in open(os.path.join(book, "figs", "MANIFEST.tsv"), encoding="utf-8"):
    fid = line.split("\t")[0]
    if fid.split("-")[0] == ch and fid not in ids:
        ids.append(fid)
for fid in ids:
    n = len(re.findall(r'src="figs/fig-%s\.png"' % re.escape(fid), html))
    if n != 1:
        problems.append(f"figure {fid} used {n} times (want 1)")

for src in re.findall(r'<img[^>]+src="([^"]+)"', html):
    if src.startswith("data:"):
        continue
    if re.match(r"https?:", src) or not os.path.exists(os.path.join(book, src)):
        problems.append(f"bad img src {src}")

for m in re.findall(r'<(?:script|link)[^>]+(?:src|href)="(https?://[^"]+)"', html):
    if "fonts.googleapis.com" not in m and "fonts.gstatic.com" not in m:
        problems.append(f"external resource {m}")

for i, js in enumerate(re.findall(r"<script(?![^>]*src)[^>]*>(.*?)</script>", html, re.S)):
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
        f.write(js)
    r = subprocess.run(["node", "--check", f.name], capture_output=True, text=True)
    os.unlink(f.name)
    if r.returncode != 0:
        problems.append(f"script {i} syntax error: {r.stderr.strip().splitlines()[-1] if r.stderr else ''}")

print(f"{page}: {len(html)//1024} KB, {len(ids)} chapter figures, {len(problems)} problems")
for p in problems:
    print("  -", p)
sys.exit(1 if problems else 0)
