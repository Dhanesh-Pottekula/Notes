# Strategy 5 — Standard Setup (daily, Nifty 50)

The setting that held up best across all Strategy 5 tests (Oct 2026). Education, not investment advice. Evidence:
`strategy5_roc_ema_sweep.md` and `../../projects/trading-equation-backtests/reports/STRATEGY5_*_REPORT.md`.

## Indicators (daily chart)

| Indicator | Settings | Look for |
|---|---|---|
| **Rate of Change (ROC)** | Length **20**, source close | above **7** (add a line at 7) |
| **EMA** | Length **50**, source close | the day's close above it |
| **MACD** | Fast **12**, slow **26**, signal **9**, source close | histogram bar bigger than the day before |
| **Stochastic RSI** | K **3**, D **3**, RSI length **14**, stochastic length **14**, source close | blue crosses above orange, blue below **50** (add a line at 50) |

## Buy (at the day's close, all four true that day)

1. ROC(20) > 7 → the stock is up more than 7% over the last 20 trading days
2. Close above the 50-day EMA
3. MACD histogram bigger than yesterday's (green growing or red shrinking)
4. Stoch RSI blue crosses above orange today (yesterday blue ≤ orange) with blue below 50

Delivery (CNC), ₹1,00,000 per trade (shares = ₹1,00,000 ÷ price), one trade at a time per stock.

## Sell (the first of these)

- **Blue touches orange** on a later day: sell then (during the day as soon as it touches; at the open if it opens there)
- **Optional stop-loss:** the **low of the day you bought** (about 2% below the buy price). Same total profit in the test, but it
  cut event-day crashes (e.g. 4 Jun 2024: NTPC −₹15.7k → −₹5.0k).

No target. A trade usually lasts about a week; trades that last 7+ days make almost all the profit.

## Money

- ₹1 lakh per stock; several stocks can be open at once (up to 13 in the test, usually 1–3).
- About **₹5 lakh** gave the best return (≈ 6% a year in the test). With ₹1–2 lakh it lost money.
- FYERS charges ≈ ₹283 per trade (mostly STT).

## Test results (all 50 Nifty 50 stocks, 1 Jan 2023 – 26 Oct 2026, FYERS charges)

| Version | Trades | Win % | Net ₹ | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|
| No stop | 299 | 41.8 | +1,53,217 | +47k | +53k | +57k | −4k |
| With stop at buy-day low | 299 | 39.1 | +1,54,307 | +42k | +64k | +58k | −10k |

Beats random buys with the same ROC/EMA filter in 97% of runs. Daily only: on 4-hour and 1-hour the same setting breaks even or
loses. Settings were chosen after seeing 2025–26, so paper-trade first or test on Nifty 200.
