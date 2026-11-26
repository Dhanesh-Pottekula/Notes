# Intraday & Swing Playbook

Concrete, rule-based setups for intraday and swing trading on NSE: entry, stop, exit, filters,
the equation behind each, how strong the evidence is, and where my books cover it.
Background and cost math: `strategies_by_timeframe.md`. Formulas: `trading_equations.md` (eq N).
Education, not investment advice. Backtest every setup with costs before trading it.

**Evidence ratings:** Strong = academic evidence incl. India · Mixed = positive gross, weak/unclear net ·
Mine = my own backtest in `projects/trading experiments/` · Untested = popular, no solid study found.

---

## Intraday (square off by 15:15–15:25)

### Risk rules for every intraday setup
- Risk **0.25–0.5%** of capital per trade; quantity = (capital × risk%) ÷ (entry − stop) (eq 8).
- **Stop trading for the day at −1% to −2%.**
- Max 2–3 trades a day; only liquid large caps (Nifty 50/100) or Nifty/Bank Nifty futures.
- Avoid the first 5 minutes' noise and trading after 15:00 unless the setup needs it.

### I-1. Opening Range Breakout (ORB) on stocks in play — Mixed
- **Filter:** relative volume RVOL = first-15-min volume ÷ 20-day average first-15-min volume **> 2**
  (news, results, block deals). Gap of 1%+ helps.
- **Setup:** opening range = high/low of **09:15–09:30**.
- **Entry:** a 5-minute candle **closes** above the range high (long) or below the low (short).
- **Stop:** opposite side of the range, or the range midpoint if the range is wide.
- **Exit:** 2R target, or trail under each 5-min higher low; close by 15:15.
- **Equations:** RVOL, ATR (eq 10), expectancy after costs (eq 1).
- **Books:** Grimes ch.15 "Opening Range" (pdf p533); Carter ch.7 "Opening Gap" (pdf p166).
- **Mine:** NY ORB gold version in `ny_orb_v1_backup.pine` (no report yet).

### I-2. Intraday momentum on Nifty futures — Mixed (strong in US, untested in India)
- **Signal:** $r_{\text{first}} = P_{09:45} / P_{\text{prev close}} - 1$.
- **Entry:** at **15:00**, long Nifty futures if r_first > 0, short if < 0. Skip if |r_first| < 0.25%.
- **Exit:** **15:25**. Stop at 0.5 × the day's ATR(14, 5-min) from entry.
- **Why:** only one trade a day, so costs stay small. Stronger on volatile / high-volume / news days.
- **Source:** Gao, Han, Li & Zhou, *JFE* 2018.

### I-3. VWAP pullback on trend days — Untested
- **Trend-day filter:** price broke the opening range and stays above VWAP (long) or below it (short);
  VWAP is sloping in that direction.
- **Entry:** price pulls back to touch VWAP and a 5-min candle closes back in the trend direction
  (a bullish engulfing / hammer at VWAP for longs).
- **Stop:** 0.5 × ATR(14, 5-min) beyond VWAP.
- **Exit:** the day's high/low retest or 2R; close by 15:15.
- **Equations:** $\text{VWAP} = \sum P_i V_i / \sum V_i$, ATR (eq 10).
- **Books:** Grimes ch.4 "Pullback" (pdf p156); Nison ch.4 reversal candles (pdf p42).

### I-4. VWAP mean reversion on range days — Untested
- **Range-day filter:** first-hour range smaller than its 20-day average; no news; VWAP flat.
- **Signal:** $z = (P - \text{VWAP}) / \sigma_{\text{intraday}}$, where σ is the std of 5-min closes from VWAP.
- **Entry:** fade |z| > 2 (sell above, buy below) after a reversal candle.
- **Stop:** |z| > 3. **Exit:** back at VWAP. No new trades after 14:30.
- **Risk:** on a trend day this keeps losing — the range-day filter is essential.

### Intraday setups to avoid
- **Scalping on 1–5 min** in cash: needs ~77% win rate to break even (see `strategies_by_timeframe.md`).
- **Indicator crossovers on 5m** (MACD/RSI/Stoch, SuperTrend+DI): my backtests lost after costs.

---

## Swing (hold days to weeks, delivery)

### Risk rules for every swing setup
- Risk **0.5–1%** per trade with an ATR-based stop (eq 8, 10); hold 5–15 positions max.
- **Market filter:** take longs only when Nifty is above its 200-day moving average (or halve size below it).
- Avoid holding through quarterly results unless the setup is about results.
- Benchmark each setup against simply holding Nifty (Sharpe, alpha — eq 2, 5).

### S-1. 52-week-high / 50-day breakout with volume — Strong (momentum family)
- **Filter:** stock within ~5% of its 52-week high; Nifty above 200 DMA.
- **Entry:** daily close above the **50-day high** on volume > 1.5 × the 20-day average.
- **Stop:** 2–3 × ATR(14) below entry. **Exit:** trail at the **20-day low** (or 3 × ATR trailing).
- **Win rate** is typically 35–45%; winners must be large — don't take early profits.
- **Equations:** ATR (eq 10), position size (eq 8), expectancy (eq 1).
- **Books:** Grimes ch.7 "Breakout" (pdf p275); Carter ch.11 "The Squeeze" (pdf p245).

### S-2. Pullback in an uptrend — Mixed (must test)
- **Trend filter:** price above the 50- and 200-day moving averages; 50 DMA above 200 DMA.
- **Entry:** pullback to the **20-day EMA** (or 3–5 down days in a row), then a daily close back above the prior day's high.
- **Stop:** below the pullback low or 1.5 × ATR. **Exit:** retest of the recent high, or 2–3R.
- **Note:** a short RSI (2-period) below 10 is a popular pullback trigger, but standard RSI(14) rules
  failed on the Sensex in Indian research — test before trusting any RSI variant.
- **Books:** Grimes ch.4 "Pullback" (pdf p156), ch.14 "Moving Averages" (pdf p492).

### S-3. Trendline Break (daily) — Mine
- **Setup:** pivot-based trendline (Tori "Action line"); entry on the daily close that breaks it,
  2- or 3-touch line.
- **Stop:** beyond the last pivot. **Target:** 2R.
- **My result:** 51.5% win rate, profitable on **13/13 symbols**, but it **rarely beat buy-and-hold**.
  Next step: compute alpha vs Nifty and combine with the S-1 market/momentum filters.
- **Files:** `tori_trendline_lab.pine`, `tori_multistock_playbook.md`.

### S-4. Daily MACD trend with "MACD crosses down" exit — Mine
- **Entry:** MACD crosses above signal, RSI > 50, Stochastic %K < 80 (daily chart).
- **Exit:** MACD crosses back below signal.
- **My result (Reliance):** profit factor ~**1.5–1.7 after delivery costs** on daily; lost on 5m.
  Needs a multi-stock and out-of-sample test before use.
- **File:** `reliance_macd_rsi_stoch.pine`.

### S-5. Pairs trade via stock futures — Strong in Indian futures (2011–2017), not in cash
- **Setup:** two cointegrated F&O stocks (same sector), half-life 5–30 days (eq 15–16).
- **Entry:** |z| > 2 — short the rich leg, long the cheap leg (β-weighted, rounded to lots).
- **Exit:** z ≈ 0. **Stop:** |z| > 3.5 or 3 half-lives.
- Full rules: `strategies_from_equations.md` #3.

### Positional (weeks to months) — strongest evidence of all
- **Momentum rotation with vol targeting**, **quality / low-vol portfolios**, **volatility-managed Nifty** —
  full rules in `strategies_from_equations.md` #1–2. Fewest trades, lowest cost drag.

---

## Quick comparison

| Setup | Style | Trades | Win rate (typical) | Evidence | First thing to test |
|---|---|---|---|---|---|
| I-1 ORB stocks in play | Intraday | 0–2/day | 25–45% | Mixed | Net of costs on Nifty 100, 2+ years of 5-min data |
| I-2 Intraday momentum | Intraday | ≤1/day | ~50% | Mixed | Nifty futures, 09:45 signal → 15:00–15:25 trade |
| I-3 VWAP pullback | Intraday | 0–2/day | — | Untested | Trend-day filter accuracy |
| I-4 VWAP reversion | Intraday | 0–3/day | — | Untested | Range-day filter accuracy |
| S-1 Breakout + volume | Swing | few/month | 35–45% | Strong | 50-day high breakout on Nifty 200 |
| S-2 Uptrend pullback | Swing | few/month | 50–65% | Mixed | 20-EMA pullback vs RSI(2) trigger |
| S-3 Trendline Break | Swing | few/month | ~51% | Mine | Alpha vs Nifty |
| S-4 Daily MACD | Swing | few/month | — | Mine | 20 stocks, out-of-sample |
| S-5 Futures pairs | Swing | few/month | — | Strong (futures) | Cointegrated F&O pairs |

**Where to start:** S-1 (breakout + volume) for swing and I-2 (intraday momentum) for intraday — both
have research support, few trades, and simple rules that are easy to backtest honestly.
