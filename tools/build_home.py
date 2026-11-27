#!/usr/bin/env python3
"""Build Notes/index.html: one home page that links every study page you read.

    python3 Notes/tools/build_home.py    # then open http://127.0.0.1:8780/ (python3 Notes/serve_notes.py)

Run it again after adding a book, a chapter or a page. What it does:
- SECTIONS below lists the shelves by hand (a book folder or a single page, with a one-line description).
  Anything listed that is not on disk is skipped and reported, so nothing links to a missing page.
- A book folder links to its own index.html (or its first chapter when it has none) and expands to every
  chNN_*.html in it, titled by the chapter's <h1>, so new chapters appear without editing this file.
- Every other .html under Notes that no shelf covers is listed under "Other pages", so no page is ever
  unreachable from here. Give it a proper shelf by adding it to SECTIONS.
- Same look as the book index pages (DDIA index styles + the light/dark switch from tools/theme_toggle.py).
"""
import glob, html, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)                       # the Notes root; this script lives in Notes/tools/
sys.path.insert(0, HERE)
from theme_toggle import add_theme  # noqa: E402

OUT = os.path.join(NOTES, "index.html")
HEAD = open(os.path.join(NOTES, "system_design", "ddia", "index.html"), encoding="utf-8").read()
STYLE = HEAD[HEAD.index("<style>"):HEAD.index("</style>") + 8]
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="stylesheet" '
         'href="https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@500;600;700&family=Source+Serif+4:'
         'ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=JetBrains+Mono:wght@400;600&display=swap">')

# Folders that hold page parts, not pages (pictures, figures, the shared highlight script, build sources).
SKIP_DIRS = {".git", "_site", "illus", "figs", "assets", "tools", "practice", "sources", "node_modules"}

# (shelf title, one line about the shelf, [(path from Notes root, title, description)]).
# A path ending in "/" is a book folder of chNN_*.html pages; anything else is one page.
SECTIONS = [
    ("Start here", "The plan, and the interview prep it leads to.", [
        ("syllabus.html", "6-month backend roadmap",
         "Month by month: DSA ↔ real systems, V8, event loop, TypeScript, PostgreSQL, Redis, system design, Kafka, AI infra, Docker, Linux, Kubernetes, CI/CD."),
        ("career/interview-topics/", "Interview prep, topic by topic",
         "14 topics, ~1,140 tickable points and ~12,460 L1/L2/L3 questions in popups; spoken answers for your own projects; sources per topic."),
    ]),
    ("AI engineering and LLMs", "Read in this order: how LLMs work → building AI apps → one full production system.", [
        ("llm/hands_on_llms/", "Hands-On Large Language Models",
         "Alammar & Grootendorst. Tokens, embeddings, attention, then prompting, agents, RAG and fine-tuning."),
        ("llm/ai_engineering/", "AI Engineering",
         "Chip Huyen. Evaluation, prompting, RAG and agents, finetuning, inference optimization, production architecture."),
        ("llm/llm_engineers_handbook/", "LLM Engineer's Handbook",
         "Iusztin & Labonne. One end-to-end LLM system: data, RAG pipelines, SFT/DPO, evaluation, deployment, LLMOps."),
    ]),
    ("System design and databases", "How data systems work, from the API down to the disk.", [
        ("system_design/ddia/", "Designing Data-Intensive Applications",
         "Kleppmann. Data models, storage, encoding, replication, partitioning, transactions, consensus, streams."),
        ("system_design/database_internals/", "Database Internals",
         "Petrov. B-trees, file formats, recovery, LSM trees, then distributed systems: failure detection, replication, consensus."),
    ]),
    ("Programming", "Language and framework notes.", [
        ("programming/python/web-frameworks.html", "Python web frameworks",
         "Django vs Flask vs FastAPI vs Starlette, WSGI vs ASGI, async/await, Pydantic, when to use which."),
        ("programming/javascript/js_notes.html", "JavaScript fundamentals",
         "Data types, type conversion and the core language rules, as a cheat-sheet."),
        ("programming/docker/docker_commands.html", "AWS and Docker set-up commands",
         "SSH into EC2, install Docker, build, run and clean up containers."),
        ("programming/linux/shell_scripting.html", "Shell scripting notes",
         "Everyday Linux commands and shell script basics, one line each."),
    ]),
    ("VLSI physical verification", "From running DRC/LVS to owning sign-off, and the scripting that gets you there.", [
        ("vlsi/tcl_perl_pv/", "Tcl and Perl for physical verification",
         "The whole PV roadmap (DRC, LVS, antenna, ERC, tape-out) plus a 12-week scripting plan: Tcl, Perl, Innovus dbGet, Calibre automation, 16 tested scripts, interview questions."),
    ]),
    ("Trading", "Chart reading, the trader's mindset, and the maths behind sizing and risk.", [
        ("trading/forex/index.html", "Forex learning roadmap",
         "8 phases from set-up to a live track record, 200+ checked resources, base rates on who actually profits."),
        ("trading/murphy/", "Technical Analysis of the Financial Markets",
         "John Murphy. Dow theory, trends, patterns, volume, moving averages, oscillators, candlesticks, intermarket."),
        ("trading/grimes/", "The Art and Science of Trading",
         "Adam Grimes (course workbook). Chartreading, market structure, pullbacks, failure tests, breakouts, psychology, quant tools."),
        ("trading/carter/", "Mastering the Trade",
         "John Carter. What moves markets, trader psychology, and concrete intraday and swing setups."),
        ("trading/wyckoff/", "Wyckoff 2.0", "Ruben Villahermosa. Accumulation, distribution and volume profile."),
        ("trading/murphy_moving_averages_visual.html", "Murphy's moving averages, interactive",
         "The moving-averages chapter as 20 live charts: lag, SMA/WMA/EMA, crossover systems with costs, Bollinger."),
        ("trading/trading_equations.html", "Trader's equation sheet",
         "19 formulas (expectancy, Sharpe, Kelly, ATR, GARCH, Black–Scholes, OU…) with calculators."),
        ("trading/concepts/", "Trading concepts",
         "My notes: order flow, VWAP and volume profile, trendlines, index funds, how to sell, the equations and how to use them."),
        ("trading/indicators/", "Indicators",
         "KAMA (Kaufman adaptive moving average) and tools that tell a trend from a sideways market."),
        ("trading/strategies/", "Strategies",
         "The playbooks: intraday and swing, Stoch RSI + MACD, strategies by timeframe and from the equations, Strategy 5 set-up."),
        ("trading/backtests/", "Backtest results",
         "Every backtest write-up: Strategy 2 and Strategy 5 on Nifty 50 names, settings sweeps, delivery and intraday variants."),
        ("trading/forex/forex_learning_path.html", "Forex learning path (text version)",
         "The roadmap as one long note: phases, resources, US set-up, backtesting."),
        ("trading/forex/smc_order_flow_research.html", "Smart-money concepts and order flow research",
         "What the evidence says about SMC and order-flow trading."),
    ]),
    ("Product thinking", "Problems worth solving.", [
        ("product_thinking/app_ideas/", "App ideas",
         "100 user problems, and the top-10 research from November 2026."),
    ]),
    ("People skills", "Working with people: managers, teams, interviews.", [
        ("product_thinking/how_to_win_friends/", "How to Win Friends and Influence People",
         "Dale Carnegie. Every chapter's principle, its stories retold, and how to use it at work and in interviews."),
    ]),
    ("Embedded", "Hardware and protocols.", [
        ("embedded/can_guide/", "A Comprehensible Guide to Controller Area Network",
         "Wilfried Voss. Frames, arbitration, bit timing, error handling and the physical layer, with bit-level simulators."),
    ]),
]


def text_of(fragment):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", fragment)).split())


def page_title(path):
    """The page's <h1> (what the reader sees first), else its <title>, else the file name."""
    s = open(path, encoding="utf-8", errors="replace").read()
    for tag in ("h1", "title"):
        m = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", s, re.S | re.I)
        if m and text_of(m.group(1)):
            return text_of(m.group(1))
    return os.path.basename(path)


def chapters(folder):
    """[(number label, relative href, heading)] for every page of a book folder, in file order."""
    full = os.path.join(NOTES, folder)
    pages = sorted(p for p in glob.glob(os.path.join(full, "*.html")) if os.path.basename(p) != "index.html")
    out = []
    for p in pages:
        name = os.path.basename(p)
        m = re.match(r"ch(\d+)([a-z]?)_", name) or re.match(r"(\d+)()-", name)
        num = (str(int(m.group(1))) + m.group(2)) if m else "·"
        out.append((num, os.path.relpath(p, NOTES), page_title(p)))
    return out


def card(href, num, title, desc, meta, extra=""):
    e = html.escape
    return (f'<li class="card" data-search="{e((title + " " + desc).lower())}"><a href="{e(href)}">'
            f'<span class="num">{num}</span><span class="t">{e(title)}</span>'
            f'<span class="d">{e(desc)} <span class="meta">{e(meta)}</span></span></a>{extra}</li>')


def chapter_list(chs):
    e = html.escape
    items = "".join(f'<li data-search="{e(t.lower())}"><a href="{e(h)}"><span class="cn">{n}</span>{e(t)}</a></li>'
                    for n, h, t in chs)
    return f'<details class="chs"><summary>All {len(chs)} pages</summary><ol>{items}</ol></details>'


def build():
    covered, missing, sections, total = set(), [], [], 0
    for shelf, about, entries in SECTIONS:
        cards = []
        for i, (path, title, desc) in enumerate(entries, 1):
            full = os.path.join(NOTES, path)
            if path.endswith("/"):
                chs = chapters(path) if os.path.isdir(full) else []
                if not chs:
                    missing.append(path)
                    continue
                covered.update(os.path.normpath(os.path.join(NOTES, h)) for _, h, _ in chs)
                index = os.path.join(full, "index.html")
                covered.add(os.path.normpath(index))
                href = os.path.relpath(index, NOTES) if os.path.exists(index) else chs[0][1]
                total += len(chs)
                cards.append(card(href, str(i), title, desc, f"{len(chs)} pages", chapter_list(chs)))
            else:
                if not os.path.isfile(full):
                    missing.append(path)
                    continue
                covered.add(os.path.normpath(full))
                total += 1
                cards.append(card(path, str(i), title, desc, "1 page"))
        if cards:
            sections.append(f'<section class="plate"><h2>{html.escape(shelf)}</h2><p class="about">{html.escape(about)}</p>'
                            f'<ol class="chapters">{"".join(cards)}</ol></section>')

    # Every page no shelf covers, so nothing is unreachable from the home page.
    others = []
    for dirpath, dirnames, files in os.walk(NOTES):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for f in sorted(files):
            p = os.path.normpath(os.path.join(dirpath, f))
            if f.endswith(".html") and p not in covered and p != os.path.normpath(OUT) \
                    and not (f == "index.html" and dirpath == os.path.join(NOTES, "llm")):
                others.append(p)
    if others:
        cards = [card(os.path.relpath(p, NOTES), "·", page_title(p), os.path.relpath(p, NOTES), "not on a shelf yet")
                 for p in others]
        total += len(others)
        sections.append('<section class="plate"><h2>Other pages</h2><p class="about">Pages no shelf lists yet '
                        '(add them to SECTIONS in tools/build_home.py).</p>'
                        f'<ol class="chapters">{"".join(cards)}</ol></section>')

    body = f"""<header>
  <div class="kicker">Dhanesh's notes · {total} pages</div>
  <h1>Everything to <em>read</em>, in one place</h1>
  <p>Every study page in this folder, grouped by subject. Open pages from here through
  <code>python3 Notes/serve_notes.py</code> so your highlights and notes are saved to files. On the website,
  highlights and notes stay in the browser you made them in.</p>
  <input id="q" type="search" placeholder="Find a book, chapter or topic…" autocomplete="off" aria-label="Search pages">
</header>
{"".join(sections)}
<p class="none" id="none" hidden>No page matches.</p>"""
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Notes Home</title>
{FONTS}
{STYLE}
<style>
.about {{ color: var(--muted); margin: -4px 0 14px; }}
#q {{ width: 100%; box-sizing: border-box; margin-top: 14px; padding: 10px 12px; font: inherit; color: var(--ink);
  background: var(--plate); border: 1px solid var(--rule); border-radius: 6px; }}
#q:focus {{ outline: 2px solid var(--c2); outline-offset: 1px; }}
li.card > details.chs {{ margin: 4px 0 0 calc(3.2em + 26px); }}
details.chs summary {{ cursor: pointer; color: var(--muted); font-size: .9em; padding: 2px 0; }}
details.chs ol {{ list-style: none; margin: 6px 0 4px; padding: 0; display: grid; gap: 2px; }}
details.chs a {{ display: flex; gap: 10px; padding: 4px 6px; border-radius: 4px; color: inherit; text-decoration: none; }}
details.chs a:hover, details.chs a:focus-visible {{ background: color-mix(in srgb, var(--c1) 12%, transparent); outline: none; }}
.cn {{ flex: 0 0 2.2em; color: var(--muted); font-family: "JetBrains Mono", monospace; font-size: .85em; padding-top: 2px; }}
.none {{ color: var(--muted); text-align: center; }}
@media (max-width: 560px) {{ li.card > details.chs {{ margin-left: 0; }} }}
</style>
</head>
<body>
<div class="wrap">
{body}
</div>
<script>
(function(){{
  var q = document.getElementById('q'), none = document.getElementById('none');
  q.addEventListener('input', function(){{
    var words = q.value.toLowerCase().split(/\\s+/).filter(Boolean), any = false;
    var hit = function(el){{ var s = el.dataset.search; return words.every(function(w){{ return s.indexOf(w) >= 0; }}); }};
    document.querySelectorAll('section.plate').forEach(function(sec){{
      var shown = 0;
      sec.querySelectorAll('li.card').forEach(function(c){{
        var subs = c.querySelectorAll('details li'), subHit = 0;
        subs.forEach(function(li){{ var ok = !words.length || hit(li); li.hidden = !ok; if (ok) subHit++; }});
        var ok = !words.length || hit(c) || subHit > 0;
        c.hidden = !ok; if (ok) shown++;
        var d = c.querySelector('details');
        if (d) d.open = words.length > 0 && subHit > 0;   // searching: open the book on just its matching pages
      }});
      sec.hidden = shown === 0; if (shown) any = true;
    }});
    none.hidden = any || !words.length;
  }});
}})();
</script>
</body>
</html>
"""
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(add_theme(page))
    print(f"built {os.path.relpath(OUT, NOTES)}: {total} pages")
    for p in missing:
        print(f"  skipped (not on disk): {p}")
    for p in others:
        print(f"  not on a shelf: {os.path.relpath(p, NOTES)}")


if __name__ == "__main__":
    build()
