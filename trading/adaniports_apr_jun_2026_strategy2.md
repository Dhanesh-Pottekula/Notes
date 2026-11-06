# ADANIPORTS, 1 Apr – 30 Jun 2026 — Strategy 2 + B200 + ADX30

One stock, one quarter, all timeframes, delivery buys, intra-candle sell, FYERS charges only, ₹1,00,000 per trade.
Education, not investment advice. Every trade with ADX, +DI/−DI, 200 average and its slope:
`../../projects/trading-equation-backtests/reports/STRATEGY2_WINDOW_ADANIPORTS_20260401_20260630_REPORT.md`
(script `experiments/strategy2_window.py ADANIPORTS 2026-04-01 2026-06-30`, reusable for any stock and dates).

## Rules

**Buy** at a candle's close when: last 5 candles closed above the 200-candle average · ADX(14) > 30 · MACD histogram bigger
than the previous candle · Stoch RSI blue crosses above orange with blue below 50. Extra versions: **+DI** (+DI above −DI),
**+SLOPE** (200 average higher than 10 candles ago). **Sell** the moment blue crosses below orange inside a candle.

ADANIPORTS in this window: ₹1,385.40 → ₹1,810.20 (**+30.7%**), a strong uptrend (its 200-day uptrend started 8 Apr 2026).

## Result (net ₹ after FYERS charges)

| Timeframe | B200 + ADX30 | + DI | + SLOPE | + DI + SLOPE |
|---|---|---|---|---|
| 15-min | 13 trades, +1,633 | 9, +468 | 13, +1,633 | 9, +468 |
| 30-min | 7, +3,023 | 3, +549 | 7, +3,023 | 3, +549 |
| 1-hour | 3, +1,770 | 2, +872 | 3, +1,770 | 2, +872 |
| 4-hour | 1, +1,973 | 1, +1,973 | 1, +1,973 | 1, +1,973 |
| Daily | 0 | 0 | 0 | 0 |
| **Total** | **24 trades, +8,399** | 15, +3,862 | 24, +8,399 | 15, +3,862 |

- **Every timeframe made a small profit, but much less than holding the stock.** Buy-and-hold of ₹1L on 1 Apr made about
  **+₹30,000** after charges. The best single timeframe made ₹3,023; all five together made ₹8,399.
- **Why:** the Stoch exit sells after a few candles (15 minutes to 3 days), so it catches small pieces of a big move.
  The best trade (30-min, bought ₹1,630.30 on 30 Apr, sold ₹1,708.40 on 4 May, **+₹4,476**) was the one that happened to be held
  over a gap up.
- **+SLOPE changed nothing:** the 200 average was rising the whole time, so every trade already passed it.
- **+DI removed 9 trades and ₹4.5k of profit.** Several good buys came on pullbacks (−DI above +DI), the same pattern as the
  4-hour Nifty 50 result in `strategy2_ma_adx_nifty50.md`.
- **Daily: no trades.** On daily ADX was above 30 on only 1 of 60 days in the window.
- 24 trades on one stock over three months is far too few to judge the strategy. The Nifty 50 tests are the real evidence.
