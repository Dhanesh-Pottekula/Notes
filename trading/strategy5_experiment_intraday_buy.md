# EXPERIMENT — Strategy 5 Daily, Buy During the Day When Blue Crosses Orange (30 Oct 2026)

An experiment on top of the standard setup (`strategy5_standard_setup.md`, unchanged). Education, not investment advice.
Script: `../../projects/trading-equation-backtests/experiments/strategy5_daily_live_buy.py`; every trade:
`reports/strategy5/daily_live_buy_trades.csv`.

## Rules

Same daily chart and settings as the standard (ROC 20 > 7 · EMA 50 · MACD 12/26/9 · Stoch RSI 3/3/14/14 < 50). The only change:
**buy during the day, the moment blue crosses above orange**, if at that same moment ROC > 7, price > EMA 50, the MACD histogram
is bigger than yesterday's and blue is below 50 (all worked out with the live price as today's close). Yesterday blue must have
been at or below orange (a new cross). **Sell** as soon as blue touches orange: the same day if the price falls back, or on a later
day. No stop-loss. Delivery, ₹1L per trade, FYERS charges (same-day round trips at intraday rates), all Nifty 50, 2023 – Oct 2026.

**How the day was followed:** the official open, then the 1-hour candles in order. The only thing unknown is the order of moves
*inside the hour of the buy*, so the same-day sell is reported as a range: **cautious** (if that hour's low reached the sell level,
assume it sold) to **favourable** (sell in that hour only when certain).

## Result vs the standard (buy at the close)

| Version | Trades | Same-day sells | Win % | FYERS charges ₹ | **Net ₹** | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|
| **Standard: buy at close** | 299 | 0 | 41.8 | 84,700 | **+1,53,217** | +47k | +53k | +57k | −4k |
| Buy during the day — cautious | 626 | 348 | 21.6 | 1,07,483 | **+21,487** | +1.04L | −51k | +30k | −62k |
| Buy during the day — favourable | 625 | 261 | 29.6 | 1,24,782 | **+2,44,013** | +1.57L | +57k | +61k | −31k |

The real result is somewhere between +₹21k and +₹2.44L. That's too wide to call better or worse than the standard (+₹1.53L).

## What happens

- **Twice as many trades:** a cross that happens during the day often **doesn't hold until the close**. Those failed crosses
  are bought and sold the same day: **−₹1.6L to −₹2.4L** on same-day trades.
- **Trades that survive overnight do well:** +₹2.6L to +₹4.1L.
- **Most buys happen in the first hour** (424 of 626 between 9:15 and 10:15), often right at the open after a gap up. That's
  also where the uncertainty is.
- **Buy price is about the same as the close** (median 0.05% below that day's close), so buying early doesn't get a better price
  on average; it just adds the failed crosses.
- **2026 is worse** than the standard (−₹31k to −₹62k vs −₹4k).

## Verdict

Not better than the standard on the evidence: the cautious figure is far below, the favourable one above, and it takes twice the
trades and more charges. Waiting for the daily close filters out the crosses that fail during the day. To settle it, the buy hour
needs finer data (15-minute data only exists from Dec 2025, too short); or paper-trade both side by side.

---

# EXPERIMENT 2 — Check in the Late Afternoon and Buy Then (30 Oct 2026)

Script: `../../projects/trading-equation-backtests/experiments/strategy5_afternoon_buy.py`; every trade:
`reports/strategy5/afternoon_buy_trades.csv`.

**Rules:** same daily chart and settings as the standard. At a fixed afternoon time, take the price at that moment as "today's
close" for the daily indicators. If blue has crossed above orange (yesterday blue ≤ orange), blue is below 50, ROC 20 > 7, price
above EMA 50 and the MACD histogram is bigger than yesterday's, **buy right then at that price**. **Sell** the moment blue touches
orange (later that afternoon or any later day). Everything after the buy happens in time order, so each check time has **one exact
result** (no cautious/favourable range).

| Check time | Trades | Sold same day | Win % | Stocks profitable | FYERS charges ₹ | **Net ₹** | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1:15 pm | 280 | 33 | 42.9 | 32/50 | 72,728 | +1,17,237 | +48k | +25k | +51k | −7k |
| **2:15 pm** | 290 | 34 | 40.0 | 30/50 | 75,388 | **+1,64,046** | +45k | +36k | +65k | **+18k** |
| 3:15 pm | 300 | 13 | 40.3 | 32/50 | 82,381 | +1,46,643 | +43k | +46k | +61k | −4k |
| 3:30 close (standard) | 299 | 0 | 41.8 | 29/50 | 84,700 | +1,53,217 | +47k | +53k | +57k | −4k |

- **2:15 pm is the best of the four** and the only one positive in every year, including 2026. In 2025–26 it made +₹82k
  vs +₹53k for the close.
- **3:15 pm ≈ the close** (288 of its 300 buys are the same as at the close, price only 0.01% different).
- **1:15 pm is worse:** more of its crosses fail by the end of the day.
- Same-day sells are few in all versions (13–34), unlike the morning buys in Experiment 1 (261–348).
- **Caveat:** the gap between 2:15 pm and the close is about ₹11k on ₹1.5L, and 4 times were tried, so part of it can be
  chance. The steady 2026 result is the more encouraging part. Paper-trade it next to the standard before switching.

## Experiment 2b — buy any time after 2:15 pm (30 Oct 2026)

**Rule:** at 2:15 pm check the daily chart; if everything already holds, buy at the 2:15 price. If not, keep watching until the
close and **buy the moment blue crosses above orange** (with ROC 20 > 7, price > EMA 50, MACD histogram rising, blue < 50 at that
moment). Sell the moment blue touches orange. The only unknown is the order of moves inside the hour of a later-afternoon buy, so
it's a narrow cautious–favourable range.

| Buy | Trades | Sold same day | Win % | Stocks profitable | FYERS charges ₹ | **Net ₹** | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|
| At the daily close (standard) | 299 | 0 | 41.8 | 29/50 | 84,700 | +1,53,217 | +47k | +53k | +57k | −4k |
| Check at 2:15 pm only | 290 | 34 | 40.0 | 30/50 | 75,388 | +1,64,046 | +45k | +36k | +65k | +18k |
| **Any time after 2:15 pm (cautious)** | 408 | 81 | 35.3 | 30/50 | 99,389 | **+1,94,175** | +88k | +31k | +66k | +10k |
| **Any time after 2:15 pm (favourable)** | 407 | 62 | 36.6 | 31/50 | 1,02,934 | **+2,16,538** | +84k | +63k | +65k | +5k |

Where the extra profit comes from (cautious → favourable):
- 290 trades already true at 2:15 pm: **+₹1,64,046** (identical to the 2:15 check)
- 100 crosses between 2:15 and 3:15 pm: **+₹33,514 → +₹57,599**
- 17–18 crosses in the last 15 minutes (3:15–3:30): **−₹3,385 → −₹5,107**

**Difference vs buying at the close: +₹41k to +₹63k more** (and every year positive, including 2026). Most of the gain is from crosses
that happen during the 2:15–3:15 pm hour; crosses after 3:15 pm add nothing. The test period (2025–26) is also better: +₹70k to
+₹76k vs +₹53k at the close. Still to do: paper-trade, or test on Nifty 200.
