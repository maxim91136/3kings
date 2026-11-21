# Rule book

## Principles
- Test criteria are fixed before computing. Results are shown even when they are unwelcome. (since Nov 18, 2026)
- Rules change only by explicit decision or at season end, never by gut feeling. Every change is recorded with its date in the log. (since Nov 18, 2026)
- Numbers come before principle: if a test refutes a rule, the rule is changed. (since Nov 18, 2026)
- Calculations in euros, with dividends where available. (since Nov 18, 2026)
- Information only: no orders are placed, no investment advice. The site shows no personal holdings. (since Nov 19, 2026)

## Buy rule
- **Buy as soon as there is money.** Tested for the S&P 500 (from 1928), gold (from 1975), bitcoin (from 2013) and 138 single stocks (from 2006): waiting for dips, distance to the high, cheaper valuations, fear signals, buying in stages or a crash reserve never did better. (since Nov 18, 2026)
- **The foundation is the S&P 500** (King of Kings). No tested challenger beat it lastingly: FTSE All-World, world incl. emerging markets, only the largest, factor ETFs, trend filters, the Crown Jewels rule selection. (since Nov 21, 2026)
- Bitcoin and gold are satellites. Bitcoin only directly, without leverage.
- The split in the calculator is freely selectable (one third each by default); the site prescribes no weighting. (since Nov 19, 2026)

## Crown Jewels (own index)
- **Universe:** current S&P 500 members and a fixed European list, renewed every season. (since Nov 21, 2026)
- **Excluded beforehand:** only the energy, materials and real estate sectors. For everyone else, the beta decides whether a company swings too much with the economy, not the industry label. (since Nov 21, 2026; before, a list of sub-industries such as hardware, semiconductors, banks, industrials)
- **Admission, all four rules:** beta below 1.15 (5 years, weekly prices, in euros against the S&P 500); at least 17 % return per year over ten years (home currency, with dividends); gross margin at least 49 % (around 50 %); net debt below twice operating profit (EBITDA). Passed two season reviews in a row = admitted automatically. (since Nov 21, 2026)
- **Removal only on a clear miss (buffer):** beta above 1.30, return below 12 %, margin below 45 % or net debt from 2.5 times. Once = warning, two season reviews in a row = out. (since Nov 21, 2026)
- **Execution:** admissions and removals take effect in the shadow books only from the close of the next trading day after the season review. (since Nov 21, 2026)
- **Weighting:** equal. The ranking by 10-year return is only displayed. (since Nov 21, 2026) The 5-year return is shown alongside, information only, not a criterion (too short, too dependent on the starting point). (since Nov 21, 2026)
- **Replication as a savings plan:** new money split equally across current members; removed stocks are not sold but get no new money. (since Nov 21, 2026)
- **Index size:** no cap; every stock that meets the rules is in. Under observation. (since Nov 21, 2026)
- **Season review:** automatic at every season end (63 trading days, next around late January 2027). Result privately via Telegram with concrete savings-plan steps, in the monthly report and in the log. (since Nov 21, 2026)
- **Status:** experiment. In the rule test 2016 to 2026 (price rules only) the selection lagged the S&P 500 (lump sum 14.0 % vs 14.3 %, savings plan 11.3 % vs 13.9 % per year). (since Nov 21, 2026)

## Bitcoin: power law check
- Midline: 1.0117e-17 × days since Jan 3, 2009 to the power of 5.82 (dollars). Floor: 0.42 × midline (matches the red line on bitbo). (since Nov 21, 2026)
- Only the monthly close is checked. A close below the floor = floor broken this month. Information only, the buy rule is unaffected. (since Nov 21, 2026)

## Market barometer (traffic lights in "At a glance")
- Green calm, yellow moderate, red stressed. Information only, not a buy or sell signal; the buy rule is unaffected. (since Nov 21, 2026)
- Fear & Greed: green from 50, yellow 25–49, red below 25. VIX: green below 20, yellow 20–30, red above 30. (since Nov 21, 2026)
- Daily change S&P 500 and gold: green when up, yellow down to −2 %, red below; bitcoin: yellow down to −5 %. Oil (month): green up to +5 %, yellow up to +15 %, red above. (since Nov 21, 2026)
- US 10-yr yield: green below 4 %, yellow up to 4.75 %, red above. ECB deposit rate: green up to 2.25 %, yellow up to 3 %, red above. Inflation US and euro area: green up to 2.5 %, yellow up to 3.5 %, red above. Euro in dollars: no colour. (since Nov 21, 2026)
- Also Shiller P/E: green below 20, yellow up to 30, red above. Buffett indicator: green below 100 %, yellow up to 150 %, red above. Yield curve 10y − 2y: green from +0.5 percentage points, yellow 0 to 0.5, red negative. (since Nov 21, 2026)
- One "Market conditions" block at the top of the page: tiles, below them details on all indicators as text without own colours. Indicators change the buy rule only if they pass a test against "buy immediately"; none has so far. (since Nov 21, 2026)
- Bitcoin vs power-law midline (price divided by midline): red below the floor (42 %), green up to 100 %, yellow up to 200 %, red above. Sixteen tiles so the grid is even. (since Nov 21, 2026)
- Colours and values are recorded daily in data/barometer.csv (forward test of the hypotheses). (since Nov 21, 2026)
- Hypotheses, fixed in advance (return 12 months after the day, compared with the average of all days): A) Fear & Greed stocks red and VIX red: S&P 500 better than average afterwards. B) US inflation red and US yield red: S&P 500 weaker afterwards. C) The number of red tiles says nothing about the S&P 500 afterwards. D) Fear & Greed crypto red and bitcoin below the power-law midline: bitcoin better than average afterwards. Tested backwards as far as data allow and forwards from Nov 21, 2026, first verdict November 2027. Confirmed hypotheses are only shown as context; the buy rule stays. (since Nov 21, 2026)

## Tactical model 3 Kings (test bench, no trading relevance)
- Three kings: S&P 500, bitcoin, gold, in euros. S&P 500 and gold play trend (200-day line) fixed; for bitcoin a strategy is chosen from the candidates at the start of each season (look-back 504 trading days). (since Nov 18, 2026)
- Capital split by volatility (inverse volatility), bitcoin weight doubled, never more than 100 %, no leverage. Rebalanced only from a 5-point deviation. (since Nov 18, 2026)
- Signal at the close; the shadow book rebalances only at the close of the next trading day (as is possible in practice). Each signal is shown until then and reported privately via Telegram. (since Nov 21, 2026)
- A season lasts 63 trading days; rules change only at season end. (since Nov 18, 2026)
- Verdict after four seasons (around November 2027): confirmed if the drawdown is smaller than holding and the return at most 2 points below. (since Nov 18, 2026)

## Shadow books (forward test, no real money)
- **Crown Jewels** since Nov 17, 2026, as a lump sum and as a savings plan (€100 per month), each against the S&P 500. Verdict November 2031: proven with at least 2 points more return per year, failed below the S&P 500. (since Nov 21, 2026)
- **S&P 500 savings plan** since Nov 17, 2026: "always immediately" vs "not at the high" (buy only 3 % below the all-time high), S&P 500 in euros. Review after one year. (since Nov 18, 2026)
- **Tactical model 3 Kings** against all three held. (since Nov 18, 2026)

## Automation and site
- **News monitor** daily around 7:45 CET, Sundays and Mondays bitcoin only. Reasons are researched from: S&P 500 ±2 %, gold ±2.5 %, bitcoin ±5 %, each Crown Jewels stock ±4 % (rounded value, daily change in euros); then all three main assets get a line. (since Nov 21, 2026)
- **Monthly report** on the 1st of each month, **annual report** on January 1, each with the power law check and Crown Jewels changes. (since Nov 21, 2026)
- **Telegram:** daily reports and reports to the channel (Crown Jewels changes there neutrally in the monthly report); savings-plan steps for Crown Jewels changes privately only. (since Nov 21, 2026)
- **Watchdog:** every morning around 9 CET a check of the data run, prices, news and (start of month) the monthly report; on failure a private Telegram message, on Sundays a short sign of life. (since Nov 21, 2026)
- **Archive:** the homepage shows the last 7 days (news and histories); everything older is in the archive by month. Nothing is deleted. (since Nov 21, 2026)
