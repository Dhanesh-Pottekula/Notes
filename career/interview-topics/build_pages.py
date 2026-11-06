"""Turn the interview-topic markdown files into study pages that look like the book pages.

The .md files stay the source; run this after editing any of them:
    python3 Notes/career/interview-topics/build_pages.py

Each NN-name.md becomes NN-name.html (00-README.md becomes index.html) with:
- the book pages' palette, fonts and light/dark switch (Notes/llm/theme_toggle.py),
- highlights + margin notes (Notes/assets/annotate/, saved by Notes/serve_notes.py),
- tickable topic checkboxes with progress, kept in this browser's localStorage ("itp:<page>"),
- "DDIA ch7", "AIE ch6" … linked to the matching study page in Notes/.
"""
import glob, hashlib, html, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(NOTES, "llm"))
from theme_toggle import add_theme          # noqa: E402
from annotate_inject import add_annotate    # noqa: E402

BOOK_DIRS = {"DDIA": "system_design/ddia", "DBI": "system_design/database_internals",
             "AIE": "llm/ai_engineering", "HOL": "llm/hands_on_llms", "LEH": "llm/llm_engineers_handbook"}


def book_pages():
    pages = {}
    for key, rel in BOOK_DIRS.items():
        for f in glob.glob(os.path.join(NOTES, rel, "ch[0-9][0-9]_*.html")):
            n = int(os.path.basename(f)[2:4])
            pages[(key, n)] = os.path.relpath(f, HERE).replace(os.sep, "/")
    return pages


BOOKS = book_pages()


def out_name(md):
    return "index.html" if md.startswith("00-") else md[:-3] + ".html"


# ---------- inline markdown ----------

def inline(text):
    keep = []

    def stash(s):
        keep.append(s)
        return f"\x00{len(keep) - 1}\x00"

    text = re.sub(r"`([^`]+)`", lambda m: stash("<code>" + html.escape(m.group(1)) + "</code>"), text)

    def md_link(m):
        label, url = m.group(1), m.group(2)
        if url.endswith(".md") and not url.startswith("http"):
            url = out_name(os.path.basename(url))
        ext = ' target="_blank" rel="noopener"' if url.startswith("http") else ""
        return stash(f'<a href="{html.escape(url)}"{ext}>{inline(label)}</a>')

    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", md_link, text)

    def bare(m):
        url = m.group(0)
        tail = ""
        # drop trailing punctuation, but keep a ")" that closes one in the URL (Wikipedia links)
        while url and (url[-1] in ".,;:" or (url[-1] == ")" and url.count(")") > url.count("("))):
            tail = url[-1] + tail
            url = url[:-1]
        short = re.sub(r"^https?://(www\.)?", "", url)
        return stash(f'<a class="ext" href="{html.escape(url)}" target="_blank" rel="noopener">'
                     f'{html.escape(short)}</a>') + tail

    text = re.sub(r"https?://[^\s<>\"']+", bare, text)
    text = html.escape(text, quote=False)

    def book(m):
        href = BOOKS.get((m.group(1), int(m.group(2))))
        return f'<a class="book" href="{href}">{m.group(0)}</a>' if href else m.group(0)

    text = re.sub(r"\b(DDIA|DBI|AIE|HOL|LEH) ch(\d+)\b", book, text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)([^*\n]+?)\*(?![\w*])", r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: keep[int(m.group(1))], text)


# ---------- blocks ----------

ITEM = re.compile(r"^(\s*)(?:[-*]|(\d+)\.)\s+(.*)$")


def render_list(lines, stem):
    """lines: list of (indent, ordered, text) items (continuations already joined)."""
    out, stack = [], []           # stack of (indent, tag)
    for indent, ordered, text in lines:
        tag = "ol" if ordered else "ul"
        while stack and indent < stack[-1][0]:
            out.append(f"</li></{stack.pop()[1]}>")
        if not stack or indent > stack[-1][0]:
            cls = ""
            box = re.match(r"\[( |x|X)\]\s+", text)
            if box and not stack:
                cls = ' class="topics"'
            out.append(f"<{tag}{cls}>")
            stack.append((indent, tag))
        else:
            out.append("</li>")
        box = re.match(r"\[( |x|X)\]\s+(.*)$", text)
        if box:
            # "topic text ↳ sources": the key hashes only the topic, so adding sources keeps the ticks
            topic, _, src = box.group(2).partition(" ↳ ")
            key = hashlib.md5(topic.strip().encode()).hexdigest()[:10]
            src_html = f'<div class="src">{inline(src.strip())}</div>' if src.strip() else ""
            out.append(f'<li class="topic"><input type="checkbox" class="tick" data-k="{key}" '
                       f'aria-label="Done"><span>{inline(topic.strip())}</span>{src_html}')
        else:
            out.append(f"<li>{inline(text)}")
    while stack:
        out.append(f"</li></{stack.pop()[1]}>")
    return "".join(out)


def render_table(rows):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    head, body = cells[0], [r for r in cells[2:]]
    h = "".join(f"<th>{inline(c)}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
    return f'<div class="tablewrap"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


def para_class(text):
    for word, cls in (("Questions", "q"), ("Learn", "learn"), ("Book", "learn"), ("Read", "learn"),
                      ("Watch", "learn"), ("Do", "learn"), ("Your work", "learn"), ("Format", "fmt")):
        if text.startswith(f"**{word}"):
            return cls
    return ""


def parse(md_text, stem):
    """Returns (title, intro_html, sections[(id, heading, html)])."""
    lines = md_text.split("\n")
    title, intro, sections = "", [], []
    cur = intro
    i = 0

    def flush_para(buf):
        if buf:
            text = " ".join(s.strip() for s in buf)
            cls = para_class(text)
            cur.append(f'<p class="{cls}">{inline(text)}</p>' if cls else f"<p>{inline(text)}</p>")
            buf.clear()

    para = []
    while i < len(lines):
        line = lines[i]
        if line.startswith("# "):
            flush_para(para)
            title = line[2:].strip()
        elif line.startswith("## "):
            flush_para(para)
            head = line[3:].strip()
            num = re.match(r"(\d+(?:\.\d+)?)", head)
            sid = "s" + num.group(1).replace(".", "-") if num else "s-" + re.sub(r"\W+", "-", head.lower()).strip("-")
            cur = []
            sections.append((sid, head, cur))
        elif line.startswith("### "):
            flush_para(para)
            cur.append(f"<h3>{inline(line[4:].strip())}</h3>")
        elif line.strip() == "---":
            flush_para(para)
        elif line.startswith(">"):
            flush_para(para)
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i].lstrip("> ").strip())
                i += 1
            cur.append(f'<p class="callout">{inline(" ".join(buf))}</p>')
            continue
        elif line.startswith("|"):
            flush_para(para)
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            cur.append(render_table(rows))
            continue
        elif ITEM.match(line):
            flush_para(para)
            items = []
            while i < len(lines):
                m = ITEM.match(lines[i])
                if m:
                    items.append([len(m.group(1)), bool(m.group(2)), m.group(3).strip()])
                elif lines[i].strip() and lines[i].startswith(" ") and items:
                    items[-1][2] += " " + lines[i].strip()       # wrapped line of the same item
                else:
                    break
                i += 1
            cur.append(render_list(items, stem))
            continue
        elif not line.strip():
            flush_para(para)
        else:
            para.append(line)
        i += 1
    flush_para(para)
    return title, "".join(intro), [(s, h, "".join(c)) for s, h, c in sections]


# ---------- page shell ----------

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@500;600;700'
         '&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400'
         '&family=JetBrains+Mono:wght@400;600&display=swap">')

CSS = """
:root {
  --paper: #eef2f5; --plate: #ffffff; --ink: #17212c; --muted: #586777; --rule: #cfd8e1; --grid: #e3e9ef;
  --c1: #d06f12; --c2: #1f7f8f; --c3: #8a4bb3; --tint: #fff3cf; --qbg: #eaf5f7; --done: #2f8f4e;
  --display: "Familjen Grotesk", "Helvetica Neue", Arial, sans-serif;
  --body: "Source Serif 4", Georgia, "Times New Roman", serif;
  --mono: "JetBrains Mono", ui-monospace, Menlo, Consolas, monospace;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --paper: #0e1318; --plate: #151c24; --ink: #e5ecf2; --muted: #95a3b1; --rule: #2a3541; --grid: #1f2832;
    --c1: #f2a04e; --c2: #4cc4d6; --c3: #c592ea; --tint: #2a2412; --qbg: #12262b; --done: #5fcf83; color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --paper: #0e1318; --plate: #151c24; --ink: #e5ecf2; --muted: #95a3b1; --rule: #2a3541; --grid: #1f2832;
  --c1: #f2a04e; --c2: #4cc4d6; --c3: #c592ea; --tint: #2a2412; --qbg: #12262b; --done: #5fcf83; color-scheme: dark;
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--paper); color: var(--ink); font-family: var(--body); font-size: 17px; line-height: 1.6;
  padding: 28px max(16px, env(safe-area-inset-right, 0px)) 80px max(16px, env(safe-area-inset-left, 0px));
  background-image: linear-gradient(var(--grid) 1px, transparent 1px), linear-gradient(90deg, var(--grid) 1px, transparent 1px);
  background-size: 28px 28px;
}
.wrap { max-width: 860px; margin: 0 auto; display: grid; grid-template-columns: minmax(0, 1fr); gap: 24px; }
.wrap > *, .plate > * { min-width: 0; }
a { color: var(--c2); text-underline-offset: 2px; }
a.ext { word-break: break-word; }
a.book { color: var(--c3); font-weight: 600; }
.crumbs { font-family: var(--mono); font-size: 12px; display: flex; gap: 14px; flex-wrap: wrap; }
.kicker { font-family: var(--mono); font-size: 12px; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }
h1 { font-family: var(--display); font-size: clamp(30px, 5.5vw, 48px); line-height: 1.05; margin: 0; text-wrap: balance; }
h2 { font-family: var(--display); font-size: 22px; line-height: 1.25; margin: 0; }
h3 { font-family: var(--display); font-size: 18px; margin: 6px 0 0; }
header { display: grid; gap: 12px; }
header p, .intro p { margin: 0; max-width: 70ch; }
.progress { display: flex; align-items: center; gap: 12px; font-family: var(--mono); font-size: 13px; color: var(--muted); }
.bar { flex: 1; max-width: 320px; height: 8px; border-radius: 99px; background: var(--rule); overflow: hidden; }
.bar i { display: block; height: 100%; width: 0; background: var(--done); transition: width .3s; }
nav.toc { display: flex; flex-wrap: wrap; gap: 6px; }
nav.toc a { font-family: var(--mono); font-size: 12px; text-decoration: none; color: var(--ink); border: 1px solid var(--rule);
  background: var(--plate); border-radius: 99px; padding: 3px 10px; }
nav.toc a:hover { border-color: var(--c1); }
nav.toc a.full { border-color: var(--done); color: var(--done); }
.plate { background: var(--plate); border: 1px solid var(--rule); border-radius: 6px; padding: 20px clamp(14px, 3vw, 26px);
  display: grid; gap: 12px; scroll-margin-top: 16px; }
.plate-head { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; }
.chip { font-family: var(--mono); font-size: 12px; color: var(--muted); white-space: nowrap; border: 1px solid var(--rule);
  border-radius: 99px; padding: 1px 9px; }
.chip.full { color: var(--done); border-color: var(--done); }
.plate p { margin: 0; }
ul, ol { margin: 0; padding-left: 22px; }
li { margin: 3px 0; }
ul.topics { list-style: none; padding: 0; display: grid; gap: 2px; }
li.topic { display: grid; grid-template-columns: 26px 1fr; align-items: start; padding: 4px 6px; border-radius: 4px; margin: 0; }
li.topic:hover { background: var(--paper); }
li.topic > ul, li.topic > ol { grid-column: 2; }
input.tick { width: 18px; height: 18px; margin: 4px 0 0; accent-color: var(--done); cursor: pointer; }
li.topic > .src { grid-column: 2; font-size: 14px; line-height: 1.5; color: var(--muted); margin: 1px 0 4px;
  padding-left: 10px; border-left: 2px solid var(--rule); }
li.topic > .src a { color: var(--c2); }
li.topic > .src a.book { color: var(--c3); }
li.topic.on > span { color: var(--muted); text-decoration: line-through; text-decoration-color: var(--done); }
p.q { background: var(--qbg); border-left: 3px solid var(--c2); border-radius: 0 6px 6px 0; padding: 10px 14px; font-size: 16px; }
p.learn { background: var(--tint); border-left: 3px solid var(--c1); border-radius: 0 6px 6px 0; padding: 10px 14px; font-size: 16px; }
p.fmt, p.callout { color: var(--muted); font-style: italic; }
code { overflow-wrap: anywhere; font-family: var(--mono); font-size: .86em; background: var(--paper); border: 1px solid var(--rule); border-radius: 3px; padding: 0 4px; }
.tablewrap { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-size: 15px; }
th, td { text-align: left; padding: 6px 10px; border-bottom: 1px solid var(--rule); vertical-align: top; }
th { font-family: var(--display); }
ol.chapters { list-style: none; margin: 0; padding: 0; display: grid; gap: 10px; }
ol.chapters a { display: grid; grid-template-columns: 3em 1fr auto; gap: 2px 12px; align-items: center; padding: 12px 14px;
  border: 1px solid var(--rule); border-radius: 6px; color: inherit; text-decoration: none; background: var(--plate); }
ol.chapters a:hover, ol.chapters a:focus-visible { border-color: var(--c1); outline: none; }
.num { font-family: var(--mono); font-weight: 600; color: var(--c1); font-size: 20px; grid-row: span 2; }
.t { font-family: var(--display); font-weight: 600; font-size: 18px; line-height: 1.25; }
.d { color: var(--muted); font-size: 15px; grid-column: 2; }
.pc { font-family: var(--mono); font-size: 12px; color: var(--muted); grid-row: span 2; text-align: right; }
.pc.full { color: var(--done); }
.pager { display: flex; justify-content: space-between; gap: 12px; font-family: var(--mono); font-size: 13px; }
@media (max-width: 520px) { body { font-size: 16px; } .plate-head { flex-direction: column; gap: 4px; }
  ol.chapters a { grid-template-columns: 2.4em 1fr; } .pc { grid-row: auto; grid-column: 2; text-align: left; } }
@media print { nav.toc, .pager, .crumbs { display: none; } body { background: none; } }
"""

# Ticks live in localStorage only (per browser), keyed by page and by a hash of the topic text,
# so adding or reordering topics never moves a tick onto the wrong line.
PAGE_JS = """<script>
(function(){
  var key = 'itp:' + location.pathname.split('/').pop();
  var done = {};
  try { done = JSON.parse(localStorage.getItem(key) || '{}'); } catch (e) {}
  var boxes = [].slice.call(document.querySelectorAll('input.tick'));
  function paint(){
    var n = 0;
    boxes.forEach(function(b){ b.checked = !!done[b.dataset.k]; b.closest('li').classList.toggle('on', b.checked); if (b.checked) n++; });
    var pct = boxes.length ? Math.round(100 * n / boxes.length) : 0;
    var t = document.getElementById('progText'), bar = document.getElementById('progBar');
    if (t) t.textContent = n + ' / ' + boxes.length + ' topics done';
    if (bar) bar.style.width = pct + '%';
    document.querySelectorAll('section.plate').forEach(function(s){
      var all = s.querySelectorAll('input.tick'), on = s.querySelectorAll('input.tick:checked');
      var chip = s.querySelector('.chip'), link = document.querySelector('nav.toc a[href="#' + s.id + '"]');
      if (chip && all.length) { chip.textContent = on.length + '/' + all.length; chip.classList.toggle('full', on.length === all.length); }
      if (link) link.classList.toggle('full', all.length > 0 && on.length === all.length);
    });
  }
  boxes.forEach(function(b){ b.addEventListener('change', function(){
    if (b.checked) done[b.dataset.k] = 1; else delete done[b.dataset.k];
    try { localStorage.setItem(key, JSON.stringify(done)); } catch (e) {}
    paint();
  }); });
  paint();
})();
</script>"""

INDEX_JS = """<script>
(function(){
  document.querySelectorAll('[data-total]').forEach(function(el){
    var done = {};
    try { done = JSON.parse(localStorage.getItem('itp:' + el.dataset.page) || '{}'); } catch (e) {}
    var n = Object.keys(done).length, total = +el.dataset.total;
    el.textContent = Math.min(n, total) + ' / ' + total;
    el.classList.toggle('full', n >= total && total > 0);
  });
})();
</script>"""


def shell(title, body, script):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
{FONTS}
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
{body}
</div>
{script}
</body>
</html>
"""


def build():
    mds = sorted(f for f in os.listdir(HERE) if re.match(r"\d\d-.*\.md$", f))
    pages = [m for m in mds if not m.startswith("00-")]
    meta = {}
    for md in pages:
        text = open(os.path.join(HERE, md), encoding="utf-8").read()
        meta[md] = (parse(text, md[:-3])[0], text.count("- [ ]") + text.count("- [x]"))

    for idx, md in enumerate(pages):
        title, intro, sections = parse(open(os.path.join(HERE, md), encoding="utf-8").read(), md[:-3])
        toc = "".join(f'<a href="#{sid}">{html.escape(re.match(r"[0-9.]+", h).group(0) if re.match(r"[0-9.]+", h) else h[:18])}</a>'
                      for sid, h, _ in sections)
        plates = "".join(
            f'<section class="plate" id="{sid}"><div class="plate-head"><h2>{inline(h)}</h2>'
            f'<span class="chip"></span></div>{body}</section>' for sid, h, body in sections)
        prev_l = f'<a href="{out_name(pages[idx - 1])}">← {html.escape(meta[pages[idx - 1]][0])}</a>' if idx else "<span></span>"
        next_l = (f'<a href="{out_name(pages[idx + 1])}">{html.escape(meta[pages[idx + 1]][0])} →</a>'
                  if idx + 1 < len(pages) else "<span></span>")
        has_ticks = meta[md][1] > 0
        prog = ('<div class="progress"><div class="bar"><i id="progBar"></i></div><span id="progText"></span></div>'
                if has_ticks else "")
        body = f"""<div class="crumbs"><a href="index.html">← All interview topics</a><a href="13-sources.html">Sources</a></div>
<header>
  <div class="kicker">Interview prep · {md[:2]}</div>
  <h1>{inline(re.sub(r"^\d+\.\s*", "", title))}</h1>
  {prog}
  <div class="intro">{intro}</div>
  <nav class="toc" aria-label="Sections">{toc}</nav>
</header>
{plates}
<div class="pager">{prev_l}{next_l}</div>"""
        out = os.path.join(HERE, out_name(md))
        page = shell(re.sub(r"^\d+\.\s*", "", title).split(" — ")[0] + " · Interview prep", body, PAGE_JS)
        write(out, page)

    # index from the README: its intro and sections, with the file table replaced by cards
    readme = open(os.path.join(HERE, "00-README.md"), encoding="utf-8").read()
    rows = {}
    for line in readme.split("\n"):
        m = re.match(r"\|\s*([^|]*)\|\s*\[[^\]]*\]\(([^)]+\.md)\)\s*\|\s*([^|]*)\|\s*([^|]*)\|", line)
        if m:
            rows[m.group(2)] = (m.group(3).strip(), m.group(4).strip())
    cards = []
    for md in pages:
        pr, when = rows.get(md, ("", ""))
        title, total = meta[md]
        sub = " · ".join(x for x in (pr, when) if x and x != "—")
        pc = f'<span class="pc" data-page="{out_name(md)}" data-total="{total}"></span>' if total else '<span class="pc"></span>'
        cards.append(f'<li><a href="{out_name(md)}"><span class="num">{md[:2]}</span>'
                     f'<span class="t">{inline(re.sub(r"^\d+\.\s*", "", title))}</span>{pc}'
                     f'<span class="d">{inline(sub)}</span></a></li>')
    readme_wo_table = re.sub(r"(?m)^\|.*\n", "", readme)
    title, intro, sections = parse(readme_wo_table, "index")
    plates = "".join(f'<section class="plate" id="{sid}"><div class="plate-head"><h2>{inline(h)}</h2></div>{b}</section>'
                     for sid, h, b in sections)
    body = f"""<header>
  <div class="kicker">Interview prep · backend · system design · AI agents</div>
  <h1>{inline(title)}</h1>
  <div class="intro">{intro}</div>
</header>
<ol class="chapters">{"".join(cards)}</ol>
{plates}"""
    write(os.path.join(HERE, "index.html"), shell("Interview Topics", body, INDEX_JS))
    print(f"built {len(pages) + 1} pages in {HERE}")


def write(path, page):
    page = add_annotate(add_theme(page), path)
    with open(path, "w", encoding="utf-8") as f:
        f.write(page)


if __name__ == "__main__":
    build()
