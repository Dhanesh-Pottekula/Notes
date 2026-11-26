# How to Sell Stocks (NSE, FYERS app)

Written Oct 2026. Exact button names in the FYERS app may change; the steps stay the same. Education, not investment advice.
Costs of a sale: see `breakeven_move_fyers.md`.

## 1. Two kinds of selling

| You want to | Product type | Rule |
|---|---|---|
| Sell shares you **own** (in your demat, i.e. Holdings) | **CNC / Delivery** | Any day, any time the market is open. Needs demat authorisation (section 3). |
| Close an **intraday buy** made today | **Intraday (MIS)** | Sell before the broker's auto square-off (~3:15–3:20 pm); otherwise the broker closes it for you (with a fee). |
| Sell **first** without owning (short) and buy back later | **Intraday (MIS) only** | Must buy back the same day. Holding a short overnight in cash stocks is not allowed; that needs futures. |

## 2. Steps in the FYERS app (selling shares you own)

1. **Portfolio → Holdings** → tap the stock.
2. Tap **Exit / Sell**.
3. **Product:** CNC / Delivery (for shares in your demat).
4. **Quantity:** all shares or part of them.
5. **Order type:**
   - **Market:** sells now at the best available price. Fast, but you take whatever price is there (slippage).
   - **Limit:** sells only at your price or better, e.g. "sell 10 at ₹4,020". May not fill.
   - **Stop-loss (SL / SL-M):** waits until price falls to a trigger, then sells. Used to cap a loss.
   - **GTT (good till triggered):** a stop or target that stays active for months; useful for swing trades.
6. Swipe / confirm **Sell**.
7. **Authorise** if asked (section 3).
8. Check **Orders**: "Executed / Complete" = sold. "Pending / Open" = waiting at your limit price.

Market hours: pre-open 9:00–9:08 am, normal trading 9:15 am–3:30 pm, Monday–Friday (not exchange holidays).
**AMO (after-market order):** place it in the evening; it goes to the exchange next morning.

## 3. Demat authorisation (needed only for delivery sells)

Shares leave your demat account when you sell, so SEBI requires your permission:
- **DDPI (one-time):** sign it once (online with Aadhaar e-sign); after that, sells go through without extra steps. Easiest.
- **eDIS / CDSL TPIN:** without DDPI, before selling you enter your **CDSL TPIN + OTP** to approve those shares. Done once per day per stock.

If you skip this, the sell order is rejected.

## 4. After the sale

- **Settlement is T+1:** the money is settled the next working day. You can usually use the sale amount to buy other shares the same day,
  but you can **withdraw it to your bank only after settlement**.
- **Charges:** STT, brokerage, exchange/SEBI fees, GST, stamp duty (on buys) and a **DP charge (~₹14.75) per stock per sell day** on
  delivery sells. Shown in the **contract note** emailed that evening.
- **Tax:** held under 1 year → short-term gain taxed at 20%; 1 year or more → 12.5% on gains above ₹1.25 lakh a year.
  Intraday profit is business income at your slab rate. Losses can be set off against gains; keep the contract notes.
- **Which shares count as sold:** first in, first out (the oldest shares you bought are treated as sold first) — affects tax.

## 5. Common mistakes

- Choosing **Intraday** product for shares you own → order rejected or treated wrongly; use **CNC / Delivery**.
- **BTST** (selling shares bought yesterday, before they reach your demat): allowed, but if the seller who sold them to you fails to
  deliver, you get "short delivery" and an auction penalty. Rare, but possible.
- A **market order** in a thinly traded stock can fill far below the last price; use a **limit** order there.
- Forgetting to close an intraday position → auto square-off at a bad price + extra fee.
