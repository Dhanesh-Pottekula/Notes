# How Much Do Traders Actually Make? — and How to Check If I Can

Researched Oct 2026. Education, not investment advice.

## 1. What the data says

| Who | Result | Source |
|---|---|---|
| Indian F&O traders, FY26 | **87.7% lost money**; total loss ₹91,685 crore; average loss ~₹1.17 lakh per trader | SEBI study (Sep 2026), via Open Magazine / Bajaj Broking |
| Indian F&O traders, FY22–24 | **93% lost money** over three years; average loss ~₹2 lakh each; total > ₹1.8 lakh crore | SEBI study (Sep 2024), via Outlook Business |
| Indian F&O traders who lost two years running and kept going | ~90% lost again the next year | SEBI FY26 study |
| Options vs futures, FY26 | ~88% of options traders lost vs ~66% of futures traders | SEBI FY26 study |
| Indian intraday cash-equity traders, FY23 | **71% lost money**; 80% lost among those with > 500 trades a year; losers paid costs equal to another 57% of their trading loss | SEBI study (Jul 2024), via Business Standard / Moneylife |
| Brazil day traders active ≥ 300 days (2013–15) | **97% lost money**; ~1% earned more than the minimum wage | Chague, De-Losso & Giovannetti, "Day Trading for a Living?" |
| Taiwan day traders | < 1% predictably profitable after fees | Barber, Lee, Liu & Odean |
| Indian large-cap mutual fund managers (professionals) | **76% lagged the index over 10 years** (to Dec 2025) | SPIVA India Year-End 2025 |

Benchmarks to beat (rough, long-run, before tax): bank FD ~6.5–7%; Nifty 50 index fund ~11–13% a year over long periods
(with falls of 30–50% along the way).

## 2. Realistic return ranges

| Approach | Realistic yearly result |
|---|---|
| Retail intraday / F&O, no tested edge | **Negative** for ~70–90% of people |
| Nifty index fund (do nothing) | ~11–13% long run |
| Professional active fund manager | Most end up slightly **below** the index after fees |
| A tested, disciplined swing/positional system | Index-like to index + a few %; the gain is often smaller drawdowns, not higher returns |
| Renaissance Medallion–type results | Exceptions; not a retail benchmark |

My own backtests: momentum rotation and weekly pullback showed 18–27% a year, but survivorship bias inflates that — the real
Nifty 200 Momentum 30 index made 14.6% a year since Oct 2020. Realistic expectation: **~12–18% a year before tax, with 15–30% drawdowns.**
Every intraday strategy I tested failed after costs.

## 3. The equation for my own yearly return

    Yearly return ≈ N × E × r
    N = trades per year · E = average profit per trade in R (after costs) · r = % of capital risked per trade

| Example | N | E | r | Yearly return |
|---|---|---|---|---|
| Swing, small real edge | 40 | +0.35R | 1% | **+14%** |
| Intraday, tiny edge | 500 | +0.02R | 0.5% | +5% |
| Intraday, tiny negative edge (costs) | 500 | −0.05R | 0.5% | **−12.5%** |

Many trades magnify a small edge **both ways** — costs turn a tiny edge negative, and N multiplies the loss.

## 4. Checklist: can I make money?

1. **Edge:** does my strategy have positive expectancy after costs in a backtest on data it was not tuned on, on more than one stock list?
2. **Win rate vs break-even:** is my real win rate clearly above p* = (avg loss + costs) / (avg win + avg loss)?
3. **Beat the lazy option:** after costs **and tax**, is my return above a Nifty index fund over the same period? If not, the index fund wins.
4. **Paper trade** 3–6 months (or ≥ 100 trades), then small real money; compare live results with the backtest.
5. **Size matters in ₹:** 15% on ₹1 lakh is ₹15,000 a year — trading can't replace a salary on small capital.
6. **Tax (equity, India):** short-term gains 20%; long-term gains 12.5% above ₹1.25 lakh a year; intraday profit is speculative
   business income taxed at slab rate. A strategy that trades often pays more tax.
7. **Stop rule:** if after 12 months my net return is below the index fund's, switch to the index fund.

## 4b. Who actually makes the money

**Trading vs investing:**
- **Short-term trading is zero-sum before costs:** for every rupee one trader wins on a price move, another trader loses it.
  After brokerage, STT, GST, exchange fees and slippage it is **negative-sum** for the traders as a group.
- **Long-term investing is positive-sum:** companies grow earnings and pay dividends, so all holders can gain together
  (Nifty ~11–13% a year long run). The investor earns the business's growth, not someone else's loss.

**Who wins (from most to least certain):**
1. **The "house" — on every trade, win or lose:** brokers (brokerage), exchanges and clearing (transaction fees),
   government (STT, GST, stamp duty, income tax).
2. **Proprietary trading firms and foreign institutions in F&O:** SEBI FY24 — prop traders made ₹33,000 crore and FPIs ₹28,000 crore
   gross profit, while "individuals and others" lost over ₹61,000 crore; **96–97% of those firms' profits came from algorithmic trading**.
   Their edges: speed, market making (earning the spread), cheaper costs, better data, huge capital and risk control.
3. **Long-term investors and index-fund holders:** earn the market's growth — the most reliable route for an individual.
4. **Fund managers:** earn fees whether or not they beat the index.
5. **A small minority of skilled retail traders:** ~7% of individual F&O traders were net profitable over FY22–24; fewer still made
   meaningful money.

Sources: https://www.outlookbusiness.com/markets/fo-frenzy-over-93-retail-investors-lost-average-rs-2-lakh-in-three-years-says-sebi ·
https://www.business-standard.com/amp/opinion/editorial/a-losing-proposition-odds-are-against-individuals-in-f-o-trading-124092401316_1.html ·
https://wrightresearch.in/blog/sebi-futures-and-option-report-individual-traders-in-fandos-incur-rs-18-lakh-crore-loss-over-3-years

## 5. Paper trading platforms (India, checked Oct 2026 — verify pricing on each site)

| Platform | Good for | Notes |
|---|---|---|
| TradingView paper trading (tradingview.com) | Stocks, swing, intraday — on the same charts I already use | Free virtual account; check whether NSE data is real-time or delayed on my plan |
| Moneybhai (Moneycontrol) | Simple stock portfolio + intraday practice | Free; large virtual balance |
| Frontpage | Stocks, with a P&L statement | Virtual cash (~₹10 lakh) |
| StockGro | Beginner, gamified, leagues | Social features |
| Neostox | Stocks + F&O with an Indian-broker-like screen | Short free trial, then paid; data may be delayed |
| Sensibull virtual trading | Options strategies | Options only |
| AlgoTest | Options strategy backtest + forward/paper testing | Options-focused |
| Streak (Zerodha) / Tradetron | Paper-trading rule-based algos before going live | Algo-focused |

For weekly/monthly strategies (weekly pullback, momentum rotation) a simple journal is enough: write down each signal, entry,
stop, exit and costs, and compare with a Nifty index fund over the same weeks.

## Sources
- Paper trading platform lists: https://algotest.in/blog/paper-trading-websites-india.md · https://www.strike.money/stock-market/paper-trading ·
  https://rupeezy.in/blog/best-paper-trading-app
- SEBI FY26 F&O study: https://openthemagazine.com/business/sebi-fo-loss-study-explained-why-9-in-10-retail-traders-lost-91685-crore-in-fy26 ·
  https://www.bajajbroking.in/share-market-news/f-and-o-losses-fall-18-percent-average-loss-per-trader-rose-to-rupees-1-16-lakh
- SEBI FY22–24 F&O study: https://www.outlookbusiness.com/markets/fo-frenzy-over-93-retail-investors-lost-average-rs-2-lakh-in-three-years-says-sebi
- SEBI intraday study (FY23): https://www.business-standard.com/amp/markets/news/7-in-10-intraday-traders-in-equity-cash-suffered-losses-in-fy23-sebi-study-124072400975_1.html ·
  https://moneylife.in/article/7-out-of-10-individual-intraday-traders-in-equity-cash-segment-make-losses-sebi-study/74733.html
- Brazil day traders: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3423101 · https://quantpedia.com/retail-day-trading-is-an-uphill-battle/
- Taiwan day traders: https://faculty.haas.berkeley.edu/odean/papers/day%20traders/Day%20Trading%20Skill%20110523.pdf
- SPIVA India Year-End 2025: https://www.spglobal.com/spdji/en/spiva/article/spiva-india-year-end-2025/
