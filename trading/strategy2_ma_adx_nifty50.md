# Strategy 2 + 50/100/200 Average + ADX 30/40, Intra-Candle Sell — Nifty 50

All 50 Nifty 50 stocks, delivery buys, all timeframes, 1 Jan 2023 – 26 Oct 2026 (15/30-min from 1 Dec 2025), FYERS charges only,
₹1,00,000 per trade. Education, not investment advice. Full reports (every timeframe in detail, random-buy comparison, by
year, charges by type): `../../projects/trading-equation-backtests/reports/STRATEGY2_MA_ADX_N50_INTRABAR_REPORT.md` (new
intra-candle sell) and `STRATEGY2_MA_ADX_N50_REPORT.md` (old sell-at-close, for comparison). Every trade:
`reports/strategy2_ma_adx_n50_intrabar/trades_all.csv`. One-stock version: `strategy2_ma_adx_adaniports.md`.

## 1. The rules

**Buy** (all on the same candle): MACD histogram bigger than the previous candle · Stoch RSI blue crosses above orange
(previous candle blue ≤ orange, this candle blue > orange) · blue below 50 · the version's filter is true · no trade open in
that stock → **buy at this candle's close**.

**Sell:** from the next candle on, **the moment blue crosses below orange while the candle is forming**. The code finds the
exact price where that happens: if the candle opens below it, sell at the open; if the low reaches it, sell at that price.
No stop-loss, no target.

**Filters (21 versions):** NONE · ADX(14) > 30 · ADX(14) > 40 · **A50/A100/A200** = last 5 daily closes above the 50/100/200-day
average (intraday timeframes use yesterday's) · **B50/B100/B200** = last 5 candles of the traded timeframe above its
50/100/200-candle average · each A and B also with ADX > 30 and ADX > 40.

**Charges:** FYERS only. Same-day = intraday rates (≈ ₹83 per ₹1L round trip); overnight = delivery rates (≈ ₹284). No slippage.
Full rule list: the chat answer of 28 Oct 2026, and the docstring of `experiments/strategy2_ma_adx.py`.

## 2. Net profit ₹, all 50 stocks added together (intra-candle sell)

| Version | 15-min | 30-min | 1-hour | 4-hour | Daily | **Total** |
|---|---|---|---|---|---|---|
| NONE | −21,00,986 | −10,38,163 | −31,48,855 | −5,10,101 | −1,17,676 | **−69,15,781** |
| ADX30 | −6,26,329 | −3,18,214 | −11,05,504 | 14,676 | −78,364 | **−21,13,735** |
| ADX40 | −2,44,742 | −1,03,625 | −3,77,389 | 42,303 | −16,042 | **−6,99,495** |
| A50 | −7,20,775 | −3,94,037 | −16,03,183 | −1,96,305 | 69,659 | **−28,44,641** |
| A50+ADX30 | −1,88,142 | −1,16,947 | −6,24,177 | **97,019** | 45,000 | **−7,87,247** |
| A50+ADX40 | −74,786 | −22,263 | −2,28,248 | −8,773 | −14,458 | **−3,48,528** |
| A100 | −8,23,527 | −4,45,568 | −16,85,217 | −1,37,632 | 41,015 | **−30,50,929** |
| A100+ADX30 | −2,41,394 | −1,54,404 | −6,73,051 | **91,335** | 41,509 | **−9,36,005** |
| A100+ADX40 | −97,119 | −27,579 | −2,31,530 | −158 | −14,100 | **−3,70,486** |
| A200 | −8,97,305 | −4,95,464 | −18,98,719 | −2,36,700 | 9,776 | **−35,18,412** |
| A200+ADX30 | −2,60,044 | −1,56,346 | −6,72,967 | 35,464 | 18,567 | **−10,35,326** |
| A200+ADX40 | −93,300 | −25,198 | −2,01,053 | 96 | −1,313 | **−3,20,768** |
| B50 | −6,42,004 | −2,21,419 | −9,80,805 | −63,689 | 69,659 | **−18,38,258** |
| B50+ADX30 | −2,19,505 | −80,585 | −4,63,697 | 27,990 | 45,000 | **−6,90,797** |
| B50+ADX40 | −78,897 | −30,214 | −2,14,234 | −9,457 | −14,458 | **−3,47,260** |
| B100 | −8,08,210 | −3,22,280 | −14,49,914 | −1,32,333 | 41,015 | **−26,71,722** |
| B100+ADX30 | −2,36,377 | −92,774 | −5,51,345 | **87,621** | 41,509 | **−7,51,366** |
| B100+ADX40 | −89,393 | −27,948 | −2,20,724 | −8,773 | −14,100 | **−3,60,938** |
| B200 | −8,16,074 | −3,88,917 | −15,80,725 | −1,01,393 | 9,776 | **−28,77,333** |
| B200+ADX30 | −2,32,149 | −1,11,739 | −5,48,324 | **92,506** | 18,567 | **−7,81,139** |
| B200+ADX40 | −90,792 | −36,008 | −2,18,082 | 8,651 | −1,313 | **−3,37,544** |

On daily, A and B are the same rule, so they give the same numbers.

## 3. What it shows

- **Every version loses in total** because of 15-min, 30-min and 1-hour (−₹3L to −₹31L each). Only 4-hour and daily ever make money.
- **Best: 4-hour + ADX > 30 + any average** (A50, A100, B100, B200): **+₹88k to +₹97k** on 680–760 trades, 23–26 of 50 stocks
  profitable. They beat random buys with the same filter in **97–100%** of runs (random buys lose ~₹80–88k). So on 4-hour,
  ADX > 30 plus the entry really does pick better moments than chance.
- **But only in 2023–2024.** For A50+ADX30 on 4-hour: 2023 +₹52k · 2024 +₹66k · 2025 −₹14k · 2026 −₹7k. Every top version
  has the same pattern. They make money in the rising market and lose afterwards.
- **ADX 30 vs 40:** ADX > 40 leaves too few trades (217–430 on 4-hour) and mostly loses. **ADX > 30 is the better level.**
- **50 vs 100 vs 200 average:** with ADX > 30 on 4-hour, all of them land at +₹88–97k except A200 (+₹35k). The length matters
  much less than the ADX filter.
- **Daily average-only (A50/B50 +₹70k)** is no better than random buys with the same filter (beats 77%), and it lost ₹81k in 2026.

## 4. Intra-candle sell vs sell-at-close

- Over all 105 version × timeframe combinations, the intra-candle sell lost **₹3.36 crore** in total vs **₹3.63 crore** for
  sell-at-close. It was better in **66 of 105**, but not on 4-hour + ADX30, where sell-at-close was higher (e.g. A50+ADX30
  +₹1.49L vs +₹97k).
- **About half the intra-candle sells happen at the open** (1,27,611 of 2,58,374): the cross happened during the gap between
  candles. So getting out "early" often only saves the move inside the candle.

## 5. Adding +DI above −DI (strong trend that points up) — 4-hour and daily

Same rules, ADX > 30 versions also run with **+DI above −DI** on the buy candle (ADX, +DI, −DI from TradingView "ADX and DI",
same timeframe). Report: `reports/STRATEGY2_MA_ADX_N50_INTRABAR_DI_REPORT.md`.

| Version | 4-hour without +DI | 4-hour **with +DI** | Daily without +DI | Daily **with +DI** |
|---|---|---|---|---|
| ADX30 only | +14,676 | **+36,178** | −78,364 | **+43,319** |
| A50 + ADX30 | +97,019 | +39,395 | +45,000 | +55,862 |
| A100 + ADX30 | +91,335 | +50,014 | +41,509 | +48,544 |
| A200 + ADX30 | +35,464 | +48,690 | +18,567 | +44,656 |
| B50 + ADX30 | +27,990 | +26,319 | +45,000 | +55,862 |
| B100 + ADX30 | +87,621 | +47,508 | +41,509 | +48,544 |
| B200 + ADX30 | +92,506 | **+57,808** | +18,567 | +44,656 |

- **+DI makes every ADX30 version positive on both timeframes** (4-hour +₹26k to +₹58k, daily +₹43k to +₹56k) and makes them
  **much steadier**: the 2025–2026 losses shrink to a few thousand rupees. Example: 4-hour B200 + ADX30 + DI: 2023 +₹45k ·
  2024 +₹31k · 2025 −₹14k · 2026 −₹4.5k, vs −₹12k / −₹16k without +DI.
- **On 4-hour it lowers the total when an average is also used** (e.g. A50 + ADX30: +₹97k → +₹39k), because the average already
  keeps you in uptrends and +DI removes some good trades. It still beats random buys in **97–100%** of runs.
- **On daily, the +DI profit is mostly the trend itself:** random buys with the same filter make +₹23k to +₹62k, and the
  strategy beats them only 43–63% of the time.
- **Most consistent version so far: 4-hour B200 + ADX30 + DI**: +₹57,808 on 559 trades, 23 of 50 stocks profitable, beats random
  100%, +₹11.5k without its best 3 trades, worst year −₹14k. Still a thin edge, about ₹100 per ₹1L trade.

### What +DI actually removes from B200 + ADX30

Splitting the B200 + ADX30 trades by +DI vs −DI on the buy candle:

| | 4-hour: +DI above −DI | 4-hour: +DI below −DI (removed by +DI) | Daily: +DI above −DI | Daily: +DI below −DI (removed) |
|---|---|---|---|---|
| Trades | 559 | 123 | 275 | 86 |
| Avg move | +0.38% | **+0.57%** | +0.45% | −0.02% |
| Net ₹ | +57,808 | **+34,699** | +44,656 | **−26,089** |

- B200 already means the stock is above its 200-candle average (a longer uptrend). Inside that, **+DI below −DI means a short,
  strong pullback**. Strategy 2's Stoch cross then buys the dip.
- **On 4-hour those dip buys made money (+₹34.7k)**, so +DI throws away good trades → use **B200 + ADX30 without +DI** on 4-hour.
- **On daily they lost (−₹26k)**, so +DI helps → use **B200 + ADX30 + DI** on daily.

## 6. Lesson

Of everything tested so far, **4-hour Strategy 2 + ADX > 30 + a 50/100/200 average** is the strongest real-time version: it beats
random timing and makes about ₹1 lakh over 3.8 years on 50 stocks at ₹1L per trade (≈ ₹130 per trade), but lost money in
2025–2026. **Adding +DI above −DI** gives less profit (≈ ₹50k) but much smaller losses in the bad years. It's the steadier choice.
Next ideas: a Nifty-above-200-day market filter for falling years, and a test on Nifty 200 to see whether the 4-hour result
holds outside Nifty 50.
