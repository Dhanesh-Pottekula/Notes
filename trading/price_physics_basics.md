# Price as a Moving Object — the Physics Basics of Trading

How speed, distance, velocity and acceleration map onto a stock price, how far ahead you can "predict" it, and why
that explains the backtest results (`backtest_results_summary.md`). Education, not investment advice.

## 1. Physics → price dictionary

| Physics | Price version | Formula | Indicator that measures it |
|---|---|---|---|
| Position *x* | Price *P* | — | the chart |
| Distance / displacement Δx | Price change, return | ΔP = Pₜ − Pₜ₋ₙ, r = ΔP / P | % change |
| Velocity *v* (direction + speed) | Trend / momentum = return per unit time | v ≈ (Pₜ − Pₜ₋ₙ) / (n · Pₜ₋ₙ) | ROC, slope of a moving average, 12-month momentum |
| Acceleration *a* | Change in momentum | a ≈ vₜ − vₜ₋₁ | MACD histogram (MACD = fast EMA − slow EMA ≈ velocity; histogram = its change) |
| Inertia (1st law) | Momentum effect: strong 12-month movers tend to keep going for a few months | — | momentum score (R₂₅₂ − R₂₁)/σ |
| Spring (Hooke, F = −kx) | Mean reversion: price pulled back to an average | OU: dx = θ(μ − x)dt + σdW | z-score, VWAP z, pairs spread |
| Vibration / shaking | Volatility (random noise around the path) | σ = st. dev. of returns | ATR, annualised vol, GARCH |
| Force | Buying − selling pressure, news | — | volume, relative volume |
| Mass | Liquidity — big, heavily traded stocks need more force to move | — | volume, market cap |
| Friction | Brokerage, taxes, slippage | ~0.05–0.1% intraday, ~0.28% delivery per round trip | cost model |
| Terrain / weather | Market regime (bull, bear, calm, turbulent) | — | 200-day average, HMM |

## 2. The prediction equation

Physics (no noise): x(t + Δt) = x + v·Δt + ½·a·Δt²  → you can predict the next second almost exactly.

Price (geometric Brownian motion — the model behind Merton and Black–Scholes):

    P(t + Δt) = P · (1 + μ·Δt + σ·√Δt · Z),   Z = a random number, usually between −2 and +2

- μ·Δt = the **velocity part** (drift) — predictable, but tiny.
- σ·√Δt·Z = the **shaking part** — size predictable, direction not.

Example: stock at ₹1000, daily volatility 2%. Tomorrow: ~68% chance between ₹980–1020, ~95% between ₹960–1040.
You can predict **how far** it may move much better than **which way** — that is why stops are set with ATR.

## 3. The key fact: velocity grows with time, noise grows with √time

Nifty roughly: μ ≈ 12% a year, σ ≈ 15% a year.

| Horizon | Drift (velocity part) | Noise (1σ) | Drift ÷ noise | Chance price is up (≈) |
|---|---|---|---|---|
| 1 day | 0.05% | 0.95% | 0.05 | 52% |
| 1 week | 0.23% | 2.1% | 0.11 | 54% |
| 1 month | 1.0% | 4.3% | 0.23 | 59% |
| 1 year | 12% | 15% | 0.8 | 79% |

(Chance ≈ Φ(drift ÷ noise), ignoring a small σ²/2 correction.)

- Over **minutes and days** the object is almost all shaking — the velocity is buried.
- Over **weeks and months** the velocity starts to show through the shaking.
- **Friction** (intraday ~0.05–0.1% a round trip) is as big as or bigger than a whole day's drift (0.05%).

## 4. How this explains the backtest results

- **Momentum rotation worked** = measuring 12-month velocity (inertia) and riding it for a month. Long horizon → signal beats noise.
- **Skipping the last month** (R₂₅₂ − R₂₁): over 1 month stocks behave like a spring (short-term reversal), so it is removed.
- **Weekly pullback worked** = velocity (uptrend via 50/200-week averages) + a small spring move (dip to the 20-week EMA) to enter cheaper.
- **Intraday failed** = tiny velocity, big shaking, and friction bigger than the velocity.
- **MACD (acceleration) was weak** = acceleration is a difference of a difference — it amplifies noise.
- **200-day filter worked** = checks the terrain: don't push a car uphill in mud.
- **GARCH helped little** = it predicts the shaking well, but profit comes from velocity, not from shaking.

## 5. One-line summary

Price = a little velocity + a lot of shaking. You can't predict the next second like a ball; you can only bet on velocity that
has had enough time to show through the noise, keep friction small, and size each bet by how much it shakes.
