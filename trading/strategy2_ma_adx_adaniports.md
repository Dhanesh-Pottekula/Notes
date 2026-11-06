# Strategy 2 + 50 / 100 / 200 Average + ADX > 40 — ADANIPORTS (one-stock check)

Delivery buys, ADANIPORTS, all timeframes, 1 Jan 2023 – 26 Oct 2026 (15/30-min from 1 Dec 2025), FYERS charges only,
₹1,00,000 per trade. Education, not investment advice. Full report with each timeframe in detail, random-buy comparison
and by year: `../../projects/trading-equation-backtests/reports/STRATEGY2_MA_ADX_ADANIPORTS_REPORT.md`. Every trade:
`reports/strategy2_ma_adx_adaniports/trades_all.csv`.

## 1. The rules

**Strategy 2:** MACD histogram bigger than the previous candle **and** Stoch RSI blue crosses above orange with blue below 50
→ buy at that close. **Sell** at the close of the first later candle where blue meets orange.

**Buy only if the filter is true:**
- **A50 / A100 / A200:** the last 5 **daily** closes above the 50 / 100 / 200-**day** average (intraday timeframes use yesterday's check)
- **B50 / B100 / B200:** the last 5 candles **of the traded timeframe** above its 50 / 100 / 200-**candle** average
- **+ADX:** also ADX(14) on the traded timeframe **above 40** (TradingView "ADX and DI")
- Baselines: **NONE** (no filter) and **ADX** (ADX > 40 only)

## 2. Net profit ₹ (ADANIPORTS)

| Version | 15-min | 30-min | 1-hour | 4-hour | Daily | **Total** | Trades |
|---|---|---|---|---|---|---|---|
| NONE | −31,860 | 615 | 1,417 | 3,076 | −1,326 | **−28,078** | 983 |
| **ADX > 40 only** | 5,176 | 5,163 | 20,000 | 13,391 | −3,833 | **+39,897** | 87 |
| A50 | −20,413 | 11,711 | −7,176 | −2,809 | 6,680 | **−12,007** | 544 |
| A100 | −25,822 | −514 | −32,183 | 1,519 | 3,460 | **−53,540** | 599 |
| A200 | −29,438 | −5,249 | −22,532 | 7,670 | 1,041 | **−48,508** | 742 |
| B50 | −16,946 | 3,999 | −1,410 | −12,202 | 6,680 | **−19,879** | 320 |
| B100 | −15,147 | 6,496 | −14,201 | −14,184 | 3,460 | **−33,576** | 420 |
| B200 | −14,313 | 16,202 | −5,297 | −506 | 1,041 | **−2,873** | 478 |
| A50 + ADX | 2,778 | 2,714 | −4,487 | 235 | 1,157 | **+2,397** | 47 |
| A100 + ADX | −268 | −728 | −1,695 | 235 | 1,157 | **−1,299** | 48 |
| A200 + ADX | 3,123 | 3,753 | −183 | 235 | 1,157 | **+8,085** | 67 |
| B50 + ADX | −2,430 | 2,220 | −2,310 | 235 | 1,157 | **−1,128** | 37 |
| B100 + ADX | −2,437 | 2,220 | −2,915 | 235 | 1,157 | **−1,740** | 37 |
| B200 + ADX | −1,957 | 2,220 | −3,077 | 235 | 1,157 | **−1,422** | 36 |

## 3. What it shows

- **50 vs 100 vs 200 average: no clear winner.** Every average-only version loses in total. The best one changes from timeframe to
  timeframe (e.g. 30-min: B200 +₹16k; daily: A50/B50 +₹6.7k; 1-hour: all lose), so the difference between lengths looks like noise.
- **ADX > 40 on its own is the best version: +₹39,897**, positive on 15-min, 30-min, 1-hour and 4-hour, and beats random buys
  with the same filter in 88–92% of runs on those timeframes. **But it's only 87 trades on one stock.** ADX > 40 is rare (about
  1 in 10 Strategy 2 signals), so a few lucky trades can decide it.
- **Average + ADX together leaves almost no trades** (36–67 over all timeframes; 4 on 4-hour, 3 on daily), so those results
  mean very little. ADX > 40 already implies a strong trend, so the average filter mostly just removes trades.
- **ADX doesn't tell direction.** ADX > 40 can also be a strong *down*trend. Adding "+DI above −DI" would keep only strong
  uptrends.

## 4. Next step

One stock gives too few ADX trades to trust. Run the same 14 versions on all Nifty 50 stocks
(`python experiments/strategy2_ma_adx.py n50`) before drawing conclusions.
