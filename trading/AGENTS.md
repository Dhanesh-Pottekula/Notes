# trading/ — trading books, pages and my own notes

Part of `Notes/` (map: `../AGENTS.md`). Two kinds of file, kept apart:

- **Pages to read** (HTML): the three book folders, `forex/`, and the two pages at this level. Open them from the
  home page (`../index.html`, via `python3 Notes/serve_notes.py`). **Do not move or rename them** — saved
  highlights are keyed by page path.
- **My notes** (Markdown): sorted by kind into the four folders below. Nothing loose at this level.

```
trading/
├── murphy/ grimes/ carter/     book study pages (HTML; each index.html is built by ../tools/build_book_index.py)
├── forex/                      forex roadmap page + its data and research
├── trading_equations.html      interactive equation sheet
├── murphy_moving_averages_visual.html
├── concepts/                   how something works (markets, costs, maths, one method explained)
├── indicators/                 one indicator, or a comparison of indicators
├── strategies/                 rules you could trade: setups, playbooks, the standard setup
└── backtests/                  results of testing a strategy (one file per test or sweep)
```

## Where a new note goes

| The note is about… | Folder |
|---|---|
| How a market mechanism, cost, formula or method works | `concepts/` |
| How one indicator works, its settings, or indicators compared | `indicators/` |
| Entry/exit rules, a setup, a playbook | `strategies/` |
| What happened when a strategy was tested (trades, sweeps, per-stock checks) | `backtests/` |

Notes mention each other by bare file name (`backtest_results_summary.md`), so a note can be found with a search
whichever folder it is in. Add a row below when you add a note. Backtest code lives in `../../projects/`, not here.

## Pages

| Path | What it is |
|------|------------|
| `trading_equations.html` | Same sheet as an interactive page with Kelly, position-size and Black–Scholes calculators (open in a browser; published copy: https://claude.ai/artifact/4Wp5pK3T9zt3yPuJPeJGCU) |
| `murphy_moving_averages_visual.html` | **Visual, interactive version of the same chapter** (open in a browser): 20 sections in book order, each with plain words, a 'picture it' intuition, a live simulated chart (lag, SMA/WMA/EMA weights, drop-off echo, 1/2/3-MA crossover systems with costs, envelopes, Bollinger squeeze, centering, cycle cancelling, weekly 10/40, trend vs chop P&L, 4-week rule, in- vs out-of-sample optimisation, Kaufman AMA + Efficiency Ratio), connections to my backtests, and a 10-question self-check |

## Books

| Path | What it is |
|------|------------|
| `murphy/` | **Technical Analysis of the Financial Markets (John Murphy) study pages**: open `index.html`; ch01–19, one interactive page per chapter. Pictures in `illus/` |
| `grimes/` | **The Art and Science of Trading (Adam Grimes, course workbook) study pages**: open `index.html`; ch00 foreword + ch01–15 (pages link ahead to a ch16 that is not written yet). Pictures in `illus/` |
| `carter/` | **Mastering the Trade (John Carter) study pages**: open `index.html`; ch00 foreword + ch01–14 (the book has 24 chapters; ch15–24 are not written yet, and some pages link ahead to them). Pictures in `illus/` |

## Forex

| Path | What it is |
|------|------------|
| `forex/index.html` | **Forex learning roadmap, interactive** (open through `serve_notes.py` → `/trading/forex/`): base rates (US quarterly profitability, ESMA, leverage-cap evidence); 8 phases (0 set up + US rules/scam filter · 1 mechanics & market structure · 2 macro & central banks · 3 price, flow & positioning · 4 strategy research & backtest rules · 5 demo forward test · 6 small live · 7 specialise), each with goal, concepts, picked resources, a task and a move-on check (labelled as a proposal); pip-value/position-size calculator, leverage widget with US caps and effective leverage, session clock in the viewer's time zone; daily/weekly routine; mistakes; **filterable library of 202 resources** (books, courses, video, podcasts, research, papers, official data, tools, data, communities, blogs) with verification badges; concept checklist. Ticks in localStorage `forex-roadmap-v2` |
| `forex/resources.js` + `forex/forex_learning_path.md` | Library data for the page (`window.FX_RESOURCES`: stable `id` slugs — ticks use them, never rename; `v` = ok/part/unv verification) and the roadmap as plain text (phases, base rates, routine, mistakes, main sources). Researched Nov 2026 by five parallel passes + spot checks |
| `forex/smc_order_flow_research.md` | **SMC / ICT and order flow add-on to the forex roadmap** (2026-11-17): what the roadmap covers and lacks, concept by concept (BOS/CHoCH, sweeps, order blocks, FVG, kill zones, Wyckoff, delta, volume/market profile); SMC "order flow" vs real order flow (needs CME futures); evidence (Osler 2003/2005 stop clusters, open backtests that find no edge, own EA results); books and tools with ok/part/unv tags; rules a computer can follow and a test plan; where each item fits in Phases 3, 4, 7. Not yet merged into `index.html` / `resources.js` |

## concepts/

| Path | What it is |
|------|------------|
| `concepts/breakeven_move_fyers.md` | **How far a ₹4,000 stock must move to cover FYERS charges + slippage**: charge table (intraday vs delivery), break-even move by trade size (intraday ~0.1–0.2%, delivery ~0.3–0.4%, 1.35% for a single share), what that does to the required win rate |
| `concepts/how_to_sell_stocks.md` | **How to sell stocks on NSE / FYERS**: delivery (CNC) vs intraday (MIS) vs short selling, app steps, order types (market, limit, stop-loss, GTT, AMO), DDPI / CDSL TPIN authorisation, T+1 settlement, charges, tax, common mistakes |
| `concepts/index_funds.md` | **Index funds** (the benchmark to beat): what they are, index mutual fund vs ETF, expense ratio and tracking error, Indian indices (Nifty 50, Next 50, 200/500, Midcap, Momentum 30 and other factor indices), why they're hard to beat (SPIVA), tax, how to choose |
| `concepts/merton_simons_and_quant_models.md` | What "the Merton equation" and "Jim Simons' theory" mean, whether they're still relevant, other quant models ranked for a retail NSE trader, Kelly applied to my own backtests, book pointers, sources |
| `concepts/murphy_moving_averages.md` | **Murphy's Moving Averages chapter** (pdf p232–264): SMA/WMA/EMA, 1-, 2- and 3-MA crossover rules (5/20, 10/50, 4-9-18), envelopes, Bollinger Bands, cycle/Fibonacci lengths, weekly MAs, pros/cons, 4-week rule (Donchian), optimisation, Kaufman AMA; linked to my backtest results |
| `concepts/order_flow.md` | **Order flow** (the "force" moving price): limit vs market orders, order book, Kyle's lambda ΔP = λ × net flow, delta / CVD / absorption / imbalance / footprint / volume profile, slow India flow data (delivery %, futures OI build-up, option OI, FII/DII, bulk deals), how to use it as a filter, limits (HFT, spoofing, data), ideas to test |
| `concepts/price_physics_basics.md` | **Price as a moving object**: physics → price dictionary (distance = return, velocity = momentum, acceleration = MACD histogram, spring = mean reversion/OU, shaking = volatility, friction = costs), the GBM prediction equation, why drift grows with t but noise with √t (drift/noise table per horizon), and how that explains the backtest results |
| `concepts/tori_trendlines_explained.md` | **How Tori's trendline method works**: swing points (5-bar pivots), support/resistance lines and the line equation, Action vs Safety line, Break and Bounce setups, 3-ATR rule, trailing exit, worked ₹ example, test results (Break works on daily, Bounce fails, 15m/1h lose, rarely beats buy-and-hold), how to use it |
| `concepts/trader_returns_reality.md` | **How much traders actually make**: SEBI studies (87.7% of F&O traders lost in FY26, 93% over FY22–24, 71% of intraday traders in FY23), Brazil/Taiwan day-trader studies, SPIVA India (76% of large-cap funds lag the index over 10 years), realistic return ranges, the N × E × r yearly-return equation, a can-I-make-money checklist with Indian tax rates, sources |
| `concepts/trading_equations.md` | **Trading equation cheat sheet** (19 formulas): expectancy, Sharpe, Sortino, max drawdown, CAPM/Fama–French; Kelly, Merton fraction, position sizing, vol targeting; ATR, annualised vol, GARCH; Black–Scholes + expected move; spread z-score, Ornstein–Uhlenbeck; HMM regimes; Almgren–Chriss, Avellaneda–Stoikov. Each with symbols, ₹ worked example, pitfalls |
| `concepts/using_equations_to_trade.md` | How the equations turn into profits: which still matter, a 5-step workflow (edge → backtest pass/fail → sizing → trade management → kill switch), a sizing Monte Carlo on my 51.5%/2R setup, and what it means for my backtests |
| `concepts/vwap_volume_profile_explained.md` | **VWAP + volume profile** (from the MindMath Money VWAP course and the Currency Pros volume-profile video): VWAP formula, bands, anchors, rolling VWAP, the course's mean-reversion / trend / band-2 reversal rules, POC and the Currency Pros checklist (BOS, sweep, imbalance, 67/75% fib), and backtest results on Nifty 50/200 (VWAP not worth trading; 15-min full-checklist setup a paper-trade lead) |

## indicators/

| Path | What it is |
|------|------------|
| `indicators/kama_kaufman_adaptive_moving_average.md` | **Kaufman Adaptive Moving Average + Efficiency Ratio**: ER = net move ÷ total path, ER → smoothing constant → KAMA (10, 2, 30) with table, worked examples, Nifty Oct 2026 example, how to tell trend vs sideways (ER, ADX, Choppiness, MA slope, BB width), my test that ER does **not** predict the next period's trendiness (corr ≈ 0, same as a random walk; volatility does persist), how to use it as a filter/trailing exit |
| `indicators/trend_vs_sideways_tools.md` | **Trend or sideways — which tool for what**: ER vs ADX vs Choppiness vs MA slope vs Bollinger width (what each measures, overlap, settings), my test on 185 Nifty 200 stocks 2014–26: none predicts next-period trendiness, BB width predicts volatility (squeeze → +10% vol), trend filters roughly double a trend-follower's gross edge (Chop < 38 best, ADX > 25 / MA slope close) but amplify good and bad years; use-case table and a practical combo |

## strategies/

| Path | What it is |
|------|------------|
| `strategies/intraday_swing_playbook.md` | **Rule-by-rule setups**: intraday (ORB on stocks in play, intraday momentum on Nifty futures, VWAP pullback, VWAP mean reversion) and swing (breakout + volume, uptrend pullback, trendline Break, daily MACD, futures pairs) — entry, stop, exit, filters, evidence rating, book pages, comparison table |
| `strategies/stoch_rsi_macd_strategy.md` | **My Stochastic RSI + MACD strategy**: rules (trend + %K/%D cross + MACD histogram rising), how the indicators work, backtest result on Nifty 50/200 15m–4h buy vs sell, intraday vs delivery (not worth trading; one small 15-min intraday sell lead); re-test with my final rules (no EMA, not-overbought/oversold, steep cross) — still not profitable on Nifty 50 |
| `strategies/strategies_by_timeframe.md` | Which strategies suit **scalping, intraday and delivery/swing** on NSE: real round-trip costs (Fyers model), break-even win-rate formula, ORB / intraday momentum / VWAP / pairs for intraday, momentum / quality / vol-managed / trend breakouts for delivery, verdict per style, sources |
| `strategies/strategies_from_equations.md` | **5 money-making strategies built on the equations**, each with exact rules, examples and risks: momentum + vol targeting, volatility-managed Nifty allocation (Merton + GARCH), pairs trading (OU), trend following on futures (ATR), selling options when IV > GARCH forecast; plus an HMM regime filter and the order to try them |
| `strategies/strategy5_standard_setup.md` | **Strategy 5 standard setup (one page)**: daily chart, ROC 20 > 7 · close above EMA 50 · MACD 12/26/9 histogram rising · Stoch RSI 3/3/14/14 cross below 50 → buy at close; sell when blue touches orange; optional stop at the buy-day low; ₹1L per stock, ≈ ₹5L capital; test results |

## backtests/

Start with `backtests/backtest_results_summary.md`: it says what worked and what failed overall.

| Path | What it is |
|------|------------|
| `backtests/adaniports_apr_jun_2026_strategy2.md` | **ADANIPORTS 1 Apr – 30 Jun 2026, Strategy 2 + B200 + ADX30 (± +DI, ± 200-average slope rising)**, all timeframes, every trade: +₹8,399 on 24 trades vs ≈ +₹30k buy-and-hold (stock +30.7%); slope filter changed nothing, +DI removed good pullback buys |
| `backtests/adaniports_macd_stoch_backtest.md` | **My MACD (both lines above/below 0, gap widening) + Stoch RSI (cross with blue < 50 / > 50, buy at the cross candle's close, exit at the close of the next touch) rules on ADANIPORTS and all Nifty 50**: 15m/30m/1h/4h/daily × intraday/delivery × buy/sell, FYERS charges only (no slippage) with the full rate list; ADANIPORTS sells looked good on 6–18 trades but **all 18 Nifty 50 versions lose** (move per trade ≈ 0 vs 0.08–0.28% charges); closest = daily/4-hour delivery buys. Every trade in `../projects/trading-equation-backtests/reports/ADANIPORTS_STOCH_MACD_REPORT.md` and `STOCH_MACD_ABOVE0_N50_REPORT.md` |
| `backtests/backtest_results_summary.md` | **Results of testing the strategies** (Oct 2026): what worked (momentum rotation, weekly pullback), what failed (all intraday — 15-min ORB failed the Nifty 200 re-check, 5-min ORB only a lead — MACD crossover on every timeframe 1m–weekly, 1-hour, pairs, futures intraday momentum), which equations mattered, intraday vs delivery verdict. Full report: `../projects/trading-equation-backtests/reports/REPORT.md` |
| `backtests/bel_macd_stoch_delivery_buys.md` | **BEL delivery buys, 23 Oct 2023 – 9 Jun 2026, my 4 MACD + Stoch RSI strategies** (all: blue crosses orange + histogram bigger than previous; 1: MACD & signal > 0, blue < 50; 2: blue < 50; 3: as 1 with < 70; 4: as 2 with < 70) on 15m/30m/1h/4h/daily, FYERS charges only: 15m–1h lose with every strategy; 4h/daily all positive but mostly BEL's +210% rise; **best lead = Strategy 2 on 4-hour** (+₹51k / 66 trades, +₹19.8k without best 3, beats 89% of random buys). Every trade in `../projects/trading-equation-backtests/reports/BEL_DELIVERY_BUYS_REPORT.md` |
| `backtests/eternal_jun_sep_2026_settings_sweep.md` | **ETERNAL 10 Jun – 10 Sep 2026, no-ROC rules, 864 MACD × Stoch RSI settings on 15m/30m/1h/4h/daily**: daily best MACD 8/17/9 + Stoch 3/5/7/7 (5 trades, +₹20,555, every trade listed), 698/864 daily settings positive; 15m/1h mostly lose; holding ETERNAL (+34%) beat all |
| `backtests/eternal_sep_oct_2026_check.md` | **ETERNAL, standard Strategy 5 check, 16–24 Sep and 22–26 Oct 2026**: day-by-day ROC/EMA/MACD/Stoch values and which rule failed; no buy in either window (17 Sep: only ROC failed; 26 Oct: ROC and blue > 50); what-if without ROC |
| `backtests/nifty50_uptrends_200dma.md` | **Main uptrend start/peak/end date of every Nifty 50 stock** (rule: start = first of 5 closes in a row above the 200-day average, end = first of 5 below; main = biggest rise peaking since 2023), with prices and gains, BEL check vs my hand-marked window, which stocks are still in an uptrend; charts per stock in `../projects/trading-equation-backtests/reports/uptrends_n50/` |
| `backtests/strategy2_above_200ma.md` | **Strategy 2 delivery buys only when price is above the 200 average for the last 5 candles**, Nifty 50, all timeframes, FYERS only (A: 5 daily closes above 200-day avg; B: 5 candles above the 200-candle avg of the traded timeframe): only daily is positive (+₹73k, but random buys with the same filter +₹57k); 4-hour −₹1.77L / −₹69k; lost in 2025–26; comparison table of every filter tried |
| `backtests/strategy2_in_uptrends.md` | **Strategy 2 delivery buys only inside uptrends, Nifty 50, all timeframes**: MAIN (each stock's main 200-day uptrend, hindsight) vs LIVE (any confirmed 200-day uptrend, tradable), FYERS only, shares and charges, random-buy check: **MAIN 4-hour +₹3.54L, beats 96% of random buys**; MAIN daily +₹4.99L but mostly the uptrend; **LIVE 4-hour −₹2.67L, daily +₹49k ≈ random**; 15m–1h lose either way |
| `backtests/strategy2_ma_adx_adaniports.md` | **Strategy 2 + 50/100/200 average filter (daily A or same-timeframe B) ± ADX(14) > 40, ADANIPORTS only**, delivery buys, all timeframes, FYERS only: no average length wins consistently (all lose in total); **ADX > 40 alone best, +₹39.9k on 87 trades**; average + ADX leaves 36–67 trades; next = run on Nifty 50 |
| `backtests/strategy2_ma_adx_nifty50.md` | **Strategy 2 + 50/100/200 average (A daily / B same timeframe) + ADX 30/40, sell the moment blue crosses below orange inside the candle, all Nifty 50, all timeframes**, FYERS only, 21 versions: every version loses in total (15m–1h); **best = 4-hour + ADX > 30 + average, +₹88–97k on ~700 trades, beats random 97–100%, but only 2023–24**; ADX 30 beats 40; intra-candle vs close-exit comparison; **+DI above −DI** (4-hour/daily): every ADX30 version positive and much steadier in 2025–26 but lower 4-hour totals (B200+ADX30+DI +₹58k, beats random 100%) |
| `backtests/strategy2_nifty50_delivery.md` | **Strategy 2 (histogram bigger than previous + Stoch blue crosses orange below 50; sell = exact opposite above 50) on all Nifty 50, delivery, 23 Oct 2023 – 26 Oct 2026, every timeframe**, FYERS charges only, shares and charges per trade: **every timeframe and side loses** (buys −₹69L, sells −₹47L over 87,848 trades); 4-hour/daily buys earn gross but less than the 0.28% delivery charge (STT > gross profit); BEL's lead doesn't carry over |
| `backtests/strategy5_experiment_intraday_buy.md` | **EXPERIMENT: the standard daily setup but buy during the day the moment blue crosses orange** (day followed with 1-hour candles; same-day sell as a cautious–favourable range): 626 trades vs 299, net +₹21k to +₹2.44L vs +₹1.53L for buy-at-close; crosses that fail the same day lose ₹1.6–2.4L; not better than the standard. **Experiment 2: check at 1:15 / 2:15 / 3:15 pm and buy then** (exact, no range): **2:15 pm best, +₹1.64L, positive every year incl. 2026 (+₹18k)**; 3:15 pm ≈ close; 1:15 pm +₹1.17L; **2b: buy any time after 2:15 pm when blue crosses = +₹1.94L to +₹2.17L (408 trades), +₹41–63k more than buying at the close, every year positive** |
| `backtests/strategy5_portfolio_1lakh.md` | **₹1 lakh compounding portfolio, Experiment 2b (buy after 2:15 pm), all Nifty 50, 2023 – Oct 2026**: every trade (company, buy/sell date & time, price, shares, amount, money before/after), indicator values at buy and sell, FYERS charges per trade, profit/loss per company, 1–5 stocks at a time (4 best: ₹1L → ₹1,17,314, +4.3%/yr, total profits ₹1,03,851 / losses −₹86,537), why ₹1L does worse (best signals skipped, charges 0.38%), strongest-ROC-first vs random |
| `backtests/strategy5_roc_ema_macd_stoch_sweep.md` | **Strategy 5 (ROC 100 > 2 + close above 100 EMA + MACD histogram rising + Stoch RSI cross below 50; sell on the first blue/orange touch) settings sweep on Nifty 50**, all timeframes, buy at close vs during the candle (cautious/favourable range), FYERS only, train 2023–24 / test 2025–26: your settings lose everywhere; best settings from train fail in test almost always; 15m–1h lose with every setting; daily ROC 20 > 2/3/5 positive in both periods (follow-up in `strategy5_roc_ema_sweep.md`) |
| `backtests/strategy5_roc_ema_sweep.md` | **Strategy 5 follow-up: ROC length (10–200) × level (0–15%) × EMA length (20–200) × EMA rule (1 or 5 candles), 560 settings × 5 timeframes, Nifty 50, buy at close**: daily is the only robust timeframe (163 settings positive in both periods); **short ROC (10–20 days) works, long ROC (100–200, incl. 100) loses in 2025–26**; best = daily ROC 20 > 7 + EMA 50: +₹1.53L, +47k/+53k/+57k/−4k by year, beats random 97%; also the standard setting on 1h/4h (daily best) and high ROC levels incl. ROC > 25 (smaller profits on daily; 4-hour ROC 150 > 25 +₹1.12L, mostly 2024); and a stop-loss at the buy candle's low (daily standard +₹1.54L ≈ no change, cuts event-day crashes; ROC 20 > 5 + stop +₹1.99L; 4-hour ROC 250 > 30 + stop +₹1.42L) |
