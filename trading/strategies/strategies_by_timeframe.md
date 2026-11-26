# Strategies by Timeframe: Scalping, Intraday, Delivery

Which strategies fit scalping, intraday and delivery (swing/positional) trading on NSE, the
equations behind each, and what the evidence and my own backtests say.
Related: `strategies_from_equations.md` (full rules for the 5 core strategies),
`using_equations_to_trade.md` (pass/fail tests and sizing), `trading_equations.md` (formulas).
Education, not investment advice.

## The deciding factor: costs vs. the size of the move

Round-trip costs from my Fyers cost model (`projects/trading experiments/supertrend_di_backtest.py`,
2026 charges), **before slippage**:

| Trade value | Intraday round trip | Delivery round trip |
|---|---|---|
| ₹50,000 | ₹53 (0.11%) | ₹173 (0.35%) |
| ₹1,00,000 | ₹83 (0.08%) | ₹284 (0.28%) |
| ₹5,00,000 | ₹225 (0.05%) | ₹1,174 (0.23%) |

Add slippage of roughly 0.02–0.03% per side for liquid large caps.

**Break-even win rate** once costs are included:

$$p^{*} = \frac{L + c}{W + L}$$

W = average win, L = average loss, c = round-trip cost + slippage, all in % of the trade.

| Style | Target W | Stop L | Cost c | Break-even win rate (no costs → with costs) |
|---|---|---|---|---|
| Scalp | 0.20% | 0.10% | 0.13% | 33% → **77%** |
| Intraday | 1.0% | 0.5% | 0.13% | 33% → **42%** |
| Swing (delivery) | 6% | 3% | 0.34% | 33% → **37%** |

Costs barely matter on a 6% swing move but are most of a 0.2% scalp. This is the main reason SEBI
found **70%+ of intraday cash traders lost money in FY23**, and **80%** of those making 500+ trades a
year lost (`projects/trading experiments/indian_market_strategies_research.md`).

---

## 1. Scalping (seconds to ~5 minutes)

**Verdict: not recommended for a retail trader in Indian cash equities.**

- Needs a ~75%+ win rate just to break even at 2:1 reward-to-risk (table above).
- Professional scalping is really **market making** (Avellaneda–Stoikov, eq 19) and order-flow
  trading, with exchange co-location, fee rebates and millisecond execution. Retail can't compete there.
- My own tests: MACD+RSI+Stoch **lost on 5m with every exit**; SuperTrend+DI "best" cells didn't
  survive 0.02–0.03% slippage.

If scalping anyway (index options/futures), the equations that matter:
- Break-even win rate (above) — compute it before every strategy.
- Order-book imbalance: $\text{OBI} = \dfrac{Q_{\text{bid}} - Q_{\text{ask}}}{Q_{\text{bid}} + Q_{\text{ask}}}$ (top-of-book quantities; > 0 means buying pressure).
- Hard daily loss limit (e.g. stop for the day at −1% of capital).

## 2. Intraday (minutes to hours, squared off by the close)

**Verdict: possible, but only with few trades a day, liquid stocks, and strict loss limits.**
Test every idea with costs + slippage first. Evidence for these is mostly gross of costs.

### a) Opening range breakout (ORB) on "stocks in play"

- **Equations:** relative volume $\text{RVOL} = \dfrac{\text{volume in first 15 min today}}{\text{avg volume in first 15 min, last 20 days}}$; ATR (eq 10) for stops; fixed-fractional size (eq 8).
- **Rules:** opening range = high/low of 09:15–09:30. Trade only stocks with RVOL > 2 (news, results).
  Buy a break above the range high (short below the low), stop at the other side of the range or
  0.1 × daily ATR, exit at the close or a 2R target. Max one trade per stock per day.
- **Evidence:** Zarattini & Aziz reported +0.13R per trade on QQQ, but **gross** of spread/slippage; an
  independent replication on five indices found the edge **reproduced gross but net ≈ zero**.
  Restricting to stocks in play is what the stronger results rely on.
- **Book:** Grimes *Art and Science of Trading* (course workbook) ch.15 "The Opening Range Phenomenon" (`books/trading/`, pdf p533).
- **Mine:** NY ORB gold strategy (`ny_orb_v1_backup.pine`) exists but has no written report yet.

### b) Intraday momentum (first half-hour → last half-hour)

- **Equation:** $r_{\text{first}} = \dfrac{P_{09:45}}{P_{\text{prev close}}} - 1$ predicts $r_{\text{last}}$ (15:00 → 15:30).
- **Rules:** at 15:00, go long Nifty futures if $r_{\text{first}} > 0$, short if < 0; exit at 15:25.
  Optionally only on high-volatility or high-volume days, where the effect was stronger.
- **Evidence:** Gao, Han, Li & Zhou (*Journal of Financial Economics* 2018) on the S&P 500 ETF, 1993–2013;
  international results are mixed and I found **no Nifty-specific study** → must be backtested here.
- **Why it's attractive:** one trade a day, so costs stay small.

### c) VWAP mean reversion (range days only)

- **Equations:** $\text{VWAP} = \dfrac{\sum P_i V_i}{\sum V_i}$; stretch $z = \dfrac{P - \text{VWAP}}{\sigma_{\text{intraday}}}$.
- **Rules:** on days without a strong trend (e.g. first-hour range below average), fade moves with
  |z| > 2 back toward VWAP; stop at |z| > 3; no new trades after 14:30.
- **Evidence:** I found **no rigorous after-cost study** — only indicator scripts. Treat as untested.

### d) Intraday pairs

Cash-market shorting is allowed intraday, so pairs (eq 15–16) can run without futures. But Indian
research found pairs profitable in **stock futures, not in the cash market**, because of costs.
Only worth testing with a slow-moving, wide spread.

### Intraday risk rules (all strategies)

- Risk 0.25–0.5% of capital per trade; **stop for the day at −1% to −2%**.
- At most 2–3 trades a day; only liquid large caps or index futures.
- Check the break-even win rate for each strategy's actual W, L and costs.

## 3. Delivery: swing and positional (days to months)

**Verdict: the best fit for a retail trader.** Moves are big relative to costs, trades are few, and
the strongest evidence in Indian equities is here. My own backtests also did best on daily charts.

| Strategy | Holding period | Main equations | Notes |
|---|---|---|---|
| **Momentum portfolio + vol targeting** | ~1–3 months per stock, monthly rebalance | risk-adjusted momentum score, 1/σ weights (eq 9, 11) | Strongest evidence (IIM-A: ~21–22%/yr, 1994–2014). Full rules in `strategies_from_equations.md` #1 |
| **Quality / low-volatility factors** | months | factor scores, σ (eq 11), beta (eq 5) | Strong evidence; smoother than momentum; blend with it |
| **Volatility-managed Nifty** | ongoing | Merton fraction + GARCH (eq 7, 12) | A better buy-and-hold. Rules in #2 |
| **Swing trend breakout (daily)** | days–weeks | ATR stop (eq 10), position size (eq 8), expectancy (eq 1) | e.g. my Tori daily Break: 51.5% win, 2R, profitable on 13/13 symbols, but rarely beat buy-and-hold → check alpha (eq 5) |
| **Daily MACD with "MACD crosses down" exit** | days–weeks | expectancy, Sharpe, drawdown | My Reliance test: PF ~1.5–1.7 after delivery costs on daily — needs out-of-sample and multi-stock test |
| **Pairs trading via stock futures** | days–weeks | z-score, OU half-life (eq 15–16) | Indian study: profitable in futures 2011–2017 after costs, not in cash |

**Delivery rules of thumb:** risk 0.5–1% per position with an ATR-based stop; hold 10–20 positions;
size by volatility; rebalance on a schedule, not on feelings; always compare with a Nifty index fund.

---

## Summary

| Style | Use it? | Best strategies | Why |
|---|---|---|---|
| Scalping | **No** (for retail cash) | — (market making needs infrastructure) | Costs require ~75%+ win rate; my 5m tests lost |
| Intraday | **Maybe**, few trades a day | ORB on stocks in play, intraday momentum on Nifty futures | Edges are thin and mostly gross of costs; must backtest net |
| Delivery / swing | **Yes** | Momentum + vol targeting, quality/low-vol, vol-managed Nifty, daily trend breakouts | Big moves vs costs; strongest evidence; my best results |

**Tax note (check current rules before relying on it):** intraday equity profits are taxed as
speculative business income at slab rates; delivery gains are capital gains (short-term under 1 year,
long-term above, at lower rates). This also favours longer holding.

## Sources

- My cost model and findings: `projects/trading experiments/` (`supertrend_di_backtest.py`, `AGENTS.md`, `indian_market_strategies_research.md`)
- [Gao, Han, Li & Zhou — Intraday Momentum: The First Half-Hour Return Predicts the Last Half-Hour Return (PDF)](https://c.mql5.com/forextsd/forum/173/intraday_momentum_-_the_first_half-hour_return_predicts_the_last_half-hour_return.pdf)
- [Alpha Architect summary of the intraday momentum paper](https://alphaarchitect.com/attention-prop-traders-the-first-half-hour-of-trading-predicts-the-last-half-hour/)
- [Market Intraday Momentum (Washington University profile)](https://profiles.wustl.edu/en/publications/market-intraday-momentum/)
- [International intraday momentum evidence (PDF)](https://dspace5old.zcu.cz/bitstream/11025/46501/1/EM_4_2021_08.pdf)
- [Intraday momentum, S&P 500 and CSI 300](https://dspace.tul.cz/handle/15240/161029)
- [ORB paper replicated on five indices: gross reproduced, net zero (MQL5 blog)](https://www.mql5.com/en/blogs/post/776235)
- [QuantConnect: Opening range breakout for stocks in play](https://www.quantconnect.com/research/18444/opening-range-breakout-for-stocks-in-play/)
- [Holmberg, Lönnbark & Lundström — ORB working paper (Umeå)](https://swopec.hhs.se/umnees/abs/umnees0845.htm)
- [LuxAlgo: Opening Range & ORB](https://www.luxalgo.com/library/concept/opening-range-and-orb.md)
