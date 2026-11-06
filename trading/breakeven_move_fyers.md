# How Far Must a ₹4,000 Stock Move Before I Make Money? (FYERS charges + slippage)

Computed Oct 2026 with the same FYERS cost model the backtests use
(`../../projects/trading-equation-backtests/src/costs.py`). Verify current rates on the FYERS brokerage calculator.
Education, not investment advice.

## 1. FYERS charges (NSE cash equity, as modelled)

| Charge | Intraday | Delivery |
|---|---|---|
| Brokerage | ₹20 or 0.03% per order, whichever is lower | ₹20 or 0.3% per order, whichever is lower |
| STT | 0.025% on the sell side | 0.1% on buy **and** sell |
| Stamp duty | 0.003% on the buy | 0.015% on the buy |
| NSE transaction fee | ~0.0031% of buy + sell | same |
| SEBI fee | 0.0001% of buy + sell | same |
| GST | 18% of (brokerage + exchange + SEBI fees) | same |
| DP charge | none | ₹14.75 per stock on the sell day |
| **Slippage** (not a fee: the price you get is worse than the price you saw) | 0.02% per side used in backtests; 0.05% for less liquid stocks | same |

## 2. Break-even move for a ₹4,000 stock (bought at ₹4,000)

**Intraday** (slippage 0.02% per side → 0.05% in brackets)

| Shares | Trade value | Break-even sell price | Move needed |
|---|---|---|---|
| 1–10 | up to ₹40k | ₹4,005.9 (₹4,008.3) | **₹5.9 = 0.15%** (₹8.3 = 0.21%) |
| 25 | ₹1L | ₹4,004.9 (₹4,007.3) | ₹4.9 = 0.12% (0.18%) |
| 100 | ₹4L | ₹4,003.5 (₹4,005.9) | ₹3.5 = 0.09% (0.15%) |
| 250 | ₹10L | ₹4,003.2 (₹4,005.6) | ₹3.2 = 0.08% (0.14%) |

**Delivery** (slippage 0.02% per side → 0.05% in brackets)

| Shares | Trade value | Break-even sell price | Move needed |
|---|---|---|---|
| 1 | ₹4k | ₹4,053.8 (₹4,056.3) | **₹54 = 1.35%** (DP ₹14.75 + brokerage hurt small trades) |
| 10 | ₹40k | ₹4,016.7 (₹4,019.1) | ₹16.7 = 0.42% (0.48%) |
| 25 | ₹1L | ₹4,013.0 (₹4,015.4) | ₹13 = 0.33% (0.39%) |
| 100 | ₹4L | ₹4,011.1 (₹4,013.5) | ₹11.1 = 0.28% (0.34%) |
| 250 | ₹10L | ₹4,010.8 (₹4,013.2) | ₹10.8 = 0.27% (0.33%) |

A short (intraday) needs the same size move **down**.

## 3. What it means

- **Rule of thumb:** intraday ≈ **0.1–0.2%** (₹4–8 on ₹4,000); delivery ≈ **0.3–0.4%** (₹11–16) once the trade is ₹40k+.
  Below ~₹20k per trade, the flat ₹20 brokerage and ₹14.75 DP charge make delivery much more expensive in %.
- **Delivery costs more per trade because of STT** (0.1% on both sides vs 0.025% on the sell only), but delivery trades aim for
  2–10% moves, so 0.3% is small. Intraday aims for 0.3–1% moves, so 0.15% is a big share of the target.
- **Break-even is not profit.** It covers the costs only. Your average winner must beat this, and win rate × average win must beat
  loss rate × average loss + costs (break-even win rate p* = (avg loss + costs) / (avg win + avg loss), see `trader_returns_reality.md`).
- **Example:** intraday target ₹20 (0.5%), stop ₹10 on ₹4,000 → costs ₹6 per trade. Net win ₹14, net loss ₹16 → you need
  a win rate above 16 / (14 + 16) = **53%**, not 33%.
- **Tax** is extra: short-term delivery gains 20%; intraday profit is taxed at your slab rate.
