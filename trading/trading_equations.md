# Trading Equations — Cheat Sheet

19 equations for measuring a strategy, sizing positions, reading volatility, pricing options,
trading mean reversion and spotting regimes, in the order to learn them. Each one has the formula,
what the symbols mean, a worked example with NSE-style numbers in ₹, and the usual mistake.

- **Interactive version** (same content + Kelly / position-size / Black–Scholes calculators):
  `trading_equations.html` in this folder (open in a browser; needs internet for the math font),
  or the published page <https://claude.ai/artifact/4Wp5pK3T9zt3yPuJPeJGCU>.
- Background on where these come from: `merton_simons_and_quant_models.md`.
- Worked examples use round assumed numbers, not live prices. Education, not investment advice.

**Priority tags:** 🟢 Learn first · 🔵 Useful next · 🟡 Know it exists

---

## A. Measure a strategy

Put these in every backtest report and compare against simply holding the Nifty.

### 1. Expectancy — average result per trade 🟢

$$E = p\,W - (1-p)\,L$$

| Symbol | Meaning |
|---|---|
| p | win rate |
| W, L | average win and average loss (in R or ₹) |

**Example:** win rate 51.5%, 2R target, 1R stop → E = 0.515 × 2 − 0.485 × 1 = **0.545R per trade**.
Risking ₹10,000 per trade ≈ ₹5,450 per trade *before* brokerage, STT and slippage.

**Watch out:** subtract costs per trade first. On short timeframes charges can exceed the whole edge.

### 2. Sharpe ratio — return per unit of volatility 🟢

$$S = \frac{\bar R_p - R_f}{\sigma_p} \qquad S_{\text{annual}} = S_{\text{daily}} \times \sqrt{252}$$

| Symbol | Meaning |
|---|---|
| R̄ₚ | average strategy return per period |
| R_f | risk-free return for the same period (e.g. T-bill rate ÷ 252 for daily) |
| σₚ | standard deviation of the strategy's returns |
| 252 | trading days a year (√52 weekly, √12 monthly) |

**Example:** daily mean 0.06%, daily std 1.2%, risk-free 6.5%/yr (0.0258%/day) →
(0.0006 − 0.000258) ÷ 0.012 × √252 ≈ **0.45**. Index-like; not worth it unless uncorrelated with the index.
Above ~1 annualised is good for a single strategy.

**Watch out:** treats upside and downside swings alike, and flatters option-selling until it blows up. Always read it with max drawdown.

### 3. Sortino ratio — Sharpe that only punishes losses 🔵

$$\text{Sortino} = \frac{\bar R_p - R_f}{\sigma_{\text{down}}}, \qquad \sigma_{\text{down}} = \sqrt{\tfrac{1}{n}\sum \min(R_t - R_f,\,0)^2}$$

**Watch out:** trend strategies with rare big winners look much better on Sortino. Check the trade count — a few lucky outliers can carry it.

### 4. Maximum drawdown — worst peak-to-trough fall 🟢

$$\text{MDD} = \max_t \frac{\text{Peak}_t - \text{Equity}_t}{\text{Peak}_t} \qquad \text{gain to recover} = \frac{1}{1-\text{MDD}} - 1$$

**Example:** ₹10L → ₹14L → ₹11.2L: MDD = (14 − 11.2) ÷ 14 = **20%**; recovering needs **+25%**. A 50% drawdown needs +100%.

**Watch out:** live drawdowns are usually worse than backtests — plan for 1.5–2× the backtested figure.

### 5. CAPM beta and alpha (+ Fama–French) — how much is just the market 🔵

$$\beta = \frac{\operatorname{Cov}(R_i, R_m)}{\operatorname{Var}(R_m)} \qquad \alpha = R_i - \big[R_f + \beta\,(R_m - R_f)\big]$$

$$R_i - R_f = \alpha + \beta_m (R_m - R_f) + \beta_s\,\text{SMB} + \beta_v\,\text{HML} + \varepsilon \quad\text{(Fama–French 3-factor)}$$

| Symbol | Meaning |
|---|---|
| R_m | market (Nifty 50) return |
| SMB | small-minus-big: small caps' return over large caps |
| HML | high-minus-low: value stocks' return over growth stocks |

**Example:** strategy 18%, Nifty 12%, risk-free 6.5%, beta 1.2 → fair return = 6.5 + 1.2 × 5.5 = 13.1%, so **α = 4.9%**. Only that part is skill.

**Watch out:** high-beta strategies beat the index in bull markets for free. Judge alpha, not raw return.

---

## B. Size positions

### 6. Kelly criterion — growth-optimal risk per trade 🟢

$$f^{*} = p - \frac{1-p}{b}$$

| Symbol | Meaning |
|---|---|
| p | win rate |
| b | reward-to-risk (average win ÷ average loss) |
| f* | fraction of capital to **risk** (lose if stopped), not position size |

**Example:** 51.5% win rate, 2R → f* = 0.515 − 0.485 ÷ 2 = **27.3%** at risk per trade.
Half Kelly 13.6%, quarter Kelly 6.8% — still far above the 1–2% most traders risk, because a backtested win rate is only an estimate.

**Watch out:** if the true win rate is a few points lower, full Kelly over-bets badly. Over-betting hurts much more than under-betting; practitioners use ¼–½ Kelly.

### 7. Merton fraction — how much of your money in stocks 🔵

$$\pi^{*} = \frac{\mu - r}{\gamma\,\sigma^{2}}$$

| Symbol | Meaning |
|---|---|
| μ − r | expected return above risk-free |
| σ | annual volatility |
| γ | risk aversion (1 = Kelly; 2–5 typical for real people) |

**Example:** Nifty μ = 12%, r = 6.5%, σ = 16% → γ = 1: 0.055 ÷ 0.0256 = **215%** (2.15× leverage — why full Kelly is too aggressive); γ = 4: **54%** equity, rest debt.

**Watch out:** very sensitive to μ, the number you know least.

### 8. Fixed-fractional position size — shares for a given stop 🟢

$$\text{Qty} = \frac{\text{Equity} \times \text{risk}\%}{\lvert\text{Entry} - \text{Stop}\rvert}$$

**Example:** ₹10,00,000 account, 1% risk (₹10,000), buy ₹1,450, stop ₹1,420 → 10,000 ÷ 30 = **333 shares** (≈ ₹4.83L of stock).

**Watch out:** gaps jump over stops; overnight and F&O positions can lose more than planned.

### 9. Volatility targeting — fractional Kelly the professional way 🔵

$$w = \frac{\sigma_{\text{target}}}{\hat\sigma_{\text{asset}}}$$

**Example:** target 15% vol per position; a 30%-vol stock gets **50%** weight, a 12%-vol stock 125% (cap at 100% without leverage).

---

## C. Volatility

### 10. Average True Range — volatility in rupees 🟢

$$TR_t = \max\big(H_t - L_t,\ \lvert H_t - C_{t-1}\rvert,\ \lvert L_t - C_{t-1}\rvert\big) \qquad ATR_t = \frac{(n-1)\,ATR_{t-1} + TR_t}{n}$$

H, L, C = high, low, close (yesterday's close captures gaps); n usually 14 (Wilder smoothing). Used inside SuperTrend.

**Example:** ATR(14) = ₹28 on a ₹1,450 stock → a 2-ATR stop is ₹56 below entry; with ₹10,000 risk that's **178 shares**.

### 11. Annualised volatility — square-root-of-time 🟢

$$\sigma_{\text{annual}} = \sigma_{\text{daily}}\sqrt{252} \qquad \text{typical 1-day move} \approx P \times \sigma_{\text{daily}}$$

**Example:** daily std 1.5% → **23.8%** a year; on a ₹1,450 stock a typical day is about **±₹22**.

**Watch out:** fat tails — "4-sigma" days happen several times a decade.

### 12. GARCH(1,1) — volatility forecasting 🔵

$$\sigma_t^{2} = \omega + \alpha\,\varepsilon_{t-1}^{2} + \beta\,\sigma_{t-1}^{2} \qquad \bar\sigma^{2} = \frac{\omega}{1-\alpha-\beta}$$

| Symbol | Meaning |
|---|---|
| ε₍t−1₎ | yesterday's surprise return |
| α | reaction to news (equity indices typically ≈ 0.05–0.10) |
| β | persistence (typically ≈ 0.85–0.93); α + β < 1 |
| σ̄² | long-run variance the forecast drifts back to |

**Watch out:** fit on returns, not prices. Python: the `arch` package.

---

## D. Options (only if you trade F&O)

### 13. Black–Scholes–Merton — option price and delta 🔵

$$C = S\,N(d_1) - K e^{-rT} N(d_2) \qquad P = K e^{-rT} N(-d_2) - S\,N(-d_1)$$

$$d_1 = \frac{\ln(S/K) + (r + \tfrac{1}{2}\sigma^{2})T}{\sigma\sqrt{T}} \qquad d_2 = d_1 - \sigma\sqrt{T} \qquad \Delta_C = N(d_1),\ \Delta_P = N(d_1) - 1$$

$$C - P = S - K e^{-rT} \quad\text{(put–call parity)}$$

| Symbol | Meaning |
|---|---|
| S, K | spot, strike |
| T | years to expiry (days ÷ 365) |
| r, σ | risk-free rate, annual volatility |
| N(·) | standard normal CDF |

Traders use it backwards: plug in the market price, solve for σ → that's the **implied volatility** on every option chain.

**Example:** Nifty 25,000, ATM strike, 30 days, r = 6.5%, σ = 14% → d₁ = 0.153, d₂ = 0.113,
**Call ≈ ₹469, Put ≈ ₹336**, call Δ 0.56, put Δ −0.44. Parity: 469 − 336 = 133 = 25,000 − 25,000·e^(−0.065×30/365). ✓

**Watch out:** the model assumes one volatility for all strikes, but Nifty has a skew (OTM puts trade at higher IV). One σ misprices the wings.

### 14. Expected move from implied volatility 🔵

$$\text{1σ move} \approx S \times \sigma_{\text{IV}} \times \sqrt{\tfrac{\text{days}}{365}}$$

**Example:** Nifty 25,000, IV 14%, 30 days → **±1,003 points** (~68% chance of ending between ~24,000 and ~26,000).

---

## E. Mean reversion and pairs

Trade the gap between two related stocks (e.g. HDFC Bank vs ICICI Bank) instead of predicting direction.

### 15. Spread and z-score 🔵

$$s_t = \ln A_t - \beta \ln B_t \qquad z_t = \frac{s_t - \mu_s}{\sigma_s}$$

β = hedge ratio from regressing ln A on ln B; μ_s, σ_s = rolling mean/std of the spread.

**Rule of thumb:** short the spread at z > +2, buy at z < −2, exit near 0. First check **cointegration** (Engle–Granger, p < 0.05) — moving together isn't enough.

### 16. Ornstein–Uhlenbeck — how fast the gap closes 🔵

$$dX_t = \theta(\mu - X_t)\,dt + \sigma\,dW_t \qquad \text{half-life} = \frac{\ln 2}{\theta}$$

Estimate θ by regressing Δsₜ = a + b·sₜ₋₁ → θ = −b.

**Example:** b = −0.07/day → half-life = ln 2 ÷ 0.07 ≈ **9.9 days**. Time-stop at 2–3 half-lives; if it hasn't closed, the relationship may have broken.

---

## F. Regimes (the Jim Simons angle)

### 17. Hidden Markov model — forward algorithm 🟡

$$\alpha_t(j) = \Big[\sum_i \alpha_{t-1}(i)\,a_{ij}\Big]\, b_j(o_t) \qquad P(\text{state}_t = j \mid o_{1..t}) = \frac{\alpha_t(j)}{\sum_k \alpha_t(k)}$$

a_ij = probability of moving from state i to j; b_j(o_t) = likelihood of today's return in state j.

**Use:** fit 2–3 states (calm/volatile, trending/choppy) to daily returns; only run your trend strategy in the trending state.

**Watch out:** use the *filtered* probability (data up to today), never the smoothed one — it peeks at the future. Python: `hmmlearn`.
Books: Bishop *PRML* ch.13 (pdf p625), Murphy *ML: A Probabilistic Perspective* ch.17 (pdf p620), AIMA ch.14 (pdf p474) — all in `../../books/ML/`.

---

## G. Institutional models (understand, rarely tradable for individuals)

### 18. Almgren–Chriss — optimal execution of a large order 🟡

$$\min\ \mathbb{E}[\text{cost}] + \lambda\,\operatorname{Var}[\text{cost}] \quad\Rightarrow\quad x_t = X\,\frac{\sinh\big(\kappa (T - t)\big)}{\sinh(\kappa T)}$$

x_t = shares still to sell; κ = urgency (rises with risk aversion λ and volatility, falls with impact cost).
Balances market impact (selling fast is expensive) against price risk (selling slowly leaves you exposed).

### 19. Avellaneda–Stoikov — market-maker quotes 🟡

$$r = s - q\,\gamma\,\sigma^{2}(T - t) \qquad \delta^{a} + \delta^{b} = \gamma\,\sigma^{2}(T - t) + \frac{2}{\gamma}\ln\Big(1 + \frac{\gamma}{k}\Big)$$

r = reservation price, s = mid, q = inventory, δᵃ + δᵇ = total spread, k = how fast fill probability drops away from mid.
The market maker shifts both quotes against its inventory to drift back to flat.

---

## What to learn first (for backtesting NSE strategies)

1. Sharpe, Sortino, max drawdown — add to every backtest; benchmark vs buying the Nifty.
2. Fractional Kelly / volatility-targeted sizing.
3. ATR / GARCH volatility for stops and sizing.
4. OU + cointegration → pairs trading (a different edge from indicators).
5. Black–Scholes + Greeks — only if moving into F&O.
