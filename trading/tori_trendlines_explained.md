# Tori Trendlines — How the Method Actually Works

Tori Trades' two-line trendline method, as coded in `../../projects/trading experiments/tori_trendline_lab.pine`
(TradingView strategy "Tori Trendline Lab") and tested in that folder and in `../../projects/trading-equation-backtests/`.
Education, not investment advice.

## 0. Her actual process is top-down (sections 2–5 below are only the lower-timeframe part)

Sources agree on the shape, not every detail (no official full write-up found): Chart Fanatics / Tradezella playbook pages,
a summary of the Chart Fanatics video, and TradingView scripts modelled on the method.

1. **Higher timeframes first (monthly → weekly → daily):** find the **main trend** from market structure —
   **higher highs + higher lows = uptrend**, **lower highs + lower lows = downtrend** — and mark the big swing highs/lows and
   support/resistance levels. This sets the **bias**: which direction to trade.
2. **Drop to the execution chart (4-hour):** draw **thick, hand-adjusted** trendlines (not snapped to exact wicks) with 2–3+ touches,
   at least ~1 week of data from the first touch to the entry. Mark the **Action Line** and the **Safety Line**.
3. **Take only setups that agree with the higher-timeframe bias:**
   - *Bounce* off a trendline that runs **with** the higher-timeframe trend, or
   - *Break* of a short counter-trend line (e.g. weekly/daily uptrend → 4H pullback makes a falling line → price breaks it → the
     big trend resumes). Needs a clear Safety Line close by; skip if it's far.
4. **Manage:** stop = Safety Line (close through it = out); move it as new swing points form; add to the position as the trend continues.
   No fixed profit target in her playbook.

```
 WEEKLY / DAILY: higher highs + higher lows → bias = LONG
        HH
   HH  /  \
  /  \/    \  ← pullback
 /   HL     \
/            ...
 4-HOUR inside that pullback:
   \
    \  /\              ← short falling line (Action Line)
     \/  \  /\___/ ← break above it → BUY, with the big trend
          \/
   Safety Line = 4H swing low / rising line below
```

**What our tests did NOT capture:** the coded version (`tori_trendline_lab.pine`, `trendline_break`) draws lines on **one** timeframe
from 5-bar pivots, with only an optional daily-EMA filter — **no higher-timeframe structure (HH/HL) bias**, no thick hand-drawn lines,
and both setups taken regardless of the bigger trend. So the results in section 7 test the mechanical core, **not** her full
top-down method. Note: HTF uptrend + pullback + break is close to the weekly pullback strategy that did pass in my backtests.

## 1. The idea in one line

Draw **two lines** on the chart: the **Action Line** tells you *when to enter*, the **Safety Line** tells you *where you're wrong*
(the stop). No indicators.

## 2. Step 1 — find swing points (pivots)

- **Swing high** = a candle whose high is the highest of the 5 candles on each side. **Swing low** = lowest low of 5 on each side.
- A swing point is only **confirmed 5 candles later** (you need the 5 candles after it) — so every line is drawn a little late.

## 3. Step 2 — draw the lines

- **Support line** = straight line through the **last two swing lows**. Rising support = uptrend.
- **Resistance line** = straight line through the **last two swing highs**. Falling resistance = downtrend.
- Line price at any candle *b*:  `line(b) = p1 + (p2 − p1) / (b2 − b1) × (b − b1)` — the slope is the trend's **velocity**
  (see `price_physics_basics.md`).
- **3-touch line:** an older (third) swing point also sits on the line, within 0.3 × ATR ("thick line" tolerance).

## 4. Step 3 — the two setups (long side; shorts are the mirror image)

### Break (the one that works)
```
 price
   |\  swing high 1
   | \        swing high 2
   |  \  /\  /\                    ← falling RESISTANCE = Action Line
   |   \/  \/  \__ ____/  ← close crosses ABOVE the line → BUY
   |            \/
   |   _____/‾‾‾‾‾\___ swing low   ← SAFETY LINE (stop) below
   +----------------------------------- time
```
- **Entry:** a candle **closes above a falling resistance line** while the previous close was below it.
- **Safety Line (stop):** the rising support line if there is one below price, otherwise the **last swing low**.
- **Skip the trade if the stop is too far:** entry − safety > 3 × ATR (Tori's "don't chase breaks far from the safety line" —
  the best rule in the system).
- **Risk R** = entry − safety. Optional target at 2R or 3R.
- First touch of the line must be ≥ 7 days old; each line can trigger only one trade.

### Bounce (doesn't work in tests)
- **Entry:** price dips to a **rising support line** (third touch, within 0.3 ATR) and **closes back above it**.
- **Stop:** a close below the line.

## 5. Step 4 — managing the trade

- **Exit** when a candle **closes below the stop line** (not just a wick).
- **Trail:** each time a new higher swing low forms, move the stop up — to the rising support line, or to the new swing low,
  whichever is higher.
- Optional fixed **2R / 3R target**.

## 6. Worked example (break)

- Swing highs: ₹1,000 at candle 0 and ₹950 at candle 20 → slope = −2.5 per candle. At candle 30 the line is at ₹925.
- Candle 29 closed ₹920 (line there ₹927.5 → below). Candle 30 closes ₹930 (above ₹925) → **break → buy ₹930**.
- Last swing low ₹900 → stop ₹900 → risk **₹30 = 1R**. ATR ₹15 → 30 is 2 × ATR ≤ 3 × ATR → trade allowed.
- 2R target = 930 + 60 = **₹990**. With ₹10L and 1% risk: ₹10,000 ÷ ₹30 = **333 shares**.

## 7. What the tests showed

**TradingView tests (13 stocks + Nifty, long only, 0.12% per side; `tori_multistock_playbook.md`):**

| Timeframe | Win rate (Break only) | Profit factor | Profitable symbols |
|---|---|---|---|
| 15-min | 20% | 0.51 | 0/13 — loses even before costs |
| 1-hour | 34% | 0.84 | 5/13 |
| 4-hour | 37% | 1.31 | 9/13 (edge faded after 2021) |
| **Daily** | **43%** (51.5% with a 2R target) | **1.90** | **12/13** (13/13 with 2R target) |

- **Break works, Bounce doesn't** (Bounce lost or broke even on every timeframe).
- On 4-hour, a MACD histogram > 0 filter helped; on daily no indicator helped.
- **Almost never beat buy-and-hold** (0 of 13 on daily) — it sits in cash much of the time.

**Portfolio test (Nifty 200, Break only, 1% risk + ATR stop; `trading-equation-backtests/reports/REPORT.md`), 2022–Oct 2026:**
weekly 12–16% a year (Sharpe 0.56–0.69; the 200-day market filter cut its drawdown from 15% to 9%), daily 8–12% (Sharpe 0.16–0.39),
1-hour and intraday lost. Equal-weight hold of the same stocks: 18.9% a year.

## 8. Why it behaves like this

- A **break of a falling line** = the downtrend's velocity flips — the start of a new move (momentum). That has a real, if small, edge.
- A **bounce** bets that a line drawn through two noisy points will hold a third time — on automatic lines it usually doesn't.
- On **short timeframes** swing points are mostly noise and costs are large relative to the moves.
- Lines are drawn **late** (5-candle confirmation), so entries are not at the bottom.

## 9. If I use it

Daily (or weekly) chart · Break only · skip breaks > 3 ATR from the Safety Line · 1% risk per trade · trail the Safety Line or take
2R–3R · only when Nifty is above its 200-day average · spread across 10–15 liquid stocks · compare with an index fund.
