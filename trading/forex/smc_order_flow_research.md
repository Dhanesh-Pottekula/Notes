# SMC and order flow: what the roadmap has, what it lacks, what to study

Researched 2026-11-17 as an add-on to the [forex roadmap](forex_learning_path.md). Education, not investment advice.

Verification tags are the same as in `resources.js`: `ok` = page opened or search returned matching details,
`part` = only third-party summaries back the details, `unv` = from memory, check before relying on it.

## 1. Short answer

- **SMC / ICT is not in the roadmap.** The only mention is one line in Phase 3 of `index.html`: most "smart
  money" vocabulary renames ideas in Wyckoff and Grimes. None of the 202 resources is about SMC, Wyckoff,
  volume profile, footprint charts or auction market theory.
- **"Order flow" is in the roadmap, but only in one of its two meanings** (see section 2).
- **You have already done more SMC work in code than in study.** `projects/Trading-EA/` has about ten SMC
  robots (wiki: `projects/Trading-EA/wiki/index.md`). None has a proven edge yet.
- **The evidence is mixed in a specific way.** One idea behind SMC (stops cluster just beyond obvious levels)
  is backed by peer-reviewed FX research. But that research found price **keeps going** when it reaches the
  stops; it did not find the sweep-then-reverse move that SMC trades. The trading rules built on top (order
  blocks, FVGs, sweeps as entries) mostly do **not** beat random entries in the open tests that exist.

## 2. Two different things are called "order flow"

| | SMC "order flow" | Real order flow |
|---|---|---|
| What it is | A story read from candles: which side is in control, where stops sit, which zone price should return to | Measured buying and selling: delta, footprint, order book (DOM), volume profile |
| Data needed | Plain OHLC candles | Every trade with bid/ask, on an exchange |
| Works on spot FX? | Yes (it is only candles) | **No.** Spot FX has no central exchange; MT5 "volume" is tick count. Use CME FX futures (6E, 6B, 6J; gold = GC) |
| In the roadmap now | Missing | Partly: academic FX papers (Evans & Lyons, Lyons) in Phases 2 and 7, plus `../concepts/order_flow.md` and `../concepts/vwap_volume_profile_explained.md` |
| Theory behind it | Wyckoff, price action, stop-hunting | Auction market theory, market microstructure |

## 3. Coverage check, concept by concept

"Roadmap" = `forex/index.html` + `resources.js`. "Notes" = other files in `Notes/trading/`. "EA code" =
`projects/Trading-EA/` (see its wiki page `concepts/smc-terms-as-coded.md`).

| Concept | Roadmap | Notes | EA code |
|---|---|---|---|
| Market structure: swing highs/lows, BOS, CHoCH / MSS | Indirect (Grimes, Murphy pages) | Named once in the VWAP note | Yes, several definitions |
| Liquidity pools, equal highs/lows | No | Grimes ch.2 and ch.5 pages mention equal highs | Swing levels only; no equal-highs check |
| Liquidity sweep / stop hunt | No | "Failure test": Grimes ch.6 page and the VWAP note | Yes |
| Inducement | No | No | No |
| Order block | No | No | Yes |
| Breaker and mitigation blocks | No | No | Breaker only, used for the stop |
| Fair value gap / imbalance, inverse FVG | No | Named once | Yes |
| Displacement | No | No | Yes, in 4 EAs (body-size ratio) |
| Premium / discount, optimal trade entry (OTE, 62–79% retrace) | No | 67% / 75% entries in the VWAP note | No |
| Kill zones (London, New York) | Sessions and the clock, not as SMC | No | Yes (fixed server hours, no DST) |
| Power of three / AMD (accumulation, manipulation, distribution) | No | No | Partly (Asian range → grab → move) |
| Wyckoff phases, spring, upthrust | No (book is in `books/trading`, no page yet) | Springs/upthrusts inside the Grimes and Carter pages; `wyckoff/` folder is empty | No |
| Delta, CVD, absorption, footprint | Link only | Yes, `order_flow.md` | One EA uses CVD |
| Volume profile, POC, value area | Link only | Yes (VWAP note, Grimes and Carter pages, backtest summary) | No |
| Market profile / auction market theory | No | One mention (Grimes ch.15 page) | No |
| DOM, tape reading | No | Short section | No |

## 4. What the evidence says

**Part of the mechanism is real (peer-reviewed):**

- Osler (2003), *Journal of Finance*, "Currency Orders and Exchange Rate Dynamics". Data: about 9,700 real
  stop-loss and take-profit orders at a large bank. Take-profit orders cluster **at** round numbers; stop-loss
  orders cluster **just beyond** them. Take-profits tend to **reverse** a move at the level; stops tend to
  **extend** it once the level breaks. `ok` https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr125.pdf
- Osler (2005), *J. of International Money and Finance*, "Stop-loss orders and price cascades in currency
  markets". Trends speed up when price reaches stop clusters. The effect lasts **hours, not days**, and she
  does not claim stops are the main cause of big moves. `ok` https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr150.pdf
- Kavajecz & Odders-White (2004), *Review of Financial Studies*, "Technical Analysis and Liquidity Provision".
  Support and resistance levels line up with peaks of resting orders in the book. Stock-market data, not FX;
  later studies repeated it on Taiwanese and Chinese stocks. `ok` https://ideas.repec.org/a/oup/rfinst/v17y2004i4p1043-1071.html

So "liquidity rests beyond obvious levels" is a fair description of the market. Note what these papers do
**not** say:
- that price reverses after taking the stops. Osler's documented effect is **continuation** through the level
  for some hours. The SMC sweep-and-reverse trade is the opposite bet at the same level, so test both;
- that a bank hunts your stop on purpose, or that an order block marks where an institution will buy again.

**The trading rules mostly fail open tests:**

- StatOasis (Ali Casey, Sep 2026): order block, FVG, sweep and OTE as fixed rules on daily SPY/QQQ/DIA/IWM,
  against a coin-flip entry and buy-and-hold. Of 32 t-statistics only one reached 2. Order blocks beat random
  entries in most variants but never with significance; FVG edge was about zero; nothing beat buy-and-hold.
  Limits: daily stock ETFs, long-only, no costs. `ok` https://statoasis.com/overfit/research/ict-backtest-what-survives
- Northmark / fxbroker-compass (Aug 2026): six SMC-style rules, 328 settings, 995,550 trades on FX, gold and
  US30. None passed; average −2.13 pips a trade; win rates 26–36%; entries were within −3 to +7 points of
  random. On 15-minute bars costs were 30–60% of the stop. **Weak source:** broker-affiliate site, written
  with AI help, period and exact rules not published. `ok` (opened) https://www.fxbroker-compass.com/en/blog/fx-order-block-fvg-liquidity-sweep-verification
- Vendor posts claiming 60–80% win rates give no data or method. Ignore them.

**Your own results say the same thing:**

- EA wiki: the sweep, FVG and kill-zone scalpers on gold are marginal or no-edge. The one promising SMC
  robot (SMC_Confluence) is in-sample only.
- `../concepts/vwap_volume_profile_explained.md`: on Nifty stocks the sweep + higher-time-frame checklist improved
  results in 26 of 36 comparisons. This is the best lead you have that a sweep **filter** adds something.
- The wiki also found that most of your SMC robots enter at market and never wait for the retest, do not check
  that an FVG is still unfilled, and do not tie the order block to the break it caused. So the textbook
  version of SMC has not been tested by your code yet.

**About ICT himself:** Michael Huddleston has taught online for more than a decade and has no audited long-run
track record. Critics also say his definitions change over time, which makes them hard to test. `part`
Treat his videos as the source of the vocabulary, not as proof.

## 5. What to study, in order

### A. The vocabulary (free; 2–3 weeks, do not go deeper before testing)

| Resource | Why | v |
|---|---|---|
| ICT 2022 Mentorship, 41 episodes, free on YouTube. https://www.youtube.com/playlist?list=PLVgHx4Z63paYiFGQ56PjTF1PGePL3r69s | The primary source. One complete model: sweep → displacement with FVG → entry on the retrace, inside kill zones. Watch this one series only; the channel has far more than you need | `part` (playlist opens with this title; owner channel and episode count seen only on third-party pages) |
| LuxAlgo "Smart Money Concepts" indicator, open source on TradingView | Read the Pine code: it shows one exact definition of BOS, CHoCH, order block, FVG, equal highs/lows, premium/discount. https://www.tradingview.com/script/CnB3fSph-Smart-Money-Concepts-LUX/ | `ok` |
| `smartmoneyconcepts` Python library (joshyattridge) | The same concepts on pandas OHLC data, ready for backtests. Beta, no validation of its own. https://github.com/joshyattridge/smart-money-concepts | `ok` |
| Your own `Trading-EA/wiki/concepts/smc-terms-as-coded.md` | What your code checks today, and where it differs from the textbook | `ok` |

There is no good book on SMC itself. The ones on sale are self-published summaries of the videos.

### B. The lineage (where the ideas come from; better written and testable)

| Resource | Covers | v |
|---|---|---|
| Villahermosa, *Wyckoff 2.0: Structures, Volume Profile and Order Flow* — **you own it** (`books/trading`) | Accumulation/distribution, spring and upthrust (= sweep), volume profile, order flow, in one book. Best single bridge between SMC and real order flow | `ok` |
| Villahermosa, *The Wyckoff Methodology in Depth* | Book 1; read it first if Wyckoff 2.0 Part 1 feels too fast | `part` |
| StockCharts ChartSchool, "The Wyckoff Method: A Tutorial" (free) | Phases A–E and the events on one page. https://chartschool.stockcharts.com/table-of-contents/market-analysis/wyckoff-analysis-articles/the-wyckoff-method-a-tutorial | `ok` |
| Weis, *Trades About to Happen* (Wiley, ISBN 9780470487808) | Springs, upthrusts, absorption, reading bar by bar | `ok` |
| Pruden, *The Three Skills of Top Trading* (Wiley 2007, ISBN 9780470050637) | Wyckoff as a rule-based system plus discipline | `ok` |
| Brooks, *Trading Price Action*: *Trends*, *Trading Ranges*, *Reversals* (Wiley 2011–12) | Failed breakouts and traps in great detail. Heavy reading; use *Trading Ranges* as a reference | `ok` |
| Grimes ch.1–8 and Volman — already in the roadmap and your pages | Failure tests, pullbacks, structure, with statistics (Grimes) | `ok` |

### C. Real order flow (auction theory, volume profile, footprint)

| Resource | Covers | v |
|---|---|---|
| Dalton, Jones & Dalton, *Mind Over Markets*, updated edition (Wiley 2013, ISBN 9781118531730) | The standard text on market profile and auction market theory: value area, balance vs trend days | `ok` |
| Dalton, *Markets in Profile* (Wiley) | The follow-up: longer time frames and behaviour | `part` |
| Trader Dale, *Volume Profile: The Insider's Guide to Trading* (ISBN 9781718092983) | Simple volume-profile setups, written for FX traders using futures volume. Vendor book: test the setups | `ok` |
| Trader Dale, *Order Flow: Trading Setups* | Footprint and delta setups | `part` |
| Harris, *Trading and Exchanges* (Oxford 2002, ISBN 9780195144703) | Who trades and why; order types; how stops and liquidity really work. The best cure for SMC myths | `ok` |
| Bouchaud et al., *Trades, Quotes and Prices* (Cambridge 2018, ISBN 9781107156050) | Order flow and price impact with data. Advanced | `ok` |
| Rosenberg & Traub, NY Fed Staff Report 262; Cabrera, Wang & Yang (2009) | Does CME futures order flow tell you about spot FX? Yes in part, but by the 2000s spot led price discovery. https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr262.pdf | `ok` |
| Beggs, *YTC Price Action Trader* | "Trapped traders" framing of sweeps | `unv` |

### D. Tools and data (prices are from third-party reviews, Oct–Nov 2026; check the vendor page)

| Tool | Use | Cost seen | v |
|---|---|---|---|
| TradingView Premium | Footprint chart on CME futures; you already use TradingView | ~$60–70/month + ~$7 CME data | `part` |
| Sierra Chart | Cheapest serious footprint / DOM platform | ~$46/month (package 11) + CME data; needs a funded futures account | `part` (sources disagree on data fees) |
| ATAS | Footprint, easier to start | €25–90/month; free plan has delayed data | `part` |
| Bookmap | Order-book heatmap | ~$49/month + ~$34 per exchange | `part` |
| Databento, dataset GLBX.MDP3 — **already in the roadmap** (Phases 4, 7) | Historical CME ticks and full order book (6E, 6B, 6J, GC) for research in Python | pay per use | `ok` (dataset), `unv` (price) |
| FX Replay / TradingView bar replay | Mark up SMC setups by hand — already in the roadmap | | `ok` |

Do not buy any of these before Phase 7. For Phases 3–4 candles are enough.

## 6. Turning the concepts into strategies you can test

Give each concept **one written rule** before testing. Suggested starting definitions (my proposals, not a
standard; the thresholds are starting values to vary). Index 1 = the last **closed** bar, as in MT5; never
read bar 0, which is still forming and repaints:

| Concept | Rule a computer can follow |
|---|---|
| Swing high | A bar whose high is above the highs of N bars on each side (N = 3 to 5); confirmed only after the N bars close |
| BOS | A **close** beyond the last confirmed swing in the trend direction |
| CHoCH / MSS | The first close beyond the last confirmed swing **against** the trend |
| Liquidity level | Previous day high/low, session high/low (Asian range), or two swings within 0.1 × ATR of each other (equal highs/lows) |
| Sweep | A bar trades beyond a liquidity level and **closes back inside** it |
| Displacement | A bar with body ≥ 1.5 × the average body of the last 20 bars |
| FVG (bullish) | `low[1] > high[3]` (three closed bars); the zone is valid until price trades through it |
| Order block (bullish) | The last down-close bar before the displacement that caused a BOS; valid until price closes below it |
| Premium / discount | Above / below the 50% line of the current swing range |
| Kill zone | Commonly quoted ICT hours: London 02:00–05:00 and New York 07:00–10:00, **New York time**, with DST handled. Treat the hours as a setting to test |

Then follow the Phase 4 rules already in the roadmap, with four additions:

1. **One concept at a time.** Test "sweep" alone, then "sweep + displacement", then add the FVG retrace entry.
   Keep a piece only if it improves on the step before. A ten-condition checklist cannot tell you which part works.
2. **Random-entry benchmark with the same stop, target and session.** Both outside tests above found SMC
   entries close to random, so this is the comparison that matters.
3. **Costs as a share of the stop.** Measure spread + commission as a share of the stop distance. My rule of
   thumb (not sourced): above about 10% the idea rarely survives. The Northmark test measured 30–60% on
   15-minute FX bars. This may be part of why your M1–M5 gold scalps are marginal; start on M15–H1.
4. **Enter on the retest, not at market**, and check the zone is still unfilled. This is the gap between the
   textbook and your current EAs.

Suggested first experiments, cheapest first:

- **0. Reverse or continue?** At previous-day and Asian-session highs/lows, compare two entries with the same
  stop size: fade the sweep (close back inside) and follow the break (close beyond). Osler predicts the second;
  SMC trades the first. This one test tells you which side of the level has anything.
- **A. Sweep as a filter.** Take your best non-SMC baseline (Supertrend + 200 EMA on gold). Does requiring a
  prior sweep of the previous day's or Asian-session high/low improve it out of sample?
- **B. The ICT 2022 model, written exactly:** sweep of a session level → displacement that leaves an FVG and
  breaks structure → limit order at the FVG → stop beyond the sweep → target the opposite liquidity level.
  EURUSD and XAUUSD, M15, 3+ years of real ticks.
- **C. Fix and re-test what exists:** SMC_Confluence out of sample (already step 2 of the wiki's next steps).
- **D. Later, Phase 7:** the same setups on 6E or GC futures with real delta — does absorption or a delta flip
  at the sweep separate winners from losers?

No part of this promises profit. The roadmap's base rates still apply, and the honest prior from the open
tests is that most SMC rules will not survive costs. The value of the work is finding out which piece, if
any, does.

## 7. Where this fits in the roadmap

| Phase | Add |
|---|---|
| 3 · Price, flow and positioning | Section A (vocabulary) and section B (Wyckoff 2.0, StockCharts tutorial, Weis). Task: mark sweeps, FVGs and BOS on 3 months of replay and write each as a play |
| 4 · Strategy research | A new row in the families table: "Liquidity / SMC rules — mechanism documented (Osler), rules mostly not better than random in open tests; test piece by piece". Sections 4 and 6 of this note |
| 7 · Specialise | Section C and D: Dalton, Harris, Bouchaud, footprint tools, CME futures data |

`index.html` and `resources.js` have not been changed yet.
