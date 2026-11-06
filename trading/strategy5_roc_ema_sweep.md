# Strategy 5 — ROC Length × Level and EMA Length × Rule (Nifty 50, 30 Oct 2026)

Follow-up to `strategy5_roc_ema_macd_stoch_sweep.md`. All 50 Nifty 50 stocks, 5 timeframes, delivery buys at the candle close,
FYERS charges only, ₹1,00,000 per trade, 1 Jan 2023 – 26 Oct 2026 (15/30-min from 1 Dec 2025). Education, not investment advice.
Full report (ROC tables per timeframe, EMA tables, every setting positive in both periods, finalists with charges by type):
`../../projects/trading-equation-backtests/reports/STRATEGY5_ROC_EMA_REPORT.md`. Every finalist trade:
`reports/strategy5/roc_ema_final_trades.csv`.

## 1. Rules

**Buy at the candle close** when: **ROC(length) > level %** · **close above the EMA** (buy candle only, or **all of the last 5
candles**) · **MACD 12/26/9 histogram bigger than the previous bar** · **Stoch RSI 3/3/14/14 blue crosses above orange, blue
below 50**. **Sell** as soon as blue touches orange during a later candle.

**Tried:** ROC length 10, 20, 30, 50, 100, 150, 200 × level 0, 1, 2, 3, 5, 7, 10, 15% × EMA 20, 50, 100, 150, 200 × EMA rule
(1 or 5 candles) = **560 settings × 5 timeframes**. Train 2023–24, test 2025–26 (15/30-min: Dec 2025–May 2026 / Jun–Oct 2026).

## 2. How many settings made money

| Timeframe | Positive overall | Positive in **both** 2023–24 and 2025–26 |
|---|---|---|
| 15-min | 8 of 406 | 0 |
| 30-min | 45 of 449 | 8 |
| 1-hour | 13 of 499 | 0 |
| 4-hour | 133 of 510 | 12 |
| **Daily** | **421 of 540** | **163** |

## 3. Daily: ROC length is what matters

**Test-period (2025–26) net ₹, EMA 100, buy candle only:**

| ROC length | > 2% | > 3% | > 5% | > 7% | > 10% |
|---|---|---|---|---|---|
| 10 | +45k | +74k | +42k | +20k | +9k |
| **20** | +5k | +16k | **+34k** | **+49k** | +27k |
| 50 | −36k | −6k | −8k | +18k | +42k |
| **100 (yours)** | **−82k** | −67k | −82k | −63k | −25k |
| 200 | −74k | −70k | −80k | −129k | −148k |

- **Short look-backs (10–20 days) keep working in 2025–26; long ones (100–200 days, including your 100) lose.** In 2023–24
  almost everything made money (a strong rally), so the test years are what separate good from bad settings.
- **ROC 20 at 3–7% works with every EMA length:** total +₹1.01L to +₹1.78L, and +₹12k to +₹53k in 2025–26 alone. That's
  a whole block of neighbouring settings, not one lucky number.
- **EMA length and the 5-candle rule matter much less** than the ROC look-back (shorter EMAs 20/50 slightly better).

## 4. Best daily versions (all 50 stocks)

| Settings | Trades | Win % | Stocks profitable | FYERS charges ₹ | **Net ₹** | 2023 | 2024 | 2025 | 2026 | Beats random |
|---|---|---|---|---|---|---|---|---|---|---|
| **ROC 20 > 7, EMA 50** | 299 | 41.8 | 29/50 | 84,700 | **+1,53,217** | +47k | +53k | +57k | −4k | 97% |
| ROC 20 > 7, EMA 200 | 285 | 42.5 | 29/50 | 80,729 | +1,38,742 | +47k | +42k | +44k | +6k | 97% |
| ROC 50 > 15, EMA 50 | 356 | 36.5 | 20/50 | 1,00,791 | +1,22,088 | +49k | +17k | +54k | +2k | 70% |
| Your settings (ROC 100 > 2, EMA 100) | 1,368 | 33.7 | 19/50 | 3,86,142 | −26,171 | +97k | −46k | +56k | −1.34L | 67% |

- **ROC 20 > 7 + EMA 50** made money in 2023, 2024 and 2025, was nearly flat in 2026 (−₹4k), and still made +₹1.08L without
  its best 3 trades. Random buys with the same ROC/EMA filter made +₹33k, so the timing adds real value (beats 97% of runs).
- About **1 trade every 3 days across all 50 stocks**, held a few days; ₹283 FYERS charges per trade, mostly STT.
- Caveat: these were picked knowing the 2025–26 result. The honest pick (best on 2023–24 only: ROC 30 > 0, EMA 20) made
  +₹1.12L overall but **lost ₹36k in 2025–26**. The ROC 20 block looks real because so many neighbouring settings agree, but
  it still needs a test on new stocks.

### How much money it really needs (ROC 20 > 7, EMA 50, daily)

₹1,00,000 is **per trade, per company**. Several companies can be open at once: up to **13 at the same time** (28 Dec 2023),
so taking every signal needed **₹12.9 lakh**. Most of the time far fewer were open (none on 39% of days, 1–2 on most others;
trades last about 5 days). With less money you must skip signals while your money is in use (first signal first):

| Money (₹1L slots) | Trades taken | Net ₹ | Per year on that money | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|
| ₹1 lakh (1 at a time) | 124 of 299 | −14,889 | −4.1% | +2k | −22k | +4k | +1k |
| ₹2 lakh | 190 | −13,027 | −1.8% | −9k | −15k | +10k | 0 |
| ₹3 lakh | 228 | +52,641 | +4.9% | +12k | +21k | +20k | 0 |
| **₹5 lakh** | 269 | **+1,15,027** | **+6.4%** | +31k | +40k | +48k | −4k |
| ₹8 lakh | 289 | +1,48,107 | +5.1% | +49k | +53k | +56k | −9k |
| ₹13 lakh (every signal) | 299 | +1,53,217 | +3.3% | +47k | +53k | +57k | −4k |

Even at the best size (≈ ₹5 lakh) it earns about **6% a year on the money set aside**, roughly what a fixed deposit pays and
below what a Nifty index fund did in this period. With only ₹1–2 lakh it lost money, because which signals you can take
depends on luck. "Simple" yearly return = total net ÷ money ÷ 3.6 years; idle money earning interest is not included.

### The standard setting on 1-hour and 4-hour

Report: `../../projects/trading-equation-backtests/reports/STRATEGY5_STANDARD_TFS_REPORT.md` (script `experiments/strategy5_standard_tfs.py`).
"Same numbers" = ROC 20 > 7, EMA 50 on that chart; "same time span" = lengths covering the same days as daily
(4-hour: ROC 40, EMA 100; 1-hour: ROC 140, EMA 350).

| Chart | Version | Trades | Win % | Stocks profitable | FYERS charges ₹ | **Net ₹** | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|
| **Daily** | standard | 299 | 41.8 | 29/50 | 84,700 | **+1,53,217** | +47k | +53k | +57k | −4k |
| 4-hour | same numbers | 194 | 37.6 | 21/50 | 53,476 | −6,729 | +18k | −26k | +12k | −11k |
| 4-hour | same time span | 788 | 35.4 | 20/50 | 2,15,947 | +28,285 | +69k | +11k | +7k | −59k |
| 1-hour | same numbers | 89 | 40.4 | 10/50 | 11,555 | +4,902 | +7k | +1k | +1k | −3k |
| 1-hour | same time span | 3,153 | 26.0 | 3/50 | 5,36,301 | −5,63,425 | −1.44L | −2.11L | −1.12L | −97k |

**Daily is clearly best.** On 4-hour and 1-hour the trades are shorter (a "blue touches orange" sell comes within hours), many
are sold the same day or next day, and charges eat the gains. 1-hour same-numbers barely trades (a 7% rise in 20 hours is rare).

### High ROC levels — "only buy if ROC > 25" (30 Oct 2026)

Report: `../../projects/trading-equation-backtests/reports/STRATEGY5_ROC_LEVELS_REPORT.md` (script
`experiments/strategy5_roc_levels.py`). Standard setting with ROC length 10–250 × level 10–100%, EMA 50, daily / 4-hour / 1-hour.

**Daily, ROC > 25 (net ₹ after FYERS charges, all 50 stocks):**

| ROC length | Trades | Win % | Stocks profitable | **Net ₹** | 2023 | 2024 | 2025 | 2026 | Beats random |
|---|---|---|---|---|---|---|---|---|---|
| 20 | 15 | 26.7 | 3 | +12,943 | −7k | +9k | +11k | 0 | 53% |
| 30 | 37 | 45.9 | 7 | +39,396 | +3k | +15k | +23k | −2k | 67% |
| 50 | 122 | 37.7 | 11 | +45,783 | +9k | +11k | +21k | +5k | 50% |
| 100 | 323 | 37.2 | 16 | +59,900 | +19k | +34k | +24k | −17k | 57% |
| 150 | 435 | 39.3 | 21 | +63,701 | +48k | +49k | +13k | −46k | 43% |
| 200 | 597 | 36.0 | 19 | −15,577 | +78k | −19k | −18k | −57k | 10% |
| 250 | 677 | 36.0 | 20 | +46,354 | +74k | +10k | +32k | −69k | 47% |
| *Standard: ROC 20 > 7* | *299* | *41.8* | *29* | ***+1,53,217*** | *+47k* | *+53k* | *+57k* | *−4k* | *97%* |

- **ROC > 25 makes a little money on daily (except ROC 200) but much less than the standard ROC 20 > 7.** It only beats
  random buys about half the time, so the profit comes from picking strong stocks, not from good timing.
- **With a short ROC (20–30), > 25% is very rare** (15–37 trades in almost 4 years: a 25% rise in a month).
- Best daily ROC levels stay **ROC 50 > 10–15** (+₹1.1–1.2L) and **ROC 20 > 5–7** (+₹1.5–1.8L).
- **4-hour is the one place a high level helps:** ROC 150 > 25 = +₹1,11,918 (388 trades, beats random 97%), ROC 250 > 30 =
  +₹1,06,708, vs −₹6,729 for the standard numbers on 4-hour. But **most of it came in 2024** (ROC 150 > 25: 2023 +5k ·
  **2024 +95k** · 2025 +12k · 2026 0), so it's less steady than daily ROC 20 > 7.
- **1-hour loses** at almost every length and level.

### Stop-loss at the buy candle's low + ROC levels 3–30 % (30 Oct 2026)

Report: `../../projects/trading-equation-backtests/reports/STRATEGY5_STOPLOSS_REPORT.md` (script `experiments/strategy5_stoploss.py`).
Every trade gets a stop at the **low of the candle it was bought on**. It sells at whichever comes first (price falls to that low,
or blue touches orange); both trigger on a falling price, so the order inside a candle is never in doubt. ROC length 10–250 ×
level 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 25, 30 %, with and without the stop, all 5 timeframes.

**Daily, ROC 20 (net ₹, all 50 stocks):**

| ROC 20 level | > 3% | > 4% | > 5% | > 6% | > 7% | > 8% | > 9% | > 10% |
|---|---|---|---|---|---|---|---|---|
| no stop | +1.67L | +1.69L | **+1.78L** | +1.67L | +1.53L | +76k | +88k | +68k |
| with stop | +1.52L | +1.54L | **+1.99L** | +1.85L | +1.54L | +81k | +96k | +70k |

- **Standard ROC 20 > 7 with the stop: +₹1,54,307 vs +₹1,53,217 without**, almost no change. The stop is about **2.2%** below the
  buy price (median); it was hit on 67 of 299 trades.
- **It cuts the event-day crashes:** the 3 Jun 2024 buys sold on 4 Jun at the stop: NTPC −₹4,959 (was −₹15,708), POWERGRID
  −₹3,847 (was −₹12,511), ULTRACEMCO −₹2,553 (was −₹4,728).
- **But it also cuts trades that dipped and then recovered**, so overall the gains and losses cancel out. 2026 got slightly worse
  (−₹9.7k vs −₹3.9k).
- **ROC 20 > 5 with the stop = +₹1,98,764** (465 trades; 2023 +94k · 2024 +50k · 2025 +89k · **2026 −34k**): highest total,
  but a bigger loss in 2026 than ROC 20 > 7.
- Levels **8–10% are clearly worse** than 5–7% (fewer trades, less profit). The sweet spot is **ROC 20 > 5–7%**.
- **On daily the stop hurts most other settings** (total of all settings +₹48.5L → +₹29.0L; 75 → 66 positive). It only pays
  off when there are big sudden crashes.
- **On 4-hour the stop helps the long-ROC versions:** ROC 250 > 30 = **+₹1,41,710** with stop (vs +₹1,06,708); ROC 250 > 25
  +₹1,34,157 (2023 +55k · 2024 +83k · 2025 +8k · 2026 −12k).
- 15-min / 30-min / 1-hour still lose with or without the stop.

## 5. Other timeframes

- **4-hour:** only ROC 20 > 5 (any EMA) and ROC 10 > 2 hold up in both periods, for **+₹5k to +₹24k**. Too small after charges.
- **15-min / 1-hour:** nothing holds up. **30-min:** 8 tiny winners (+₹5k range).

## 6. Lesson

For Strategy 5 the useful change is **ROC 20 instead of ROC 100, with a 5–7% level, on daily candles**: "the stock rose 5–7%+
in the last month and Stoch just turned up from below 50". It's the first version in all these tests that made money in
each of 2023, 2024 and 2025 and nearly broke even in the falling 2026. Next: run it on Nifty 200 (stocks it hasn't seen) and
paper-trade it.
