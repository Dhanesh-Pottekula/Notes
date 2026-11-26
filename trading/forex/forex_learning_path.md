# Forex learning roadmap (text version)

The interactive page is [`index.html`](index.html). Open it through `python3 Notes/serve_notes.py` →
`/trading/forex/`. It has the full **library of 202 resources** (`resources.js`), each with its link, level,
cost and verification badge. The page also has the calculators, a session clock in your time zone, and tick
boxes. This file is the roadmap in plain text.

Researched Nov 2026 in five parallel passes, then spot checks:
- books
- courses and media
- institutional and academic sources
- tools, data and platforms
- how professionals say to learn

**Phase lengths and move-on checks are a proposal.** No credible source gives numbers for demo length, risk
per trade or stage gates.

---

## Base rates first

| Number | What | Source / caveat |
|---|---|---|
| 61–66% | of active US accounts at one dealer were unprofitable each quarter, Q4 2025 – Q3 2026 | tastyfx disclosure; measured per quarter |
| 74–89% | of EU retail CFD accounts lost money before the 2018 leverage caps | ESMA; 12-month basis, not comparable with the US figure |
| 97% | of Brazilians who day-traded 300+ days lost money; 1.1% beat minimum wage | Chague et al.; index futures, **not FX** |
| ~7% | of 100,000 prop-firm traders ever got a payout | FPFX data via Finance Magnates; one vendor, not audited |

**Good news:** leverage *causes* losses. After the US 50:1 cap in 2010, US forex traders did better than EU
traders without a cap. The main reason is that they stopped holding losers (Heimer & Imas, *RFS* 2022). After
Australia's caps, losing accounts fell from 64% to 50% a quarter (ASIC CP348).

## Phase 0: Set up and ground rules (week 1)

**Trading from the US:**
- **Who can hold your money:** only CFTC-registered dealers. In Sep 2026 six firms held all US retail forex
  money, about $470m: FOREX.com, OANDA, Schwab Futures and Forex, tastyfx (formerly IG US), Interactive
  Brokers and Trading.com.
- **Leverage:** 50:1 on major pairs and 20:1 on others (17 CFR 5.9).
- **FIFO, no hedging:** NFA Rule 2-43 bans offsetting positions in one account, and positions close
  first-in, first-out.
- **No CFDs** for US retail.
- **Platforms:** MT5 at tastyfx and FOREX.com. OANDA US has MT4, TradingView and its API, but no MT5.
- **Gold:** FOREX.com is reported to offer spot XAU/USD to US clients, but this isn't confirmed on its US site.
  The exchange route is CME gold futures, including Micro Gold.
- **Exchange alternative:** CME Micro EUR/USD (M6E) is 12,500 EUR at $1.25 a tick. It has no daily swap.

**Scam filter:**
- The FTC acted against two trading-"education" sellers over earnings claims: Online Trading Academy (2020) and
  IM Mastery Academy / IYOVIA (2025–26).
- The CFTC fraud advisory lists the red flags.
- Check firms and people on NFA BASIC.
- Ask any vendor for a verified Myfxbook or FX Blue link.

**Do:**
- Open demo accounts at OANDA (for the Python API) and at tastyfx or FOREX.com (for MT5).
- Set up TradingView, the Forex Factory calendar and a journal.

**Move on when:** both demos work, the journal exists, and you can state the leverage cap and FIFO rule from
memory.

## Phase 1: Mechanics and market structure (weeks 1–3)

**Learn:**
- Quotes, pips and lots, and pip value.
- Spread accounts vs commission accounts.
- Leverage vs margin vs risk.
- Swap and the 5 pm New York rollover, including triple Wednesday.
- Spot, forwards, FX swaps, futures, options and NDFs.

**Market structure (BIS 2025):**
- Turnover is $9.5tn a day. FX swaps are 42% of it and spot 31%.
- The UK has about 38% of trading and the US about 19%. 59% of trading is electronic.
- Dealers internalise over 80% of customer trades.
- Last look is covered by FX Global Code Principle 17.
- FX "volume" in MT5 is tick volume, not traded size.

**Use:**
- BabyPips School of Pipsology
- Volatility.RED (the r/Forex wiki)
- CME *Introduction to FX* and the Micro FX course
- Lien, *Day Trading and Swing Trading the Currency Market*
- Weithers, *Foreign Exchange*
- Donnelly, *The Art of Currency Trading*
- The BIS Triennial Survey

**Do:**
- Code pip value and position size in Python, and check them against MT5.
- Log spreads at five times of day for a week on both demos.

**Move on when:** you can explain margin, pip value, swap and spread without notes, and your code matches MT5.

## Phase 2: Macro and central banks (weeks 3–8)

**Learn:**
- How central-bank surprises move currencies, and how to read market-implied odds of a rate move.
- Covered vs uncovered interest parity: uncovered parity fails, and that failure is the carry trade.
- Meese–Rogoff (forecasting is hard).
- Real rates, data surprises, risk-on/risk-off, commodity currencies.
- The dollar's role: on 89% of trades and 56.7% of reserves.
- Order flow, and month-end/fix flows.

**How pros learn:** go deep on one currency, and read speeches and data releases in full (Adam Button). Write a
daily note (Brent Donnelly).

**Use:**
- MIT 14.02, lectures 17–22
- St. Louis Fed module on the new policy tools
- Wang, *Central Banking 101*
- Laïdi
- Chandler
- ING THINK FX Daily
- Marc to Market
- investingLive
- Odd Lots and Macro Musings
- RateProbability or FedWatch
- FRED
- The 11 central banks' policy pages

**Do:** for four weeks, write a 5-line daily note on one pair:
1. What's priced in
2. The next catalyst
3. COT positioning
4. Your view
5. What would prove you wrong

Before each release, write your expectation and check it.

**Move on when:** four weeks of notes with no gaps, and you can explain the last three big moves in the pair.

## Phase 3: Price, flow and positioning (weeks 6–10)

**Reuse your pages:** Murphy ch.4–7 and ch.17, Grimes ch.1–8, 14 and 15, Carter, the order-flow and VWAP notes.

**FX quirks:**
- Daily candles should close at New York 5 pm.
- Session highs and lows, the Asian range and round numbers act as levels.
- The CFTC Traders in Financial Futures report shows positioning.
- The month-end and London 4 pm fix flows are documented (Evans 2018; Melvin & Prins 2015).

**Use:**
- Volman, *Understanding Price Action* (5-minute charts) and *Forex Price Action Scalping* (70-tick charts)
- Grimes's free course
- *Naked Forex* (test its setups yourself)
- Menkhoff & Taylor (2007)
- Bar replay in TradingView or FX Replay

**Do:** replay 3 months of 15-minute charts. Write each setup as a "play" with exact rules: context, trigger,
stop, target and invalidation.

**Move on when:** you have 2–3 plays a computer could follow.

## Phase 4: Strategy research (months 2–4)

| Family | Evidence |
|---|---|
| Carry | Priced risk factor (Lustig, Roussanov & Verdelhan 2011). Crashes when funding dries up (Brunnermeier, Nagel & Pedersen 2008). Weaker since ~2010. |
| Momentum | Real and largely unrelated to carry, but concentrated in costly currencies (Menkhoff et al. 2012) |
| Value | Fundamentals-adjusted real exchange rates predict returns (Menkhoff et al. 2017; Asness et al. 2013). Slow. |
| Flow timing | Month-end and fix effects documented; may be arbitraged by now |
| Session breakout, news | Untested. Small edges that spreads and fills decide. |
| Grid / martingale | Avoid |

**Backtest rules:**
1. Model spread (worst session), commission and **daily swap**.
2. Use real ticks for intraday (MT5 real-tick mode, or Dukascopy via Tickstory).
3. Add slippage and delay, and test on two data sources.
4. Keep parameters few, and prefer settings that work across a range.
5. Use walk-forward.
6. Benchmark against carry/trend baselines and random entries.
7. Get enough trades.
8. Keep turnover low.

**Use:**
- Carver, *Systematic Trading* and *Leveraged Trading*, plus his blog
- The carry, momentum and value papers
- Robot Wealth on carry and on turnover
- Dukascopy, Tickstory, the MT5 tester
- The OANDA v20 API
- NautilusTrader or LEAN

**Do:**
- Build G10 carry and 12-month momentum baselines from FRED.
- Re-test the EAs in `projects/Trading-EA/` on real ticks over 2+ years, with slippage, walk-forward and a
  second data source.
- Drop hedged-position logic if you'll trade a US account.

**Move on when:** one strategy shows positive expectancy after all costs out of sample, holds up across nearby
settings, beats random entries, and has a drawdown you'd accept with real money.

## Phase 5: Demo forward test (2–3+ months, 50–100 trades)

**Do:**
- Trade only the Phase 4 plays, sized with the calculator.
- Journal every trade: setup, reason, screenshot, costs, whether you followed the rules, and emotion.
- Compare results with the backtest's expected range.

Donnelly's win rate is 50–53% every year: he profits because his winners are bigger than his losers.

**Use:**
- Rick Wright's daily routine
- Douglas, *Trading in the Zone*
- Steenbarger
- The Donnelly interview
- Myfxbook, FX Blue or Tradervue

**Move on when:** at least 2–3 months and 50–100 trades have passed (whichever comes later), results are inside
the backtest range, the journal is complete, and there were zero rule breaks in the last month.

## Phase 6: Small live (6+ months, 100+ trades)

**Rules:**
- **Capital:** money you can lose; Carver's Starter System needs about $1,500.
- **Leverage:** effective leverage about 1–1.5× (Carver, and the r/Forex wiki).
- **Risk per trade:** ≤ 0.5–1% of equity. This is a rule of thumb, not sourced.
- **Loss limits:** set a daily and a monthly limit.
- **Reviews:** monthly and quarterly, as a business. Separate bad luck from process errors.

Prop challenges are a paid lottery with known odds, not a learning stage.

**Use:**
- Donnelly, *Alpha Trader*
- The Market Wizards books (Kovner, Lipschutz)
- IBKR or CME micro FX futures
- Edgewonk
- am/FX ($69/month) if you want a paid daily

**Move on when:** 100+ live trades over 6+ months, with cost-adjusted returns positive and in line with the
backtest, and drawdown within limits.

## Phase 7: Specialise and scale (ongoing)

**Scaling:** increase size in steps, only after good reviews. Add strategies that don't move together;
Donnelly lost his edge after 2008 because he had only one.

**Areas to specialise in:**
- **Microstructure:** Lyons, Evans, Sarno & Taylor, BIS papers on execution algorithms.
- **Options:** DeRosa → Jewitt → Wystup or Castagna.
- **History:** Eichengreen, Funabashi, Naef, Soros.
- **CME futures data:** Databento.

## Routine

| When | What |
|---|---|
| Before | Check you're fit to trade · balance and risk checked · open orders checked · calendar and what's priced in · overnight headlines plus one bank note · dollar index, yields, oil, gold, equities · higher time frames, then your own, with levels marked |
| During | Only playbook trades · size with the calculator, stop and target set before entry · decide before events whether to exit, trail or stay awake · no new trades after the daily loss limit |
| After | Journal every trade with a screenshot · log daily P&L · replay the day bar by bar · check overnight event risk |
| Weekly / monthly | Weekend calendar and COT · one-page weekly note · monthly stats by play · quarterly keep/fix/drop · change size only at reviews |

Sources: Rick Wright (FXStreet), the r/Forex wiki's process page, the Donnelly interview.

## Mistakes that end accounts

1. Too much leverage
2. Overtrading
3. Overfitting
4. Ignoring swap and spread
5. Holding losers while cutting winners
6. Averaging down, grids, martingale
7. Copying others and joining signal groups (Heimer & Simon)
8. Strategy hopping
9. Having only one strategy
10. Paying gurus

## Sources

Every source is in `resources.js`, with a verification field: `ok` means the link was confirmed (opened, or returned by a search with matching details), `part` means only
through search summaries, `unv` means from memory. The page's Method section lists the sources behind each
number. The main ones:
- BIS QR Dec 2025: https://www.bis.org/publ/qtrpdf/r_qt2512b.htm
- CFTC FCM/RFED data: https://www.cftc.gov/MarketReports/financialfcmdata/index.htm
- 17 CFR 5.9: https://www.law.cornell.edu/cfr/text/17/5.9
- NFA Rule 2-43: https://www.nfa.futures.org/rulebook/rules.aspx?RuleID=RULE%202-43&Section=4
- tastyfx disclosure: https://prod.wsprod.tastyfx.com/public-and-risk-disclosures/
- ESMA 2018: https://www.esma.europa.eu/press-news/esma-news/esma-agrees-prohibit-binary-options-and-restrict-cfds-protect-retail-investors
- ASIC CP348: https://download.asic.gov.au/media/2v2br3vw/cp348-published-18-october-2021.pdf
- Heimer & Imas: https://econpapers.repec.org/RePEc:oup:rfinst:v:35:y:2022:i:4:p:1643-1681.
- FPFX prop data: https://www.financemagnates.com/forex/exclusive-only-7-of-300000-prop-trading-accounts-achieved-payouts/
- FTC, Online Trading Academy: https://www.ftc.gov/news-events/news/press-releases/2020/09/ftc-settlement-requires-online-trading-academy-forgive-consumer-debt-principals-turn-over-millions
- FTC, IM Mastery Academy: https://www.ftc.gov/legal-library/browse/cases-proceedings/im-mastery
- Donnelly interview: https://excessreturnspod.substack.com/p/full-transcript-brent-donnelly-on-862
- Carver: https://qoppac.blogspot.com/2019/10/new-book-leveraged-trading.html
- r/Forex wiki: https://volatility.red/Forex
