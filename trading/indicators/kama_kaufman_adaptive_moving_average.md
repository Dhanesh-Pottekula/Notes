# Kaufman's Adaptive Moving Average (KAMA) and the Efficiency Ratio — Trend vs Sideways

From Perry Kaufman, *Smarter Trading* (1995); also in Murphy, *Technical Analysis of the Financial Markets*, Moving Averages,
pdf p263 (see `../murphy_moving_averages.md` §10). Numbers below measured on my own NSE data (Oct 2026). Education, not investment advice.

## 1. The problem it solves

A normal moving average has a fixed speed. A fast one (10-day) follows trends quickly but whipsaws in a range.
A slow one (50-day) ignores the noise but enters trends late. KAMA changes its own speed bar by bar:
- **fast** when price is moving cleanly in one direction;
- **almost frozen** when price is going up and down without getting anywhere.

## 2. The Efficiency Ratio (ER) — "how straight was the road?"

```
ER = |Close_t − Close_{t−n}|  ÷  Σ |Close_i − Close_{i−1}|   (over the last n bars, usually n = 10)
        net distance travelled         total distance walked
```

- **ER = 1:** every bar moved the same way, a perfectly straight trend.
- **ER = 0:** price walked a lot but ended where it started, pure chop.
- Physics picture (`../price_physics_basics.md`): ER = displacement ÷ path length. It compares **drift** (direction) with **noise**.

**Example, 10 days.** The stock goes 100 → 110 in daily steps of +1. Net = 10, path = 10, so **ER = 1.0**.
Another stock goes 100 → 102 → 99 → 103 → 100 → 104 → 101 → 103 → 100 → 102 → 101. Net = 1, path = 2+3+4+3+4+3+2+3+2+1 = 27,
so **ER = 0.04**.

## 3. From ER to KAMA (Kaufman's default 10, 2, 30)

```
fast = 2/(2+1) = 0.667        slow = 2/(30+1) = 0.0645
SC   = [ ER × (fast − slow) + slow ]²          ← smoothing constant, squared to push choppy values toward zero
KAMA_t = KAMA_{t−1} + SC × (Close_t − KAMA_{t−1})
```

| ER | SC | Acts like | Meaning |
|---|---|---|---|
| 1.0 | 0.444 | ~3-day EMA | trend: hugs price |
| 0.5 | 0.133 | ~14-day EMA | mixed |
| 0.2 | 0.034 | ~60-day EMA | weak |
| 0.0 | 0.004 | ~500-day EMA | chop: line goes flat |

The square is the key trick: an ER of 0.2 does not give "20% of the fast speed". It gives about 8% of it, so in a range the
line almost stops moving and price crosses it back and forth without dragging it.

**Nifty in October 2026 (real):** ER(10) was 0.58 on 8 Oct (SC 0.17, KAMA moving); since 13 Oct it has been **0.02–0.31**, and
KAMA has sat at **22,768–22,800 for two weeks** while Nifty swung between 22,600 and 23,150. The flat line *is* the signal: sideways.

## 4. How do we tell trending vs sideways?

**Read ER directly** (the same number KAMA uses):

| ER(10) on daily bars | Read it as | How often on Nifty, 2009–2026 |
|---|---|---|
| > 0.5 | trending | 26% of days |
| 0.2 – 0.5 | mixed / weak trend | 41% |
| < 0.2 | sideways | 33% |

Nifty's median daily ER(10) is 0.31, and a **pure random walk** scores 0.27. So most of the time, the market's
"trendiness" over 10 days is close to what coin-flips would produce.

**The threshold depends on n.** The longer the window, the more noise the path adds, so ER falls. Nifty's median ER is 0.31 for
n = 10, 0.21 for n = 20, 0.13 for n = 60 and 0.09 for n = 120. Never reuse a "0.3" threshold across different lengths or timeframes.
Pick it from that market's own percentiles.

**Other tools that answer the same question:**

| Tool | Trend when | Sideways when |
|---|---|---|
| **ADX (14)** | > 25 | < 20 |
| **Choppiness Index (14)** | < 38 | > 62 |
| **MA slope** | the 50-day MA rises or falls by > ~0.5 ATR over 10 bars | flat |
| **Bollinger Band width** | expanding | squeezed (often *before* a breakout) |
| **Price vs 200-DMA** | far above or below | crossing it back and forth |
| **KAMA itself** | sloping | flat |

ER and the Choppiness Index are nearly the same idea (net move vs total path). ADX measures directional movement vs range.
All of them describe **the bars you already have**.
Which one to use for what, tested on 185 Nifty 200 stocks: `trend_vs_sideways_tools.md`.

## 5. The important part: can ER *predict* the next trend? (my test)

I asked: if today's ER is high, will the **next** 10 days also trend? (Nifty daily 2009–2026, plus 188 Nifty 200 stocks.)

| ER(10) today | Median ER of the next 10 days | P(next 10 days trend, ER > 0.4) |
|---|---|---|
| 0 – 0.2 (sideways) | 0.31 | 38% |
| 0.2 – 0.4 | 0.33 | 40% |
| 0.4 – 0.6 | 0.30 | 39% |
| 0.6 – 1.0 (strong trend) | 0.29 | 34% |

- **Correlation between today's ER and the next period's ER:** −0.04 (10-day), −0.11 (20-day), −0.04 (60-day) on Nifty. The median
  across 188 stocks is −0.03. A random walk gives −0.02. Hourly Nifty bars give −0.01.
- In contrast, **volatility does persist**: the correlation of 10-day volatility with the next 10 days' is **+0.58**.

**So: ER tells you what the market *is doing*, not what it *will do*.** A sideways stretch is as likely to be followed by a trend
as by more chop. "How much it moves" is predictable; "whether it moves in a straight line" is not, at least not from ER.

That is why KAMA is useful as an adaptive tool, not as a forecaster:
- It needs no prediction. It reacts to whatever ER the market gives it, bar by bar, and stays quiet in chop.
- The cost: when a trend begins after a range, ER starts low, so KAMA is slow at the start of the move. It catches the middle of
  the trend, like every moving average.
- A crossover on a flat KAMA still happens in a range. Kaufman adds a **filter**: only act when KAMA has moved by more than a
  fraction (e.g. 0.1–0.2) of the standard deviation of its recent changes.

## 6. How to use it (and what my backtests say)

1. **As a regime filter:** skip trend signals (MA cross, breakout, MACD) when ER or ADX says "sideways", and skip mean-reversion
   signals when it says "trending". It removes some whipsaws; it does not make a losing signal profitable.
   - My **Adaptive SuperTrend** test (`../../../projects/trading experiments/supertrend_di_backtest.py`, `er_len=14, er_thr=0.30`)
     used exactly this filter. It still **lost to costs on short timeframes**.
   - The filter that helped most in my tests was the slow one: **Nifty above its 200-DMA** (+0.26 Sharpe, see
     `../backtest_results_summary.md`). Slow filters work because they describe the big trend, which lasts longer.
2. **As a trailing exit:** KAMA flattens in pauses and speeds up in strong moves, so it suits trailing a position.
3. **Use daily or weekly bars.** On 15-min or 1-hour bars, ER flips between "trend" and "chop" many times a day, and every flip costs
   charges (`../breakeven_move_fyers.md`).
4. Not yet tested by me: a full KAMA crossover / KAMA-filter backtest on Nifty 200 daily. Worth a project if I want the number.

## 7. One-line summary

**ER = net move ÷ total path.** High means trending, low means sideways. KAMA uses ER² to pick its speed. ER describes the present
well, but on Nifty it has **zero** power to forecast whether the next 10–60 days will trend. Use it to *adapt*, not to *predict*.
