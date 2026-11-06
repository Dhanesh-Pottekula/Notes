# ETERNAL — Standard Strategy 5 Check, 16–24 Sep 2026 and 22–26 Oct 2026

Standard setup (`strategy5_standard_setup.md`): daily chart, buy at the close when ROC(20) > 7 · close > EMA 50 · MACD histogram
bigger than yesterday's · Stoch RSI blue crosses above orange with blue < 50; sell when blue touches orange. Also checked the
"buy after 2:15 pm" experiment. Data available up to 26 Oct 2026 (TradingView export). Education, not investment advice.

**Result: no buy in either window, for both the standard and the after-2:15 pm version.**

## 16–24 Sep 2026 (daily close values)

| Date | Close ₹ | ROC20 % | EMA 50 ₹ | MACD hist (yday → today) | Blue %K (yday → today) | Orange %D (yday → today) | What failed |
|---|---|---|---|---|---|---|---|
| 16 Sep | 317.00 | +0.35 | 309.02 | −2.24 → −2.28 | 11.98 → 11.94 | 10.05 → 11.97 | ROC, histogram falling, no cross |
| **17 Sep** | 322.35 | **+0.73** | 309.55 | −2.28 → −1.88 ✅ | 11.94 → **19.61** | 11.97 → 14.51 | **only ROC** (cross ✅, blue < 50 ✅, above EMA ✅) |
| 18 Sep | 326.85 | −0.34 | 310.22 | −1.88 → −1.29 | 19.61 → 43.09 | 14.51 → 24.88 | ROC, no new cross (already above) |
| 21 Sep | 335.90 | +2.41 | 311.23 | −1.29 → −0.30 | 43.09 → 72.35 | 24.88 → 45.02 | ROC, no new cross, blue > 50 |
| 22 Sep | 342.00 | +4.54 | 312.44 | −0.30 → 0.69 | 72.35 → 90.14 | 45.02 → 68.53 | ROC, no new cross, blue > 50 |
| 23 Sep | 342.65 | +3.52 | 313.62 | 0.69 → 1.28 | 90.14 → 100.00 | 68.53 → 87.50 | ROC, no new cross, blue > 50 |
| 24 Sep | 335.50 | +2.60 | 314.48 | 1.28 → 1.09 | 100.00 → 87.45 | 87.50 → 92.53 | blue fell below orange |

## 22–26 Oct 2026 (daily close values)

| Date | Close ₹ | ROC20 % | EMA 50 ₹ | MACD hist (yday → today) | Blue %K (yday → today) | Orange %D (yday → today) | What failed |
|---|---|---|---|---|---|---|---|
| 22 Oct | 304.45 | −10.98 | 317.76 | −1.26 → −1.99 | 46.69 → 22.07 | 50.18 → 42.32 | ROC, below EMA, histogram falling, no cross |
| 23 Oct | 317.40 | −7.37 | 317.75 | −1.99 → −1.51 ✅ | 22.07 → 25.31 | 42.32 → 31.36 | ROC, just below EMA, no cross |
| **26 Oct** | 325.55 | **−2.97** | 318.05 | −1.51 → −0.60 ✅ | 25.31 → **52.87** | 31.36 → 33.42 | **ROC** and **blue 52.9 (above 50)** (cross ✅, above EMA ✅) |

At 2:15 pm on 26 Oct, blue was 54.5 (also above 50) and ROC −2.4%, so the after-2:15 version didn't buy either.

## What-if (not the strategy): without the ROC rule

17 Sep would have bought 310 shares at ₹322.35 and sold at the 24 Sep open at ₹338.70: **+₹4,779** after ₹290 FYERS charges.
But the same no-ROC rule then bought 6 Oct (−₹2,372) and 15 Oct (−₹2,570). ETERNAL was going sideways (ROC near 0), which is
exactly the kind of market the ROC > 7 rule is meant to skip.

## Re-test without the ROC filter (3 Nov 2026)

Same rules minus ROC(20) > 7 (close > EMA 50 · MACD histogram rising · Stoch RSI cross up with blue < 50 · sell on the touch).

| Window | Buy at the close | Buy after 2:15 pm |
|---|---|---|
| 16–24 Sep 2026 | **1 trade: +₹4,778.97** | **1 trade: +₹4,208.10** |
| 22–26 Oct 2026 | none (26 Oct blue 52.87 > 50) | none (blue 54.5 at 2:15 pm) |

**Buy at the close (17 Sep → 24 Sep):** bought 310 × ₹322.35 = ₹99,928.50 on 17 Sep (EMA 50 309.55, MACD 2.16 / signal 4.04,
histogram −2.28 → −1.88, blue 11.94 → 19.61, orange 11.97 → 14.51, ROC20 +0.73%). Sold at the 24 Sep open ₹338.70 (gap down
to the touch level; blue 92.60 vs orange 94.25). Gross +₹5,068.50 − FYERS ₹289.53 (brokerage 40.00, STT 204.93, NSE 6.29,
SEBI 0.20, stamp 14.99, GST 8.37, DP 14.75) = **+₹4,778.97**, held 7 days.

**Buy after 2:15 pm:** 308 × ₹324.10 at 2:15 pm on 17 Sep (blue 22.69 vs orange 15.54), same sale: **+₹4,208.10** (FYERS ₹288.70).

**But across all 50 Nifty 50 stocks (daily, buy at close, 2023 – Oct 2026), removing ROC is worse:**

| Version | Trades | Win % | Stocks profitable | FYERS charges ₹ | **Net ₹** | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|
| With ROC 20 > 7 (standard) | 299 | 41.8 | 29/50 | 84,700 | **+1,53,217** | +47k | +53k | +57k | −4k |
| Without ROC | 1,340 | 35.4 | 24/50 | 3,78,426 | **+90,883** | +1.58L | −18k | +75k | **−1.24L** |

ETERNAL alone does better without ROC (+₹57,434 vs +₹10,970 over 2023–26), but the whole index does worse: 4.5× the trades, 4.5×
the charges, and a −₹1.24L 2026. The standard keeps ROC 20 > 7.

## Trading the rules again and again inside the windows (no ROC, every timeframe)

Script `../../projects/trading-equation-backtests/experiments/strategy5_window_trades.py`; every trade with indicator values and
each FYERS charge: `reports/strategy5/window_trades_eternal.csv`. Buy at each candle close when the rules hold, sell when blue
touches orange, buy again on the next signal; a trade still open at the window's end is sold at that day's last close.

| Window | Chart | Trades | Won | FYERS charges ₹ | **Net ₹** |
|---|---|---|---|---|---|
| 16–24 Sep 2026 | 15-min | 6 | 3 | 496 | **+1,105** |
| 16–24 Sep 2026 | 30-min | 3 | 1 | 652 | **+468** |
| 16–24 Sep 2026 | 1-hour | 0 | — | — | 0 (crosses came with blue already above 50) |
| 16–24 Sep 2026 | 4-hour | 0 | — | — | 0 (same) |
| 16–24 Sep 2026 | Daily | 1 | 1 | 290 | **+4,779** |
| 22–26 Oct 2026 | all charts | 0 | — | — | 0 (price mostly below EMA 50; crosses had blue above 50) |

15-min trades, 16–24 Sep (₹1L each, all sold the same day → intraday charges ≈ ₹83):

| Buy | Price | Sell | Price | Why | Net ₹ |
|---|---|---|---|---|---|
| 17 Sep 2:15 pm | 324.65 | 17 Sep 2:45 pm | 323.82 | touch | −337 |
| 18 Sep 9:15 am | 327.10 | 18 Sep 10:15 am | 328.75 | touch (open) | +421 |
| 21 Sep 9:30 am | 330.00 | 21 Sep 10:15 am | 330.95 | touch (open) | +205 |
| 21 Sep 12:30 pm | 330.60 | 21 Sep 2:15 pm | 334.25 | touch (open) | +1,019 |
| 23 Sep 10:30 am | 342.75 | 23 Sep 11:15 am | 342.72 | touch | −91 |
| 23 Sep 1:30 pm | 343.10 | 23 Sep 2:15 pm | 343.00 | touch (open) | −112 |

30-min trades: 18 Sep 9:15 → 10:45 (−128), 21 Sep 12:45 → 22 Sep 9:15 (+885, delivery), 22 Sep 2:15 pm → 23 Sep 9:15 (−288).

The daily chart made the most (+₹4,779) from one week-long move; the 15-min chart caught the same rise in 6 small pieces and paid
6× the charges. Across Nifty 50 in earlier tests, 15-min/30-min lose overall, so these few days are not a general result.
