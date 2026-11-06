# Strategy 2 Delivery Buys Inside Uptrends — Nifty 50

Strategy 2 buys taken only while each stock is in an uptrend (200-day-average rule from `nifty50_uptrends_200dma.md`).
Delivery, same-day sells allowed, FYERS charges only, ₹1,00,000 per trade, all 50 stocks, all timeframes, entries from 1 Jan
2023. Education, not investment advice. Report with charges by type and per-stock tables:
`../../projects/trading-equation-backtests/reports/STRATEGY2_UPTRENDS_REPORT.md`. Every trade:
`reports/strategy2_uptrends/trades_all.csv`.

## 1. The rules

**Buy:** MACD histogram bigger than the previous candle **and** Stoch RSI blue crosses above orange with blue below 50
→ buy at that candle's close. **Sell** at the close of the first later candle where blue meets orange. Shares = ₹1,00,000 ÷ price.

**Buys allowed only on these dates** (the sell follows the normal rule):
- **MAIN**: each stock's main uptrend, start to end date. **Uses hindsight**, because you only know which uptrend was the biggest
  after it has ended.
- **LIVE**: any 200-day-average uptrend, from the day after the 5th close above the average until the day before the 5th close
  below it. **Tradable in real time.**

## 2. Result (all 50 stocks added together)

| Timeframe | MAIN trades | MAIN net ₹ | MAIN vs random buys | LIVE trades | LIVE net ₹ | LIVE vs random buys |
|---|---|---|---|---|---|---|
| 15-min* | 763 | −1,38,537 | beats 3% | 7,880 | −11,50,043 | beats 1% |
| 30-min* | 386 | −91,255 | beats 10% | 4,024 | −7,21,559 | beats 46% |
| 1-hour | 6,924 | −7,16,031 | beats 63% | 12,463 | −20,98,291 | beats 44% |
| 4-hour | 1,955 | **+3,54,128** | **beats 96%** (random +₹1.56L) | 3,590 | −2,66,983 | beats 92% (random −₹4.34L) |
| Daily | 1,034 | **+4,98,784** | beats 69% (random +₹4.51L) | 1,853 | **+49,259** | beats 52% (random +₹38k) |

\* 15-min and 30-min data start 1 Dec 2025, after most main uptrends had ended, so few stocks are included.

**4-hour MAIN in detail:** 1,955 buys · 3,00,943 shares · 41.4% winners · 30 of 50 stocks profitable · gross +₹9.02L −
FYERS charges ₹5.48L = **net +₹3.54L** · average move +0.47% vs 0.28% charges · +₹3.0L even without the best 3 trades.
By year: 2023 +₹2.14L · 2024 +₹1.19L · 2025 +₹64k · 2026 −₹44k.

## 3. What it means

- **Restricting buys to uptrends turns 4-hour and daily from losses into profits.** Without the filter (`strategy2_nifty50_delivery.md`)
  4-hour buys lost ₹4.06L and daily ₹1.49L.
- **But the MAIN dates use hindsight.** Inside the main uptrend even random buys make money (+₹1.56L on 4-hour, +₹4.51L on daily).
  - **4-hour:** the strategy beat random buys in 96% of runs, so the entry adds something on top of the uptrend.
  - **Daily:** it's mostly the uptrend (beats only 69%).
- **The version you could actually trade (LIVE) mostly loses.** 4-hour −₹2.67L. Daily +₹49k, about the same as random buys
  (+₹38k), and it lost ₹2.36L in 2026. Real-time uptrends include false starts and late-trend buys that the hindsight "main
  uptrend" leaves out.
- **15-min, 30-min and 1-hour lose either way.** The move per trade (−0.08% to +0.11%) is below the 0.12–0.21% charges.

## 4. Lesson

Strategy 2's 4-hour entry adds real value inside a strong uptrend: it beat random buys in 96% of runs. The problem is knowing
you're in one. A plain 200-day average filter isn't enough. Ideas worth testing next on 4-hour LIVE: a stronger trend filter
(e.g. 200-day average rising **and** price within 10% of its 52-week high), or a market filter (only buy when Nifty itself is
above its 200-day average), which helped in earlier tests (`backtest_results_summary.md`).
