# Order Flow — What It Is and How to Use It

Follows `price_physics_basics.md`: if price is a moving object, **order flow is the force** that moves it.
Education, not investment advice.

## 1. What order flow is

Every trade needs a buyer and a seller. What matters is **who was in a hurry**.

- **Limit order** = "I'll buy at ₹99 / sell at ₹101" — waits in the **order book**. Passive, provides liquidity.
- **Market order** = "buy/sell now at any price" — hits the book. **Aggressive**, takes liquidity. The aggressor moves price.
- **Order book (market depth)**: queue of bids (buyers below price) and asks (sellers above price).

```
 ASK  101.20  x 1,500   ← sellers waiting
 ASK  101.10  x   800
 ---- spread ----
 BID  101.00  x 3,000   ← buyers waiting
 BID  100.90  x 2,200
```

A market buy of 1,000 eats the 800 at 101.10 and 200 at 101.20 → price ticks up. **Order flow = the stream of these
aggressive buys and sells.**

## 2. The physics: F = m·a for markets (Kyle's lambda)

    ΔP = λ × (aggressive buy volume − aggressive sell volume)

- Net order flow = **force**.
- λ (price impact) = **1 / mass**. Liquid stocks (Reliance, HDFC Bank) = heavy, low λ; small caps = light, high λ.
- Research (Cont, Kukanov & Stoikov 2014, "The Price Impact of Order Book Events"): order-flow imbalance explains a large
  share of short-term price changes **at the same moment** — but its power to **predict** the next move fades within
  seconds to minutes.

## 3. Order-flow measures

| Measure | What it is | Reading |
|---|---|---|
| **Delta** | Aggressive buy volume − aggressive sell volume in a bar | + = buyers pushing, − = sellers pushing |
| **Cumulative delta (CVD)** | Running sum of delta through the day | Rising CVD + rising price = real buying |
| **Divergence** | Price makes a new high, CVD doesn't | Push is weakening (like a car running out of fuel) |
| **Absorption** | Huge aggressive selling but price doesn't fall | A big passive buyer is soaking it up → likely support |
| **Order-book imbalance** | (Bid size − ask size) / (bid + ask) at the top levels | Tilts very short-term direction; easily faked (spoofing) |
| **Footprint chart** | Buy vs sell volume at every price inside each candle | Shows where the fight happened |
| **Volume profile** | Volume traded at each price over a period | POC (busiest price) and value area act as magnets / support |
| **VWAP** | Average price weighted by volume | Where the day's money traded on average |

## 4. Slower order flow (works for swing/delivery, India-specific)

| Data | Where | How to read it |
|---|---|---|
| **Delivery %** | NSE bhavcopy (`DELIV_PER`), daily | Price up + high delivery % = real buyers taking shares home; low % = intraday churn |
| **Futures OI + price** | NSE F&O data | Price ↑ OI ↑ = long build-up · Price ↓ OI ↑ = short build-up · Price ↑ OI ↓ = short covering · Price ↓ OI ↓ = long unwinding |
| **Option OI by strike** | NSE option chain | Big put OI = support, big call OI = resistance (writers defending) |
| **FII / DII flows** | NSE daily | Big institutions' net buying — market-level tide |
| **Bulk / block deals** | NSE daily | Large player entries/exits in a stock |

## 5. How to use it

1. **Confirm a breakout:** take an ORB/breakout only if delta (or CVD) agrees with the direction and relative volume is high.
   Price breaks out but delta is flat/negative → likely a fake breakout.
2. **Spot fakes and turns:** absorption at a level, or price/CVD divergence → don't chase; tighten stops.
3. **Place entries/stops:** buy pullbacks to the volume-profile POC/value-area edge or VWAP, put stops beyond the level where
   absorption happened.
4. **Swing filter:** prefer breakouts/pullbacks where delivery % is above the stock's average and futures show long build-up.

## 6. Limits — be honest

- Order flow is strongest over **seconds to minutes** — that is HFT territory. Retail speed and costs (see the friction section in
  `price_physics_basics.md`) make pure order-book scalping a losing game.
- The order book can be **faked** (spoofing, iceberg orders). Executed trades (delta) are more reliable than resting orders.
- **Data:** true delta needs tick data with bid/ask. TradingView footprint/CVD needs a paid plan; free OHLCV only allows a
  rough proxy: delta ≈ volume × ((C − L) − (H − C)) / (H − L) (the accumulation/distribution idea).
  NSE gives 5 depth levels free; some brokers offer 20+.
- Use it as a **filter on a strategy that already has an edge**, not as the edge itself.

## 7. Puzzle: more buying (positive delta) but a red candle

Real example (footprint, one candle): total buy 107.18K, total sell 79.11K, delta **+28.07K**, yet the candle closed **red**.
Per price level (high → low), sell × buy: 802×11.0K · 10.5K×**45.1K** · 7.4K×10.1K · 16.9K×20.5K · 8.5K×3.7K · 4.4K×8.4K ·
**21.6K**×4.6K · 4.4K×3.0K · 4.6K×795.

Why it happens:
1. **Delta counts impatience, not winners.** Every share has a buyer and a seller; "buy volume" only means the buyer was the
   aggressor (market order). Aggressive buyers can be met by a wall of **passive limit sellers** (often big players, icebergs)
   who refill the ask — the push is **absorbed** and price doesn't rise. Force against a wall ≠ motion.
2. **A footprint shows price, not time.** The buying happened at the **top** of the candle (45.1K at the second-highest level),
   the selling dominated the **bottom** levels (21.6K vs 4.6K, 8.5K vs 3.7K). Buyers were in charge early, sellers took over lower down.
3. **Liquidity can vanish.** If passive buyers cancel their bids, a little selling drops price a lot (λ rises — the object got lighter).
4. **Classification noise.** Buy/sell tagging is estimated from bid/ask at trade time; some volume is mis-tagged.

How to read it: **positive delta + red candle near a high = buyers absorbed and trapped** (the 45.1K bought near the high is now
losing). Bearish if the next candle breaks the low — trapped buyers' stop-losses add selling. Invalidated if price reclaims the
level where the big buying happened. One candle is never enough; use context (trend, VWAP, key levels, cumulative delta).

## 8. How to know who was impatient (the aggressor)

The exchange's matching engine knows exactly: the **incoming order that matched a resting order** is the aggressor.
Public/retail feeds usually don't send that flag, so platforms **infer** it:

| Method | Rule | Notes |
|---|---|---|
| **Quote rule** | Trade at/above the ask (or above mid) = **buyer** aggressive; at/below the bid (or below mid) = **seller** | Needs bid/ask at the moment of the trade |
| **Tick rule** | Price up vs previous trade = buy; down = sell; unchanged = same as last | Works without quotes; noisier |
| **Lee–Ready** | Quote rule, and tick rule for trades exactly at mid | Standard in research |
| **Bulk volume classification** | Bar's buy share ≈ Φ(ΔP / σ) | For bars without tick data |
| **OHLC proxy** | Buy share ≈ (Close − Low) / (High − Low) | Crudest, free-data only |

Example: bid ₹100.00 / ask ₹100.05. Print 500 @ ₹100.05 → buyer paid up → **impatient buyer**. Print 300 @ ₹100.00 →
seller accepted the bid → **impatient seller**.

What to watch on screen:
- **Time & sales (tape):** prints at ask (green) vs at bid (red); speed of prints; big prints.
- **Market depth:** ask queue being eaten = buyers impatient; queue that keeps refilling = a patient (often iceberg) seller.
- **Sweeps:** one order lifting several price levels at once = very impatient (urgent news, stop-losses, a big fund).
- **Patience signs:** large resting orders that don't move, orders added below/above price, absorption.

Limits in India: retail broker feeds send snapshot updates (~1 per second), not every trade, so retail footprints/delta are
estimates; tick-by-tick feeds are for institutions. Check each platform's docs for which rule it uses.

## 9. Link to my backtests

The only intraday lead (5-min ORB, long + short) already uses **relative volume** — a crude order-flow measure. Untested ideas:
delta/CVD confirmation on ORB entries, and delivery % as a filter on the weekly pullback.
