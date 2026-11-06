# Strategies Built From the Equations

How the equations in `trading_equations.md` are used to actually make money: each strategy below
uses an equation as the **signal itself**, not just for measuring or sizing.
Education, not investment advice — every strategy here has losing periods, and none is guaranteed.

## Where the money comes from

Quant strategies earn money in one of two ways, and the equation is the tool that measures it:

1. **Getting paid for a risk others avoid** — e.g. option sellers are paid to insure against crashes.
2. **Exploiting a repeatable behaviour** — e.g. investors under-react to news, so trends persist
   (momentum); two related stocks drift apart and get pulled back (mean reversion).

## Strategy overview

| # | Strategy | Main equations | Instrument | Difficulty | Where profit comes from |
|---|---|---|---|---|---|
| 1 | Momentum portfolio with volatility targeting | Sharpe-style ranking, vol targeting (eq 9), annualised vol (eq 11) | Cash stocks, long only | Easy | Trends persist (momentum premium) |
| 2 | Volatility-managed index allocation | Merton fraction (eq 7), GARCH (eq 12) | Nifty index fund/ETF + liquid/debt fund | Easy | Avoiding high-volatility crash periods improves risk-adjusted return |
| 3 | Pairs trading | Spread z-score (eq 15), Ornstein–Uhlenbeck (eq 16) | Stock futures (to short overnight) | Medium | Related stocks' gap closes |
| 4 | Trend following on index futures | ATR (eq 10), vol targeting (eq 9) | Nifty / Bank Nifty futures | Medium | Big trending moves |
| 5 | Selling options when IV is too high | Black–Scholes (eq 13), expected move (eq 14), GARCH (eq 12) | Nifty options, defined-risk spreads | Hard / risky | Volatility risk premium (IV usually > realised vol) |
| + | Regime filter on any of the above | HMM (eq 17) | — | Medium | Fewer trades in bad conditions |

---

## 1. Momentum portfolio with volatility targeting (best starting point)

**Idea:** stocks that went up most over the last year tend to keep outperforming for a few months.
My research file (`../../projects/trading experiments/indian_market_strategies_research.md`) found
momentum to be the strongest factor in Indian equities (IIM Ahmedabad: ~21–22% a year, 1994–2014).

**Equations:**
- Momentum score (risk-adjusted): $\text{score} = \dfrac{R_{12\text{m}} - R_{1\text{m}}}{\sigma_{\text{annual}}}$ — 12-month return skipping the last month, divided by volatility (eq 11).
- Weight per stock (eq 9): $w_i = \dfrac{1/\sigma_i}{\sum_j 1/\sigma_j}$ — calmer stocks get more money.
- Portfolio-level vol target: if portfolio vol > target (e.g. 18%), hold part in cash: $\text{exposure} = \min(1,\ \sigma_{\text{target}}/\hat\sigma_{\text{portfolio}})$.

**Rules:**
1. Universe: Nifty 100 or Nifty 200 stocks.
2. On the first trading day of each month, compute the score for every stock.
3. Buy the top 15–20, weighted by 1/σ.
4. Next month: sell stocks that fell out of the top ~30 (a buffer cuts trading costs), buy new entrants.
5. Optional crash filter: if Nifty is below its 200-day average, cut exposure by half.

**Example:** stock A rose 45% with 30% vol → score 1.5; stock B rose 30% with 15% vol → score 2.0.
B ranks higher (more return per unit of risk) and gets twice A's weight.

**What goes wrong:** momentum crashes — sharp reversals after bear markets (e.g. a 2020-style rebound
punishes it). Underperforms in choppy years. Taxes: frequent rebalancing makes gains short-term.

**Benchmark:** NSE has momentum indices (Nifty 200 Momentum 30) with index funds — if my version
can't beat that after costs, buy the fund.

## 2. Volatility-managed index allocation (Merton + GARCH)

**Idea:** high-volatility periods tend to come with poor risk-adjusted returns, so holding less equity
when volatility is high and more when it's calm improves Sharpe ("volatility-managed portfolios",
Moreira & Muir, *Journal of Finance* 2017).

**Equations:**
- Merton fraction (eq 7): $\pi_t = \dfrac{\mu - r}{\gamma\,\hat\sigma_t^{2}}$, with $\hat\sigma_t$ from a GARCH(1,1) forecast (eq 12), capped at 100%.

**Rules:**
1. Every week/month, forecast Nifty volatility with GARCH on daily returns.
2. Set equity share = π_t (e.g. μ − r = 5.5%, γ = 3): σ = 12% → 100% (capped); σ = 20% → 46%; σ = 30% → 20%.
3. Rest goes into a liquid/debt fund. Rebalance only when the target moves by > 10 points (saves cost).

**What goes wrong:** volatility spikes and rebounds fast (you de-risk near a bottom and miss the
bounce). μ is a guess — keep it conservative.

## 3. Pairs trading (Ornstein–Uhlenbeck)

**Idea:** two stocks driven by the same business (e.g. two private banks, two IT services firms, two
cement companies) drift apart temporarily and get pulled back together. Profit is the gap closing,
regardless of where the market goes.

**Equations:**
- Hedge ratio β from regressing ln A on ln B; spread $s_t = \ln A_t - \beta \ln B_t$ (eq 15).
- Cointegration test (Engle–Granger): proceed only if p < 0.05.
- Z-score $z_t = (s_t - \mu_s)/\sigma_s$ on a rolling window (eq 15).
- OU speed: regress $\Delta s_t = a + b\,s_{t-1}$, θ = −b, half-life = ln 2 / θ (eq 16). Keep pairs with half-life of ~5–30 days.

**Rules:**
1. z > +2 → short A, long β × B (sell the expensive one, buy the cheap one). z < −2 → the reverse.
2. Exit when z returns to ~0.
3. Stop if |z| > 3.5, or after 3 half-lives without converging (the relationship may have broken).
4. Re-test cointegration every month; drop pairs that fail.

**Example:** half-life 10 days, z hits −2.3 → buy A futures, sell B futures in the β ratio. Typical
win: a 2σ move of the spread; typical hold: 1–3 half-lives.

**India-specific constraint:** you can only short cash stocks intraday. Holding pairs overnight needs
**stock futures** (only F&O stocks, fixed lot sizes, margin) — so both legs must be F&O stocks, and lot
sizes make exact β ratios approximate.

**What goes wrong:** a real business change (merger, regulation, fraud) breaks the pair for good —
that's why the |z| and time stops exist.

## 4. Trend following on index futures (ATR + vol targeting)

**Idea:** markets sometimes trend for months. Trend followers lose small amounts often and make large
amounts occasionally; win rate is usually 35–45%.

**Equations:** ATR (eq 10) for stops; vol-targeted size (eq 9): contracts = (capital × risk%) ÷ (k × ATR × lot size).

**Rules (one simple version):**
1. Long when price closes above its 50-day high; short when it closes below its 50-day low (Donchian breakout).
2. Initial stop 2–3 ATR away; trail the stop at the 20-day low/high.
3. Size so a stop-out costs 0.5–1% of capital.

**What goes wrong:** long sideways periods produce many small losses in a row. Futures roll costs and
gaps add up. A single index trends less reliably than a diversified basket of markets.

## 5. Selling options when implied volatility is too high (hardest, riskiest)

**Idea:** option buyers overpay on average — implied volatility (IV, from Black–Scholes run backwards)
is usually above the volatility that actually happens. Sellers collect that difference, the
**volatility risk premium**.

**Equations:**
- Edge signal: $\text{VRP} = \sigma_{\text{IV}} - \hat\sigma_{\text{GARCH}}$ — trade only when IV is clearly above the GARCH forecast (eq 12–13).
- Strike placement with the expected move (eq 14): $\pm S \times \sigma_{\text{IV}} \sqrt{\text{days}/365}$ — sell strikes outside the 1σ range.
- Greeks from Black–Scholes to keep the position near delta-neutral.

**Rules (defined-risk version):**
1. Only trade when IV − GARCH forecast > ~3 vol points.
2. Iron condor: sell a call and a put just outside the expected move, buy further wings to cap the loss.
3. Take profit at ~50% of the premium collected; exit if the loss reaches ~2× the premium.
4. Risk per position ≤ 1–2% of capital (max loss of the condor, not the margin).

**Example:** Nifty 25,000, IV 14%, 30 days → expected move ±1,003. Sell ~26,000 call and ~24,000 put,
buy ~26,500 call and ~23,500 put. Profit if Nifty stays roughly between the short strikes.

**What goes wrong:** this strategy wins often and loses big — one crash can erase months of premium.
Never sell naked options. SEBI data shows 87–93% of F&O traders lose money; SEBI's 2024 rules
(fewer weekly expiries, larger lot sizes) also changed the economics. Paper-trade first.

## + Regime filter (HMM)

Fit a 2-state HMM (calm/volatile) to daily Nifty returns with `hmmlearn`. Run strategies 1, 4 and 5
only in the calm state, or halve size in the volatile state. Use only the **filtered** state
probability (data up to today), otherwise the backtest cheats.

---

## Suggested order to try (all as backtests first, under `projects/`)

1. **Momentum + vol targeting** — cash market, long only, monthly, least work, best evidence.
2. **Volatility-managed Nifty allocation** — a better version of buy-and-hold.
3. **Pairs trading** — a market-neutral edge; needs futures for real trading.
4. Trend following on futures.
5. Option selling — only after the others, and only with defined risk.

For every one: backtest with costs → pass the tests in `using_equations_to_trade.md` → paper trade →
small real size → scale up only if live results match the backtest.
