"""Add a light/dark theme switch to every study page (idempotent).

The pages already define light colours on :root and dark ones under
:root[data-theme="dark"] (plus the system-dark media query), so the switch only
has to set data-theme on <html> and remember the choice in localStorage.
build_index.py calls add_theme() too, so rebuilt index pages keep the switch.

Usage: python3 theme_toggle.py [folder ...]
  (updates every .html under the given folders; default Notes/llm)
"""
import glob, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
START, END = "<!-- theme:start -->", "<!-- theme:end -->"

# Runs before first paint, so a saved choice never flashes the other theme.
HEAD_JS = START + """<script>
(function(){ try { var t = localStorage.getItem('llm-theme'); if (t === 'light' || t === 'dark') document.documentElement.setAttribute('data-theme', t); } catch (e) {} })();
</script>""" + END

BODY_UI = START + """<style>
.theme-btn { position: fixed; right: 14px; bottom: calc(14px + env(safe-area-inset-bottom, 0px)); z-index: 50;
  width: 44px; height: 44px; border-radius: 50%; border: 1px solid var(--rule); background: var(--plate); color: var(--ink);
  font-size: 20px; line-height: 1; cursor: pointer; box-shadow: 0 2px 10px rgba(0,0,0,.18); display: grid; place-items: center; }
.theme-btn:hover { border-color: var(--muted); }
.theme-btn:focus-visible { outline: 2px solid var(--c2); outline-offset: 2px; }
@media print { .theme-btn { display: none; } }
</style>
<button type="button" class="theme-btn" id="themeBtn"></button>
<script>
(function(){
  var root = document.documentElement, btn = document.getElementById('themeBtn');
  function current(){
    var t = root.getAttribute('data-theme');
    if (t === 'light' || t === 'dark') return t;
    return window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  function paint(){
    var dark = current() === 'dark';
    btn.textContent = dark ? '\\u2600' : '\\u263E';
    btn.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
    btn.title = btn.getAttribute('aria-label');
  }
  btn.addEventListener('click', function(){
    var next = current() === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('llm-theme', next); } catch (e) {}
    paint();
    window.dispatchEvent(new Event('themechange'));   // canvas widgets redraw with the new colours
  });
  paint();
})();
</script>""" + END


def strip(html):
    # Also eat the newlines around a block so repeated runs leave the file unchanged.
    return re.sub(r"\n*" + re.escape(START) + r".*?" + re.escape(END) + r"\n?", "\n", html, flags=re.S)


def add_theme(html):
    html = strip(html)
    html = html.replace("</head>", HEAD_JS + "\n</head>", 1)
    i = html.rfind("</body>")
    if i < 0:   # </body> is optional in HTML; such pages just end, so the switch goes last
        return html.rstrip("\n") + "\n" + BODY_UI + "\n"
    return html[:i] + BODY_UI + "\n" + html[i:]


if __name__ == "__main__":
    import sys
    roots = sys.argv[1:] or [HERE]
    files = sorted(f for r in roots for f in glob.glob(os.path.join(r, "**", "*.html"), recursive=True))
    for f in files:
        src = open(f, encoding="utf-8").read()
        out = add_theme(src)
        if out != src:
            open(f, "w", encoding="utf-8").write(out)
    print(len(files), "pages have the theme switch")
