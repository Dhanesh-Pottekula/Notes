# Strategy 2 on Nifty 50 — Delivery Buys and Opposite Sells (23 Oct 2023 – 26 Oct 2026)

My best BEL lead (`bel_macd_stoch_delivery_buys.md`) tested on all 50 Nifty 50 stocks, every timeframe, buys and the exact
opposite sells, FYERS charges only (no slippage), ₹1,00,000 per trade. Education, not investment advice.
Report with per-stock tables and charges by type: `../../projects/trading-equation-backtests/reports/STRATEGY2_N50_REPORT.md`.
Every trade (stock, time, price, shares, each FYERS charge, net, indicator values): `reports/strategy2_n50/trades_all.csv`.

## 1. The rules

**Buy:** MACD histogram bigger than the previous candle **and** Stoch RSI blue crosses **above** orange with blue **below 50**
→ buy at that candle's close. **Sell** at the close of the first later candle where blue meets orange (blue ≤ orange).

**Sell (exact opposite):** histogram **smaller** than the previous candle **and** blue crosses **below** orange with blue
**above 50** → short at that close. **Buy back** at the close of the first later candle where blue meets orange (blue ≥ orange).

Shares per trade = ₹1,00,000 ÷ price, rounded down (on average ~125 shares). Same-day trades pay FYERS intraday charges,
overnight buys FYERS delivery charges, overnight shorts FYERS stock-futures charges (cash shorts can't be held overnight; real
futures lot sizes, often ₹5–15 lakh, are not modelled). 15-min and 30-min data start 1 Dec 2025.

## 2. Result (all 50 stocks added together)

| Timeframe | Side | Trades | Shares bought/sold | FYERS charges ₹ | Charges per trade ₹ | Gross ₹ | **Net ₹** | Stocks profitable | Beats random |
|---|---|---|---|---|---|---|---|---|---|
| 15-min | BUY | 15,766 | 19,17,747 | 19,31,144 | 122 | −3,77,718 | **−23,08,863** | 0/50 | 0% |
| 15-min | SELL | 14,922 | 17,91,709 | 12,89,123 | 86 | −1,53,565 | **−14,42,688** | 0/50 | 0% |
| 30-min | BUY | 7,943 | 9,48,228 | 12,69,728 | 160 | −92,481 | **−13,62,210** | 1/50 | 50% |
| 30-min | SELL | 7,736 | 9,17,753 | 6,98,905 | 90 | +1,56,731 | **−5,42,174** | 10/50 | 64% |
| 1-hour | BUY | 14,525 | 18,35,518 | 30,25,970 | 208 | +3,45,901 | **−26,80,070** | 2/50 | 18% |
| 1-hour | SELL | 14,112 | 17,72,094 | 13,58,818 | 96 | −4,09,487 | **−17,68,305** | 0/50 | 77% |
| 4-hour | BUY | 4,180 | 5,28,670 | 11,67,802 | 279 | +7,62,258 | **−4,05,544** | 18/50 | 89% |
| 4-hour | SELL | 4,289 | 5,33,870 | 4,41,135 | 103 | −65,345 | **−5,06,481** | 13/50 | 100% |
| Daily | BUY | 2,216 | 2,80,706 | 6,25,483 | 282 | +4,76,960 | **−1,48,523** | 22/50 | 21% |
| Daily | SELL | 2,159 | 2,74,984 | 2,22,634 | 103 | −1,85,532 | **−4,08,166** | 14/50 | 100% |

All buys: 44,630 trades, 55.1 lakh shares, ₹80.2 lakh FYERS charges, net −₹69.1 lakh.
All sells: 43,218 trades, 52.9 lakh shares, ₹40.1 lakh FYERS charges, net −₹46.7 lakh.

- **Every timeframe and side loses money.** BEL's 4-hour profit doesn't carry over: on Nifty 50 the 4-hour buys lose ₹4.06 lakh.
  Only 18 of 50 stocks were profitable; the best were BSE (+₹1.03L), HINDALCO, APOLLOHOSP, BEL and JIOFIN.
- **4-hour and daily buys do earn before charges** (+₹7.6L and +₹4.8L gross; average move +0.18% / +0.22% per trade), but the
  0.28% delivery charge per trade is bigger. **STT alone was ₹8.2L on 4-hour buys**, more than the whole gross profit.
- **The years don't agree.** 4-hour buys made money in late 2023 and 2025 but lost ₹6.5L in 2026; daily buys made money in
  2023–2025 and lost ₹5.6L in 2026, the falling market.
- **"Beats random" for sells is misleading.** Random shorts lose a lot in a rising market, so the sells beat them while still losing money.
- **15-min to 1-hour lose with almost every stock.** 60–80% of those trades are sold the same day with a ~0% move.

## 3. Lesson

Strategy 2 isn't a trading system on its own: the entry has a small edge on 4-hour and daily buys, but it's smaller than FYERS
delivery charges, and it reverses in falling years. BEL's result was one of the better stocks in a strong rally. If testing
further, the only places with a gross edge are 4-hour and daily buys. They need trades that hold longer (a slower exit) so each move
is bigger than the 0.28% charge, plus a market filter (e.g. only buy when Nifty is above its 200-day average) for years like 2026.
