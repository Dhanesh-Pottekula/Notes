"""Build the interview question bank pages from the .md files in this folder.

    python3 Notes/career/interview-questions/build.py

- NN-name.md   → NN-name.html (one topic, every question, grouped by sub-topic)
- 00-README.md → index.html   (cards for every topic, with question counts and your progress)
- all .md      → all.html     (every question from every topic on one page, with search and level filters)

Markdown parsing, page shell, palette, light/dark switch and highlights/notes are reused from
../interview-topics/build_pages.py so both folders look the same. Format rules: FORMAT.md.

Ticks are kept in this browser's localStorage under "iqb:<page>.html", keyed by a hash of the question text,
so a tick shows on the topic page and on all.html alike, and editing other questions never moves it.
"""
import html, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "interview-topics"))
import build_pages as bp   # noqa: E402

inline, parse, shell, write = bp.inline, bp.parse, bp.shell, bp.write

bp.CSS += """
code.lv { font-weight: 600; font-size: 11px; border-radius: 99px; padding: 1px 7px; margin-right: 6px; vertical-align: 1px; border: 0; }
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
.tools { position: sticky; top: 0; z-index: 5; display: flex; flex-wrap: wrap; gap: 8px; align-items: center;
  background: var(--paper); padding: 8px 0; border-bottom: 1px solid var(--rule); }
.tools input[type=search] { flex: 1 1 220px; min-width: 0; font: inherit; font-size: 15px; padding: 6px 10px;
  border: 1px solid var(--rule); border-radius: 6px; background: var(--plate); color: var(--ink); }
.tools button { font-family: var(--mono); font-size: 12px; padding: 4px 10px; border-radius: 99px; cursor: pointer;
  border: 1px solid var(--rule); background: var(--plate); color: var(--ink); }
.tools button.on { border-color: var(--c1); color: var(--c1); font-weight: 600; }
.tools .shown { font-family: var(--mono); font-size: 12px; color: var(--muted); }
.filehead { margin-top: 18px; padding: 14px 0 4px; border-top: 3px solid var(--c1); scroll-margin-top: 60px; }
.filehead h2 { font-size: 28px; }
.filehead a { font-family: var(--mono); font-size: 12px; }
.stats { font-family: var(--mono); font-size: 13px; color: var(--muted); }
.hide { display: none !important; }
"""

TOOLS = """<div class="tools" role="search">
  <input type="search" id="q" placeholder="Search questions…" aria-label="Search questions">
  <button data-lv="" class="on">All</button><button data-lv="L1">L1</button><button data-lv="L2">L2</button>
  <button data-lv="L3">L3</button><button data-lv="todo">Not ticked</button>
  <span class="shown" id="shown"></span>
</div>"""

# One script for topic pages and all.html: ticks are stored per source page (section[data-page]).
PAGE_JS = """<script>
(function(){
  var stores = {};
  function store(p){ if (!stores[p]) { try { stores[p] = JSON.parse(localStorage.getItem('iqb:' + p) || '{}'); } catch (e) { stores[p] = {}; } } return stores[p]; }
  function save(p){ try { localStorage.setItem('iqb:' + p, JSON.stringify(stores[p])); } catch (e) {} }
  var boxes = [].slice.call(document.querySelectorAll('input.tick'));
  boxes.forEach(function(b){ b.dataset.p = b.closest('section').dataset.page; });
  function paint(){
    var n = 0;
    boxes.forEach(function(b){ b.checked = !!store(b.dataset.p)[b.dataset.k]; b.closest('li').classList.toggle('on', b.checked); if (b.checked) n++; });
    var t = document.getElementById('progText'), bar = document.getElementById('progBar');
    if (t) t.textContent = n + ' / ' + boxes.length + ' questions ticked';
    if (bar) bar.style.width = (boxes.length ? Math.round(100 * n / boxes.length) : 0) + '%';
    document.querySelectorAll('section.plate').forEach(function(s){
      var all = s.querySelectorAll('input.tick'), on = s.querySelectorAll('input.tick:checked');
      var chip = s.querySelector('.chip'), link = document.querySelector('nav.toc a[href="#' + s.id + '"]');
      if (chip && all.length) { chip.textContent = on.length + '/' + all.length; chip.classList.toggle('full', on.length === all.length); }
      if (link) link.classList.toggle('full', all.length > 0 && on.length === all.length);
    });
  }
  boxes.forEach(function(b){ b.addEventListener('change', function(){
    var s = store(b.dataset.p);
    if (b.checked) s[b.dataset.k] = 1; else delete s[b.dataset.k];
    save(b.dataset.p); paint(); filter();
  }); });
  var q = document.getElementById('q'), lv = '', btns = [].slice.call(document.querySelectorAll('.tools button'));
  var items = [].slice.call(document.querySelectorAll('li.topic')).map(function(li){
    var c = li.querySelector('code.lv');
    return { li: li, text: li.textContent.toLowerCase(), lv: c ? c.textContent : '' };
  });
  function filter(){
    var words = (q && q.value || '').toLowerCase().split(/\\s+/).filter(Boolean), shown = 0;
    items.forEach(function(it){
      var ok = words.every(function(w){ return it.text.indexOf(w) >= 0; });
      if (ok && lv === 'todo') ok = !it.li.classList.contains('on');
      else if (ok && lv) ok = it.lv === lv;
      it.li.classList.toggle('hide', !ok); if (ok) shown++;
    });
    var active = words.length || lv;
    document.querySelectorAll('section.plate').forEach(function(s){
      var any = s.querySelector('li.topic:not(.hide)');
      s.classList.toggle('hide', !!active && !any);
    });
    document.querySelectorAll('.filehead').forEach(function(h){
      var any = document.querySelector('section.plate[data-page="' + h.dataset.page + '"]:not(.hide)');
      h.classList.toggle('hide', !!active && !any);
    });
    var el = document.getElementById('shown');
    if (el) el.textContent = active ? shown + ' shown' : items.length + ' questions';
  }
  if (q) q.addEventListener('input', filter);
  btns.forEach(function(b){ b.addEventListener('click', function(){
    lv = b.dataset.lv; btns.forEach(function(x){ x.classList.toggle('on', x === b); }); filter();
  }); });
  paint(); filter();
})();
</script>"""

INDEX_JS = """<script>
(function(){
  document.querySelectorAll('[data-total]').forEach(function(el){
    var done = {};
    try { done = JSON.parse(localStorage.getItem('iqb:' + el.dataset.page) || '{}'); } catch (e) {}
    var n = Object.keys(done).length, total = +el.dataset.total;
    el.textContent = Math.min(n, total) + ' / ' + total;
    el.classList.toggle('full', n >= total && total > 0);
  });
})();
</script>"""


def levels(page):
    return re.sub(r"<code>(L[123])</code>", lambda m: f'<code class="lv {m.group(1).lower()}">{m.group(1)}</code>', page)


def out_name(md):
    return "index.html" if md.startswith("00-") else md[:-3] + ".html"


def plain_title(title):
    return re.sub(r"^\d+\.\s*", "", title)


def count(text):
    return {k: len(re.findall(rf"(?m)^- \[[ xX]\] `{k}`", text)) for k in ("L1", "L2", "L3")} | {
        "all": len(re.findall(r"(?m)^- \[[ xX]\] ", text))}


def plates(md, sections, prefix=""):
    page = out_name(md)
    return "".join(
        f'<section class="plate" id="{prefix}{sid}" data-page="{page}"><div class="plate-head"><h2>{inline(h)}</h2>'
        f'<span class="chip"></span></div>{body}</section>' for sid, h, body in sections)


def toc(sections, prefix=""):
    out = []
    for sid, h, _ in sections:
        m = re.match(r"[0-9.]+", h)
        label = m.group(0) if m else h[:18]
        out.append(f'<a href="#{prefix}{sid}" title="{html.escape(h)}">{html.escape(label)}</a>')
    return "".join(out)


def build():
    mds = sorted(f for f in os.listdir(HERE) if re.match(r"\d\d-.*\.md$", f) and not f.startswith("00-"))
    data = {}
    for md in mds:
        text = open(os.path.join(HERE, md), encoding="utf-8").read()
        title, intro, sections = parse(text, md[:-3])
        data[md] = (title, intro, sections, count(text))

    progress = ('<div class="progress"><div class="bar"><i id="progBar"></i></div><span id="progText"></span></div>')
    for i, md in enumerate(mds):
        title, intro, sections, c = data[md]
        prev_l = f'<a href="{out_name(mds[i - 1])}">← {html.escape(plain_title(data[mds[i - 1]][0]))}</a>' if i else "<span></span>"
        next_l = (f'<a href="{out_name(mds[i + 1])}">{html.escape(plain_title(data[mds[i + 1]][0]))} →</a>'
                  if i + 1 < len(mds) else "<span></span>")
        body = f"""<div class="crumbs"><a href="index.html">← All topics</a><a href="all.html">All questions on one page</a><a href="../interview-topics/index.html">Topic checklists</a></div>
<header>
  <div class="kicker">Interview questions · {md[:2]}</div>
  <h1>{inline(plain_title(title))}</h1>
  <div class="stats">{c['all']} questions · L1 {c['L1']} · L2 {c['L2']} · L3 {c['L3']} · {len(sections)} sub-topics</div>
  {progress}
  <div class="intro">{intro}</div>
  <nav class="toc" aria-label="Sub-topics">{toc(sections)}</nav>
</header>
{TOOLS}
{plates(md, sections)}
<div class="pager">{prev_l}{next_l}</div>"""
        write(os.path.join(HERE, out_name(md)),
              levels(shell(plain_title(title).split(" — ")[0] + " · Interview questions", body, PAGE_JS)))

    # all.html: every topic, one after another
    total = {k: sum(d[3][k] for d in data.values()) for k in ("all", "L1", "L2", "L3")}
    parts, nav = [], []
    for md in mds:
        title, intro, sections, c = data[md]
        stem = md[:-3]
        nav.append(f'<a href="#f-{stem}" title="{html.escape(plain_title(title))}">{md[:2]} {html.escape(plain_title(title).split(" — ")[0])}</a>')
        parts.append(f'<div class="filehead" id="f-{stem}" data-page="{out_name(md)}"><h2>{inline(title)}</h2>'
                     f'<a href="{out_name(md)}">open this topic alone →</a> '
                     f'<span class="stats">· {c["all"]} questions</span></div>'
                     + plates(md, sections, prefix=stem + "-"))
    body = f"""<div class="crumbs"><a href="index.html">← All topics</a><a href="../interview-topics/index.html">Topic checklists</a></div>
<header>
  <div class="kicker">Interview questions · everything on one page</div>
  <h1>All interview questions</h1>
  <div class="stats">{total['all']} questions in {len(mds)} topics · L1 {total['L1']} · L2 {total['L2']} · L3 {total['L3']}</div>
  {progress}
  <nav class="toc" aria-label="Topics">{"".join(nav)}</nav>
</header>
{TOOLS}
{"".join(parts)}"""
    write(os.path.join(HERE, "all.html"), levels(shell("All Interview Questions", body, PAGE_JS)))

    # index.html from the README: cards replace the file table
    readme = open(os.path.join(HERE, "00-README.md"), encoding="utf-8").read()
    area = {}
    for line in readme.split("\n"):
        m = re.match(r"\|\s*\d+\s*\|\s*\[[^\]]*\]\(([^)]+\.md)\)\s*\|\s*([^|]*)\|", line)
        if m:
            area[m.group(1)] = m.group(2).strip()
    cards = []
    for md in mds:
        title, _, sections, c = data[md]
        sub = f"{area.get(md, '')} · {c['all']} questions · {len(sections)} sub-topics"
        cards.append(f'<li><a href="{out_name(md)}"><span class="num">{md[:2]}</span>'
                     f'<span class="t">{inline(plain_title(title))}</span>'
                     f'<span class="pc" data-page="{out_name(md)}" data-total="{c["all"]}"></span>'
                     f'<span class="d">{inline(sub)}</span></a></li>')
    missing = [r for r in area if r not in data]
    title, intro, sections = parse(re.sub(r"(?m)^\|.*\n", "", readme), "index")
    readme_plates = "".join(f'<section class="plate" id="{sid}"><div class="plate-head"><h2>{inline(h)}</h2></div>{b}</section>'
                            for sid, h, b in sections)
    body = f"""<header>
  <div class="kicker">Interview prep · backend · system design · AI agents and harnesses</div>
  <h1>{inline(title)}</h1>
  <div class="stats">{total['all']} questions in {len(mds)} topics · L1 {total['L1']} · L2 {total['L2']} · L3 {total['L3']}</div>
  <div class="intro">{intro}</div>
  <p><a href="all.html"><strong>Open every question on one page (search + filters) →</strong></a></p>
</header>
{readme_plates[:readme_plates.find('</section>') + 10]}
<ol class="chapters">{"".join(cards)}</ol>
{readme_plates[readme_plates.find('</section>') + 10:]}"""
    write(os.path.join(HERE, "index.html"), levels(shell("Interview Question Bank", body, INDEX_JS)))
    print(f"built {len(mds)} topic pages + all.html + index.html: {total['all']} questions "
          f"(L1 {total['L1']}, L2 {total['L2']}, L3 {total['L3']})")
    if missing:
        print("README lists files that do not exist yet:", ", ".join(missing))


if __name__ == "__main__":
    build()
