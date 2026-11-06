# ETERNAL, 10 Jun – 10 Sep 2026 — MACD × Stoch RSI Settings on Every Chart (no ROC)

Rules (the no-ROC version from `eternal_sep_oct_2026_check.md`): buy at a candle close when the close is above EMA 50, the MACD
histogram is bigger than the previous bar, and Stoch RSI blue crosses above orange **with blue below 50 on that buy candle**; sell
the moment blue touches orange; trade again on the next signal; a trade still open on 10 Sep is sold at the last close.
Delivery, ₹1,00,000 per trade, FYERS charges only. Education, not investment advice.
Script `../../projects/trading-equation-backtests/experiments/strategy5_window_sweep.py`; all results and the top trades in
`reports/strategy5/window_sweep_eternal_2026-06-10_2026-09-10/`.

**Tried:** MACD 12/26/9 (default), 8/21/5, 5/35/5, 19/39/9, 8/17/9, 24/52/18 × Stoch RSI K 2/3/5 × D 2/3/5 × RSI length 7/9/14/21 ×
stochastic length 7/9/14/21 = **864 settings per chart**, on 15-min, 30-min, 1-hour, 4-hour, daily. ETERNAL rose **+34.3%** in the
window (₹239.80 → ₹322.10), so holding it would have made about +₹34k on ₹1L.

## Results (net ₹ after FYERS charges, ₹1L per trade)

| Chart | Default (MACD 12/26/9, Stoch 3/3/14/14) | Best setting in the window | Settings that made money | Also made money before the window* |
|---|---|---|---|---|
| 15-min | 41 trades, −₹5,564 | MACD 19/39/9 · Stoch 5/5/9/21: 31 trades, +₹7,402 | 145 of 864 | 40 |
| 30-min | 19 trades, +₹202 | MACD 24/52/18 · Stoch 5/3/7/7: 11 trades, +₹6,802 | 191 of 864 | 40 |
| 1-hour | 15 trades, −₹5,601 | MACD 24/52/18 · Stoch 2/2/21/14: 10 trades, +₹2,633 | 49 of 864 | 32 |
| 4-hour | 8 trades, +₹6,213 | MACD 5/35/5 · Stoch 5/2/14/9: 10 trades, +₹11,170 | 463 of 864 | 411 |
| **Daily** | 1 trade, +₹1,856 | **MACD 8/17/9 · Stoch 3/5/7/7: 5 trades, +₹20,555** | **698 of 864** | **669** |

\* "Before" = the same rules and settings on ETERNAL from 1 Jan 2023 (15/30-min: 1 Dec 2025) to 9 Jun 2026.

**Best daily setting, every trade (MACD 8/17/9, Stoch RSI K 3 · D 5 · RSI 7 · stochastic 7):**

| Buy | Price ₹ | Sell | Price ₹ | Shares | FYERS ₹ | Net ₹ |
|---|---|---|---|---|---|---|
| 15 Jun 2026 | 252.00 | 23 Jun (open) | 263.00 | 396 | 288.49 | +4,067.51 |
| 30 Jun 2026 | 264.60 | 8 Jul (open) | 288.50 | 377 | 293.23 | +8,717.07 |
| 23 Jul 2026 | 287.10 | 3 Aug (open) | 303.50 | 348 | 290.15 | +5,417.05 |
| 13 Aug 2026 | 318.00 | 14 Aug (open) | 317.80 | 314 | 284.04 | −346.84 |
| 19 Aug 2026 | 320.00 | 26 Aug | 329.58 | 312 | 287.17 | +2,700.44 |
| | | | | | **1,443** | **+20,555** |

Before the window the same setting made +₹58,793 on ETERNAL (28 trades), and +₹502 on 1 trade after it.

## What it shows

- **Daily and 4-hour are robust for ETERNAL:** most settings make money (698 and 463 of 864), and most of those also made money
  before the window. Faster Stoch settings (RSI/stochastic length 7–9, D 5) give more daily trades and catch more of the rise.
- **15-min and 1-hour mostly lose:** only 6–17% of settings make money, and most of those lose before the window. Their "best"
  settings are mostly luck.
- **Nothing beats simply holding ETERNAL here** (+34%, ≈ +₹34k): the best daily setting caught +₹20.6k. Strong one-way rallies
  favour holding; this strategy steps in and out.
- 864 settings on one stock and one window will always produce some great-looking numbers. Before using a setting, test it on
  Nifty 50 (the standard-setup tests found MACD 12/26/9 + Stoch 3/3/14/14 on daily to be the most consistent across all stocks).
