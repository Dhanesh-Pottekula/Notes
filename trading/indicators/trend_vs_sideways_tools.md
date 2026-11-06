# Trend or Sideways? — ER vs ADX vs Choppiness vs MA Slope vs Bollinger Width

Five common ways to tell whether a market is trending or going sideways: what each one measures, what it is good for, and what
my own test on 185 Nifty 200 stocks (daily, 2014–Oct 2026, ~484k stock-days) showed. Education, not investment advice.
KAMA and the Efficiency Ratio in detail: `kama_kaufman_adaptive_moving_average.md`.

## 1. What each tool actually measures

| Tool | Formula idea | Measures | Gives direction? | Speed |
|---|---|---|---|---|
| **Efficiency Ratio (ER, 10)** | net move ÷ total path | how *straight* price moved | no | fast (raw, no smoothing) |
| **ADX (14)** | smoothed \|+DI − −DI\| ÷ (+DI + −DI) | how *one-sided* the bars are (higher highs vs lower lows) | no (+DI vs −DI does) | slow (double-smoothed, ~2×14 bars of lag) |
| **Choppiness Index (14)** | log(Σ true range ÷ 14-bar high–low range) | how much of the bars' movement was wasted inside the range | no | medium |
| **MA slope** (50-SMA, 10-bar change ÷ ATR) | how fast the average is rising/falling | the *direction* and pace of the trend | **yes** | slow (MA lag) |
| **Bollinger Band width** (20, 2) | 4 × std dev ÷ 20-SMA | **volatility**, not trend | no | medium |

**Overlap (rank correlation between the tools, my data):**
- **ER and Choppiness overlap a lot** (−0.55): two versions of "net move vs total movement". You don't need both.
- **Choppiness and BB width** −0.59; **ADX and BB width** +0.44: big trends usually come with big ranges.
- **MA slope** has almost no correlation with any of the others (≤ 0.17). It is the only one that tells you **which way**.

## 2. Test A — can any of them predict the *next* 10 days?

Rank correlation between today's value and the next 10 days' trendiness (ER), volatility change, and size of the move:

| Tool | → next-10-day ER (trendiness) | → volatility expansion | → next \|move\| ÷ ATR |
|---|---|---|---|
| ER | −0.02 | +0.05 | +0.01 |
| ADX | −0.03 | −0.05 | −0.03 |
| Choppiness | +0.02 | +0.08 | +0.01 |
| MA slope | −0.02 | +0.00 | +0.00 |
| **BB width (percentile)** | −0.04 | **−0.23** | −0.07 |

- **None of them predicts whether the next 10 days will trend or chop.** Trending stocks and sideways stocks are followed by
  trendiness of about 0.28–0.31 either way.
- **Only Bollinger width predicts something: volatility.** After a squeeze (width in the bottom 20% of the last year), the next
  10 days' volatility was **10% higher** than the last 20 days' (ratio 1.10). After very wide bands it was **18% lower** (0.82).
  Volatility goes back toward normal. The squeeze tells you "a bigger move is likely". It does not tell you which way.

## 3. Test B — do they help a trend-follower?

Bet in the direction of the 50-day SMA slope, then measure the average 20-day return in that direction. Compare each tool's
"trending" and "sideways" readings. Gross returns, before charges.

| State today | Share of days | Avg 20-day return in trend direction | Hit rate |
|---|---|---|---|
| All days (no filter) | 100% | +0.25% | 50.6% |
| **Choppiness < 38** | 12% | **+0.66%** | 52.3% |
| ADX > 25 | 43% | +0.46% | 51.4% |
| \|MA slope\| > 1 ATR | 25% | +0.46% | 51.5% |
| ER > 0.5 | 23% | +0.43% | 51.1% |
| BB squeeze (bottom 20%) | 22% | +0.29% | 51.0% |
| ER < 0.2 | 35% | +0.22% | 50.8% |
| ADX < 20 | 36% | +0.15% | 50.5% |
| Choppiness > 62 | 10% | +0.14% | 50.4% |
| \|MA slope\| < 0.25 ATR | 22% | **+0.03%** | 50.0% |

- **Every "trending" filter roughly doubles the trend-follower's edge**, and every "sideways" reading roughly kills it. So yes,
  they separate good conditions for trend-following from bad ones.
- **The hit rate hardly moves** (50% → 51–52%). The gain comes from **bigger winning moves**, not more frequent wins.
- **Choppiness < 38** was strongest but is rare (12% of days). **ADX > 25** and **MA slope** were almost as good and cover 25–43% of days.
- **ADX rising vs falling made no difference** (+0.47% vs +0.43%), despite the popular rule "only trade when ADX is rising".
- **The edge is small.** +0.5% per 20 days gross is about the size of a delivery round trip's charges plus slippage (~0.3–0.4%),
  so a filter on its own is not a tradable strategy. It only improves a signal that already has an edge.

**But look at it year by year** (avg 20-day return in trend direction, %):

| Year | No filter | \|slope\| > 1 | ADX > 25 | ER > 0.5 |
|---|---|---|---|---|
| 2018 | −0.70 | −1.14 | **−1.46** | −0.57 |
| 2022 | −0.17 | **−0.93** | −0.22 | +0.13 |
| 2023 | +1.49 | +2.53 | **+2.66** | +2.09 |
| 2024 | +1.31 | **+2.15** | +1.73 | +1.35 |
| 2026 | −0.48 | **−1.53** | −1.15 | −0.44 |

The filters mostly **amplify the year**: in trend-friendly years (2021, 2023–24) they make it better, and in choppy, reversing years
(2018, 2026) they make it *worse* (ER > 0.5 was the exception in 2022). "Trending right now" is not "will keep trending". This is the same lesson as Test A,
seen through returns.

## 4. Which one is better for what

| You want to… | Use | Why |
|---|---|---|
| **Know which way to trade** | **MA slope** (or price vs 200-DMA) | The only one with direction. My best filter so far is Nifty above its 200-DMA (+0.26 Sharpe in `../backtest_results_summary.md`) |
| **Turn a trend system on or off** | **ADX > 25** (simple, common) or **Choppiness < 38** (stricter, rarer) | Both separated good and bad trend-following days best in Test B. Don't bother with "ADX rising" |
| **Avoid trading in chop** | **Choppiness > 62** or **\|MA slope\| < 0.25 ATR** | Trend-following made ~0% in these states |
| **Make an indicator adapt its own speed** | **ER** (inside KAMA) | Fast, no smoothing lag, a clean 0–1 scale. Built to be plugged into a formula |
| **Expect a big move / size positions / options** | **BB width** (squeeze) | The only tool that predicted anything: volatility expands after a squeeze, shrinks after wide bands. No direction |
| **Mean-reversion (range) trading** | **ADX < 20** + **Choppiness > 62** | Shows the market is going nowhere *now*, but test Test A again: chop doesn't reliably continue either |

**Practical combo:** *direction* from MA slope / 200-DMA, *permission* from ADX or Choppiness, *size* from ATR or BB width.
ER and Choppiness are nearly the same, so pick one of them.

## 5. Settings and reading tips

- **ADX:** 14 is standard. Under 20 is no trend; over 25 is a trend; over 40 is a strong trend that may be stretched. It is slow:
  by the time ADX crosses 25 the trend is usually weeks old. +DI above −DI means uptrend.
- **Choppiness:** 14 bars. The 38.2 / 61.8 lines are Fibonacci levels, but they are just thresholds. 100 = pure chop, 0 = straight line.
- **ER:** 10 bars. Thresholds depend on the window length (Nifty median 0.31 at n = 10, 0.13 at n = 60), so use percentiles.
- **MA slope:** divide by ATR so the number means the same on a ₹100 stock and a ₹10,000 stock.
- **BB width:** compare with its own last year (percentile), never as a raw number across stocks.
- **Timeframe:** on 15-min or 1-hour bars, all of these flip between "trend" and "chop" many times a day. Use daily or weekly.

## 6. One-line summary

**MA slope tells you which way; ADX or Choppiness tell you whether trend-following is worth it right now; ER drives adaptive
indicators like KAMA; BB width predicts volatility, not direction.** None of them predicts whether the *next* period will trend.
