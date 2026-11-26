"""Turn the interview-topic markdown files into study pages that look like the book pages.

The .md files (here, in Notes/career/sources/interview-topics/) stay the source; run this after editing any of them:
    python3 Notes/career/sources/interview-topics/build_pages.py
The pages are written to Notes/career/interview-topics/ (HTML only; their paths key the saved highlights, so keep them there).

Each NN-name.md becomes NN-name.html (00-README.md becomes index.html) with:
- the book pages' palette, fonts and light/dark switch (Notes/llm/theme_toggle.py),
- highlights + margin notes (Notes/assets/annotate/, saved by Notes/serve_notes.py),
- tickable topic checkboxes with progress, kept in this browser's localStorage ("itp:<page>"),
- "DDIA ch7", "AIE ch6" … linked to the matching study page in Notes/,
- note popups: a link to `notes/<name>.md` opens that markdown, rendered into the page at build time,
  in a popup with "Copy markdown" and a copy button on every code block (works from file:// too),
- questions under each point: sub-bullets that start with a level tag (`  - `L2` question ↳ hint`) are taken off
  the page and shown by the point's "Questions N" button in a popup with level filters, ticks ("itq:<page>",
  keyed by a hash of the question text) and copy; ticks made in the old question bank ("iqb:*") carry over,
- a spoken answer under a point (`  - **Answer:** paragraph ¶ paragraph`) is shown right under the point's line,
  always open, in an indented answer box; ` ¶ ` separates its paragraphs,
- every popup blurs the page behind it and takes highlights + notes of its own (scope "q:" or "n:" + its
  key, same .notes.json); they show only while that popup is open.
"""
import glob, hashlib, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))                      # sources: the .md files + notes/
NOTES = os.path.abspath(os.path.join(HERE, "..", "..", ".."))          # the Notes root
OUT = os.path.join(NOTES, "career", "interview-topics")                # the HTML pages you open
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
            pages[(key, n)] = os.path.relpath(f, OUT).replace(os.sep, "/")
    return pages


BOOKS = book_pages()

# The notes the page being built links to: id -> (title, raw markdown, rendered html). Reset per page.
USED_NOTES = {}
# The questions under each point of the page being built: point key -> {"t": point html, "q": [[key, level, html, hint]]}.
PAGE_QUESTIONS = {}
LEVEL = re.compile(r"`(L[123])`\s+")
ANSWER = re.compile(r"\*\*Answer:\*\*\s+")


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
        if url.startswith("notes/") and url.endswith(".md"):
            return stash(note_link(label, url))
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


def split_questions(lines):
    """
    Take the level-tagged questions and the **Answer:** sub-bullet off each tickable point.

    Returns:
        (kept items, {kept index: [question text]}, {kept index: answer text}).

    """
    kept, questions, answers, owner = [], {}, {}, None
    for indent, ordered, text in lines:
        if indent == 0:
            owner = len(kept) if re.match(r"\[( |x|X)\]\s+", text) else None
        elif owner is not None and LEVEL.match(text):
            questions.setdefault(owner, []).append(text)
            continue
        elif owner is not None and ANSWER.match(text):
            answers[owner] = ANSWER.sub("", text, count=1)
            continue
        kept.append([indent, ordered, text])
    return kept, questions, answers


def question_button(point_key, topic, questions):
    """Register a point's questions for the page and return the button that opens them."""
    rows = []
    for raw in questions:
        text, _, hint = raw.partition(" ↳ ")
        level = LEVEL.match(text).group(1)
        rows.append([hashlib.md5(text.strip().encode()).hexdigest()[:10], level,
                     inline(LEVEL.sub("", text, count=1).strip()), inline(hint.strip()) if hint.strip() else ""])
    PAGE_QUESTIONS[point_key] = {"t": inline(topic), "q": rows}
    return (f'<button type="button" class="qbtn" data-p="{point_key}">Questions '
            f'<span class="qn">{len(rows)}</span></button>')


def answer_block(answer):
    """A point's spoken answer, shown under the point's line: one <p> per ` ¶ `-separated paragraph."""
    paras = "".join(f"<p>{inline(p.strip())}</p>" for p in answer.split(" ¶ ") if p.strip())
    return f'<div class="ans"><div class="ans-label">Answer</div>{paras}</div>'


def render_list(lines, stem):
    """lines: list of (indent, ordered, text) items (continuations already joined)."""
    lines, questions, answers = split_questions(lines)
    out, stack = [], []           # stack of (indent, tag)
    for index, (indent, ordered, text) in enumerate(lines):
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
            asked = question_button(key, topic.strip(), questions[index]) if index in questions else ""
            said = answer_block(answers[index]) if index in answers else ""
            out.append(f'<li class="topic{" has-ans" if said else ""}"><input type="checkbox" class="tick" data-k="{key}" '
                       f'aria-label="Done"><span>{inline(topic.strip())}</span>{said}{src_html}{asked}')
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


# ---------- note popups ----------

def note_link(label, url):
    """Register the note a link points at (read and rendered once per page) and return the link that opens it."""
    note_id = re.sub(r"[^a-z0-9]+", "-", os.path.basename(url)[:-3].lower()).strip("-")
    if note_id not in USED_NOTES:
        raw = open(os.path.join(HERE, url), encoding="utf-8").read()
        title, body = render_note(raw)
        USED_NOTES[note_id] = (title or label, raw, body)
    return f'<a class="note-link" href="{html.escape(url)}" data-note="{note_id}">{inline(label)}</a>'


def render_note(md_text):
    """Render a whole note: headings, code fences, tables, lists, rules and paragraphs. Returns (title, html)."""
    lines = md_text.split("\n")
    title, out, para = "", [], []

    def flush():
        if para:
            out.append(f"<p>{inline(' '.join(s.strip() for s in para))}</p>")
            para.clear()

    i = 0
    while i < len(lines):
        line, bare = lines[i], lines[i].strip()
        heading = re.match(r"(#{1,4}) (.*)", line)
        if bare.startswith("```"):
            flush()
            code = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            out.append('<div class="codewrap"><button type="button" class="copy-code">Copy</button>'
                       f'<pre><code>{html.escape(chr(10).join(code))}</code></pre></div>')
        elif heading and len(heading.group(1)) == 1 and not title:
            flush()
            title = heading.group(2).strip()
        elif heading:
            flush()
            level = min(len(heading.group(1)) + 1, 4)
            out.append(f"<h{level}>{inline(heading.group(2).strip())}</h{level}>")
        elif bare == "---":
            flush()
            out.append("<hr>")
        elif bare.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip())
                i += 1
            out.append(render_table(rows))
            continue
        elif ITEM.match(line):
            flush()
            items = []
            while i < len(lines):
                m = ITEM.match(lines[i])
                if m:
                    items.append([len(m.group(1)), bool(m.group(2)), m.group(3).strip()])
                elif lines[i].startswith(" ") and lines[i].strip() and not lines[i].strip().startswith("|") and items:
                    items[-1][2] += " " + lines[i].strip()
                else:
                    break
                i += 1
            out.append(render_list(items, "note"))
            continue
        elif not bare:
            flush()
        else:
            para.append(line)
        i += 1
    flush()
    return title, "".join(out)


def note_dialogs():
    """One closed <dialog> per note the page links to, carrying its rendered body and its raw markdown for copying."""
    out = []
    for note_id, (title, raw, body) in USED_NOTES.items():
        source = json.dumps(raw).replace("</", "<\\/")
        out.append(
            f'<dialog class="note" id="note-{note_id}" aria-labelledby="note-{note_id}-t"><div class="note-inner">'
            f'<div class="note-head"><h2 id="note-{note_id}-t">{inline(title)}</h2>'
            '<button type="button" class="note-copy">Copy markdown</button>'
            '<button type="button" class="note-close" aria-label="Close">×</button></div>'
            f'<div class="note-body">{body}</div></div>'
            f'<script type="application/json" class="note-src">{source}</script></dialog>')
    return "".join(out)


def question_dialog():
    """The one popup every point's questions open in, with the page's questions as data; empty when it has none."""
    if not PAGE_QUESTIONS:
        return ""
    data = json.dumps(PAGE_QUESTIONS, ensure_ascii=False).replace("</", "<\\/")
    filters = "".join(f'<button type="button" data-lv="{lv}"{" class=\"on\"" if lv == "all" else ""}>'
                      f'{"All" if lv == "all" else lv} <b></b></button>' for lv in ("all", "L1", "L2", "L3"))
    return ('<dialog class="note qdlg" id="qdlg" aria-labelledby="qdlg-t"><div class="note-inner">'
            '<div class="note-head"><h2 id="qdlg-t"></h2>'
            '<button type="button" class="note-copy">Copy</button>'
            '<button type="button" class="note-close" aria-label="Close">×</button></div>'
            f'<div class="qbar">{filters}<span class="qprog"></span></div>'
            '<ol class="qlist note-body"></ol></div></dialog>'
            f'<script type="application/json" id="qdata">{data}</script>')


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
        if line.strip().startswith("```"):
            flush_para(para)
            code = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            cur.append(f'<pre class="example"><code>{html.escape(chr(10).join(code))}</code></pre>')
        elif line.startswith("# "):
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
  --c1: #d06f12; --c2: #1f7f8f; --c3: #8a4bb3; --tint: #fff3cf; --qbg: #eaf5f7; --abg: #f6f3fa; --done: #2f8f4e;
  --display: "Familjen Grotesk", "Helvetica Neue", Arial, sans-serif;
  --body: "Source Serif 4", Georgia, "Times New Roman", serif;
  --mono: "JetBrains Mono", ui-monospace, Menlo, Consolas, monospace;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --paper: #0e1318; --plate: #151c24; --ink: #e5ecf2; --muted: #95a3b1; --rule: #2a3541; --grid: #1f2832;
    --c1: #f2a04e; --c2: #4cc4d6; --c3: #c592ea; --tint: #2a2412; --qbg: #12262b; --abg: #1a1a24; --done: #5fcf83; color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --paper: #0e1318; --plate: #151c24; --ink: #e5ecf2; --muted: #95a3b1; --rule: #2a3541; --grid: #1f2832;
  --c1: #f2a04e; --c2: #4cc4d6; --c3: #c592ea; --tint: #2a2412; --qbg: #12262b; --abg: #1a1a24; --done: #5fcf83; color-scheme: dark;
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
li.topic { display: grid; grid-template-columns: 26px minmax(0, 1fr); align-items: start; padding: 4px 6px; border-radius: 4px; margin: 0; }
li.topic:hover { background: var(--paper); }
li.topic > ul, li.topic > ol { grid-column: 2; }
input.tick { width: 18px; height: 18px; margin: 4px 0 0; accent-color: var(--done); cursor: pointer; }
li.topic > .src { grid-column: 2; font-size: 14px; line-height: 1.5; color: var(--muted); margin: 1px 0 4px;
  padding-left: 10px; border-left: 2px solid var(--rule); overflow-wrap: anywhere; }
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
a.note-link { font-family: var(--mono); font-size: 13px; text-decoration: none; border: 1px solid var(--c2); border-radius: 99px;
  padding: 1px 10px; }
a.note-link::before { content: "📝 "; }
a.note-link:hover { background: var(--qbg); }
dialog.note { width: min(980px, 96vw); max-width: none; max-height: 92vh; padding: 0; border: 1px solid var(--rule);
  border-radius: 8px; background: var(--plate); color: var(--ink); }
dialog.note::backdrop { background: rgba(10, 15, 20, .35); -webkit-backdrop-filter: blur(6px); backdrop-filter: blur(6px); }
.note-inner { display: flex; flex-direction: column; max-height: 92vh; }
.note-head { display: flex; align-items: center; gap: 10px; padding: 12px 16px; border-bottom: 1px solid var(--rule); }
.note-head h2 { flex: 1; font-size: 18px; }
.note-head button, .copy-code { font-family: var(--mono); font-size: 12px; cursor: pointer; background: var(--paper);
  color: var(--ink); border: 1px solid var(--rule); border-radius: 4px; padding: 4px 10px; }
.note-head button:hover, .copy-code:hover { border-color: var(--c2); }
.note-head .note-close { font-size: 18px; line-height: 1; padding: 2px 10px; }
.note-body { position: relative; overflow: auto; padding: 16px clamp(14px, 3vw, 24px) 28px; display: grid; gap: 12px; }
@media (min-width: 760px) { dialog.note { width: min(1240px, calc(100vw - 152px)); } }
@media (min-width: 900px) { .note-body.ann-scope { padding-right: 300px; } }
.note-body > * { min-width: 0; }
.note-body p { margin: 0; }
.note-body h3 { font-family: var(--display); font-size: 20px; margin: 10px 0 0; }
.note-body h4 { font-family: var(--display); font-size: 17px; margin: 4px 0 0; }
.note-body hr { border: 0; border-top: 1px solid var(--rule); width: 100%; margin: 6px 0; }
.codewrap { position: relative; }
.copy-code { position: absolute; top: 6px; right: 6px; }
.note-body pre { margin: 0; overflow-x: auto; background: var(--paper); border: 1px solid var(--rule); border-radius: 6px;
  padding: 12px; }
.note-body pre code { border: 0; background: none; padding: 0; font-size: 12px; line-height: 1.35; white-space: pre;
  overflow-wrap: normal; }
pre.example { margin: 0; overflow-x: auto; background: var(--paper); border: 1px solid var(--rule); border-radius: 6px;
  padding: 12px; }
pre.example code { border: 0; background: none; padding: 0; white-space: pre; overflow-wrap: normal; }
li.topic > .qbtn { grid-column: 2; justify-self: start; margin: 2px 0 6px; font-family: var(--mono); font-size: 12px;
  cursor: pointer; color: var(--c2); background: var(--plate); border: 1px solid var(--c2); border-radius: 99px;
  padding: 2px 11px; }
li.topic > .qbtn:hover { background: var(--qbg); }
li.topic > .qbtn.full { color: var(--done); border-color: var(--done); }
li.topic.has-ans { padding-bottom: 10px; }
li.topic.has-ans:hover { background: none; }
li.topic > .ans { grid-column: 2; min-width: 0; margin: 8px 0 6px; padding: 10px 16px 12px; background: var(--abg);
  border-left: 3px solid var(--c3); border-radius: 0 6px 6px 0; font-size: 16px; line-height: 1.65; display: grid; gap: 10px; }
li.topic > .ans p { margin: 0; max-width: 72ch; }
.ans-label { font-family: var(--mono); font-size: 11px; letter-spacing: .08em; text-transform: uppercase; color: var(--c3);
  margin-bottom: -4px; }
@media (max-width: 520px) { li.topic > .ans { padding: 8px 12px 10px; margin-left: -20px; } }
.qbar { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; padding: 8px 16px;
  border-bottom: 1px solid var(--rule); }
.qbar button { font-family: var(--mono); font-size: 12px; cursor: pointer; color: var(--ink); background: var(--paper);
  border: 1px solid var(--rule); border-radius: 99px; padding: 2px 10px; }
.qbar button.on { border-color: var(--c2); color: var(--c2); }
.qbar b { font-weight: 400; color: var(--muted); }
.qprog { margin-left: auto; font-family: var(--mono); font-size: 12px; color: var(--muted); }
ol.qlist { list-style: none; margin: 0; display: grid; gap: 2px; align-content: start; }
li.qitem { display: grid; grid-template-columns: 26px 1fr; align-items: start; padding: 6px; border-radius: 4px; margin: 0; }
li.qitem:hover { background: var(--paper); }
li.qitem.on .qt { color: var(--muted); text-decoration: line-through; text-decoration-color: var(--done); }
.qh { font-size: 14px; color: var(--muted); margin-top: 2px; }
input.qtick { width: 18px; height: 18px; margin: 4px 0 0; accent-color: var(--done); cursor: pointer; }
code.lv { font-weight: 600; font-size: 11px; border-radius: 99px; padding: 1px 7px; margin-right: 6px; vertical-align: 1px;
  border: 0; }
code.l1 { background: #d9f0e0; color: #1d6b37; }
code.l2 { background: #fdebc8; color: #8a5300; }
code.l3 { background: #f6dbe4; color: #9b1c4a; }
:root[data-theme="dark"] code.l1 { background: #163a24; color: #7fe0a0; }
:root[data-theme="dark"] code.l2 { background: #3a2b10; color: #f5c46b; }
:root[data-theme="dark"] code.l3 { background: #3d1826; color: #f39ab9; }
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) code.l1 { background: #163a24; color: #7fe0a0; }
  :root:not([data-theme="light"]) code.l2 { background: #3a2b10; color: #f5c46b; }
  :root:not([data-theme="light"]) code.l3 { background: #3d1826; color: #f39ab9; }
}
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

# A modal dialog makes the rest of the page inert, so the copy fallback's textarea goes inside the open dialog.
POPUP_JS = """<script>
(function(){
  var page = location.pathname.split('/').pop();
  var dataEl = document.getElementById('qdata');
  var points = dataEl ? JSON.parse(dataEl.textContent) : {};
  var store = 'itq:' + page, done = {};
  try { done = JSON.parse(localStorage.getItem(store) || '{}'); } catch (e) {}
  // Ticks made in the old question bank pages are keyed the same way, so they carry over here.
  try {
    var old = {};
    for (var i = 0; i < localStorage.length; i++) {
      var k = localStorage.key(i);
      if (k && k.indexOf('iqb:') === 0) { var o = JSON.parse(localStorage.getItem(k) || '{}'); for (var h in o) old[h] = 1; }
    }
    var moved = false;
    Object.keys(points).forEach(function(p){ points[p].q.forEach(function(q){ if (old[q[0]] && !done[q[0]]) { done[q[0]] = 1; moved = true; } }); });
    if (moved) localStorage.setItem(store, JSON.stringify(done));
  } catch (e) {}
  function save(){ try { localStorage.setItem(store, JSON.stringify(done)); } catch (e) {} }
  function count(p){ var q = points[p].q, n = 0; q.forEach(function(r){ if (done[r[0]]) n++; }); return n; }
  function paintButtons(){
    document.querySelectorAll('button.qbtn').forEach(function(b){
      var p = b.dataset.p, all = points[p].q.length, n = count(p);
      b.querySelector('.qn').textContent = n ? n + '/' + all : all;
      b.classList.toggle('full', n === all);
    });
  }
  var dlg = document.getElementById('qdlg'), current = null, level = 'all';
  function paintDialog(){
    var rows = points[current].q, list = dlg.querySelector('.qlist'), n = 0, counts = { all: rows.length, L1: 0, L2: 0, L3: 0 };
    list.innerHTML = '';
    rows.forEach(function(r){
      counts[r[1]]++;
      if (level !== 'all' && r[1] !== level) return;
      var li = document.createElement('li');
      li.className = 'qitem' + (done[r[0]] ? ' on' : '');
      li.innerHTML = '<input type="checkbox" class="qtick" aria-label="Answered"' + (done[r[0]] ? ' checked' : '') + '>'
        + '<div><code class="lv ' + r[1].toLowerCase() + '">' + r[1] + '</code><span class="qt">' + r[2] + '</span>'
        + (r[3] ? '<div class="qh">' + r[3] + '</div>' : '') + '</div>';
      li.querySelector('input').addEventListener('change', function(e){
        if (e.target.checked) done[r[0]] = 1; else delete done[r[0]];
        li.classList.toggle('on', e.target.checked); save(); paintProgress(); paintButtons();
      });
      list.appendChild(li);
    });
    dlg.querySelectorAll('.qbar button').forEach(function(b){
      b.classList.toggle('on', b.dataset.lv === level);
      b.querySelector('b').textContent = counts[b.dataset.lv];
      b.hidden = b.dataset.lv !== 'all' && !counts[b.dataset.lv];
    });
    paintProgress();
  }
  function paintProgress(){ dlg.querySelector('.qprog').textContent = count(current) + ' / ' + points[current].q.length + ' answered'; }
  function questionsText(){
    return [].map.call(dlg.querySelectorAll('.qitem'), function(li, i){
      var hint = li.querySelector('.qh');
      return (i + 1) + '. [' + li.querySelector('.lv').textContent + '] ' + li.querySelector('.qt').textContent + (hint ? ' (' + hint.textContent + ')' : '');
    }).join('\\n');
  }
  function flash(btn, text){ var was = btn.textContent; btn.textContent = text; setTimeout(function(){ btn.textContent = was; }, 1400); }
  function copy(text, btn){
    function legacy(){
      var ta = document.createElement('textarea');
      ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.top = '-1000px';
      (btn.closest('dialog') || document.body).appendChild(ta); ta.select();
      var ok = false; try { ok = document.execCommand('copy'); } catch (e) {}
      ta.remove(); flash(btn, ok ? 'Copied' : 'Copy failed');
    }
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(function(){ flash(btn, 'Copied'); }, legacy);
    else legacy();
  }
  // annotate.js loads late (defer + its stylesheet), so it is looked up at open time, not here.
  function annotate(body, key){ if (window.__ann && window.__ann.scope) window.__ann.scope(body, key); }
  // The close event can land after the popup was opened again, so only a still-closed popup gives its notes back.
  function release(d){ if (!d.open && window.__ann && window.__ann.unscope) window.__ann.unscope(d); }
  document.querySelectorAll('dialog.note').forEach(function(d){ d.addEventListener('close', function(){ release(d); }); });
  paintButtons();
  document.addEventListener('click', function(e){
    var link = e.target.closest('a.note-link');
    if (link) {
      var opened = document.getElementById('note-' + link.dataset.note);
      if (opened && opened.showModal) {
        e.preventDefault(); opened.showModal(); opened.querySelector('.note-body').scrollTop = 0;
        annotate(opened.querySelector('.note-body'), 'n:' + link.dataset.note);
      }
      return;
    }
    var asked = e.target.closest('button.qbtn');
    if (asked && dlg) {
      current = asked.dataset.p; level = 'all';
      dlg.querySelector('#qdlg-t').innerHTML = points[current].t;
      paintDialog(); dlg.showModal(); dlg.querySelector('.qlist').scrollTop = 0;
      annotate(dlg.querySelector('.qlist'), 'q:' + current);
      return;
    }
    var open = e.target.closest('dialog.note');
    if (!open) return;
    if (e.target === open || e.target.closest('.note-close')) { open.close(); release(open); return; }
    var filter = e.target.closest('.qbar button');
    if (filter) { level = filter.dataset.lv; paintDialog(); annotate(dlg.querySelector('.qlist'), 'q:' + current); return; }
    var whole = e.target.closest('.note-copy');
    if (whole) {
      var text = open === dlg ? questionsText() : JSON.parse(open.querySelector('.note-src').textContent);
      copy(text, whole); return;
    }
    var block = e.target.closest('.copy-code');
    if (block) copy(block.nextElementSibling.textContent, block);
  });
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
        meta[md] = (parse(text, md[:-3])[0], text.count("- [ ]") + text.count("- [x]"),
                    len(re.findall(r"(?m)^\s+- `L[123]` ", text)))

    for idx, md in enumerate(pages):
        USED_NOTES.clear()
        PAGE_QUESTIONS.clear()
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
<div class="pager">{prev_l}{next_l}</div>{note_dialogs()}{question_dialog()}"""
        out = os.path.join(OUT, out_name(md))
        script = PAGE_JS + POPUP_JS if USED_NOTES or PAGE_QUESTIONS else PAGE_JS
        page = shell(re.sub(r"^\d+\.\s*", "", title).split(" — ")[0] + " · Interview prep", body, script)
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
        title, total, asked = meta[md]
        sub = " · ".join(x for x in (pr, when, f"{asked:,} questions" if asked else "") if x and x != "—")
        pc = f'<span class="pc" data-page="{out_name(md)}" data-total="{total}"></span>' if total else '<span class="pc"></span>'
        cards.append(f'<li><a href="{out_name(md)}"><span class="num">{md[:2]}</span>'
                     f'<span class="t">{inline(re.sub(r"^\d+\.\s*", "", title))}</span>{pc}'
                     f'<span class="d">{inline(sub)}</span></a></li>')
    readme_wo_table = re.sub(r"(?m)^\|.*\n", "", readme)
    USED_NOTES.clear()
    PAGE_QUESTIONS.clear()
    title, intro, sections = parse(readme_wo_table, "index")
    plates = "".join(f'<section class="plate" id="{sid}"><div class="plate-head"><h2>{inline(h)}</h2></div>{b}</section>'
                     for sid, h, b in sections)
    body = f"""<header>
  <div class="kicker">Interview prep · backend · system design · AI agents</div>
  <h1>{inline(title)}</h1>
  <div class="intro">{intro}</div>
</header>
<ol class="chapters">{"".join(cards)}</ol>
{plates}{note_dialogs()}{question_dialog()}"""
    script = INDEX_JS + POPUP_JS if USED_NOTES or PAGE_QUESTIONS else INDEX_JS
    write(os.path.join(OUT, "index.html"), shell("Interview Topics", body, script))
    print(f"built {len(pages) + 1} pages in {OUT}")


def write(path, page):
    page = add_annotate(add_theme(page), path)
    with open(path, "w", encoding="utf-8") as f:
        f.write(page)


if __name__ == "__main__":
    build()
