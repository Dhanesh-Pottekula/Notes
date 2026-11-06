# My MACD + Stochastic RSI Rules — ADANIPORTS and Nifty 50 Backtest (Oct 2026)

Five timeframes, intraday and delivery, buy and sell tested separately, **FYERS charges only (no slippage)**, ₹1,00,000 per
trade. Education, not investment advice. Reports with every trade (entry/exit time and price, qty, each FYERS charge,
MACD/signal/histogram and %K/%D values):
- ADANIPORTS: `../../projects/trading-equation-backtests/reports/ADANIPORTS_STOCH_MACD_REPORT.md` (`reports/adaniports/trades_all.csv`)
- Nifty 50: `../../projects/trading-equation-backtests/reports/STOCH_MACD_ABOVE0_N50_REPORT.md` (`reports/stochmacd_above0_n50/trades_all.csv`)

## 1. The rules

**Buy.** All of these must be true on the same candle:
1. MACD line above 0 **and** signal line above 0
2. The gap is widening: histogram (MACD − signal) is positive and bigger than on the previous candle
3. Stoch RSI blue line (%K) crosses above the orange line (%D) on this candle, with blue below 50

→ **Buy at that candle's close**, as soon as the cross is confirmed.
**Exit** at the close of the first later candle where blue touches orange (blue ≤ orange). No stop-loss.

**Sell (short)** is the mirror: both MACD lines below 0, the gap widening downward, blue crosses below orange with blue above 50 →
short at that close, and cover at the close of the candle where blue touches orange again.

Settings MACD 12/26/9, Stoch RSI 3/3/14/14. Intraday trades are squared off at the close of the last candle starting before
15:15. Delivery buys pay cash-delivery charges; overnight shorts pay stock-futures charges. Same-day round trips pay intraday charges.

**Costs (FYERS, ₹1L in and ₹1L out):** intraday ≈ ₹83 (0.08%) · delivery buy ≈ ₹284 (0.28%, of which STT is ₹200) ·
futures short ≈ ₹104 (0.10%). Full rate list: brokerage ₹20 or 0.03% (intraday/futures) / 0.3% (delivery) per order,
whichever is lower; STT 0.025% sell (intraday), 0.1% both sides (delivery), 0.05% sell (futures); NSE 0.0030699% (equity) /
0.0018299% (futures); SEBI ₹10/crore; IPFT ₹0.01/crore; stamp 0.003% / 0.015% / 0.002% on buy; GST 18%; DP ₹14.75 per delivery
sell. Not included: income tax, FYERS' ₹59 auto square-off fee, and real futures lot sizes.

## 2. ADANIPORTS (net P&L after FYERS charges)

| Timeframe | Data | Intraday buy | Intraday sell | Delivery buy | Delivery sell |
|---|---|---|---|---|---|
| 15-min | Dec 2025 – Oct 2026 | 14 trades, −₹1,747 | 11, −₹628 | 16, −₹2,535 | 11, −₹628 |
| 30-min | Dec 2025 – Oct 2026 | 8, −₹1,438 | 6, **+₹2,412** | 8, −₹1,999 | 7, **+₹3,206** |
| 1-hour | Jan 2023 – Oct 2026 | 24, −₹5,370 | 9, −₹1,111 | 28, −₹4,281 | 12, **+₹6,323** |
| 4-hour | Jan 2023 – Oct 2026 | 1, −₹214 | 3, −₹1,007 | 3, **+₹639** | 8, −₹3,922 |
| Daily | Apr 2009 – Oct 2026 | — | — | 26, −₹35,859 | 18, **+₹9,597** |

Too few trades on one stock (1–28 per version) to separate an edge from luck. That's why the rules were also run on all of Nifty 50.

## 3. Nifty 50 (all 50 stocks added together)

| Timeframe | Intraday buy | Intraday sell | Delivery buy | Delivery sell |
|---|---|---|---|---|
| 15-min | 813 trades, −₹80k | 889, −₹66k | 857, −₹1.17L | 982, −₹95k |
| 30-min | 361, −₹33k | 441, −₹7.8k | 395, −₹61k | 488, −₹19k |
| 1-hour | 987, −₹46k | 797, −₹66k | 1,181, −₹1.42L | 983, −₹85k |
| 4-hour | 205, −₹28k | 181, −₹25k | 333, −₹5.5k | 297, −₹41k |
| Daily | — | — | 874, −₹21k | 615, −₹2.18L |

- **All 18 versions lose money,** even with FYERS charges only and no slippage. Win rates are 29–41%.
- **There's almost no edge before costs.** The average move per trade ranges from −0.25% to +0.26%, against FYERS charges of 0.08–0.28%.
  The two closest are **daily delivery buys** (+0.26% move vs 0.285% cost, −₹21k; the second half since 2018 made +₹25k) and
  **4-hour delivery buys** (+0.26% vs 0.28%, −₹5.5k; first half +₹17k, second half −₹23k). Neither is consistent.
- **The ADANIPORTS sell profits were luck.** Daily sells made +₹9.6k on ADANIPORTS but −₹2.18L across Nifty 50, and 1-hour delivery
  sells made +₹6.3k vs −₹85k.
- **Why trades are rare:** on Nifty 50 1-hour, 323,701 candles → 157,330 with both MACD lines above 0 → 34,421 also with a widening gap
  → 5,578 also with a blue-over-orange cross → 1,181 also with blue below 50.
- **Why trades are short (about 3–4 candles):** orange (%D) is only a 3-candle average of blue (%K), so blue touches it again almost immediately.

## 4. Lesson

The entry finds moments of strong momentum where the Stoch is still "cheap". The touch exit then leaves within 3–4 candles, before
the move can pay for the charges. Don't trade these rules as they are. If testing further, change the **exit**, not the entry:
hold until the MACD histogram turns, or use a swing stop plus 2R target. Delivery buys on daily or 4-hour are the only versions
worth a second look.
