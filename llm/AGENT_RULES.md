# Rules for a chapter-page agent (read with BRIEF.md)

1. Read `/Users/dhanesh/Desktop/GFV/Notes/llm/BRIEF.md` fully first — it is the spec (page structure, rules,
   chapter table with pdf ranges and prev/next file names). Open the style reference it names and copy its `<head>`.
2. **Write durably, plate by plate.** Never compose the whole page in memory and write it once at the end.
   First write the file with `<head>`, crumbs, hero, "How the chapter fits together" plate, TOC, then the marker
   `<!-- @@MORE@@ -->` followed by `</div></body></html>`. Then, for each section, read its PDF pages and
   insert the finished plate just before `<!-- @@MORE@@ -->` (Edit tool or a small script). If you get cut off, the
   file on disk is a resumable partial.
3. Read every pdf page of the range with `/Users/dhanesh/Desktop/GFV/tools/bin/pdftool text "<pdf>" A B` in
   10–15 page slices. Read (look at) every figure PNG of the chapter before describing it.
4. **Explain in your own words.** Never copy the book's sentences or long code listings verbatim. Code: short
   illustrative snippets with your own names showing the same idea; explain each part.
5. Simple words, analogies (Indian everyday life welcome), worked examples with numbers, own SVG visuals and at
   least one interactive / step-through visual per major section, interview-angle boxes. Simplify the language,
   never the content: every definition, list item, number, caveat, footnote and figure is covered.
6. After all plates: Summary + Key terms, "Where you meet this in real systems", "Check yourself" (10–15
   `<details>` Q&As), References `<details>`. Then remove the `<!-- @@MORE@@ -->` marker. The file must end with
   `</html>`.
7. Completeness pass: re-read the PDF section by section against your page and add anything missing. Then an
   enrich pass.
8. Run `cd /Users/dhanesh/Desktop/GFV/Notes/llm && python3 check_page.py <book dir> <file> <chapter no.>` and fix
   every problem. Also confirm `tail -c 20 <file>` shows `</html>` and the last plate's pdf chip reaches the
   chapter's last pdf page.
9. **Scratch files:** several agents share one scratchpad. Put every helper script / temp file in your own
   subfolder named after your chapter (e.g. `scratchpad/hb_ch06/`), never a generic name like `ins.py` at the
   scratchpad root, and never run a script you did not write. Before any insert, verify the target path is your file.
10. Only touch your own chapter file (and nothing in `books/`). Don't edit BRIEF.md, index pages or other chapters.
11. Final reply (short): file path, size, number of plates, figures used, checker result, anything you could not cover.
