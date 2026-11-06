# VWAP and Volume Profile — How They Work and What My Backtests Showed

Notes from two YouTube videos, plus the result of testing both on NSE stocks (Oct 2026). Education, not investment advice.
- Video 1: MindMath Money, "MASTER VWAP Trading in 75 Minutes (Full Indicator & Strategy Course)" — https://www.youtube.com/watch?v=52UMotdu4Mk
- Video 2: Currency Pros, "The Truth About Volume Profile (And Why You're Doing It Wrong)" — https://www.youtube.com/watch?v=ITXbm_sTTEs
- Full report: `../../projects/trading-equation-backtests/reports/VWAP_REPORT.md`

## 1. VWAP in plain words

- **VWAP (volume-weighted average price)** = the average price of the day, where prices with more volume count more.
  It is roughly "the average price everyone paid today".
  `VWAP = Σ(price × volume) ÷ Σ volume`, added up from the start of the session (or another anchor).
- Price can be the typical price (H+L+C)/3 (TradingView default), the close, or (O+H+L+C)/4.
- **Above VWAP:** buyers are paying more than the day's average → buyers in control (long bias).
  **Below VWAP:** sellers in control (short bias). A cross of VWAP = control may be changing.
- **Why it matters:** big funds judge their fills against VWAP (buying below it = a good fill), so the line attracts orders and
  often acts as **moving support/resistance**.
- **The VWAP moves faster** when price is far from it and volume is high; quiet low-volume bars barely move it.
- It **resets every session**, which is why the line jumps at each day's open.

## 2. Bands, anchors, settings

- **Bands** = standard deviations around VWAP: `band k = VWAP ± k × σ`, σ = volume-weighted std of price from the anchor.
  Roughly 68% / 95% / 99% of trading sits inside band 1 / 2 / 3 (only if prices were normally distributed — they aren't).
  Band 1 = normal pullbacks; bands 2–3 = stretched / extreme prices.
- **Anchor** = where the VWAP starts adding up. Session (day trading), week (1-hour charts), month (4-hour / daily),
  quarter, earnings date, or any candle you pick (**anchored VWAP** from a major high/low or news candle).
- **Rolling VWAP** = never resets; uses a fixed look-back window instead.

## 3. The VWAP course's trading rules

1. **Biggest mistake:** buying just because price touched VWAP. VWAP is **context, not a trigger**. A flat VWAP (sideways
   market) gives the most false signals.
2. **Method A — mean reversion:** VWAP flat, price stretches to band 1–2, a reversal candle forms → trade back to VWAP.
3. **Method B — trend continuation:** VWAP clearly sloping, price pulls back to VWAP (or band 1), a hammer/engulfing forms →
   trade with the trend.
4. **Final strategy (reversal):** all three must line up — touch of **band 2** + an old **horizontal support/resistance** level
   (best with a *failure test*: a quick break of the level that closes back) + a **candle pattern** (shooting star, hammer,
   engulfing, morning/evening star). Enter at the candle close, stop just past the pattern's extreme, target **2R**.

## 4. Volume profile and the POC (video 2)

- **Volume profile** = a sideways histogram of how much volume traded **at each price** over a range (not per time bar).
- **POC (point of control)** = the price with the most volume. **High-volume areas** act like resistance (price struggles
  through them); **low-volume areas** let price move fast.
- Currency Pros use it as a **bonus check** on their own checklist (4 × 25 points): higher-timeframe alignment (sell when the
  daily chart is in the top half of its range, buy in the bottom half), **break of structure**, **liquidity sweep** (a false
  break of an old high/low), **imbalance** (fair-value gap). They enter with **limit orders at the 67% (≈1:2) or 75% (≈1:3)
  Fibonacci retracement** of the range, stop beyond the range, target the other end.
- **POC rule:** POC at your entry level = stronger setup. **POC at the far end of the range, next to your stop = skip it** —
  price tends to get pulled there and hit the stop.
- On stocks the volume is real exchange volume; in forex/CFDs it is only your broker's volume.

## 5. What my backtests showed (Nifty 50 + Nifty 200, FYERS costs)

| Approach | Result |
|---|---|
| VWAP course, every setup, 1-min → daily | **Not worth trading.** Raw band touches: median win rate 27%. Each added check (candle, level) helped, but the median Sharpe stayed negative; intraday win rates 28–47% vs 41–60% needed after charges |
| VWAP swing (weekly / monthly anchor), delivery | Lost in most settings; best 6–9% a year, below just holding the stocks (14–19%) |
| Currency Pros + POC, 5-min / 1-hour / 4-hour | Lost on both stock lists |
| Currency Pros + POC, **15-min intraday, full checklist** | **Lead:** Nifty 200 all 7 settings profitable, best +₹1.35L on ₹10L in 11 months, 51% wins vs 40% needed — but mostly in Jun–Oct 2026; only 2 of 7 settings positive in both halves. Nifty 50: roughly flat (−₹22k to +₹15k) |
| Currency Pros + POC, daily delivery | Nifty 200: 4–11% a year in 2022–26, beat random entries — but below holding the stocks (18.9%). Nifty 50: 1–4% a year |
| The POC filter itself | Little help. "Skip if POC near stop": no change on average. "POC at entry": helped intraday (17 of 24 pairs), not delivery |
| The full checklist (sweep + higher-TF) | Helped clearly: better in 26 of 36 pairs, intraday and delivery |

## 6. Takeaways

- The course's warning is correct: **VWAP alone is not an edge**. Extra confirmation helps, but not enough to pay intraday costs.
- In the Currency Pros setup, **the checklist did the work, not the volume profile**.
- Only lead worth paper trading: **15-min, full checklist, 75% limit entry, intraday**, on liquid stocks — compare live results with
  the backtest for 3+ months before risking money.
- Videos show the clearest examples, picked by eye. Fixed rules on 50–200 stocks are a much harder test.
