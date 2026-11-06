# BEL — MACD + Stochastic RSI Delivery Buys, 4 Strategies (23 Oct 2023 – 9 Jun 2026)

Delivery buys only (same-day sells allowed), FYERS charges only (no slippage), ₹1,00,000 per trade, all timeframes.
Education, not investment advice. Every trade (buy/sell time and price, qty, each FYERS charge, MACD/signal/histogram, %K/%D):
`../../projects/trading-equation-backtests/reports/BEL_DELIVERY_BUYS_REPORT.md` and `reports/bel_delivery/trades_all.csv`.
Same idea tested earlier on ADANIPORTS / Nifty 50: `adaniports_macd_stoch_backtest.md`.

## 1. The rules

**Common to all four.** On the same candle:
- the Stoch RSI blue line (%K) **crosses above** the orange line (%D): previous candle blue ≤ orange, this candle blue > orange
- the MACD histogram is **bigger than on the previous candle** (green or red bar)

→ **buy at that candle's close.** **Sell at the close of the first later candle where blue meets orange** (blue ≤ orange).
No stop-loss. Settings MACD 12/26/9, Stoch RSI 3/3/14/14.

| Strategy | MACD line and signal line | Blue at the cross |
|---|---|---|
| **1** | both **> 0** | **below 50** |
| **2** | anywhere | **below 50** |
| **3** | both **> 0** | **below 70** |
| **4** | anywhere | **below 70** |

FYERS charges: held overnight ≈ ₹284 (0.28%) per ₹1L round trip; sold the same day ≈ ₹83 (0.08%, intraday rates).
15-min and 30-min data only start on 1 Dec 2025, so those two cover Dec 2025 – 9 Jun 2026.

## 2. Result (net P&L after FYERS charges)

| Timeframe | Strategy 1 | Strategy 2 | Strategy 3 | Strategy 4 |
|---|---|---|---|---|
| 15-min | 71 trades, −₹3,509 | 200, −₹25,026 | 82, −₹5,957 | 235, −₹27,608 |
| 30-min | 21, −₹749 | 86, −₹9,044 | 34, −₹2,766 | 111, −₹9,797 |
| 1-hour | 113, −₹13,791 | 249, −₹32,000 | 142, −₹5,257 | 305, −₹18,326 |
| 4-hour | 29, **+₹18,433** | 66, **+₹51,328** | 34, **+₹21,428** | 82, **+₹44,673** |
| Daily | 24, **+₹27,084** | 44, **+₹50,235** | 24, **+₹27,084** | 48, **+₹55,399** |

BEL buy-and-hold over the same window: about **+210%** (1-hour/4-hour/daily) and −0.8% (15/30-min, Dec 2025 – Jun 2026).

**Is it real?** Random buys held for the same number of candles also make money, because BEL tripled. So each result is compared with 500 random-buy runs:

| | 4-hour 1 | 4-hour 2 | 4-hour 3 | 4-hour 4 | Daily 1 | Daily 2 | Daily 3 | Daily 4 |
|---|---|---|---|---|---|---|---|---|
| Beats % of random runs | 77% | **89%** | 81% | 82% | 78% | 77% | 75% | 82% |
| Net without the best 3 trades | −₹13.1k | **+₹19.8k** | −₹10.1k | +₹13.1k | −₹19.6k | +₹62 | −₹19.6k | +₹5.2k |

- **15-min, 30-min and 1-hour lose with every strategy.** Most of those trades are sold the same day, and the move is ≈ 0.0–0.14%,
  while charges are 0.12–0.20%.
- **4-hour and daily make money with every strategy.** But that's mostly BEL rising: only **Strategy 2 on 4-hour** stays clearly
  positive without its best 3 trades (+₹19.8k), makes money in 2023, 2024 and 2025 (−₹5.6k in 2026), and beats 89% of random runs.
  Daily profits come almost entirely from a few 2024 trades.
- **70 instead of 50** adds about 10–25% more trades. It helped on 1-hour (losses got smaller) but made 4-hour slightly worse.
  On daily, Strategy 3 gave exactly the same 24 trades as Strategy 1.
- **The MACD > 0 filter (1, 3) cuts trades by more than half, and the profit with them.** In Strategy 1, 223 of 258 buys came on a
  red but shrinking histogram: a Stoch cross after a pullback usually comes while MACD is still below its signal line.

## 3. Lesson

On BEL, only the slower timeframes make the trades long enough (about 3–4 candles = 1–2 days on 4-hour) to cover the 0.28%
delivery charges. Strategy 2 on 4-hour (histogram bigger than previous + blue crosses orange below 50) is the best lead. It's still
one stock in a strongly rising market, and 89% is below the usual 95% bar. Next: test Strategy 2 / 4 on 4-hour across all Nifty 50
stocks, and add a stop-loss. The 4 Jun 2024 election-day crash (−18.7% in one trade) shows what can happen without one.
