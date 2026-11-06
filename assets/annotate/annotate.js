/* Highlights + notes for every study page.
 *
 * A tool dock sits on the left edge:
 *   - a colour = highlighter: every text selection is highlighted in that colour at once
 *   - pin      = click any spot on the page to pin a note there
 *   - eraser   = click a highlight or pin to remove it
 *   - eye      = show / hide the note cards (hidden by default on phones)
 * With no tool picked, selecting text pops up a small bar (colours + Note), and clicking a highlight lets you
 * recolour it, add a note or delete it.
 * Note cards sit in the side margin, joined to their text by a line, and can be dragged anywhere.
 *
 * Storage, per page: <page>.notes.json beside the .html when the page is served by Notes/serve_notes.py
 * (GET/PUT <Notes root>/__notes?page=<path from Notes root>), and always a copy in localStorage
 * ("ann:<path from Notes root>"); on load the newer of the two wins.
 * Anchors are quoted text + 40 characters either side (a pin: just the text either side), so they survive
 * edits elsewhere on the page.
 */
(function () {
  "use strict";
  if (window.__ann) return;

  var COLORS = ["yellow", "green", "blue", "pink", "purple"];
  var MIN_GUTTER = 250;
  var NARROW = 760;
  var SKIP = "script,style,svg,textarea,input,select,noscript,canvas,.ann-ui,.ann-pin,.theme-btn";
  // Page controls that would navigate or react to a click: with a tool picked they only take highlights and pins.
  var CLICKABLE = "a[href],button,summary,label,[onclick],[role=button],[role=tab],[tabindex]:not([tabindex=\"-1\"])";
  var SVGNS = "http://www.w3.org/2000/svg";

  var script = document.currentScript;
  var root = new URL("../../", script.src);
  var path = decodeURIComponent(location.pathname);
  var rootPath = decodeURIComponent(root.pathname);
  var pageId = path.indexOf(rootPath) === 0 ? path.slice(rootPath.length) : path.replace(/^\/+/, "");
  var storeKey = "ann:" + pageId;
  var serverUrl = /^https?:$/.test(root.protocol) ? root.href + "__notes?page=" + encodeURIComponent(pageId) : null;

  var container, state, lastColor = "yellow";
  var tool = null;               // null | "pin" | "erase" | a colour
  var showNotes = true;
  var ui = {}, cards = {};
  var serverOk = false, saveTimer = null, layoutQueued = false;
  var popFor = null;             // the small bar: {kind: "new", range} | {kind: "item", id}
  var activeId = null;

  // ---------- small helpers ----------
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function btn(cls, html, title, onClick) {
    var b = el("button", cls, html); b.type = "button";
    if (title) { b.title = title; b.setAttribute("aria-label", title); }
    b.addEventListener("click", onClick);
    return b;
  }
  function uid() { return Date.now().toString(36) + Math.random().toString(36).slice(2, 7); }
  function byId(id) { for (var i = 0; i < state.items.length; i++) if (state.items[i].id === id) return state.items[i]; return null; }
  function anchorsOf(id) { return container.querySelectorAll('[data-ann="' + id + '"]'); }
  function each(list, fn) { Array.prototype.forEach.call(list, fn); }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function isTouch() { return matchMedia("(pointer: coarse)").matches; }
  function narrow() { return document.documentElement.clientWidth < NARROW; }
  function touch(item) { item.updated = Date.now(); item.rev = (item.rev || 0) + 1; }
  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
  // Phones and wide screens keep separate dragged positions: a spot in a desktop margin means nothing on a phone.
  function posKey() { return narrow() ? "posNarrow" : "pos"; }

  var ICON = {
    pen: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 15l-4 4h4l2-2"/><path d="M14.5 4.5l5 5-8 8-5-5z"/></svg>',
    pin: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-6-5.6-6-11a6 6 0 0 1 12 0c0 5.4-6 11-6 11z"/><circle cx="12" cy="10" r="2.2"/></svg>',
    erase: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4l5 5-9 9H7l-4-4z"/><path d="M11 20h10"/></svg>',
    eye: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg>',
    eyeOff: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3l18 18"/><path d="M10.6 6.1A10 10 0 0 1 12 6c6.4 0 10 6 10 6a17 17 0 0 1-3.3 3.9M6.6 6.6A17 17 0 0 0 2 12s3.6 7 10 7a9.6 9.6 0 0 0 4.4-1"/></svg>',
    note: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20h4L19 9l-4-4L4 16v4z"/><path d="M13 7l4 4"/></svg>',
    check: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
    home: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 14L4 9l5-5"/><path d="M4 9h10.5a5.5 5.5 0 0 1 0 11H11"/></svg>',
    trash: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/></svg>'
  };

  // ---------- text index: the page's text as one string, mapped back to text nodes ----------
  function buildIndex() {
    var nodes = [], text = "";
    var walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) { return n.parentElement && n.parentElement.closest(SKIP) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT; }
    });
    for (var n = walker.nextNode(); n; n = walker.nextNode()) { nodes.push({ n: n, s: text.length }); text += n.data; }
    return { nodes: nodes, text: text };
  }

  function offsetOf(idx, node, off) {
    for (var i = 0; i < idx.nodes.length; i++) if (idx.nodes[i].n === node) return idx.nodes[i].s + off;
    var r = document.createRange();
    r.setStart(node, off);
    for (var j = 0; j < idx.nodes.length; j++) if (r.comparePoint(idx.nodes[j].n, 0) >= 0) return idx.nodes[j].s;
    return idx.text.length;
  }

  function quoteFromRange(range) {
    var idx = buildIndex();
    var s = offsetOf(idx, range.startContainer, range.startOffset);
    var e = offsetOf(idx, range.endContainer, range.endOffset);
    while (s < e && /\s/.test(idx.text[s])) s++;
    while (e > s && /\s/.test(idx.text[e - 1])) e--;
    if (e - s < 1) return null;
    // Snap to whole words, like a highlighter pen: a drag that starts or ends mid-word takes the whole word.
    while (s > 0 && /\w/.test(idx.text[s - 1]) && /\w/.test(idx.text[s])) s--;
    while (e < idx.text.length && /\w/.test(idx.text[e - 1]) && /\w/.test(idx.text[e])) e++;
    return { exact: idx.text.slice(s, e), prefix: idx.text.slice(Math.max(0, s - 40), s), suffix: idx.text.slice(e, e + 40) };
  }

  function quoteFromPoint(x, y) {
    var node, off;
    if (document.caretPositionFromPoint) { var p = document.caretPositionFromPoint(x, y); if (p) { node = p.offsetNode; off = p.offset; } }
    else if (document.caretRangeFromPoint) { var r = document.caretRangeFromPoint(x, y); if (r) { node = r.startContainer; off = r.startOffset; } }
    if (!node || !container.contains(node)) return null;
    var idx = buildIndex();
    var g = offsetOf(idx, node, off);
    // Snap to the nearest word boundary so the pin never splits a word.
    while (g > 0 && g < idx.text.length && /\w/.test(idx.text[g - 1]) && /\w/.test(idx.text[g])) g--;
    return { exact: "", prefix: idx.text.slice(Math.max(0, g - 40), g), suffix: idx.text.slice(g, g + 40) };
  }

  function locate(idx, q) {
    var text = idx.text;
    if (!q.exact) {
      var key = q.prefix.slice(-24) + q.suffix.slice(0, 24);
      var at = key ? text.indexOf(key) : -1;
      if (at >= 0) { var g = at + q.prefix.slice(-24).length; return [g, g]; }
      var ps = q.prefix.slice(-24), pa = ps ? text.indexOf(ps) : -1;
      return pa >= 0 ? [pa + ps.length, pa + ps.length] : null;
    }
    var best = -1, bestScore = -1, from = 0, tries = 0;
    for (;;) {
      var hit = text.indexOf(q.exact, from);
      if (hit < 0 || tries++ > 300) break;
      var score = 0, before = text.slice(0, hit), after = text.slice(hit + q.exact.length);
      for (var i = 1; i <= q.prefix.length && before[before.length - i] === q.prefix[q.prefix.length - i]; i++) score++;
      for (var k = 0; k < q.suffix.length && after[k] === q.suffix[k]; k++) score++;
      if (score > bestScore) { bestScore = score; best = hit; }
      from = hit + 1;
    }
    return best < 0 ? null : [best, best + q.exact.length];
  }

  // ---------- anchors in the DOM: <mark> for highlights, a pin <span> for point notes ----------
  function place(item) {
    var idx = buildIndex(), span = locate(idx, item.quote);
    item.orphan = !span;
    if (!span) return;
    if (item.kind === "pin") return placePin(item, idx, span[0]);
    idx.nodes.forEach(function (en) {
      var a = Math.max(span[0], en.s), b = Math.min(span[1], en.s + en.n.data.length);
      if (a >= b || !en.n.data.slice(a - en.s, b - en.s).trim()) return;
      var node = en.n;
      if (b - en.s < node.data.length) node.splitText(b - en.s);
      var mid = a - en.s > 0 ? node.splitText(a - en.s) : node;
      var m = document.createElement("mark");
      m.className = "ann-hl" + (item.note ? " ann-has-note" : "");
      m.dataset.ann = item.id;
      m.dataset.color = item.color;
      mid.parentNode.insertBefore(m, mid);
      m.appendChild(mid);
    });
  }

  function placePin(item, idx, g) {
    var hit = null;
    for (var i = 0; i < idx.nodes.length; i++) {
      var en = idx.nodes[i];
      if (g >= en.s && g <= en.s + en.n.data.length) { hit = en; if (g < en.s + en.n.data.length) break; }
    }
    if (!hit) { item.orphan = true; return; }
    var off = g - hit.s, pin = el("span", "ann-pin");
    pin.dataset.ann = item.id; pin.dataset.color = item.color;
    pin.title = "Note";
    if (off >= hit.n.data.length) hit.n.parentNode.insertBefore(pin, hit.n.nextSibling);
    else hit.n.parentNode.insertBefore(pin, off > 0 ? hit.n.splitText(off) : hit.n);
  }

  function unplace(id) {
    each(anchorsOf(id), function (m) {
      var parent = m.parentNode;
      while (m.firstChild) parent.insertBefore(m.firstChild, m);
      parent.removeChild(m);
      parent.normalize();
    });
  }

  function restyle(item) {
    each(anchorsOf(item.id), function (m) {
      m.dataset.color = item.color;
      m.classList.toggle("ann-has-note", !!item.note);
    });
  }

  // ---------- storage ----------
  function readLocal() { try { return JSON.parse(localStorage.getItem(storeKey) || "null"); } catch (e) { return null; } }

  function readServer() {
    if (!serverUrl) return Promise.resolve(null);
    var ctrl = window.AbortController ? new AbortController() : null;
    var timer = setTimeout(function () { ctrl && ctrl.abort(); }, 2000);
    return fetch(serverUrl, { cache: "no-store", signal: ctrl && ctrl.signal })
      .then(function (r) { clearTimeout(timer); serverOk = r.ok; return r.ok ? r.json() : null; })
      .catch(function () { clearTimeout(timer); serverOk = false; return null; });
  }

  function snapshot() {
    return { version: 2, page: pageId, saved: state.saved, items: state.items.map(function (it) {
      var out = { id: it.id, kind: it.kind || "highlight", color: it.color, quote: it.quote, note: it.note || "", created: it.created, updated: it.updated };
      if (it.pos) out.pos = it.pos;
      if (it.posNarrow) out.posNarrow = it.posNarrow;
      return out;
    }) };
  }

  function save() {
    state.saved = Date.now();
    try { localStorage.setItem(storeKey, JSON.stringify(snapshot())); } catch (e) {}
    clearTimeout(saveTimer);
    saveTimer = setTimeout(pushServer, 350);
    updateDock();
  }

  function pushServer() {
    if (!serverUrl) return updateDock();
    fetch(serverUrl, { method: "PUT", headers: { "content-type": "application/json" }, body: JSON.stringify(snapshot()) })
      .then(function (r) { serverOk = r.ok; updateDock(); })
      .catch(function () { serverOk = false; updateDock(); });
  }

  // ---------- the tool dock ----------
  function buildDock() {
    var dock = el("div", "ann-ui ann-dock");
    dock.setAttribute("role", "toolbar"); dock.setAttribute("aria-label", "Highlighter and notes");
    ui.dockToggle = btn("ann-dbtn ann-dock-toggle", ICON.pen + '<span class="ann-count"></span>', "Highlighter · select text then 1–5 or H to highlight, N to pin a note at the mouse, Esc to stop", function () {
      var open = !dock.classList.contains("ann-dock-open");
      dock.classList.toggle("ann-dock-open", open);
      if (!open) setTool(null);
    });
    dock.appendChild(ui.dockToggle);
    var tools = el("div", "ann-dock-tools");
    ui.toolBtns = {};
    COLORS.forEach(function (c) {
      var b = btn("ann-dbtn ann-dcolor", "<i></i>", cap(c) + " highlighter (" + (COLORS.indexOf(c) + 1) + ")", function () { setTool(tool === c ? null : c); });
      b.dataset.color = c; ui.toolBtns[c] = b; tools.appendChild(b);
    });
    tools.appendChild(el("span", "ann-dsep"));
    ui.toolBtns.pin = btn("ann-dbtn", ICON.pin, "Pin a note anywhere: click a spot (P) — or press N to pin where the mouse is", function () { setTool(tool === "pin" ? null : "pin"); });
    ui.toolBtns.erase = btn("ann-dbtn", ICON.erase, "Eraser: click a highlight or pin to remove it (E)", function () { setTool(tool === "erase" ? null : "erase"); });
    ui.eye = btn("ann-dbtn", ICON.eye, "Hide notes", function () { setShowNotes(!showNotes); });
    tools.appendChild(ui.toolBtns.pin); tools.appendChild(ui.toolBtns.erase);
    tools.appendChild(el("span", "ann-dsep")); tools.appendChild(ui.eye);
    dock.appendChild(tools);
    dock.addEventListener("mousedown", function (e) { if (!e.target.closest("textarea")) e.preventDefault(); });
    document.body.appendChild(dock);
    ui.dock = dock;
    if (!narrow()) dock.classList.add("ann-dock-open");
  }

  function setTool(t) {
    tool = t;
    if (t && COLORS.indexOf(t) >= 0) lastColor = t;
    var rootEl = document.documentElement;
    rootEl.classList.toggle("ann-tool-color", !!t && COLORS.indexOf(t) >= 0);
    rootEl.classList.toggle("ann-tool-pin", t === "pin");
    rootEl.classList.toggle("ann-tool-erase", t === "erase");
    Object.keys(ui.toolBtns).forEach(function (k) { ui.toolBtns[k].classList.toggle("ann-on", k === t); });
    // Links are draggable by default, which turns a highlighter drag into dragging the link away.
    each(container.querySelectorAll("a[href]"), function (a) {
      if (t) { if (!a.hasAttribute("data-ann-drag")) a.setAttribute("data-ann-drag", a.getAttribute("draggable") || ""); a.setAttribute("draggable", "false"); }
      else if (a.hasAttribute("data-ann-drag")) {
        var was = a.getAttribute("data-ann-drag");
        if (was) a.setAttribute("draggable", was); else a.removeAttribute("draggable");
        a.removeAttribute("data-ann-drag");
      }
    });
    hidePop();
    // Highlight whatever was already selected when a colour is picked.
    if (t && COLORS.indexOf(t) >= 0) { var sel = window.getSelection(); if (sel && !sel.isCollapsed) highlightSelection(t); }
  }

  function setShowNotes(on) {
    showNotes = on;
    document.documentElement.classList.toggle("ann-notes-hidden", !on);
    try { localStorage.setItem("ann:show:" + (narrow() ? "narrow" : "wide"), on ? "1" : "0"); } catch (e) {}
    updateDock(); layout();
  }

  function updateDock() {
    if (!ui.dock) return;
    var n = state.items.length;
    ui.dockToggle.querySelector(".ann-count").textContent = n || "";
    ui.eye.innerHTML = showNotes ? ICON.eye : ICON.eyeOff;
    var where = serverOk ? "saved to " + pageId.split("/").pop().replace(/\.html$/, ".notes.json")
      : "saved in this browser only (open through serve_notes.py to save to a file)";
    ui.eye.title = (showNotes ? "Hide notes" : "Show notes") + " · " + n + " on this page, " + where;
    ui.eye.setAttribute("aria-label", ui.eye.title);
  }

  // ---------- creating highlights and pins ----------
  function selectionRange() {
    var sel = window.getSelection();
    if (!sel || sel.isCollapsed || !sel.rangeCount) return null;
    var range = sel.getRangeAt(0);
    if (!container.contains(range.commonAncestorContainer)) return null;
    var anc = range.commonAncestorContainer.nodeType === 1 ? range.commonAncestorContainer : range.commonAncestorContainer.parentElement;
    if (anc.closest(SKIP) || !range.toString().trim()) return null;
    return range;
  }

  function addHighlight(range, color) {
    var q = quoteFromRange(range);
    if (!q) return null;
    var now = Date.now();
    var item = { id: uid(), kind: "highlight", color: color, quote: q, note: "", created: now, updated: now, rev: 1 };
    state.items.push(item);
    place(item);
    var sel = window.getSelection(); if (sel) sel.removeAllRanges();
    return item;
  }

  function highlightSelection(color) {
    var range = selectionRange();
    if (!range) return;
    if (addHighlight(range, color)) { save(); layout(); }
  }

  function addPin(x, y) {
    var q = quoteFromPoint(x, y);
    if (!q) return;
    var now = Date.now();
    var item = { id: uid(), kind: "pin", color: lastColor, quote: q, note: "", created: now, updated: now, rev: 1, fresh: true };
    state.items.push(item);
    place(item);
    if (item.orphan) { state.items.pop(); return; }
    save();
    setTool(null);
    edit(item.id);
  }

  function remove(id) {
    unplace(id);
    state.items = state.items.filter(function (it) { return it.id !== id; });
    if (cards[id]) { cards[id].remove(); delete cards[id]; }
    save(); layout();
  }

  function confirmRemove(item) {
    if (item.note && !window.confirm("Delete this note?\n\n" + item.note.slice(0, 160))) return;
    remove(item.id);
  }

  // ---------- the small pop-up bar (no tool picked) ----------
  function buildPop() {
    var t = el("div", "ann-ui ann-toolbar");
    COLORS.forEach(function (c) {
      var b = btn("ann-swatch", "", "Highlight " + c, function () { onPopColor(c); });
      b.dataset.color = c; t.appendChild(b);
    });
    t.appendChild(el("span", "ann-sep"));
    t.appendChild(btn("ann-tbtn", ICON.note + "<span>Note</span>", "Add a note", onPopNote));
    ui.popDel = btn("ann-tbtn", ICON.trash, "Remove", function () { if (popFor && popFor.kind === "item") { var it = byId(popFor.id); hidePop(); confirmRemove(it); } });
    t.appendChild(ui.popDel);
    t.addEventListener("mousedown", function (e) { e.preventDefault(); });
    document.body.appendChild(t);
    ui.pop = t;
  }

  function showPop(rect, target) {
    popFor = target;
    var t = ui.pop, item = target.kind === "item" ? byId(target.id) : null;
    ui.popDel.style.display = item ? "" : "none";
    each(t.querySelectorAll(".ann-swatch"), function (b) { b.classList.toggle("ann-current", !!item && b.dataset.color === item.color); });
    t.classList.add("ann-show");
    var w = t.offsetWidth, h = t.offsetHeight, sx = window.scrollX, sy = window.scrollY;
    var top = rect.top + sy - h - 10;
    if (isTouch() || top < sy + 8) top = rect.bottom + sy + 12;
    var left = rect.left + sx + rect.width / 2 - w / 2;
    left = Math.max(sx + 8, Math.min(left, sx + document.documentElement.clientWidth - w - 8));
    t.style.top = top + "px"; t.style.left = left + "px";
  }

  function hidePop() {
    if (popFor && popFor.kind === "item") setActive(null);
    popFor = null;
    if (ui.pop) ui.pop.classList.remove("ann-show");
  }

  function onPopColor(c) {
    if (!popFor) return;
    lastColor = c;
    if (popFor.kind === "new") { if (addHighlight(popFor.range, c)) { save(); layout(); } }
    else { var it = byId(popFor.id); it.color = c; touch(it); restyle(it); save(); layout(); }
    hidePop();
  }

  function onPopNote() {
    if (!popFor) return;
    var isNew = popFor.kind === "new";
    var item = isNew ? addHighlight(popFor.range, lastColor) : byId(popFor.id);
    hidePop();
    if (!item) return;
    if (isNew) save();
    edit(item.id);
  }

  // ---------- note cards ----------
  function tiltOf(id) {
    var h = 0;
    for (var i = 0; i < id.length; i++) h = (h * 31 + id.charCodeAt(i)) | 0;
    return ((Math.abs(h) % 7) - 3) * 0.45;
  }

  // What a pin's card quotes: the visible words of the paragraph, item or link the pin sits in.
  function pinLabel(item) {
    var pin = anchorsOf(item.id)[0];
    var block = pin && (pin.closest("p,li,a,td,th,h1,h2,h3,h4,figcaption,blockquote,summary,dd,dt") || pin.parentElement);
    var words = (block ? block.innerText : item.quote.suffix).trim().split(/\s+/).filter(Boolean);
    return words.length ? words.slice(0, 7).join(" ") + (words.length > 7 ? " …" : "") : "Pinned here";
  }

  function buildCard(item) {
    var c = el("div", "ann-ui ann-card" + (item.kind === "pin" ? " ann-card-pin" : "") + (item.editing ? " ann-editing" : ""));
    c.dataset.color = item.color; c.dataset.ann = item.id; c.dataset.rev = item.rev || 0; c.dataset.editing = item.editing ? 1 : 0;
    c.style.setProperty("--tilt", tiltOf(item.id) + "deg");
    c.appendChild(el("span", "ann-tape"));
    var head = el("div", "ann-head");
    head.appendChild(el("span", "ann-badge", item.num || ""));
    head.appendChild(el("span", "ann-quote", item.kind === "pin"
      ? esc(pinLabel(item))
      : "“" + esc(item.quote.exact) + "”"));
    c.appendChild(head);
    var foot = el("div", "ann-foot");
    var stamp = el("span", "ann-stamp", new Date(item.updated).toLocaleDateString(undefined, { day: "numeric", month: "short" }));
    var tools = el("span", "ann-icons");
    if (item.editing) {
      // Cards are rebuilt when they change, so the unsaved text lives on the item, not in the textarea.
      var ta = el("textarea", "ann-input");
      ta.rows = 2;
      ta.value = item.draft != null ? item.draft : item.note || "";
      ta.placeholder = "Write your note…";
      var grow = function () { ta.style.height = "auto"; ta.style.height = ta.scrollHeight + "px"; };
      ta.addEventListener("input", function () { item.draft = ta.value; grow(); drawLines(); });
      ta.addEventListener("keydown", function (e) {
        if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) { e.preventDefault(); commit(item, ta.value); }
        if (e.key === "Escape") { e.preventDefault(); cancel(item); }
      });
      ta.addEventListener("blur", function () {
        setTimeout(function () { if (c.isConnected && item.editing && !c.contains(document.activeElement)) commit(item, ta.value); }, 150);
      });
      c.appendChild(ta);
      stamp.textContent = "⌘↵ to save · Esc to cancel";
      tools.appendChild(btn("ann-ibtn", ICON.trash, "Delete", function () { item.editing = false; remove(item.id); }));
      tools.appendChild(btn("ann-ibtn ann-ok", ICON.check, "Save", function () { commit(item, ta.value); }));
      each(tools.querySelectorAll("button"), function (b) { b.addEventListener("mousedown", function (e) { e.preventDefault(); }); });
      setTimeout(function () { grow(); ta.focus({ preventScroll: true }); ta.setSelectionRange(ta.value.length, ta.value.length); }, 40);
    } else {
      c.appendChild(el("div", "ann-note", esc(item.note || "")));
      if (item[posKey()]) tools.appendChild(btn("ann-ibtn", ICON.home, "Put back beside its text", function (e) { e.stopPropagation(); delete item[posKey()]; touch(item); save(); layout(); }));
      tools.appendChild(btn("ann-ibtn", ICON.note, "Edit", function (e) { e.stopPropagation(); edit(item.id); }));
      tools.appendChild(btn("ann-ibtn", ICON.trash, "Delete", function (e) { e.stopPropagation(); confirmRemove(item); }));
      c.addEventListener("dblclick", function (e) { if (!e.target.closest("button")) edit(item.id); });
    }
    foot.appendChild(stamp); foot.appendChild(tools);
    c.appendChild(foot);
    c.addEventListener("mouseenter", function () { setActive(item.id); });
    c.addEventListener("mouseleave", function () { setActive(null); });
    enableDrag(c, item);
    return c;
  }

  function cancel(item) {
    item.editing = false;
    delete item.draft;
    if (item.kind === "pin" && !item.note) { remove(item.id); return; }
    touch(item); layout();
  }

  function commit(item, text) {
    item.editing = false;
    delete item.draft;
    var note = text.trim();
    if (item.kind === "pin" && !note) { remove(item.id); return; }
    if (note !== (item.note || "")) { item.note = note; restyle(item); }
    touch(item); save(); layout();
  }

  function edit(id) {
    state.items.forEach(function (it) { if (it.editing !== (it.id === id)) { it.editing = it.id === id; touch(it); } });
    if (!showNotes) setShowNotes(true); else layout();
    var c = cards[id];
    if (c) { var r = c.getBoundingClientRect(); if (r.top < 0 || r.bottom > innerHeight) c.scrollIntoView({ behavior: "smooth", block: "center" }); }
  }

  function setActive(id) {
    if (activeId === id) return;
    activeId = id;
    each(document.querySelectorAll(".ann-active"), function (x) { x.classList.remove("ann-active"); });
    if (id) each(document.querySelectorAll('[data-ann="' + id + '"]'), function (x) { x.classList.add("ann-active"); });
  }

  function flash(id) {
    each(anchorsOf(id), function (x) { x.classList.remove("ann-flash"); void x.offsetWidth; x.classList.add("ann-flash"); });
  }

  // ---------- dragging a card ----------
  function enableDrag(c, item) {
    c.addEventListener("pointerdown", function (e) {
      if (e.button !== 0 || e.target.closest("button,textarea,a")) return;
      var startX = e.pageX, startY = e.pageY, left = parseFloat(c.style.left), top = parseFloat(c.style.top), moved = false;
      c.setPointerCapture(e.pointerId);
      function move(ev) {
        var dx = ev.pageX - startX, dy = ev.pageY - startY;
        if (!moved && Math.abs(dx) + Math.abs(dy) < 4) return;
        if (!moved) { moved = true; c.classList.add("ann-dragging"); }
        c.style.left = left + dx + "px"; c.style.top = top + dy + "px";
        drawLines();
      }
      function up() {
        c.removeEventListener("pointermove", move); c.removeEventListener("pointerup", up); c.removeEventListener("pointercancel", up);
        c.classList.remove("ann-dragging");
        if (!moved) { var m = anchorsOf(item.id)[0]; if (m && !item.editing) { m.scrollIntoView({ behavior: "smooth", block: "center" }); flash(item.id); } return; }
        var a = anchorPoint(item), box = container.getBoundingClientRect();
        if (a) { item[posKey()] = { ox: parseFloat(c.style.left) - (box.left + window.scrollX), oy: parseFloat(c.style.top) - a.y }; save(); }
        touch(item); layout();
      }
      c.addEventListener("pointermove", move); c.addEventListener("pointerup", up); c.addEventListener("pointercancel", up);
    });
  }

  // ---------- layout: cards beside their text, lines between ----------
  function gutter() {
    var r = container.getBoundingClientRect(), vw = document.documentElement.clientWidth;
    var right = vw - r.right, left = r.left;
    if (right >= MIN_GUTTER) return { side: "right", room: right, r: r };
    if (left >= MIN_GUTTER) return { side: "left", room: left, r: r };
    return { side: "over", room: vw, r: r };
  }

  function anchorPoint(item) {
    var first = anchorsOf(item.id)[0];
    if (!first) return null;
    var rect = item.kind === "pin" ? first.getBoundingClientRect() : (first.getClientRects()[0] || first.getBoundingClientRect());
    var sx = window.scrollX, sy = window.scrollY;
    // A pin's badge floats just above its text line, so its line runs in the gap above that line.
    if (item.kind === "pin") { var py = rect.top + sy - 13; return { x: rect.left + sx + 9, xl: rect.left + sx - 9, y: py, mid: py, gap: rect.top + sy - 3, under: py + 8 }; }
    // The line starts at the number badge, which sits at the end of the highlight's last piece.
    var list = anchorsOf(item.id), lastRects = list[list.length - 1].getClientRects(), end = lastRects[lastRects.length - 1] || rect;
    var badge = item.num ? 18 : 0;
    return { x: end.right + sx + badge, xl: rect.left + sx, y: rect.top + sy, mid: end.top + sy + end.height / 2, gap: end.bottom + sy + 3, under: end.bottom + sy + 1.5 };
  }

  function queueLayout() {
    if (layoutQueued) return;
    layoutQueued = true;
    requestAnimationFrame(function () { layoutQueued = false; layout(); });
  }

  // Number every note (pins, and highlights that carry a note) in reading order; the badge on the text
  // and on its card show the same number.
  function renumber() {
    var noted = state.items.filter(function (it) { return !it.orphan && (it.note || it.kind === "pin") && anchorsOf(it.id)[0]; });
    noted.sort(function (p, q) { return anchorsOf(p.id)[0].compareDocumentPosition(anchorsOf(q.id)[0]) & 4 ? -1 : 1; });
    state.items.forEach(function (it) { it.num = 0; });
    noted.forEach(function (it, k) { it.num = k + 1; });
    each(container.querySelectorAll("[data-num]"), function (x) { x.removeAttribute("data-num"); });
    noted.forEach(function (it) {
      var list = anchorsOf(it.id);
      list[it.kind === "pin" ? 0 : list.length - 1].setAttribute("data-num", it.num);
    });
  }

  function layout() {
    renumber();
    var g = gutter(), sx = window.scrollX, vw = document.documentElement.clientWidth;
    var w = g.side === "over" ? Math.min(270, vw - 40) : Math.min(290, g.room - 60);
    var autoX = g.side === "right" ? g.r.right + sx + 36 : g.side === "left" ? g.r.left + sx - 36 - w : sx + vw - w - 14;
    var boxLeft = g.r.left + sx;

    var rows = [];
    state.items.forEach(function (it) {
      var wanted = showNotes && !it.orphan && (it.note || it.editing || it.kind === "pin");
      if (!wanted) { if (cards[it.id]) { cards[it.id].remove(); delete cards[it.id]; } return; }
      var a = anchorPoint(it);
      if (a) rows.push({ it: it, a: a });
    });
    var live = {};
    rows.forEach(function (row) { live[row.it.id] = 1; });
    Object.keys(cards).forEach(function (id) { if (!live[id]) { cards[id].remove(); delete cards[id]; } });

    rows.sort(function (p, q) { return p.a.y - q.a.y; });
    var bottom = -Infinity;
    rows.forEach(function (row) {
      var it = row.it, c = cards[it.id];
      if (!c || c.dataset.rev !== String(it.rev || 0) || c.dataset.editing !== (it.editing ? "1" : "0")) {
        var fresh = buildCard(it);
        if (c) c.replaceWith(fresh); else { fresh.classList.add("ann-enter"); ui.layer.appendChild(fresh); }
        c = cards[it.id] = fresh;
      }
      c.querySelector(".ann-badge").textContent = it.num || "";
      c.style.width = w + "px";
      var pos = it[posKey()];
      if (pos) {
        // A spot chosen on a wide screen can be off a narrow one: keep the card on screen.
        c.style.left = Math.max(sx + 8, Math.min(boxLeft + pos.ox, sx + vw - w - 8)) + "px";
        c.style.top = row.a.y + pos.oy + "px";
      } else {
        c.style.left = autoX + "px";
        var top = Math.max(row.a.y - 14, bottom + 16);
        c.style.top = top + "px";
        bottom = top + c.offsetHeight;
      }
      c.classList.toggle("ann-active", it.id === activeId);
      // Focus the note box the moment its card is placed, so typing right after N / a click lands in it.
      var input = it.editing && c.querySelector(".ann-input");
      if (input && document.activeElement !== input) {
        input.focus({ preventScroll: true });
        input.setSelectionRange(input.value.length, input.value.length);
      }
    });
    drawLines();
  }

  // One smooth curve per note, from its text to its card; a new line draws itself in once.
  var drawn = {};
  function drawLines() {
    var svg = ui.lines, doc = document.documentElement;
    svg.innerHTML = "";
    svg.setAttribute("width", doc.scrollWidth); svg.setAttribute("height", doc.scrollHeight);
    var box = container.getBoundingClientRect(), sx = window.scrollX;
    Object.keys(cards).forEach(function (id) {
      var it = byId(id), c = cards[id];
      if (!it) return;
      var a = anchorPoint(it);
      if (!a) return;
      var cl = parseFloat(c.style.left), ct = parseFloat(c.style.top), cw = c.offsetWidth, ch = c.offsetHeight;
      var d, x1, y1;
      if (a.x > cl + 16 && a.x < cl + cw - 16) {
        // Card straight above or below its text (phones, or dragged there): a soft vertical swoop.
        var below = ct > a.y;
        x1 = a.x; y1 = below ? a.under + 2 : a.y - 2;
        var y2 = below ? ct : ct + ch, x2 = Math.max(cl + 24, Math.min(a.x + 30, cl + cw - 24)), my = (y1 + y2) / 2;
        d = "M" + x1 + " " + y1 + " C" + x1 + " " + my + " " + x2 + " " + my + " " + x2 + " " + y2;
      } else {
        // Leader line: from the badge into the gap between text lines, along that gap to the edge of the
        // page column (never through the words), then one soft curve into the card.
        var toRight = cl + cw / 2 > a.x, dir = toRight ? 1 : -1;
        x1 = toRight ? a.x : a.xl; y1 = a.mid;
        var gy = a.gap, edge = toRight ? Math.max(box.right + sx + 10, x1 + 14) : Math.min(box.left + sx - 10, x1 - 14);
        var tx = toRight ? cl - 2 : cl + cw + 2, ty = ct + 26;
        var r = Math.min(8, Math.abs(gy - y1));
        if ((toRight && tx < edge) || (!toRight && tx > edge)) edge = (x1 + tx) / 2;
        var k = Math.max(24, Math.abs(tx - edge) * 0.55);
        d = "M" + x1 + " " + y1 +
          " Q" + x1 + " " + gy + " " + (x1 + dir * r) + " " + gy +
          " L" + (edge - dir * 2) + " " + gy +
          " C" + (edge + dir * k) + " " + gy + " " + (tx - dir * k) + " " + ty + " " + tx + " " + ty;
      }
      var p = document.createElementNS(SVGNS, "path");
      p.setAttribute("d", d);
      p.dataset.ann = id; p.dataset.color = it.color;
      if (id === activeId) p.classList.add("ann-active");
      svg.appendChild(p);
      if (!drawn[id]) {
        drawn[id] = 1;
        var len = p.getTotalLength();
        p.style.strokeDasharray = len; p.style.strokeDashoffset = len;
        p.getBoundingClientRect();
        p.style.transition = "stroke-dashoffset .7s cubic-bezier(.2,.8,.2,1)";
        p.style.strokeDashoffset = 0;
        setTimeout(function () { p.style.strokeDasharray = ""; p.style.transition = ""; }, 750);
      }
      var dot = document.createElementNS(SVGNS, "circle");
      dot.setAttribute("cx", x1); dot.setAttribute("cy", y1); dot.setAttribute("r", 3.2); dot.dataset.color = it.color;
      svg.appendChild(dot);
    });
  }

  // ---------- events ----------
  var selTimer = null;
  function onSelectionDone(e) {
    if (e && e.target && e.target.closest && e.target.closest(".ann-ui")) return;
    if (tool === "pin" || tool === "erase") return;
    var range = selectionRange();
    if (!range) { if (popFor && popFor.kind === "new") hidePop(); return; }
    if (tool) { highlightSelection(tool); return; }
    showPop(range.getBoundingClientRect(), { kind: "new", range: range.cloneRange() });
  }

  function bind() {
    document.addEventListener("mouseup", function (e) { setTimeout(function () { onSelectionDone(e); }, 0); });
    document.addEventListener("keyup", function (e) { if (e.shiftKey) onSelectionDone(e); });
    document.addEventListener("selectionchange", function () {
      if (!isTouch()) return;
      clearTimeout(selTimer); selTimer = setTimeout(onSelectionDone, 450);
    });
    document.addEventListener("click", function (e) {
      if (!e.target.closest || e.target.closest(".ann-ui")) return;
      var inPage = container.contains(e.target);
      var hit = e.target.closest("mark.ann-hl, .ann-pin");
      var control = inPage && e.target.closest(CLICKABLE);
      // With a tool picked, links and widgets on the page do nothing; the click belongs to the tool.
      if (tool && inPage && control) { e.preventDefault(); e.stopPropagation(); }
      if (tool === "erase") { if (hit) { e.preventDefault(); e.stopPropagation(); confirmRemove(byId(hit.dataset.ann)); } return; }
      if (tool === "pin") {
        if (inPage) { e.preventDefault(); e.stopPropagation(); addPin(e.clientX, e.clientY); }
        return;
      }
      if (tool) return;
      var sel = window.getSelection();
      // The click that ends a text selection inside a link must not open the link.
      if (control && sel && !sel.isCollapsed) { e.preventDefault(); return; }
      if (hit && control) { e.preventDefault(); e.stopPropagation(); }
      if (hit && (!sel || sel.isCollapsed)) {
        var id = hit.dataset.ann, it = byId(id);
        setActive(id);
        if (it.kind === "pin") { if (!showNotes) setShowNotes(true); var c = cards[id]; if (c) c.scrollIntoView({ behavior: "smooth", block: "nearest" }); return; }
        showPop(hit.getBoundingClientRect(), { kind: "item", id: id });
        return;
      }
      if (popFor && popFor.kind === "item") hidePop();
    }, true);
    container.addEventListener("mouseover", function (e) { var m = e.target.closest("mark.ann-hl, .ann-pin"); if (m) setActive(m.dataset.ann); });
    container.addEventListener("mouseout", function (e) { var m = e.target.closest("mark.ann-hl, .ann-pin"); if (m) setActive(null); });
    // Shortcuts. N: pin a note where the mouse pointer is. With text selected, 1-5 highlight it in that colour
    // and H in the last colour; with nothing selected, 1-5 / P / E pick that tool (press again to drop it).
    var mouse = null;
    document.addEventListener("mousemove", function (e) { mouse = { x: e.clientX, y: e.clientY }; }, { passive: true });
    document.addEventListener("keydown", function (e) {
      var typing = e.target.closest && e.target.closest("textarea,input,select,[contenteditable],[contenteditable=true]");
      if (e.key === "Escape" && !typing) { hidePop(); setTool(null); return; }
      if (typing || e.metaKey || e.ctrlKey || e.altKey || e.repeat) return;
      var key = e.key.toLowerCase(), n = "12345".indexOf(key), selected = selectionRange();
      if (key === "n") {
        var under = mouse && document.elementFromPoint(mouse.x, mouse.y);
        if (!under || !container.contains(under) || under.closest(".ann-ui")) return;
        e.preventDefault(); addPin(mouse.x, mouse.y);
      } else if (n >= 0 && selected) {
        e.preventDefault(); lastColor = COLORS[n]; hidePop(); highlightSelection(COLORS[n]);
      } else if (key === "h" && selected) {
        e.preventDefault(); hidePop(); highlightSelection(lastColor);
      } else if (n >= 0 || key === "p" || key === "e") {
        var t = n >= 0 ? COLORS[n] : key === "p" ? "pin" : "erase";
        e.preventDefault(); ui.dock.classList.add("ann-dock-open"); setTool(tool === t ? null : t);
      }
    });
    window.addEventListener("resize", function () { hidePop(); queueLayout(); });
    window.addEventListener("load", queueLayout);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(queueLayout);
    if (window.ResizeObserver) new ResizeObserver(queueLayout).observe(container);
  }

  // ---------- start ----------
  function adopt(data) {
    state = data || { version: 2, page: pageId, saved: 0, items: [] };
    state.items.forEach(function (it) { it.kind = it.kind || "highlight"; it.rev = 1; });
  }

  function start() {
    container = document.querySelector(".wrap") || document.querySelector("main") || document.body;
    adopt(readLocal());
    var pref = null;
    try { pref = localStorage.getItem("ann:show:" + (narrow() ? "narrow" : "wide")); } catch (e) {}
    showNotes = pref ? pref === "1" : !narrow();
    document.documentElement.classList.toggle("ann-notes-hidden", !showNotes);

    ui.layer = el("div", "ann-layer"); document.body.appendChild(ui.layer);
    ui.lines = document.createElementNS(SVGNS, "svg");
    ui.lines.setAttribute("class", "ann-lines"); ui.lines.setAttribute("aria-hidden", "true");
    document.body.appendChild(ui.lines);
    buildDock(); buildPop(); bind();
    state.items.forEach(place);
    updateDock(); layout();

    readServer().then(function (remote) {
      if (remote && (remote.saved || 0) > (state.saved || 0)) {
        state.items.forEach(function (it) { unplace(it.id); });
        Object.keys(cards).forEach(function (id) { cards[id].remove(); delete cards[id]; });
        adopt(remote);
        try { localStorage.setItem(storeKey, JSON.stringify(snapshot())); } catch (e) {}
        state.items.forEach(place);
        layout();
      } else if (serverOk && state.items.length && (!remote || (remote.saved || 0) < (state.saved || 0))) {
        pushServer();
      }
      updateDock();
    });
    window.__ann = { state: function () { return state; }, layout: layout, pageId: pageId, setTool: setTool };
  }

  // Draw nothing until the stylesheet is in, or the controls flash unstyled on load.
  var started = false;
  function startOnce() { if (started) return; started = true; start(); }
  // The notes are written in a handwriting face; pages already load Google Fonts, so this is the same source.
  var hand = document.createElement("link");
  hand.rel = "stylesheet"; hand.href = "https://fonts.googleapis.com/css2?family=Caveat:wght@500;600;700&display=swap";
  document.head.appendChild(hand);
  var link = document.createElement("link");
  link.rel = "stylesheet"; link.href = new URL("annotate.css", script.src).href;
  link.onload = link.onerror = function () {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", startOnce); else startOnce();
  };
  document.head.appendChild(link);
})();
