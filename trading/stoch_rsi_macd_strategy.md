# My Stochastic RSI + MACD Strategy — Rules and Backtest Result

Tested Oct 2026 on all Nifty 50 stocks (re-checked on Nifty 200), 15-min / 30-min / 1-hour / 4-hour, buy and sell separately,
intraday and delivery, FYERS charges. Education, not investment advice.
Full report: `../../projects/trading-equation-backtests/reports/STOCH_MACD_REPORT.md`.

## 1. The rules

**Buy** when all three are true on a closed candle (sell = the mirror):
1. **Trend is up:** price above the 200 EMA and the 50 EMA above the 200 EMA.
2. **Stochastic RSI:** the blue line (%K) crosses **above** the orange line (%D).
3. **MACD:** if MACD is below its signal line, the gap is shrinking; if above, the gap is growing.
   → Both mean the **MACD histogram is higher than on the last candle** (momentum turning up).

Settings: Stoch RSI 14, 14, 3, 3 · MACD 12, 26, 9. Stop: below the lowest low of the last 10 candles.

## 2. How the indicators work (quick)

- **RSI** (0–100) measures how strong recent up-moves are versus down-moves.
- **Stochastic RSI** asks "where is RSI inside its own range of the last 14 bars?" (0 = lowest, 100 = highest). It is very fast
  and crosses many times a day on intraday charts.
- **MACD** = EMA12 − EMA26 (speed of the trend). **Signal** = EMA9 of MACD. **Histogram** = MACD − signal = whether that speed is
  increasing (acceleration — see `price_physics_basics.md`).

## 3. Result

| | Intraday | Delivery |
|---|---|---|
| **BUY** | Lost on Nifty 50 in all 36 versions; win rate 35–42% vs 42–47% needed | Lost (no version beat cash, except one 4-hour Nifty 200 version at 6.8%/yr) |
| **SELL** | One small lead: **15-min, EMA trend, any Stoch cross, trailing stop** — profitable on both lists and both halves (+₹45k / +₹60k on ₹10L in 10 months), beat random shorts 20/20 | Lost (as stock-futures shorts) |

- **4-hour buys** made 15–42% a year in 2023–24 but lost in 2025–26 → the good years were the market, not the rules.
- **Delivery on 15/30-min:** the stop is only ~0.2% away but delivery charges are ~0.25% → every trade starts more than 1R behind.
- **More signals = worse.** Allowing 10 trades a day instead of 3 turned the best sell version from +₹45k into −₹1.35L.
- **Didn't help:** higher-timeframe trend, waiting for the Stoch cross from below 20 / above 80, exiting on the opposite Stoch cross
  (in delivery it was a disaster — too many trades).
- **The sell lead's caveats:** small (≈ +5% in 10 months), dies at 0.03% slippage on Nifty 50, only tested in one falling market
  (2026). Paper trade only.

## 3b. Re-test with my final rules (Oct 2026)

Final rules: **no EMA trend** (the MACD histogram is the trend check: buy when red bars shrink or green bars grow, sell the mirror);
Stoch RSI blue crosses orange, **buy not in overbought (both lines ≤ 80), sell not in oversold (both ≥ 20)**, and only on a **steep
cross** (blue line moves ≥ X points in the crossing candle; X = 10 / 15 / 20 tested — the median cross moves ~7).
Report: `../../projects/trading-equation-backtests/reports/STOCH_MACD_USER_REPORT.md`.

| | Intraday | Delivery |
|---|---|---|
| **BUY** | Nifty 50: 0 of 36 versions beat cash. Nifty 200: tiny gains on 15/30-min, not consistent | Nifty 50: 1 of 48 beat cash; 15/30-min lose big to charges |
| **SELL** | 0 of 36 on both lists | Least bad: 30-min steep cross + 2R as futures short — Nifty 200 +₹83k to +₹1.1L (both halves), Nifty 50 +₹42k (first half only) |

- **Steep cross = the most useful rule:** ≥ 20 points improved delivery sells in 23 of 24 comparisons, delivery buys 17 of 24.
- **No EMA filter** helped buys, hurt sells (the 15-min sell lead disappeared).
- Entries beat random entries, but win rates (39–48%) stay just under break-even (41–53%) after charges.

## 4. Lesson

Combining two momentum indicators gives a nice-looking entry on a chart, but on 50–200 stocks with real costs the win rate stays
below break-even. Slower, rarer trades (weekly pullback, monthly momentum rotation) are still the only things that worked in my tests.
