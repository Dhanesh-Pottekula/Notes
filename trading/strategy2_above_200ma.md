# Strategy 2 Buys Only When Price Is Above the 200 Average for 5 Candles — Nifty 50

Delivery buys, all 50 stocks, all timeframes, entries 1 Jan 2023 – 26 Oct 2026, FYERS charges only, ₹1,00,000 per trade.
Education, not investment advice. Report with charges by type, by year and per stock:
`../../projects/trading-equation-backtests/reports/STRATEGY2_ABOVE_MA_REPORT.md`. Every trade:
`reports/strategy2_above_ma/trades_all.csv`.

## 1. The rules

**Filter first:** price has been above its 200 average for the last 5 candles. Tested two ways:
- **A (daily average):** the last 5 **daily** closes are all above the **200-day** average. Intraday timeframes use yesterday's check.
- **B (same timeframe):** the last 5 candles **of the timeframe you trade** are all above that timeframe's **200-candle** average
  (e.g. on 4-hour: the last 5 four-hour closes above the 200 four-hour-candle average).

**Then Strategy 2:** MACD histogram bigger than the previous candle **and** Stoch RSI blue crosses above orange with blue
below 50 → buy at that close. **Sell** at the close of the first later candle where blue meets orange.

## 2. Result (all 50 stocks added together)

| Timeframe | A trades | A net ₹ | B trades | B net ₹ | Random buys with the same filter (A / B) |
|---|---|---|---|---|---|
| 15-min* | 7,023 | −10,15,943 | 6,000 | −8,56,907 | −9.18L / −7.13L |
| 30-min* | 3,603 | −6,68,324 | 2,978 | −5,54,188 | −6.30L / −4.72L |
| 1-hour | 11,717 | −19,71,866 | 8,703 | −16,30,229 | −19.42L / −13.83L |
| 4-hour | 3,237 | −1,76,669 | 2,615 | −68,663 | −3.74L / −2.63L |
| Daily | 1,650 | **+72,992** | 1,650 | **+72,992** | +57k / +57k |

\* 15-min and 30-min data start 1 Dec 2025. On daily, A and B are the same rule.

**Daily in detail:** 1,650 buys · 2,25,539 shares · 38.3% winners · 23 of 50 stocks profitable · gross +₹5.39L − FYERS charges
₹4.66L (STT is most of it) = **net +₹73k**. Without the best 3 trades: −₹6k. By year: 2023 +₹1.59L · 2024 +₹1.20L ·
2025 −₹12k · 2026 −₹1.95L.

## 3. What it means

- **The filter helps a little but doesn't make the strategy work.** 4-hour improves from −₹4.06L (no filter) to −₹1.77L (A) /
  −₹69k (B). Daily goes from −₹1.49L to +₹73k.
- **The daily profit is from the filter, not the entry.** Random buys with the same filter make +₹57k, and Strategy 2 beats
  them only 56% of the time. Without its 3 best trades it's slightly negative.
- **On 4-hour the entry does beat random buys (91–93%),** like in the uptrend test, but it still loses after FYERS
  charges: the move per trade (+0.23–0.26%) is just under the 0.28% delivery charge.
- **It only worked in 2023–2024**, when most stocks were rising. In 2025–2026 every timeframe lost money.
- **15-min to 1-hour lose with both filters.** The trades are too short to cover the charges.

## 4. Compared with the earlier tests

| Strategy 2 delivery buys, Nifty 50 | 4-hour net | Daily net |
|---|---|---|
| No filter (23 Oct 2023 –) | −₹4.06L | −₹1.49L |
| Above 200 average, last 5 candles: A / B | −₹1.77L / −₹69k | +₹73k |
| Inside any confirmed 200-day uptrend (LIVE) | −₹2.67L | +₹49k |
| Inside each stock's main uptrend (hindsight) | +₹3.54L | +₹4.99L |

The trend filters you can use in real time all land close to break-even. Only the hindsight version is clearly profitable.
