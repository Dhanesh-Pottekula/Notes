# Backtest Results — Which Equation Strategies Actually Work (Oct 2026)

Summary of the full test in `../../projects/trading-equation-backtests/reports/REPORT.md` (all tables, method, limits).
NSE data from TradingView up to 26 Oct 2026, ₹10L per test, real FYERS charges + 0.02% slippage per side,
parameters chosen on earlier data and judged on later data. Education, not investment advice.

## What worked

| Strategy | Style | 2022–26 result (after costs) | Why I trust it (and the catch) |
|---|---|---|---|
| **Momentum rotation** — monthly, top 20 Nifty 200 stocks by (12m − 1m return) ÷ volatility, 1/σ weights, half exposure when Nifty < 200-DMA | Positional (delivery) | 27%/yr, Sharpe ~1.15, max DD 15% (2015–21 also 27%) | Beat equal-weight hold of the same stocks and all 20 random portfolios. **Catch:** survivorship bias — since Oct 2020 the backtest made 35%/yr vs 14.6%/yr for the real Nifty 200 Momentum 30 index. |
| **Weekly pullback** — weekly uptrend (close > 50-wk > 200-wk avg), dip to 20-week EMA, buy when the week closes above last week's high; 2.5 ATR stop, 2R target | Swing (delivery) | 18.5–26%/yr, Sharpe 1.12–1.28, max DD 11–16%, ~61% win rate | All 8 parameter settings profitable out-of-sample; beat all 20 random-entry runs; costs only ~2% of profit. |
| Weekly MACD, weekly trendline break | Swing (delivery) | 12–16%/yr, Sharpe ~0.6–0.7 | Decent but below an equal-weight hold of the same stocks (18.9%). |

## What didn't

- **Daily swing:** breakout 13–18%/yr but no better than just holding the same stocks; daily pullback ≈ cash; daily MACD negative.
- **1-hour (2023–26):** great in the 2023–24 rally, flat/negative in 2025–26; **intraday mode lost**, delivery ≈ cash.
- **Intraday 15-min / 5-min:** on Nifty 50 only **opening range breakout (long + short, high relative volume)** made money
  (+₹70k on ₹10L in 11 months on 15-min), but the **re-check on all Nifty 200 stocks killed the 15-min version**: all 43
  settings lost (none profitable in both halves), the same setting lost ₹1.46L. The **5-min** version (long + short, RVOL ≥ 2) held up on Nifty 200
  (17 of 20 settings profitable, +₹48k in 3.5 months, still +₹16k at 0.05% slippage) — a lead to paper trade, not proven:
  only 3.5 months / ~170 trades, and 15-min and 5-min disagree over the same weeks. Long-only ORB lost everywhere.
  VWAP pullback / VWAP reversion lost in every version.
- **Intraday signals held as delivery:** lost heavily — delivery costs (~0.28%/trade) are bigger than intraday-sized moves.
- **Intraday momentum on Nifty futures:** tiny real edge, eaten by ~₹480 charges + slippage per ₹10L trade.
- **MACD crossover (my rules: buy on cross up / confirmed above zero, sell on cross down, short below zero):** tested on 1-min to
  weekly, intraday and delivery, 8 variants each, Nifty 50 + Nifty 200 — **not worth trading anywhere.** Fast timeframes lose to
  costs (delivery mode lost 60–85%); the 15-min Nifty 200 intraday win (+₹1.47L) lost in all 8 settings on Nifty 50; weekly made
  11–16%/yr but below just holding the stocks (14–19%), and random buy weeks with the same sell rule did as well.
  Full report: `../../projects/trading-equation-backtests/reports/MACD_REPORT.md`.
- **VWAP course (MindMath Money video) — reversal at band 2, mean reversion, trend pullback:** 1-min to daily, intraday and delivery,
  Nifty 50 + Nifty 200 — **not worth trading.** Each confluence the course adds (candle pattern, horizontal level) makes it less
  bad, but every setup's median Sharpe stays negative; win rates 28–47% vs 41–60% needed intraday.
- **Currency Pros checklist + volume-profile POC (video):** the full checklist (sweep + higher-TF premium/discount) beat the core
  setup; the POC filter added little. **Lead:** 15-min intraday, full checklist, limit at the 75% retracement — +₹1.35L on Nifty 200
  in 11 months, but mostly in Jun–Oct 2026 (only 2 of 7 settings positive in both halves) and roughly flat on Nifty 50 → paper trade
  only. Daily version: 4–11%/yr on Nifty 200, below
  holding the stocks. Full report: `../../projects/trading-equation-backtests/reports/VWAP_REPORT.md`; how it works:
  `vwap_volume_profile_explained.md`.
- **Stochastic RSI + MACD (my rules: trend + %K crosses %D + MACD histogram rising):** 15m/30m/1h/4h, buy and sell separately,
  intraday and delivery, Nifty 50 + Nifty 200 — **not worth trading.** Buys lost everywhere (4-hour buys made money in 2023–24, lost in
  2025–26); delivery on fast charts loses to charges. One small lead: 15-min intraday SELL with a trailing stop (+₹45k / +₹60k on ₹10L,
  both lists, both halves) — falling-market sample only, paper trade. Full report:
  `../../projects/trading-equation-backtests/reports/STOCH_MACD_REPORT.md`; rules: `stoch_rsi_macd_strategy.md`.
  **Re-test with my final rules** (no EMA, MACD histogram as trend, buy not overbought / sell not oversold, steep Stoch cross):
  Nifty 50 lost on every timeframe/side/mode except 2 of 168 versions; steep cross helped (esp. delivery sells); least bad = 30-min
  steep-cross futures short (Nifty 200 +₹1.1L, Nifty 50 flat). Report: `.../reports/STOCH_MACD_USER_REPORT.md`.
- **Pairs trading:** lost even before costs. **Vol-managed Nifty (Merton + GARCH):** smaller drawdowns, less return than holding.

## Which equations mattered

- **200-day market filter:** the one consistent winner (+0.26 Sharpe, −8 points drawdown out-of-sample on average).
- **Fixed 1% risk sizing + ATR stops:** as good as or better than volatility targeting.
- **GARCH size cut, HMM regime filter, volatility targeting:** no consistent improvement.
- **Daily-trend filter on 1-hour trades:** helped out-of-sample.
- **Break-even win rate p\* = (L + c)/(W + L):** every losing run had a win rate below its p\*; winners cleared it by up to 28 points.

## Intraday vs delivery — verdict

Delivery on **weekly/monthly signals** is where the edge is. No intraday strategy passed: 15-min ORB failed on Nifty 200, and
5-min ORB long + short is only a lead on 3.5 months of data. Intraday signals held as delivery are the worst of both.

## Next

1. Paper trade momentum rotation + weekly pullback for 3–6 months; compare with the Nifty 200 Momentum 30 index.
2. Get historical Nifty 200 membership to remove survivorship bias, then re-test those two.
3. Keep the 200-DMA filter on every long strategy.
4. Intraday: only paper trade 5-min ORB long + short; re-test with 12+ months of 5-min data.
