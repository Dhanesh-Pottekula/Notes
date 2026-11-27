#!/usr/bin/env python3
"""Build the Tcl + Perl for physical verification pages from src/*.body.txt.

    python3 Notes/vlsi/tcl_perl_pv/src/build.py

Why a build step: the pages show a lot of Tcl and Perl, which is full of < > &. Here the code is written
raw and escaped once, and every snippet marked "run" is really executed, with its real output printed
under it, so the pages cannot show code that does not work.

In a body file:
  <<<tcl run | optional title      raw code until a line with only >>>   ("run" = execute and show output)
  <<<perl run | title              same for Perl
  <<<tcl | title                   shown, not executed
  <<<innovus | title               shown with a "not run here" badge (also: calibre, svrf, shell, text)
  {{script:drc_summary.pl|out=drc_summary_pl}}   a file from ../scripts plus its saved output (src/out/*.txt)
  {{fixture:top.drc.summary|1-20}}               lines of a sample input file from ../fixtures
After building, the theme switch and the highlight/notes script are added (Notes/tools).
"""
import html, os, re, subprocess, sys

SRC = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.dirname(SRC)
SCRIPTS = os.path.join(BOOK, "scripts")
FIXTURES = os.path.join(BOOK, "fixtures")
OUT = os.path.join(SRC, "out")
TOOLS = os.path.normpath(os.path.join(BOOK, "..", "..", "tools"))

PAGES = [  # (file, short nav title)
    ("index.html", "Scripting plan"),
    ("ch00_pv_roadmap.html", "0 · Whole PV roadmap"),
    ("ch01_tcl.html", "1 · Tcl"),
    ("ch02_perl.html", "2 · Perl"),
    ("ch03_innovus.html", "3 · Innovus"),
    ("ch04_calibre.html", "4 · Calibre"),
    ("ch05_script_bank.html", "5 · Script bank"),
    ("ch06_interview.html", "6 · Interview"),
]
LANG = {"tcl": "Tcl", "perl": "Perl", "innovus": "Innovus Tcl", "calibre": "Calibre Tcl", "svrf": "SVRF",
        "shell": "Shell", "text": "Text"}
NOT_RUN = {"innovus", "calibre", "svrf"}
VERS = {}


def version(lang):
    if lang not in VERS:
        if lang == "tcl":
            VERS[lang] = "Tcl " + subprocess.run(["tclsh"], input="puts [info patchlevel]", capture_output=True,
                                                 text=True).stdout.strip()
        else:
            v = subprocess.run(["perl", "-e", "print $^V"], capture_output=True, text=True).stdout.strip()
            VERS[lang] = "Perl " + v.lstrip("v")
    return VERS[lang]


def esc(s):
    return html.escape(s, quote=False)


def run_snippet(lang, code, where):
    cmd = ["tclsh"] if lang == "tcl" else ["perl"]
    r = subprocess.run(cmd, input=code, capture_output=True, text=True, cwd=SCRIPTS, timeout=20)
    out = (r.stdout + r.stderr).rstrip("\n")
    if r.returncode != 0:
        sys.exit(f"SNIPPET FAILED in {where}:\n{code}\n--- output ---\n{out}")
    return out


def code_block(lang, flags, title, code, where):
    code = code.strip("\n")
    badge, out_html = "", ""
    if "run" in flags:
        out = run_snippet(lang, code, where)
        badge = f'<span class="badge ok">ran on {version(lang)}</span>'
        out_html = f'<pre class="out"><span class="outlabel">output</span>{esc(out)}</pre>' if out else ""
    elif lang in NOT_RUN:
        badge = '<span class="badge warn">not run here · check in your tool</span>'
    cap = f'<figcaption><span class="lang">{LANG.get(lang, lang)}</span><span class="cap">{title}</span>{badge}</figcaption>'
    return f'<figure class="code">{cap}<pre><code>{esc(code)}</code></pre>{out_html}</figure>'


def script_block(m):
    name, _, opt = m.group(1).partition("|")
    code = open(os.path.join(SCRIPTS, name), encoding="utf-8").read().rstrip("\n")
    lang = "Perl" if name.endswith((".pl", ".pm")) else "Tcl" if name.endswith(".tcl") else "Shell"
    out_html, badge = "", ""
    if opt.startswith("out="):
        out = open(os.path.join(OUT, opt[4:] + ".txt"), encoding="utf-8").read().rstrip("\n")
        out_html = f'<pre class="out"><span class="outlabel">real run on the sample files</span>{esc(out)}</pre>'
        badge = '<span class="badge ok">tested</span>'
    cap = (f'<figcaption><span class="lang">{lang}</span><span class="cap"><a href="scripts/{name}">scripts/{name}</a>'
           f' · {len(code.splitlines())} lines</span>{badge}</figcaption>')
    return f'<figure class="code">{cap}<pre><code>{esc(code)}</code></pre>{out_html}</figure>'


def fixture_block(m):
    name, _, rng = m.group(1).partition("|")
    lines = open(os.path.join(FIXTURES, name), encoding="utf-8").read().rstrip("\n").split("\n")
    if rng:
        a, b = (int(x) for x in rng.split("-"))
        lines = lines[a - 1:b]
    cap = (f'<figcaption><span class="lang">Sample input</span><span class="cap"><a href="fixtures/{name}">fixtures/{name}</a>'
           f'</span><span class="badge note">practice file, written for this guide</span></figcaption>')
    return f'<figure class="code">{cap}<pre><code>{esc(chr(10).join(lines))}</code></pre></figure>'


def render_body(text, where):
    out, lines, i = [], text.split("\n"), 0
    while i < len(lines):
        m = re.match(r"^<<<(\w+)([^|]*)(?:\|(.*))?$", lines[i])
        if not m:
            out.append(lines[i]); i += 1; continue
        j = i + 1
        while lines[j].strip() != ">>>":
            j += 1
        out.append(code_block(m.group(1), m.group(2).split(), (m.group(3) or "").strip(), "\n".join(lines[i + 1:j]),
                              f"{where} line {i + 1}"))
        i = j + 1
    body = "\n".join(out)
    body = re.sub(r"\{\{script:([^}]+)\}\}", script_block, body)
    body = re.sub(r"\{\{fixture:([^}]+)\}\}", fixture_block, body)
    return body


def main():
    style = open(os.path.join(SRC, "style.css"), encoding="utf-8").read()
    for n, (page, _short) in enumerate(PAGES):
        raw = open(os.path.join(SRC, page.replace(".html", ".body.txt")), encoding="utf-8").read()
        meta, _, body = raw.partition("\n---\n")
        info = dict(l.split(": ", 1) for l in meta.strip().split("\n"))
        body = render_body(body, page)
        toc = "".join(f'<li><a href="#{i}">{re.sub("<[^>]+>", "", t)}</a></li>'
                      for i, t in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body))
        nav = ['<a href="../../index.html">← Notes home</a>']
        if n:
            nav.append('<a href="index.html">Scripting plan</a>')
            nav.append(f'<a href="{PAGES[n - 1][0]}">‹ {PAGES[n - 1][1]}</a>')
        if n + 1 < len(PAGES):
            nav.append(f'<a href="{PAGES[n + 1][0]}">{PAGES[n + 1][1]} ›</a>')
        nav_html = '<nav class="crumbs">' + "".join(nav) + "</nav>"
        doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(info['title'])} · Tcl and Perl for physical verification</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=JetBrains+Mono:wght@400;600&display=swap">
<style>
{style}
</style>
</head>
<body>
<main>
{nav_html}
<header class="hero">
<p class="kicker">{info['kicker']}</p>
<h1>{info['title']}</h1>
<p class="lede">{info['lede']}</p>
</header>
<section class="toc"><h2 class="toc-h">On this page</h2><ol>{toc}</ol></section>
{body}
{nav_html}
</main>
</body>
</html>
"""
        with open(os.path.join(BOOK, page), "w", encoding="utf-8") as f:
            f.write(doc)
        print(f"built {page}  {len(doc) // 1024} KB")
    for tool in ("theme_toggle.py", "annotate_inject.py"):
        subprocess.run([sys.executable, os.path.join(TOOLS, tool), BOOK], check=True, stdout=subprocess.DEVNULL)


if __name__ == "__main__":
    main()
