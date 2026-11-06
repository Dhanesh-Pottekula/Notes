# Strategy 5 — ROC + EMA + MACD + Stoch RSI, Settings Sweep on Nifty 50 (30 Oct 2026)

All 50 Nifty 50 stocks, 15-min / 30-min / 1-hour / 4-hour / daily, delivery buys (same-day sells allowed), FYERS charges only,
₹1,00,000 per trade, 1 Jan 2023 – 26 Oct 2026 (15/30-min from 1 Dec 2025). Education, not investment advice.
Full report: `../../projects/trading-equation-backtests/reports/STRATEGY5_REPORT.md` (every setting tried, train/test, finalists,
FYERS charges by type). Every finalist trade: `reports/strategy5/final_trades.csv`.

## 1. The rules

**Buy** when all four are true (all on the traded timeframe):
1. **Rate of Change** of the close over 100 candles **above 2%**
2. **Close above the 100 EMA** (that candle only, no 5-candle rule)
3. **MACD histogram bigger than the previous bar**
4. **Stoch RSI blue crosses above orange**, with **blue below 50**

**Two ways to buy:**
- **At the candle close** (all four true on the closed candle)
- **During the candle**: the moment all four become true. The order of moves inside a candle can't be known from candle data,
  so it's reported as a range: *cautious* (if the low reached the sell level, assume it sold in the buy candle) to
  *favourable* (sell in the buy candle only when certain).

**Sell** as soon as blue **touches** orange during any later candle, at that exact price (the open if it gaps there).

**Settings tried** (one indicator at a time, then the best 2 of each combined, 64 set-ups per timeframe):
Stoch K/D 2/3/5 · RSI/stochastic length 7/9/14/21 · blue level 30/50/70 · MACD 12/26/9, 8/21/5, 5/35/5, 19/39/9, 8/17/9,
24/52/18 · EMA 20/50/100/150/200 · ROC length 20/50/100/200 × level 0/1/2/3/5.
**Honesty check:** settings were picked on **2023–24 (train)** and then tested on **2025–26 (test)**, which they never saw.
(15/30-min: train Dec 2025 – May 2026, test Jun – Oct 2026.)

## 2. Your exact settings (net ₹, all 50 stocks)

| Timeframe | Buy at close | Buy during candle (cautious → favourable) |
|---|---|---|
| 15-min | −4,27,319 | −7,79,943 → −4,43,606 |
| 30-min | −1,92,898 | −4,43,933 → −77,686 |
| 1-hour | −11,89,222 | −22,32,542 → −9,57,268 |
| 4-hour | −52,411 | −8,10,190 → +2,01,371 |
| Daily | −26,171 | −5,91,068 → +4,23,852 |

## 3. What the sweep found

- **15-min, 30-min and 1-hour lose with almost every setting** (buy at close: 1 of 162 settings positive). The trades are too
  short to pay the charges.
- **Buying during the candle** only looks good under the favourable assumption. Under the cautious one, **all 270 settings
  lose**. The truth is in between, so it isn't reliable.
- **Settings chosen on 2023–24 failed on 2025–26 almost every time.** Buy at close, the best combined set-ups made
  4-hour +₹3.01L (train) → **−₹2.19L (test)**; daily +₹4.07L → **−₹82k**. 0 of 64 4-hour and 0 of 64 daily combined set-ups
  were positive in the test years. Picking the best settings from the past doesn't carry into the future here.
- **What helped a little, consistently:** slower Stoch lines (**K/D 5/5**), blue **below 30** instead of 50, and slower MACD
  (**24/52/18**). They cut losing trades on every timeframe but didn't make the fast timeframes profitable.
- **Positive in both periods:** daily, buy at close, **ROC 20 > 2 / 3 / 5** (other settings yours): +₹1.07L / +₹1.23L /
  **+₹1.51L** (ROC 20 > 5: train +₹1.18L, test +₹34k), plus 4-hour ROC 20 > 5 (+₹11k). All four use ROC 20. The follow-up
  sweep `strategy5_roc_ema_sweep.md` tests ROC length × level × EMA in detail.

## 4. Lesson

(Numbers updated 30 Oct 2026 after fixing a floating-point edge case where blue exactly equal to orange wasn't counted as a
touch; 0.6% of trades changed.)

Changing indicator lengths doesn't fix this strategy: the same pattern as all earlier tests appears (works in the 2023–24
rally, fails in 2025–26, and short timeframes lose to charges). The exit (sell at the first blue/orange touch) keeps trades too
short. Next things worth testing: a slower exit, and the daily ROC 20 > 5 version on Nifty 200.
