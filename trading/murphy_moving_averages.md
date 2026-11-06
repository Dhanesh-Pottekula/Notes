# Murphy — Moving Averages (chapter summary)

*Technical Analysis of the Financial Markets*, John J. Murphy, chapter "Moving Averages":
printed pages 195–224 = **pdf p232–264** in `../../books/trading/John_J._Murphy_-_Technical_Analysis_Of_The_Financial_Markets.pdf`.
The PDF is scanned. Read it with `tools/bin/pdftool ocr "<pdf>" 232 264` from the GFV root.
This is a summary in my own words plus links to my backtests. Education, not investment advice.
**Visual, interactive version** (live charts for every section + self-check quiz): `murphy_moving_averages_visual.html` in this folder.

## 1. What a moving average is (pdf p232–234)

- **Simple MA (SMA):** the average of the last N closes. Each new day adds the newest close and drops the oldest, so the line "moves".
- **What it's for:** it's a **trend-following** tool. It smooths out the noise so the trend is easier to see, and it tells you
  *after the fact* that a trend has started or ended. Murphy's line: "The moving average is a follower, not a leader." It never predicts.
- **The cost is lag.** Smoothing and lag are the same thing. A 20-day MA hugs price closely; a 200-day MA is smooth but slow.
- **Which price to use:** usually the close. Variants use the midpoint (H+L)/2, the typical price (H+L+C)/3, or two separate MAs of
  the highs and lows, which form a band ("neutral zone").

## 2. The three types (pdf p236–237)

| Type | How it weights the data | Problem it fixes |
|---|---|---|
| **Simple (SMA)** | Every day weighted equally (10-day → 10% each) | — (Murphy's critics: it only covers N days and treats old = new) |
| **Linearly weighted (WMA)** | Day 10 × 10, day 9 × 9 … day 1 × 1, divided by the sum | Recent data counts more |
| **Exponential (EMA)** | `EMA_today = α·Close + (1−α)·EMA_yesterday` | Recent data counts more **and** all past data still has a small effect |

The α conversion Murphy gives: α = 10% ≈ a 20-day average, α = 5% ≈ a 40-day average. The usual formula is
**α = 2 / (N + 1)** (N = 20 → α ≈ 0.095). An EMA reacts faster than an SMA of the same length.
Murphy mostly uses the **simple** MA and says there's no real evidence that the fancier types work better (pdf p262).

## 3. Signal methods

### One MA (pdf p238–240)
- **Buy** when price **closes above** the MA; **sell** when it closes below.
- **Stronger** when the MA itself turns in the same direction (example: Intel and the 50-day).
- **Trade-off:** a short MA (5–10 days) gives early signals but many **whipsaws**; a long MA gives fewer, later, more reliable signals.
- Corollary: **long MAs are better while a trend continues, short MAs are better when it's reversing.** That's why one MA alone isn't enough.

### Two MAs, the double crossover (pdf p240–242)
- **Buy** when the short MA crosses above the long MA; **sell** when it crosses below. It lags a bit more than one MA but gives fewer whipsaws.
- Popular pairs: **5/20** and **9/18** (futures), **10/50** (stocks).

### Three MAs, the triple crossover 4-9-18 (pdf p241–244)
From R.C. Allen (1972). Uptrend alignment: 4 > 9 > 18; downtrend: 4 < 9 < 18.
- **Alert:** the 4-day crosses both of the others.
- **Confirmed signal:** the 9-day then crosses the 18-day.

## 4. Bands around an MA

### Percentage envelopes (pdf p244–247)
Lines a fixed % above and below the MA flag an **overextended** market:
3% around a 21-day MA for short-term trading, 5% around a 10-week or 10% around a 40-week MA for long-term analysis.

### Bollinger Bands (pdf p248–250)
- Middle line: **20-day SMA**. Bands at **±2 standard deviations**.
- Upper band = overbought, lower band = oversold.
- **Bands as targets:** after a bounce off the lower band and a close above the 20-day, the upper band is the target (and the reverse on the way down).
- **Strong uptrend:** price rides between the upper band and the 20-day; a **close below the 20-day warns of a reversal**.
- **Width = volatility.** Very wide bands often mean a trend is ending; very narrow bands (a "squeeze") often come before a new trend.
- Also works on weekly/monthly charts (20 weeks / 20 months). Best combined with oscillators (the next chapter).
- **Centering:** a statistically "correct" MA is plotted in the middle of its period, but that delays signals, so it's only used for cycle analysis.

## 5. Why 5, 10, 20, 40 (cycles and Fibonacci) (pdf p251–252)
- A month has about 20 trading days, and cycles tend to be **harmonic** (half or double their neighbours). That explains 5/10/20/40, and 4/9/18 is a variant of that.
- Fibonacci numbers (13, 21, 34, 55…) also seem to work well as MA lengths.

## 6. Long-term charts (pdf p252)
On **weekly** charts, use **10/13-week with 30/40-week** MAs. The **40-week (≈200-day)** MA tends to act as support in bull-market corrections.

## 7. Pros and cons (pdf p253–255)
- **Pros:** you trade with the trend, cut losses short and let profits run. It's mechanical, so there's no emotion in it.
- **Cons:** MAs work badly in **sideways/choppy** markets, which Murphy puts at **a third to half of the time**. Use an oscillator
  in ranges, and ADX to tell which kind of market you're in.
- **MA as an oscillator:** the gap between two MAs (e.g. two EMAs) is an oscillator. **MACD** is exactly that (covered in the Oscillators chapter, pdf p266+).
- MAs can be applied to anything: indicators, ratios, oscillators.

## 8. Alternative: the 4-week rule / channel breakout (Donchian) (pdf p256–261)
- **Rule:** buy (and cover shorts) when price **exceeds the highs of the previous 4 full calendar weeks**; sell (and go short) when it
  **breaks the lows of the previous 4 weeks**. It's always in the market.
- **Evidence Murphy cites:** in 1970 Dunn & Hargitt rated it the best system they tested. Lukac's studies (1975–84, then 23 systems
  over 1976–86) found **channel breakouts and MA crossovers** were the only consistent winners.
- **Not always in the market:** enter on a 4-week breakout, exit on a 1- or 2-week breakout the other way, then wait for the next 4-week signal.
- **As a filter:** only take an MA crossover if a 2-week breakout agrees.
- **Tuning:** halve or double the period (1, 2, 4, 8 weeks) to make it faster or slower, e.g. a 1-week trailing stop after a sharp
  rally, or 8 weeks to sit out trading ranges.
- On charts this is a **20-day (4-week) price channel** (Donchian channel).

## 9. Optimisation (pdf p261–262)
Testing to find the best MA length per market can help, but Murphy says it isn't the Holy Grail.
Optimise only if you follow a handful of markets; if you follow many, use the **same settings everywhere**.
Common defaults: futures 4/9, 9/18, 5/20, 10/40; stocks **50-day**, plus **30/40-week (200-day)** for long-term; Bollinger 20-day / 20-week (≈100-day).

## 10. Adaptive moving average (Kaufman AMA) (pdf p263)
The speed adjusts itself using an **Efficiency Ratio**:

```
ER = |Close_t − Close_{t−n}| / Σ |Close_i − Close_{i−1}|      (net move ÷ total path)
```

ER near 1 means a clean trend, so the average speeds up. ER near 0 means chop, so it slows down and avoids whipsaws.

## How this connects to my own tests

| Murphy says | What my backtests found |
|---|---|
| MAs fail in sideways markets (⅓–½ of the time) | **MACD crossover** (an MA-difference oscillator) was not worth trading on any timeframe from 1-min to weekly (`backtest_results_summary.md`) |
| The 40-week / 200-day MA is the key long-term trend line | The **200-day market filter** was the one consistent winner (+0.26 Sharpe, −8 pts drawdown); the **weekly pullback** (close > 50-wk > 200-wk, dip to the 20-week EMA) made 18.5–26%/yr |
| Long MAs are better while the trend continues | "Delivery on weekly/monthly signals is where the edge is"; no intraday strategy passed (`backtest_results_summary.md`) |
| Kaufman's Efficiency Ratio filters chop | The **Adaptive SuperTrend** I tested uses the same ER idea (`er_len=14, er_thr=0.30` in `../../projects/trading experiments/supertrend_di_backtest.py`); it still lost to costs on short timeframes |
| Channel breakouts (4-week rule) are among the best systems | Daily breakout made 13–18%/yr but no better than holding the same stocks. A real 4-week (20-day) Donchian test hasn't been done; worth a project |

**Practical takeaways**
1. Use MAs on **daily/weekly** charts to define the trend (200-day / 40-week), not as a stand-alone intraday signal.
2. Add a trend/chop filter (ADX, Efficiency Ratio, or "is the MA itself sloping?") before taking crossover signals.
3. Next test idea: a **4-week Donchian breakout with a 2-week exit** on Nifty 200 stocks, plus the 200-DMA filter.

Related: Grimes, *Art and Science of Trading* (course workbook), ch.14 Moving Averages, pdf p492 (a quantitative test of MAs) ·
Nison, ch.13 Candles with moving averages, pdf p220.
