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
- The split in the calculator is freely selectable. The default is provisionally 80 % S&P 500, 10 % gold, 10 % bitcoin (one of the blends that meet the rule set in advance). The later test of all 231 blends gave 30 / 60 / 10 as best under the rule; the decision on the default is open. Test result on about 12 years of bitcoin data, no recommendation. (since Nov 22, 2026, previously one third each)

## Crown Jewels (own index)
- **Universe:** current S&P 500 members and a fixed European list, renewed every season. (since Nov 21, 2026)
- **Excluded beforehand:** only the energy, materials and real estate sectors. For everyone else, the beta decides whether a company swings too much with the economy, not the industry label. (since Nov 21, 2026; before, a list of sub-industries such as hardware, semiconductors, banks, industrials)
- **Admission, all six rules:** beta at most 1.15 (5 years, weekly prices, in euros against the S&P 500); at least 17 % return per year over ten years (home currency, with dividends); gross margin at least 45 %; net debt below twice operating profit (EBITDA); **steady runner:** at most 20 % of weeks more than 20 % below the previous high (time under water) and own volatility at most 30 % a year (both 10 years, weekly prices, home currency). Passed two season reviews in a row = admitted automatically. (since Nov 21, 2026; margin previously 49 %, steady-runner rules new)
- **Removal only on a clear miss (buffer):** beta above 1.30, return below 12 %, margin below 40 %, net debt from 2.5 times, more than 30 % time under water or volatility above 35 %. Once = warning, two season reviews in a row = out. (since Nov 21, 2026)
- **Execution:** admissions and removals take effect in the shadow books only from the close of the next trading day after the season review. (since Nov 21, 2026)
- **Weighting:** equal. The ranking by 10-year return is only displayed. (since Nov 21, 2026) The 5-year return is shown alongside, information only, not a criterion (too short, too dependent on the starting point). (since Nov 21, 2026)
- **Replication as a savings plan:** new money split equally across current members; removed stocks are not sold but get no new money. (since Nov 21, 2026)
- **Index size:** no cap; every stock that meets the rules is in. Under observation. (since Nov 21, 2026)
- Hypothesis E, fixed in advance (both directions): on Nov 20, 2026 the Crown Jewels are split into weak (5-year return below half the 10-year return) and strong (list in data/these_e.json). The return of both groups over the following 12 months is compared, equally weighted in euros, each also against the S&P 500. Reversal confirmed if weak leads strong by at least 3 points; momentum confirmed if strong leads weak by at least 3 points; otherwise no difference. Verdict Nov 20, 2027. Only 11 stocks and one year: weak evidence, repeated every year. (since Nov 21, 2026)
- Hypothesis F, early warning 200-day line (fixed in advance): every month it is recorded which Crown Jewels are below their 200-day line (data/these_f.json). After 12 months the return of the group "below" is compared with "above", equally weighted. Early warning confirmed if "below" does at least 3 points worse on average across all snapshots. First verdict November 2027. Information only, not a rule; the line is shown in the Crown Jewels list. (since Nov 21, 2026)
- **Talent Scouting** (information only): a talent is not yet a Crown Jewel and over 5 years (weekly prices) returns at least 15 % a year, spent at most 15 % of the time more than 20 % below the high, has volatility of at most 30 % and a beta of at most 1.15; plus gross margin from 45 %, debt below twice EBITDA and revenue growth of at least 10 % a year over 3 years (since Nov 22, 2026). Updated at every season review; every list is recorded (forward test: who later becomes a Crown Jewel?). (since Nov 22, 2026)
- **Review calendar** on the page: all review dates fixed in advance with a countdown (power-law monthly close, monthly report, season review, verdicts November 2027 and 2031). **Traffic-light history:** red, yellow and green tiles per day, 7/30/90 days. **Explanations** ("i") on every tile. **S&P 500 versus gold** under "King of Kings". All information only. (since Nov 22, 2026)
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
- Additional bitcoin candidate from the next season (season 39, around end of January 2027): trend mix of the 50-, 100-, 200- and 300-day lines, partly invested (a quarter per line). Selection as always by a 504-trading-day lookback. (since Nov 21, 2026)
- Bitcoin lines compared (information only): hold, line 50, 100, 200, 300 and mix are tracked side by side, forward from Nov 20, 2026 and as a backtest, all results, not just the best. Cost 0.1 % per side. (since Nov 21, 2026)
- A season lasts 63 trading days; rules change only at season end. (since Nov 18, 2026)
- Verdict after four seasons (around November 2027): confirmed if the drawdown is smaller than holding and the return at most 2 points below. (since Nov 18, 2026)

## Shadow books (forward test, no real money)
- **Crown Jewels** since Nov 17, 2026, as a lump sum and as a savings plan (€100 per month), each against the S&P 500. Verdict November 2031: proven with at least 2 points more return per year, failed below the S&P 500. (since Nov 21, 2026)
- **S&P 500 savings plan** since Nov 17, 2026: "always immediately" vs "not at the high" (buy only 3 % below the all-time high), S&P 500 in euros. Review after one year. (since Nov 18, 2026)
- **Trend portfolio 16 markets** since Nov 20, 2026, no leverage, in euros, versus the S&P 500: six trend signals per market (price above the price 50/100/200 days ago; breakout above the 50/100/200-day high, active until the low is broken), weight = share of signals × 10 % target volatility / 60-day volatility / 16, long only, total at most 100 %, rest cash, executed at the next close, cost 0.05 % per side. Markets: SPY, QQQ, IWM, EFA, EEM, GLD, SLV, DBC, USO, TLT, IEF, HYG, VNQ, UUP, bitcoin, ethereum. Verdict after one year, without interest and taxes. (since Nov 22, 2026)
- **Tactical model 3 Kings** against all three held. (since Nov 18, 2026)

## Automation and site
- **News monitor** daily around 7 AM CET, Sundays and Mondays bitcoin only. Reasons are researched from: S&P 500 ±2 %, gold ±2.5 %, bitcoin ±5 %, each Crown Jewels stock ±4 % (rounded value, daily change in euros); then all three main assets get a line. (since Nov 21, 2026)
- **Monthly report** on the 1st of each month, **annual report** on January 1, each with the power law check and Crown Jewels changes. (since Nov 21, 2026)
- **Telegram:** daily reports and reports to the channel (Crown Jewels changes there neutrally in the monthly report); savings-plan steps for Crown Jewels changes privately only. (since Nov 21, 2026)
- **Watchdog:** every morning around 9 CET a check of the data run, prices, news and (start of month) the monthly report; on failure a private Telegram message, on Sundays a short sign of life. (since Nov 21, 2026)
- **Archive:** the homepage shows the last 7 days (news and histories); everything older is in the archive by month. Nothing is deleted. (since Nov 21, 2026)
