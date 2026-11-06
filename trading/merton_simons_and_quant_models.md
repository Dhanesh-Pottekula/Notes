# Merton, Jim Simons, and Whether Quant Models Still Matter

Notes from researching "the Merton equation" and "Jim Simons' theory" (Oct 2026), and whether they
are still relevant to trading. The formulas themselves are in `trading_equations.md`.

## 1. "The Merton equation" — Robert C. Merton (Nobel 1997)

People usually mean one of these:

| Name | What it says | Formula |
|---|---|---|
| **Black–Scholes–Merton** | Price an option from a hedged stock + cash mix; the price depends on volatility, not on expected direction | $C = S\,N(d_1) - K e^{-rT} N(d_2)$ (see equation 13) |
| **Merton portfolio problem** | How much of your wealth to keep in stocks | $\pi^* = (\mu - r)/(\gamma\sigma^2)$; with γ = 1 it's continuous **Kelly** (equation 7) |
| Merton credit model | A company's equity is a call option on its assets, with the debt as strike → estimates default risk | — |
| Merton jump-diffusion | Black–Scholes plus sudden price jumps | — |

**Still relevant?**
- **Black–Scholes: yes, as the market's common language, not as truth.** Every option chain (NSE included) shows implied volatility and Greeks computed from it. Traders run it backwards to turn prices into IV and compare options by that. Its constant-volatility assumption is wrong: real markets show a **volatility smile/skew** — a study of Nifty options found a U-shaped smile. Desks extend it with Heston (stochastic volatility), jump-diffusion and local volatility.
- **Merton/Kelly sizing: very relevant.** Professional trend-following funds use **volatility targeting**, which a 2026 paper describes as fractional Kelly. Practitioners use **¼–½ of Kelly** because edge estimates are noisy and over-betting is far more costly than under-betting.

## 2. "Jim Simons' theory" — Renaissance Technologies / Medallion fund

- **There is no published Simons equation.** Viral "Simons equation" posts often show the **Chern–Simons** form, which is geometry/physics, not markets.
- **What's publicly known** (mostly from Zuckerman's *The Man Who Solved the Market*; Renaissance has never disclosed its methods):
  - First recruit **Leonard Baum** co-created the **Baum–Welch algorithm** for hidden Markov models (estimating hidden states from observed data).
  - **Peter Brown and Robert Mercer** joined in 1993 from IBM's HMM-based speech-recognition team.
  - Strategies are described as statistical arbitrage, pattern recognition and high-frequency trading; no primary source confirms the exact models used today.
- **The idea in one line:** small statistical edge × huge number of independent bets × careful sizing.
  Expected profit ≈ N × (p·avg win − (1−p)·avg loss); with p only slightly above 50% but N in the
  millions, results become very reliable.
- **What an individual can use:** HMM **regime detection** (trending vs choppy, calm vs volatile) as a
  filter on existing strategies (equation 17). The real edge — data, infrastructure, execution — isn't copyable.

## 3. Other models worth knowing (and how relevant)

| Area | Model | Relevance for a retail NSE trader |
|---|---|---|
| Performance | Sharpe, Sortino, max drawdown | Essential — put in every backtest |
| Performance | CAPM (Sharpe/Lintner), Fama–French 3-factor | Useful — separates skill (alpha) from market exposure (beta). Fama & French (2004) say CAPM's empirical record is poor, but it's still widely used |
| Sizing | Kelly / fractional Kelly / vol targeting | Essential |
| Volatility | GARCH(1,1) | Useful for forecasting volatility from returns |
| Volatility | Heston stochastic volatility | Standard for fitting option prices and the smile; only needed for options work |
| Mean reversion | Ornstein–Uhlenbeck + cointegration (Avellaneda & Lee 2010 stat-arb) | Useful — opens up pairs trading, a different edge from indicators |
| Execution | Almgren–Chriss | Know it exists — needs large orders |
| Market making | Avellaneda–Stoikov | Know it exists — needs tick data and fast infrastructure |

## 4. Applied to my own backtests (`projects/trading experiments/`)

Best Tori trendline result: daily, Break setup, **51.5% win rate, 2R target**.
- Expectancy = 0.515 × 2 − 0.485 = 0.545R per trade before costs.
- Full Kelly = 0.515 − 0.485/2 ≈ **27% of capital at risk per trade** — far too aggressive because the
  win rate is an estimate and costs/slippage lower it. Quarter Kelly (~7%) is still above the usual 1–2%.
- Lesson: costs, slippage and honest edge estimates decide the outcome — the same thing the backtests showed.

## 5. Where my books cover this (`books/ML/`)

The library covers the statistics side, not the finance formulas:
- HMMs (the Simons angle): Bishop *PRML* ch.13 pdf p625 · Murphy *ML: A Probabilistic Perspective* ch.17 pdf p620 · AIMA ch.14 pdf p474
- Kalman filters / state-space (dynamic hedge ratios for pairs): Murphy *Probabilistic Perspective* ch.18 pdf p662
- Grimes *Art and Science of Trading* (course workbook) (`books/trading/`): ch.11 quant tools pdf p412, ch.16 quantitative evidence pdf p546

**Gap:** nothing on Black–Scholes, GARCH or OU. Good additions: Hull, *Options, Futures and Other
Derivatives*; Ernest Chan, *Algorithmic Trading* (mean reversion, Kelly, practitioner-focused).

## Sources

- [FinCAD: Pushing the Limits of Local Volatility](https://fincad.com/resources/resource-library/article/pushing-limits-local-volatility-option-pricing)
- [CMC Markets: Black-Scholes Model Explained](https://www.cmcmarkets.com/en-gb/options-trading/what-is-the-black-scholes-model)
- [Strike Money: Black-Scholes Assumptions and Limitations](https://www.strike.money/options/black-scholes-model)
- [Stylized patterns of implied volatility in India: NSE Nifty options](https://www.doi.org/10.1108/JIBR-12-2013-0103)
- [arXiv: The Science and Practice of Trend-Following Systems](https://arxiv.org/pdf/2607.19497)
- [LuxAlgo: Kelly Criterion](https://www.luxalgo.com/library/concept/kelly-criterion.md)
- [BSIC: Kelly's Criterion in Portfolio Optimization](https://bsic.it/exploring-the-application-of-kellys-criterion-in-portfolio-optimization/)
- [Wikipedia: Renaissance Technologies](https://en.wikipedia.org/wiki/Renaissance_Technologies)
- [PWL Capital: Medallion Fund, an exception to the indexing rule](https://pwlcapital.com/renaissance-technologies-medallion-fund-an-exception-to-the-indexing-rule/)
- [Novel Investor: notes on *The Man Who Solved the Market*](https://novelinvestor.com/notes/the-man-who-solved-the-market-by-gregory-zuckerman/)
- [Fama & French (2004): The Capital Asset Pricing Model](https://floridapsc.com/library/filings/2023/00092-2023/Support/Staff%20Exhibit%20167/Witness%20Testimony%20Workpapers/Witness%20Nelson/32_Fama%20&%20French,%20Capital%20Asset%20Pricing%20Model,%20Summer%202004.pdf)
- [arXiv: Statistical Arbitrage for Multiple Co-Integrated Stocks](https://arxiv.org/pdf/1908.02164)
- [arXiv: An Application of the Ornstein–Uhlenbeck Process to Pairs Trading](https://arxiv.org/html/2412.12458v1)
- [Massey: On Practitioners' Closed-Form GARCH Option Pricing](https://mro.massey.ac.nz/handle/10179/69759)
- [arXiv: Optimal Execution and Macroscopic Market Making](https://arxiv.org/pdf/2504.06717)
- [Guéant: The Financial Mathematics of Market Liquidity](https://hal.archives-ouvertes.fr/hal-01393136)
