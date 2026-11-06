# Main Uptrend of Every Nifty 50 Stock (200-Day Average Rule)

The uptrend start and end date for each Nifty 50 stock, the same idea as my BEL window (23 Oct 2023 – 9 Jun 2026) but with one
fixed rule for every stock. Education, not investment advice. Made by
`../../projects/trading-equation-backtests/experiments/find_uptrends.py` on daily closes up to 26 Oct 2026.
Charts for every stock: `../../projects/trading-equation-backtests/reports/uptrends_n50/<STOCK>.png`. Every uptrend (not just
the main one): `reports/uptrends_n50_all.csv`.

## 1. The rule

- **Start:** the first of **5 daily closes in a row above the 200-day simple moving average**.
- **End:** the first of **5 daily closes in a row below the 200-day average**.
- **Peak:** the highest close between start and end.
- **Main uptrend:** of all uptrends that peaked on or after 1 Jan 2023, the one with the biggest rise from start to peak.
  Uptrends already running on 1 Jan 2023 are included with their real start date (marked *).
- The 5-day confirmation filters one-day blips. With a 1-day rule, BEL breaks into 19 pieces since 2023; with 5 days, 4.

## 2. BEL check (my hand-marked window was 23 Oct 2023 – 9 Jun 2026)

| Start | Peak | End | Rise to peak |
|---|---|---|---|
| 05 Apr 2023 | 11 Jul 2024 | 08 Jan 2025 | +241% |
| 20 Mar 2025 | 24 Mar 2025 | 02 Apr 2025 | +2% |
| 15 Apr 2025 | 06 Mar 2026 | 29 May 2026 | +60% |
| 17 Jun 2026 | 22 Jun 2026 | 24 Jun 2026 | +3% |

The rule doesn't give one window like mine. BEL closed below its 200-day average for about 2 months in Jan–Mar 2025, so the
rule splits there. Its second uptrend ends on 29 May 2026, close to my 9 Jun 2026 end date.

## 3. All 50 stocks (sorted by rise to peak)

| Stock | Start | Start ₹ | Peak | Peak ₹ | End | End ₹ | Start → peak | Start → end |
|---|---|---|---|---|---|---|---|---|
| BSE | 31 May 2023 | 185.90 | 10 Jun 2025 | 3,005.40 | 23 Sep 2025 | 2,122.20 | +1517% | +1042% |
| TRENT | 06 Mar 2023 | 883.60 | 11 Oct 2024 | 5,489.97 | 20 Jan 2025 | 4,060.00 | +521% | +359% |
| ETERNAL | 26 Apr 2023 | 58.20 | 06 Dec 2024 | 302.95 | 21 Jan 2025 | 214.55 | +421% | +269% |
| NTPC * | 23 Nov 2020 | 93.65 | 30 Sep 2024 | 443.20 | 14 Nov 2024 | 372.50 | +373% | +298% |
| MAXHEALTH * | 03 Aug 2022 | 369.95 | 03 Jul 2025 | 1,301.40 | 24 Sep 2025 | 1,133.20 | +252% | +206% |
| BEL | 05 Apr 2023 | 98.25 | 11 Jul 2024 | 335.50 | 08 Jan 2025 | 282.10 | +241% | +187% |
| BAJAJ-AUTO | 16 Mar 2023 | 3,800.20 | 27 Sep 2024 | 12,666.40 | 13 Nov 2024 | 9,452.15 | +233% | +149% |
| BHARTIARTL | 06 Apr 2023 | 765.95 | 21 Nov 2025 | 2,162.70 | 24 Feb 2026 | 1,941.00 | +182% | +153% |
| SHRIRAMFIN | 05 Apr 2023 | 257.81 | 26 Sep 2024 | 725.69 | 09 Jan 2025 | 561.97 | +181% | +118% |
| TMPV | 05 Apr 2023 | 257.52 | 30 Jul 2024 | 701.43 | 03 Oct 2024 | 558.87 | +172% | +117% |
| INDIGO | 31 Mar 2023 | 1,910.65 | 12 Sep 2024 | 4,994.65 | 07 Nov 2024 | 3,995.75 | +161% | +109% |
| M&M | 23 May 2023 | 1,268.55 | 02 Jan 2025 | 3,211.10 | 17 Feb 2025 | 2,831.95 | +153% | +123% |
| ONGC * | 29 Dec 2022 | 144.65 | 01 Aug 2024 | 341.75 | 21 Oct 2024 | 276.60 | +136% | +91% |
| COALINDIA | 30 Jun 2023 | 231.00 | 01 Aug 2024 | 540.40 | 25 Oct 2024 | 461.10 | +134% | +100% |
| POWERGRID | 27 Feb 2023 | 164.40 | 26 Sep 2024 | 365.45 | 20 Dec 2024 | 315.80 | +122% | +92% |
| ITC * | 04 Mar 2022 | 212.86 | 20 Jul 2023 | 464.56 | 30 Jan 2024 | 413.49 | +118% | +94% |
| LT * | 27 Jul 2022 | 1,796.65 | 03 Jun 2024 | 3,897.15 | 03 Oct 2024 | 3,497.65 | +117% | +95% |
| ADANIPORTS | 25 Jul 2023 | 749.25 | 01 Aug 2024 | 1,590.15 | 22 Oct 2024 | 1,362.85 | +112% | +82% |
| SUNPHARMA | 31 May 2023 | 975.35 | 27 Sep 2024 | 1,948.70 | 14 Feb 2025 | 1,700.50 | +100% | +74% |
| ULTRACEMCO * | 27 Oct 2022 | 6,436.80 | 13 Dec 2024 | 12,083.90 | 10 Jan 2025 | 10,865.20 | +88% | +69% |
| AXISBANK * | 27 Jul 2022 | 718.95 | 12 Jul 2024 | 1,317.30 | 13 Nov 2024 | 1,139.15 | +83% | +58% |
| HINDALCO | 13 Jul 2023 | 435.20 | 01 Oct 2024 | 761.55 | 16 Dec 2024 | 653.50 | +75% | +50% |
| GRASIM | 05 Apr 2023 | 1,652.64 | 12 Jul 2024 | 2,843.75 | 19 Dec 2024 | 2,539.05 | +72% | +54% |
| APOLLOHOSP | 24 Apr 2023 | 4,399.05 | 07 Jan 2025 | 7,436.75 | 11 Feb 2025 | 6,317.35 | +69% | +44% |
| EICHERMOT | 20 Feb 2025 | 4,888.40 | 26 Feb 2026 | 8,190.00 | 18 May 2026 | 6,913.00 | +68% | +41% |
| TATASTEEL | 05 Jun 2023 | 109.40 | 14 Jun 2024 | 183.15 | 03 Sep 2024 | 152.15 | +67% | +39% |
| DRREDDY | 12 Jan 2023 | 862.12 | 21 Aug 2024 | 1,412.49 | 12 Nov 2024 | 1,263.90 | +64% | +47% |
| ADANIENT | 24 Nov 2023 | 2,158.54 | 03 Jun 2024 | 3,535.64 | 03 Sep 2024 | 2,944.81 | +64% | +36% |
| CIPLA | 11 Jul 2023 | 1,027.80 | 09 Oct 2024 | 1,680.50 | 13 Nov 2024 | 1,505.60 | +64% | +46% |
| TATACONSUM | 02 May 2023 | 770.19 | 07 Mar 2024 | 1,246.33 | 04 Oct 2024 | 1,130.40 | +62% | +47% |
| HCLTECH * | 01 Nov 2022 | 1,060.05 | 22 Feb 2024 | 1,686.40 | 30 Apr 2024 | 1,366.60 | +59% | +29% |
| SBIN | 01 Dec 2023 | 571.75 | 03 Jun 2024 | 905.65 | 24 Dec 2024 | 812.05 | +58% | +42% |
| TITAN | 16 Mar 2023 | 2,450.35 | 29 Jan 2024 | 3,866.65 | 06 May 2024 | 3,280.15 | +58% | +34% |
| MARUTI | 02 May 2023 | 8,776.85 | 27 Sep 2024 | 13,495.60 | 22 Oct 2024 | 11,923.30 | +54% | +36% |
| ICICIBANK | 31 Mar 2023 | 877.25 | 16 Dec 2024 | 1,346.10 | 21 Feb 2025 | 1,232.95 | +53% | +41% |
| BAJFINANCE | 02 Jan 2025 | 738.92 | 23 Oct 2025 | 1,094.15 | 20 Jan 2026 | 933.20 | +48% | +26% |
| RELIANCE | 05 Jun 2023 | 1,124.50 | 08 Jul 2024 | 1,600.90 | 03 Oct 2024 | 1,406.98 | +42% | +25% |
| JSWSTEEL | 04 Feb 2025 | 944.25 | 26 Aug 2026 | 1,341.00 | 07 Oct 2026 | 1,230.00 | +42% | +30% |
| TECHM | 26 Apr 2024 | 1,278.75 | 13 Dec 2024 | 1,796.40 | 27 Feb 2025 | 1,588.25 | +40% | +24% |
| NESTLEIND | 31 Mar 2023 | 985.22 | 01 Jan 2024 | 1,368.62 | 25 Jul 2024 | 1,240.32 | +39% | +26% |
| TCS | 30 Jun 2023 | 3,302.25 | 30 Aug 2024 | 4,553.75 | 03 Jan 2025 | 4,099.90 | +38% | +24% |
| SBILIFE | 06 Jun 2024 | 1,442.85 | 03 Sep 2024 | 1,928.65 | 08 Nov 2024 | 1,569.95 | +34% | +9% |
| INFY | 19 Jun 2024 | 1,511.35 | 13 Dec 2024 | 1,999.70 | 24 Feb 2025 | 1,764.10 | +32% | +17% |
| HDFCBANK | 05 Jun 2024 | 775.90 | 30 Jul 2025 | 1,012.90 | 06 Jan 2026 | 962.20 | +31% | +24% |
| HDFCLIFE | 08 May 2023 | 549.55 | 12 Dec 2023 | 707.35 | 15 Jan 2024 | 614.45 | +29% | +12% |
| BAJAJFINSV | 02 Jan 2025 | 1,700.65 | 23 Oct 2025 | 2,176.60 | 08 Jan 2026 | 2,008.90 | +28% | +18% |
| KOTAKBANK | 31 Dec 2024 | 357.21 | 22 Apr 2025 | 453.76 | 25 Aug 2025 | 396.66 | +27% | +11% |
| ASIANPAINT | 15 Oct 2025 | 2,375.10 | 05 Dec 2025 | 2,968.50 | 28 Jan 2026 | 2,511.80 | +25% | +6% |
| HINDUNILVR | 04 Jun 2024 | 2,457.62 | 23 Sep 2024 | 2,981.62 | 31 Oct 2024 | 2,489.08 | +21% | +1% |
| JIOFIN | 04 Jun 2025 | 290.35 | 04 Aug 2025 | 333.90 | 08 Jan 2026 | 293.55 | +15% | +1% |

\* uptrend was already running on 1 Jan 2023; the start shown is its real, earlier start.

## 4. What stands out

- **35 of 50 main uptrends ended between Jun 2024 and Mar 2025**, the market top and the correction that followed. For most stocks
  the big run was 2023–2024.
- **Biggest:** BSE (+1517%), TRENT (+521%), ETERNAL (+421%), NTPC* (+373%), MAXHEALTH* (+252%), BEL (+241%).
- **Weakest:** private banks, FMCG and IT (HDFCBANK, KOTAKBANK, HINDUNILVR, ASIANPAINT, INFY, TCS): only +20–38%.
- **Still in an uptrend on the latest data:** ADANIPORTS (since 08 Apr 2026), ADANIENT (since 23 Apr 2026), ETERNAL (since 01 Jul 2026), KOTAKBANK (since 21 Aug 2026), TRENT (since 06 Oct 2026), BSE (since 12 Oct 2026), BAJAJ-AUTO (since 13 Oct 2026), TECHM (since 13 Oct 2026), HCLTECH (since 15 Oct 2026), ICICIBANK (since 15 Oct 2026).
- The "end" is a confirmed break below the 200-day average, so it comes after the peak, often 10–25% below it.
  Start → end is what you'd have made by buying at the start and selling at the end.

## 5. Caveats

- One fixed rule, not hand-picked: the dates won't always match where you'd draw them on a chart.
- The 200-day average lags by design: starts come after the low and ends come after the top.
- Current Nifty 50 members only. JIOFIN listed in Aug 2023, so its 200-day average only exists from mid-2024.
