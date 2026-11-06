# Using the Equations to Trade Profitably

Which equations still matter, and how they turn into money in practice. Formulas are in
`trading_equations.md` (numbers like "eq 6" refer to it). Education, not investment advice.

## The core idea

No equation finds profits by itself. Profit comes from an **edge**: a repeatable pattern that pays
more than it costs. The equations do three jobs around that edge:

1. **Prove the edge is real** after costs, and bigger than just holding the Nifty.
2. **Size positions** so you survive the bad runs and let the edge compound.
3. **Control risk** with stops, time limits and kill switches when the edge fades.

Most retail traders lose on #1 (no edge after costs) or #2 (betting too big). SEBI's data says
87–93% of F&O traders lose money (`../../projects/trading experiments/indian_market_strategies_research.md`).

## Which equations still matter

| Equation | Still matters? | How it makes or saves money |
|---|---|---|
| Expectancy (eq 1) | Essential | Tells you if a strategy makes money per trade after costs. Negative → stop, no matter how good it looks |
| Sharpe / Sortino (eq 2–3) | Essential | Compares strategies fairly. Below buy-and-hold Nifty → just buy the index |
| Max drawdown (eq 4) | Essential | Decides if you can stick with it, and when to switch a strategy off |
| CAPM alpha/beta (eq 5) | Yes | Shows whether profit is skill (alpha) or just a leveraged bet on the market (beta) |
| Kelly / Merton (eq 6–7) | Yes, as a ceiling | Upper limit on bet size. Use ≤ ¼ of it |
| Fixed-fractional size (eq 8) | Essential | Turns "risk 1%" into an exact share count; the main thing that keeps accounts alive |
| Vol targeting (eq 9) | Yes | Equal risk per position; what professional trend-following funds use |
| ATR (eq 10) | Essential | Stops that adapt to how much a stock normally moves |
| Annualised vol / GARCH (eq 11–12) | Yes | Cut size when volatility spikes, before the big losses |
| Black–Scholes / expected move (eq 13–14) | Only for F&O | Read IV, compare IV with realised volatility, know your Greeks |
| OU + z-score (eq 15–16) | Yes | Pairs trading: a market-neutral edge that doesn't need a direction call |
| HMM regimes (eq 17) | Optional | Turn strategies on or off by market regime |
| Almgren–Chriss, Avellaneda–Stoikov (eq 18–19) | Not for retail | Need large orders, tick data and fast infrastructure |

## The workflow: from idea to live trading

### Step 1 — Start from a known source of edge

Edges with research behind them (see the research file above):
- **Momentum / trend:** stocks that rose over 6–12 months tend to keep rising. This and quality/low-vol
  factors have the strongest evidence in Indian equities.
- **Mean reversion between related stocks:** pairs trading (eq 15–16).
- **Volatility risk premium:** option IV is usually above the volatility that actually happens, so
  option sellers earn a premium on average. They also take rare, large losses, so it needs strict sizing.

Single-indicator rules (RSI/MACD crossovers) have weak evidence. My own backtests found the same.

### Step 2 — Backtest and apply pass/fail tests

Run the backtest **with real costs and slippage**, then check:

| Test | Equation | Pass if |
|---|---|---|
| Edge after costs | Expectancy | > 0 R per trade, over **at least ~100 trades** |
| Better than the index? | Sharpe vs Nifty buy-and-hold | Higher Sharpe, or low correlation to the index |
| Skill vs market | Alpha, beta | Alpha > 0; beta isn't doing all the work |
| Survivable | Max drawdown | A drawdown 1.5–2× the backtest's would still be bearable |
| Robust | Same stats | Positive on most symbols **and** on data the rules weren't tuned on (out-of-sample) |

If it fails any test, don't trade it. That decision alone saves most of the money retail traders lose.

### Step 3 — Size every trade

1. Choose risk per trade: **0.5–1%** of capital (eq 8).
2. Place the stop by volatility: e.g. 2 × ATR from entry (eq 10).
3. Quantity = (capital × risk%) ÷ (entry − stop).
4. Check against Kelly (eq 6): never risk more than ¼ of full Kelly.
5. Across a portfolio, scale each position so they carry similar volatility (eq 9), and cut size when
   GARCH/realised volatility jumps (eq 12).

### Step 4 — Manage the trade

- Exit at the stop or target, with no exceptions.
- Mean-reversion trades get a **time stop** of 2–3 OU half-lives (eq 16).
- Optional: only trade a trend strategy when an HMM says the market is trending (eq 17).

### Step 5 — Monitor live and switch off when broken

- Track rolling expectancy and Sharpe over the last 30–50 trades.
- **Kill switch:** stop trading the strategy if the live drawdown passes 1.5–2× the backtested
  maximum, or expectancy turns negative over a meaningful sample. Edges fade; this catches it.

## Why sizing matters more than the entry signal (simulation)

Setup from my best backtest: daily trendline Break, **51.5% win rate, 2R target**, with **0.1R cost**
per trade. 20,000 simulated paths of 200 trades each. The second and third blocks show what happens
if the true win rate is lower than the backtest says, which is common.

| True win rate (expectancy after cost) | Risk per trade | Median end (× start) | Chance of a ≥ 50% drawdown | Chance of losing 90% |
|---|---|---|---|---|
| 51.5% (+0.45R) | 1% | 2.4× | 0% | 0% |
| | 2% | 5.4× | 0% | 0% |
| | 6.8% (¼ Kelly) | 145× | 39% | 0% |
| | 27.3% (full Kelly) | huge | **100%** | 3% |
| 45% (+0.25R) | 1% | 1.6× | 0% | 0% |
| | 2% | 2.5× | 0.2% | 0% |
| | 6.8% | 10.9× | **79%** | 0.1% |
| | 27.3% | 0.19× | 100% | **47%** |
| 36% (−0.02R, no real edge) | 1% | 0.94× | 0.2% | 0% |
| | 2% | 0.85× | 25% | 0% |
| | 6.8% | 0.30× | 99.5% | 21% |
| | 27.3% | ~0× | 100% | **99%** |

What it shows:
- At 1–2% risk you survive every case, including the one where the edge turns out to be zero.
- Big sizing only looks good if the backtest's win rate is exactly right. If it's a few points lower,
  the same sizing turns a good strategy into a likely wipe-out.
- The large multipliers assume the edge stays constant for 200 trades with independent outcomes.
  Real edges decay and losses cluster, so real results are much lower. Read the table for the
  drawdown and ruin columns, not as a profit forecast.

## Applied to my backtests (`projects/trading experiments/`)

- **SuperTrend + DI:** expectancy turned negative after charges → fails Step 2. Don't trade it.
- **MACD + RSI + Stoch:** negative on 5m; the daily version with the "MACD crosses down" exit had
  profit factor ~1.5–1.7 after delivery costs → worth adding Sharpe, drawdown and an out-of-sample test.
- **Tori trendline Break (daily):** positive on 13/13 symbols but rarely beat buy-and-hold → Sharpe/alpha
  vs Nifty is the deciding test. If alpha ≈ 0, an index fund does the same job with less work.
- **Next experiments worth running:** a momentum portfolio with vol-targeted sizing, and a
  cointegrated pairs strategy with OU-based exits. These rely on edges with more evidence than
  indicator crossovers.
