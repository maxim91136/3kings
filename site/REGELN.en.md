# Rule changes (log)

Rules change only at the end of a season or by explicit decision. Every change is recorded here. The German version is the original; this is a translation.

## 2026-11-18: Bitcoin gets the additional candidate Trend SMA100
Fast trend line, 100 days.
Reason: test on real prices, team Sharpe 1.25 instead of 1.12, same drawdown (15 %).
Caveat: the line was chosen after seeing the results (data snooping), so the p-value is optimistic.
Effect today: none, the bitcoin champion remains Trend SMA200. Watch live in the shadow book.

## 2026-11-18: Admission test for equity ETFs and Power Law (real data)
- Candidates tested: URTH, VT, QUAL, MTUM, USMV, XLK, TLT, IEF, EFA, EEM, ETH. None passed the rules (team Sharpe 1.25 without, 1.00 to 1.24 with the candidate). No change, nothing added to the bench.
- Power Law (causal, data from 2010): PL ramp Sharpe 0.87 = holding, but drawdown 49 % instead of 83 %. No better return. No signal in the heartbeat rule; information only.

## 2026-11-18: Bitcoin weighting level 2 (explicit decision)
- Capital allocation: inverse volatility, bitcoin weight x2 (spot, no leverage, total never above 100 %).
- Test 2017-2026: return 14.9 -> 17.6 %/yr, drawdown 15 -> 16 %, Sharpe 1.25 unchanged. Levels x3/x5 rejected (drawdown 21/29 %). Back-test, no guarantee.
- XLK as a fourth king and adding the ETFs/ETH/bonds: not added (little effect, too close to SPY).
- Admission test ETFs and Power Law (real data): all 11 candidates failed; Power Law ramp = holding with a smaller drawdown, not added.
- Next review of the rules: end of season.

## 2026-11-18: Fixed in advance how the rules are measured (before results exist)
Principle: no back and forth. Rules change only at the end of a season or by explicit decision, never by gut feeling.
1. Long-term test S&P 500 (longtest.py, price index from 1928): the trend filter counts as proven for the S&P only if it reduces the drawdown versus holding in the crisis epochs 1973-1982 AND 2000-2009. Otherwise it is reassessed for the S&P (next end of season).
2. Live check (shadow book, after 4 seasons = about Nov 2027): confirmed if the drawdown is smaller than holding and the return at most 2 points lower; failed if the return is more than 5 points lower AND the drawdown not smaller; otherwise keep watching.

### Result long-term test S&P (2026-11-18, price index 1930-2026, without dividends/interest)
Criterion 1 met: Trend SMA200 reduces the drawdown in 1973-1982 (48 -> 16 %) and 2000-2009 (57 -> 26 %). Overall: return 6.3 % vs 6.2 % (holding), drawdown 49 % vs 83 %. Weakness: 2010-2026 trend 6.6 % vs holding 11.8 %/yr. Volatility targeting protects much less in crashes (1930s 72 %, 2000s 47 %), but did better than trend in 2010-2026. No rule change.

## 2026-11-18: Study "buying in stages" (fixed in advance, before computing)
Idea: after a trend break, return early with part of the money instead of all at once. Exactly 3 rules, nothing added later (multiple-testing protection):
- R0 base: Trend SMA200 (all or nothing).
- R1 two stages: 50 % invested when price above SMA50; another 50 % when above SMA200.
- R2 three stages: one third each above SMA50, SMA100, SMA200.
- R3 deep stage: like R0, plus 50 % invested when price above SMA50 AND at least 20 % below the 252-day high (recovery after a deep decline).
Data: S&P 500 from 1930 (epochs as in longtest.py), bitcoin from 2011 (btc_long.csv, four epochs). Costs 5 bps (S&P) or 10 bps (BTC) per rebalancing.
Criterion: a rule counts as better than R0 only if (a) its Sharpe is at least as good as R0 in most epochs (S&P: at least 4 of 6, BTC: at least 3 of 4), (b) overall Sharpe at least +0.03, (c) the maximum drawdown is no more than 3 points worse overall and no more than 5 points worse in the S&P crisis epochs 1973-1982 and 2000-2009. If several pass, the simplest applies. Valid only if the criterion is met for the S&P AND bitcoin; otherwise no change. Earliest implementation at end of season.

### Result study "buying in stages" (2026-11-18, staged.py)
S&P (1930-2026): R1/R2/R3 miss the criterion (Sharpe at least as good as R0 in only 3 of 6 epochs; overall +0.01 to +0.02). Stages help 1930-1982 and hurt 1983-2009 (false signals). Bitcoin (2011-2026): all three meet the criterion (R1: Sharpe 1.20 -> 1.37, drawdown 78 -> 71 %, better in 4 of 4 epochs). Overall criterion (S&P AND bitcoin) NOT met -> no rule change. Open for end of season: bitcoin stages (R1) as an explicit individual decision, not by rule.

## 2026-11-18: Review (Opus), fixed in advance before computing (review.py)
Assumptions: S&P price index 1928-2026 without dividends, cash without interest (the two roughly offset). Tax: 26.375 % German capital gains tax, 30 % partial exemption (equity ETF) = 18.46 % on realised gains, loss carry-forward, allowance ignored. Costs 5 bps per rebalancing. Rebalancing only at more than 2 points deviation.
Question 1, fixed champion for the S&P: Trend SMA200 replaces the champion selection for the S&P if, after tax over 1930-2026, it has (a) a return at most 0.3 points below the champion selection, (b) a smaller overall drawdown and (c) smaller drawdowns in 1973-1982 and 2000-2009.
Question 2, buying rule for new money (same amount monthly, windows of 10 and 20 years, start every 6 months from 1930):
  K1 buy immediately, never sell; K2 buying pause: buy only above SMA200, otherwise accumulate, buy the accumulated amount on the signal, never sell; K3 full trend (buys and sells with SMA200); K4 dip reserve: 80 % immediately, 20 % reserve, reserve fully invested at a decline >= 20 % from the 12-month high, never sell; K5 current champion selection.
  Recommended is the rule with the highest median final wealth after tax over 20-year windows. Another rule is recommended only if its median is at most 2 % lower AND its worst paper loss (value/paid in) is at least 10 points smaller in the median window.

### Result review (2026-11-18, review.py)
Question 1 MET: after tax 1930-2026 Trend SMA200 5.2 %/yr, drawdown 49 % vs champion selection 4.3 %/yr, 64 % (crises 17 vs 22 %, 26 vs 49 %). Holding 6.0 %/yr, 83 %. -> From now on the S&P plays Trend SMA200 permanently (heartbeat.py FIXED). Team 2017-2026 practically unchanged (17.6 %/yr, drawdown 17 instead of 16 %, Sharpe 1.26).
Question 2: 20-year windows, median final value/paid in: K1 immediate 2.14; K2 buying pause 2.14; K4 dip reserve 2.08; K3 full trend 1.82; K5 champion 1.69. Recommended by the criterion: K1 (buy immediately). K2 same median, worst paper loss −38 instead of −67 %, but median paper loss only 4 points smaller (criterion 10) -> not recommended, possible only as an explicit decision.
Site: "New money / S&P 500 only" now shows K1 (buy, full amount) plus the trend state as information.

## 2026-11-18: Buying rule for new money = "not at the high" (explicit decision)
Starting idea: don't buy at the all-time high. ath.py (S&P 1930-2026, monthly, before tax): "not at the high" (buy only if at least 3 % below the all-time high, otherwise accumulate) 20-year median 2.43 vs immediate 2.44, better in 41 % of windows, practically free. "Wait for −10 %" costs clearly (2.18). Buying from −20 % earned more on average (5 years 10.9 vs 8.7 %/yr at the high), but buying at the high was not more often negative than at −3 to −20 %.
Rule: S&P within 3 % of the all-time high -> accumulate; otherwise buy the amount plus reserve. Replaces K1 on the site.

## 2026-11-18: Study "valuation + fear" for the buying rule (fixed in advance, valuation.py)
New money monthly, S&P price index, before tax, cash without interest, dividends not included. Valuation = Shiller P/E as a percentile of its OWN history up to each day (causal). Fear = VIX (only from 1990).
Rules: N "not at the high" (current rule, buy from 3 % below the all-time high). B1 valuation brake: if the P/E is in the top fifth of its history, buy only from 10 % below the high, otherwise like N. B2 like B1, but only from 20 %. B3 like B1, but accumulated money is invested after 12 months at the latest. A1 (from 1990) fear buy: like N, plus everything is invested immediately at VIX >= 30, even near the high. A2 (from 1990): B1 plus fear buy (VIX >= 30 lifts the brake).
Criterion: a rule replaces N only if, over 20-year windows (10-year windows for the fear rules), the median final value is at most 1 % below N AND the worst 10 % are better than N, OR the median is at least 2 % above N.

### Result study "valuation + fear" (2026-11-18)
No rule meets the criterion, N stays. 20 yrs from 1930: N 2.43 | B1 2.26 (longest wait 6.2 yrs) | B2 2.19 (9.6 yrs) | B3 2.40. Reason: since 1995 the Shiller P/E was in the top fifth of its history on 94 % of days, so a valuation brake waits for years. 10 yrs from 1990: A1 (fear buy VIX >= 30) identical to N, because high fear always coincided with prices more than 3 % below the high, so N already buys in fearful phases. A2 1.47 vs N 1.53.

## 2026-11-18: Addendum "relative valuation" (fixed in advance, valuation.py --relativ)
Shiller P/E as a percentile of only the last 10 or 20 years (causal). R10/R20: in the top fifth of that window buy only from 10 % below the high, otherwise like N. R10c: like R10, but buy anyway after waiting 12 months at most. G10: in the bottom fifth of the last 10 years buy immediately, even near the high, otherwise like N. Same criterion as above (20-year windows from 1930).
Result: no rule meets the criterion, N stays. N 2.43 | R10 2.19 | R20 2.26 | R10c 2.37 | G10 2.43 (identical to N: cheap phases always coincided with prices below the high). Relatively "expensive" on about 36 % of days, so the brake then misses the upswings.

## 2026-11-18: Study "relative strength for new money" (fixed in advance, strength.py)
1 unit of new money monthly, never sell, costs 5 bps (BTC 10 bps). Window 5 years, start every month. Rules:
M0 everything into the S&P (comparison). M1 split equally across all. M2 everything into the strongest of the last 6 months. M3 everything into the strongest of the last 12 months excluding the last month (12-1). M4 like M3, but only if its 12-month return is positive, otherwise accumulate until one is positive (dual momentum). M5 everything into the weakest of the last 12 months (contrarian).
Test A: bitcoin, S&P, gold (2015-2026). Test B: S&P and gold only (without bitcoin). Test C: broad ETFs VT, EEM, IEF, XLK (2008-2026, prices including distributions).
Criterion: a rule beats M0 only if its median final value in Test B AND Test C is at least 3 % above M0 (above VT in Test C) and it leads in both halves of the start dates. Test A alone does not count (bitcoin look-back).
Result: no rule meets the criterion, no change. Test B (S&P/gold): all rules 1.42-1.43 vs S&P 1.49. Test C: strength 12-1 (M3/M4) 1.48 vs world ETF 1.29, but buys almost only XLK (tech look-back 2008-2026), contrarian (M5) 1.14. Test A (with bitcoin): everything that adds bitcoin beats the S&P (1.96-2.17), contrarian best (2.17); look-back only, does not count.

## 2026-11-18: Buy signal in euros (eurtest.py)
Euro investor 2004-2026, 10-year windows, values in euros: immediate 2.121 | signal in dollars 2.125 | signal in euros 2.125 (at least as good as immediate in 100 % of windows). Signals differ on 21 % of days. -> Signal and savings-plan shadow book now use the S&P in euros (sparplan.py, USE_EUR).

## 2026-11-18: Euro view for the team model (finding only, no change)
Team 2017-2026 in euros: 15.4 %/yr, drawdown 16 %, Sharpe 1.07 (in dollars 17.6 %, 17 %, 1.26). Holding in euros 22.9 %/yr, drawdown 25 %. The gap to holding is larger in euros because the cash share does not capture the dollar gains. Trend signals in dollars vs euros differ: bitcoin 2 %, S&P 12 %, gold 22 % of days. Whether the team model should compute in euros: decision at end of season. Site shows the distance to the all-time high for all three in euros.

## 2026-11-18: Long-term test gold (fixed in advance, goldtest.py)
Data: monthly gold price (datasets/gold-prices, USD) from 1971-08 (end of fixed gold price). Monthly signals, costs 5 bps, cash without interest. Holding vs 10-month trend (roughly 200 days).
Criterion: the trend filter counts as proven for gold if it reduces the largest drawdown overall AND in the bear epoch 1981-2000, and the overall return is at most 2 points per year below holding. Then gold plays Trend SMA200 permanently on the test bench (like the S&P). Otherwise gold plays holding permanently.
Result gold (1971-2026, monthly): trend 10.1 %/yr, drawdown 32 % vs holding 8.6 %/yr, 62 %; 1981-2000 drawdown 31 vs 54 %. Criterion MET -> gold plays Trend SMA200 permanently on the test bench.
Note: in the short window 2017-2026 (euros) the team model with the gold trend was weaker (12.9 %/yr, drawdown 21 %, Sharpe 0.94) than with the gold selection (15.4 %, 16 %, 1.07). The long-term data count (fixed in advance).

## 2026-11-18: Test bench computes in euros (explicit decision)
heartbeat.py converts all prices to euros (to_eur). Finding 2017-2026 in euros: team model 12.9 %/yr, drawdown 21 %, Sharpe 0.94; holding all three equally 22.9 %/yr, drawdown 25 %, Sharpe 1.19. In euros the team model trails holding even risk-adjusted; assess honestly at end of season.

## 2026-11-18: Cross-check total return, interest, inflation, start 1929 (fixed in advance, totalreturn.py)
Occasion: criticism by a second AI (Gemini): price index without dividends, cash without interest, nominal, start only 1930. Data: Shiller (datasets/s-and-p-500), monthly 1871-06/2023 (dividend, inflation, 10-yr rate). Total return = (price + dividend/12) / previous month's price - 1. Cash rate unknown (only the 10-year rate available): test with 0 % and with 50 % of the 10-year rate as a rough proxy for savings/short bonds. Real = deflated by US inflation (CPI). Costs 5 bps. No taxes.
Question A (buying rule): 1 unit monthly, 20-year windows, start every 6 months from 1929-01 (including 1929), total return, cash with interest. "Not at the high" (buy from 3 % below the all-time high, monthly prices) holds if its median final value is at least 99 % of "buy immediately" AND the worst 10 % are no more than 1 % lower. Separately: start at the September 1929 high and in March 2000 (20 and 10 years), information only.
Question B (trend): 10-month trend (~200 days) on total return with cash interest vs holding, epochs as in longtest.py. The trend stays proven if it reduces the drawdown versus holding in 1973-1982 and 2000-2009 AND the overall return is at most 1.0 point/yr below holding (nominal, cash at 50 % of the 10-yr rate). Otherwise the trend as a crash brake is reassessed (end of season).

### Result cross-check total return (2026-11-18, totalreturn.py, Shiller 1929-2023)
Question A: criterion NOT met (7 of 8 variants). With dividends and interest, "not at the high" costs more than in the price-index test: 20 yrs nominal median 3.39 vs immediate 3.46 (about 2 % less), 10 yrs 1.74 vs 1.79 (about 3 %); better than immediate in only 1-12 % of windows (previously 41 %). Single starts Sept 1929, March 2000, Jan 1973: practically identical to immediate. Worst 10 % only about 1-4 % worse. The earlier finding "practically free" only holds without dividends and was too optimistic; the criticism was justified.
Question B: the 10-month trend stays proven: 1930-2023 total return 10.9 %/yr, drawdown 22 % vs holding 9.8 %/yr, 78 %; 1973-1982 11 vs 39 %, 2000-2009 6 vs 49 %. Weakness remains 1983-1999 and 2010-2023 (2-3 points/yr behind holding).
The "not at the high" rule was an explicit decision (principle); its cost is now known: about 2-3 % of final wealth in the median. Change only by explicit decision.

## 2026-11-18: Buying rule for new money = buy immediately (explicit decision, replaces "not at the high")
Reason: total-return cross-check (totalreturn.py): "not at the high" costs 2-3 % of final wealth and was better than immediate in only 1-12 % of windows. Principle: numbers before principle. The site always shows "Buy". "Not at the high" continues as a comparison in the savings-plan shadow book (sparplan.py: regel_signal). Review: after one year. To undo: couple signal in sparplan.py back to buy.

## 2026-11-18: Elite 9 and factor ETFs (display and shadow book only, no money)
Exception to "no single stocks": observation only, no recommendation, no influence on the buying rule.
Elite 9 (starting list of 2026-11-18, selected in HINDSIGHT, source of the figures unclear): CME Group, Ferrari, Waste Management, Mastercard, Visa, Cintas, Hermès (Paris, EUR), Microsoft, Alphabet. The list's 9 rules: beta < 1.15; gross margin > 50 %; monopoly/duopoly; no cyclicality; pricing power; no existential disruption risk; 10-year return (total return) ~17 % p.a.; debt/equity < 1.0; growing moat.
Computed automatically (from prices): beta (daily, 5 years, against the S&P 500) and 10-year return p.a. Everything else (margin, monopoly, cyclicality, disruption, moat, debt) is NOT checked, only taken over. Computed values are compared with the list values; deviations > 3 points are shown.
A back-test of the list is worthless (survivorship: rule 7 selects past winners). It is shown for illustration only and labelled as such. THE test is the Elite shadow book from 2026-11-18: 9 stocks equal weight, in euros, against the S&P 500 in euros.
Criterion (after 3 years, from 2029-11): proven if the return is at least 2 points per year above the S&P AND the drawdown not larger; failed if the return is below the S&P; otherwise keep watching. After 1 year an interim status only, no verdict.
Factor ETFs: QUAL (quality), MTUM (momentum), USMV (min. volatility), XLK (tech), plus VT and URTH (world) against SPY, in euros, from 2015-07. Display: return per year, drawdown, Sharpe, beta. Admission test of 2026-11-18: all failed (see above). No new rule.

## 2026-11-18: Elite 9 becomes Elite 5 (explicit decision: whoever fails the rules is out)
Only rule 1 (beta < 1.15) and rule 7 (10-year return >= 17 % p.a., read strictly) can be checked. Result from prices: passed: Mastercard (0.89 / 20.7), Visa (0.82 / 18.6), Ferrari (0.90 / 23.3), Cintas (0.77 / 24.4), Microsoft (1.09 / 25.0). Out: Alphabet (beta 1.19), CME (14.8 %), Waste Management (15.5 %), Hermès (14.0 %). The list is frozen from now on (no automatic change). The Elite shadow book restarts with the 5, equal weight, in euros, against the S&P 500; criterion unchanged (3 years, +2 points p.a., drawdown not larger). The other seven rules remain unchecked.

## 2026-11-18: Screening for further Elite candidates (fixed before computing)
Universe: about 130 well-known quality companies US/Europe (list in screen.py). Hard rules as for Elite 5: beta < 1.15 (5 years daily, in euros against the S&P 500 in euros) AND 10-year return >= 17 % p.a. (home currency, including dividends). Those that pass are then assessed by hand against the soft rules (margin > 50 %, monopoly, not cyclical, debt < 1, no disruption risk); this assessment is judgement, not measurement. Admission only by explicit decision. Note: selecting by past return finds, by definition, the winners of the past.

## 2026-11-18: Screening result, Elite 5 becomes Elite 6 (explicit decision)
About 40 of 130 pass the hard rules; after the soft rules (judgement) remain IDEXX (beta 1.09 / 19.7 %), ASML (30.3 %, but cyclical), Constellation Software (18.8 %), Deutsche Börse (18.3 %; beta of European stocks measured too low because of time zones). Admitted: IDEXX only. ASML not (cyclical, the rule applies), although unique. The shadow book restarts with 6, criterion unchanged.

## 2026-11-18: Elite 6 admission values frozen
Beta and 10-year return of the Elite 6 are fixed as of 2026-11-18 (data/elite_frozen.json), no nightly recalculation. Going forward, only the shadow book measures. A new snapshot only on explicit review.

## 2026-11-18: Margin rule clarified (explicit decision)
Gemini check: Cintas gross margin 49.7 % (Q4 FY 2025), just below 50 %. Decision: Cintas stays. The margin rule is a soft rule (judgement) and from now on reads "gross margin around 50 % or more, tolerance 1 point". The hard rules (beta < 1.15, 10 yrs >= 17 %) stay without tolerance.

## 2026-11-18: Elite shadow book extended to 5 years (explicit decision)
Verdict after 5 instead of 3 years, i.e. from 2031-11. Criterion otherwise unchanged (at least +2 points p.a. above the S&P 500 with no larger drawdown = proven; return below the S&P = failed). Interim status yearly, without a verdict. Changed before the first data point, i.e. without knowledge of results.

## 2026-11-19: Test buying rule for single stocks (fixed before computing)
Question: does waiting for a distance to the all-time high pay off for single stocks?
Universe: all ~130 companies from screen.py (not just the Elite 6, otherwise survivorship is maximal). Remaining bias: the universe also consists of today's large companies.
Per stock: from 2006-01 (or once 10 years of history exist) 1 unit of money each month. "immediate": buy immediately. "wait X" (X = 10, 15, 20, 25 %): accumulate money (2 % interest p.a.), buy everything once price <= (1 - X) * previous high. End 2026-11: value per unit paid in, remaining cash counts with interest. Adjusted prices (including dividends), home currency, month-end values.
Criterion: a waiting rule counts as proven if it (a) yields at least 3 % more final wealth in the median across all stocks, (b) beats immediate for at least 60 % of stocks, and (c) both also hold for 2016-2026 alone. Otherwise: not valid. The result only changes what the site shows, no purchases.
Display: distance to the high per Elite stock (current, information only).
Result 2026-11-19 (138 stocks, MMC without data): waiting is clearly worse for single stocks. From 2006 median: 10 % −3.4 %, 15 % −6.9 %, 20 % −10.0 %, 25 % −16.3 %; better for only 7-10 % of stocks. From 2016: −4.5 / −8.1 / −13.3 / −21.4 %; better for 9-21 %. Criterion clearly missed in both periods. Waiting rule for single stocks: NOT VALID. Remaining bias: universe of today's large companies.

## 2026-11-19: Waiting to buy bitcoin (same setup as single stocks, monthly money, 2 % interest on waiting money)
Rolling windows from 2013 (3 and 5 years). Waiting for −20/−30/−40/−50/−60 % from the high: median −6 to −17 %, better in only 10-27 % of start months. Whole period 2013-2026: −30 to −53 %. Not valid. Limitation: a single asset, short history.

## 2026-11-19: Test "only the largest" (S&P 500 Top 20), fixed before computing
The iShares S&P 500 Top 20 (IE000VA628D5) only exists since 11/2024, too short. Substitutes with the same idea: XLG (S&P 500 Top 50, from 2005) and OEF (S&P 100, from 2000), against SPY, prices including distributions, in euros.
Criterion (as for factor ETFs): admission only if the return p.a. is higher AND higher in BOTH halves (to 2015 / from 2015) AND the maximum drawdown is not larger than SPY. Otherwise display only.
Result (in euros, 2005-06 to 2026-11): XLG 11.4 %/yr (drawdown 47 %) vs SPY 11.3 % (51 %); to 2015 6.8 vs 8.0 %; from 2015 15.3 vs 14.0 %. OEF: 11.5 vs 11.3 %; to 2015 7.3 vs 8.0; from 2015 15.0 vs 14.0. Practically equal over 21 years, the lead only since 2015 (mega-cap phase), worse before. Criterion (both halves) missed. Not admitted. The Top 20 is even more concentrated (NVIDIA, Apple, Microsoft alone over 40 %), i.e. a bet on the last ten years continuing.

## 2026-11-19: Waiting to buy gold (same setup as bitcoin and single stocks)
Monthly money, 2 % interest on waiting money, rolling 5- and 10-year windows from 1975 (monthly data in dollars). Waiting for −10 to −30 % from the high: median ±0 % (gold was almost always below its old high from 1980 to 2008, so the rule bought immediately anyway), better in only 14–35 % of start months, worst case −54 %, best +19 %. Not valid. With this, "buy immediately" has been tested for all three assets (S&P 500, bitcoin, gold) and for single stocks.

## 2026-11-19: Site general and bilingual
The site is written without reference to any personal holdings and treats all three assets equally. Header: per asset the price, change, distance to the high and the test result "Buy". Calculator with a freely chosen split (default one third each, no weighting recommendation). Languages German and English.

## 2026-11-20: Study "time horizons" (fixed in advance, before computing; horizon.py + horizonlong.py)
Question: is SMA200 as the trend line a lucky hit, or does it sit on a plateau? And do the team model's look-back 504 / season 63 fit?
Fixed selection (nothing added later, ALL results are shown):
- Lines: SMA 50, 100, 150, 200, 300 (price above = invested, otherwise cash). Gold monthly only: 3, 5, 7, 10, 14 months (roughly 63..294 days).
- Part 1 short (horizon.py, real prices 2015-2026, euro view not included): lines per player.
- Part 1 long (horizonlong.py): S&P 500 from 1930 in the epochs of longtest.py (6 epochs); bitcoin from 2011 in 4 epochs (2011-2014, 2015-2018, 2019-2022, 2023-2026); gold monthly from 1971 (information). Price index, cash without interest, costs 5 bps (BTC 10 bps).
- Part 2 (horizon.py, 2015-2026): team model look-back 252/504/756 x season 21/63/126, information only.
Criterion for a line (replacing SMA200): another line N replaces SMA200 only if, for the S&P AND bitcoin:
 (a) overall Sharpe at least +0.05 versus SMA200;
 (b) Sharpe at least as good as SMA200 in most epochs (S&P at least 4 of 6, BTC at least 3 of 4);
 (c) overall maximum drawdown no more than 3 points worse, and in the S&P crisis epochs 1973-1982 and 2000-2009 no more than 5 points worse than SMA200;
 (d) plateau: both neighbouring lines of N (in the order 50-100-150-200-300) have an overall Sharpe at least that of SMA200 (no isolated peak).
 Multiple-testing protection: 4 alternatives per asset, so (a) to (d) apply jointly and for both assets. If several pass, the simplest applies (SMA200 stays on a tie).
 Gold: information only, no rule change (gold is fixed at SMA200 after the long-term test).
Criterion part 2: no rule change from part 2 alone (only 11 years, one regime). Judge findings only by plateau. Change at the earliest at end of season by explicit decision.
If the criterion is not met: SMA200 stays; a different line choice counts as not proven.

### Result study "time horizons" (2026-11-20, horizon.py + horizonlong.py)
Criterion NOT met, no rule change: SMA200 stays.
- S&P 1930-2026 (overall Sharpe): SMA50 0.52 | 100 0.53 | 150 0.53 | 200 0.57 | 300 0.56 (holding 0.42). Drawdown 47-53 % instead of 83 %. All lines sit on a plateau; the length hardly matters, the trend filter itself counts. No alternative passes (a) and (b) (epochs better than SMA200: 2-3 of 6, 4 needed). SMA300 is almost equal (plateau, drawdown ok), but not +0.05 better.
- Bitcoin 2011-2026 (overall Sharpe): SMA50 1.27 | 100 1.16 | 150 1.07 | 200 1.03 | 300 0.99 (holding 0.90). SMA50 and SMA100 pass all four points for bitcoin, but not for the S&P; the test requires both. Caveat: short lines switch often (13 and 8 times per year), costs of 10 bps included, taxes not.
- Gold monthly (information only): 3 to 14 months all Sharpe 0.66-0.72, drawdown 29-40 % instead of 62 %; again a plateau.
- Short window 2017-2026 (part 1): S&P and gold lines all trail holding on return (SPY 7-10.5 % vs 13.9 %), with about 20 % instead of 34 % drawdown.
- Part 2 (team model, 2017-2026): look-back 504 sits on a plateau (Sharpe 1.11-1.14, drawdown 14-17 %, across all three season lengths). Look-back 252 is weaker (Sharpe 1.04-1.08, drawdown 22-25 %). The peak value look-back 756 / season 126 (1.23) has weaker neighbours (1.06 and 1.14): isolated peak, not adopted.
Open for end of season: bitcoin line (SMA50/100 beat SMA200 for bitcoin alone; SMA100 is already a candidate in the bitcoin squad, the data-snooping caveat of 2026-11-18 applies).

## 2026-11-21: Test "FTSE All-World vs S&P 500" (fixed before computing; ftse.py)
Question: is a global index better than the S&P 500 as the core?
Data: the actual FTSE All-World via the Vanguard FTSE All-World ETF (VWRL, launched 05/2012; older data not freely available) vs SPY, prices including distributions, in euros, same period. ETF costs are included in the prices.
Metrics: return p.a., maximum drawdown, both halves of the period, share of rolling 5-year windows with a lead, savings plan €100/month.
Criterion (as for factor ETFs and the Top 20): the FTSE All-World replaces the S&P 500 as the core only if return p.a. is higher AND higher in BOTH halves AND the maximum drawdown is not larger. Otherwise display only.
Data correction (before evaluation, noticed after the first run): the Yahoo series for VWRL has a one-day jump of −24 % in 2013 without a matching market move (data error). Rule: a daily FTSE move above 12 % while SPY moves less than 5 % counts as a data break; the test starts after the last break. The criterion is unchanged.

### Result "FTSE All-World vs S&P 500" (2026-11-21, ftse.py)
Period 06/2013 to 11/2026 in euros, including distributions. S&P 500 15.2 %/yr (x6.68), FTSE All-World 11.8 %/yr (x4.46). Halves (split 03/2020): until 2020 15.3 vs 10.3 %, from 2020 15.1 vs 13.3 %. Maximum drawdown 33.1 vs 33.3 %: broader diversification did not reduce the drawdown. Rolling 5-year windows: FTSE ahead in 0 of 102. Savings plan €100/month (€16,200 paid in): €46,076 vs €37,433.
Criterion NOT met (on any point). The S&P 500 remains the core. Caveat: only 13 years and a period of strong US outperformance; before that (e.g. 2000-2009) the world was ahead of the US. The test therefore only covers this period, not that it is always so.

## 2026-11-21: Monthly power law check for bitcoin (powerlaw.py, fixed before evaluation)
Midline (fair value): 1.0117e-17 × days^5.82 (days since Jan 3, 2009, in dollars). Floor: 0.42 × midline, matched to the red floor on bitbo on Nov 21, 2026 (about $68,000).
Check: every completed month at the monthly close (last daily close, dollars). A close below the floor = "floor broken this month". Prices within the month do not count. Shown: current status, consecutive months below, and all months below since 2015.
Consequence: information only. The buy rule (buy as soon as there is money) is unaffected; the model is adjusted only by explicit decision.
First evaluation (data from 07/2015): monthly closes below the floor so far only 06/2026 ($58,524, 1.7 % below). Lowest earlier monthly closes: 12/2022 and 09/2015 (each just above the line, 0.43 × midline). November 2026 is running at about 0.36 × midline (as of Nov 20).

## 2026-11-21: Long-term extension "World vs USA" (fixed before computing; worldlong.py)
Reason: the FTSE test covers only 13 years (one period of US outperformance). The FTSE All-World itself is not freely available over long periods; substitute with the same idea from one source (MSCI, gross total return, month-end, dollars): MSCI World and MSCI ACWI (world incl. emerging markets) vs MSCI USA (practically the S&P 500). Calculated in dollars; for a euro investor the currency changes both sides equally, so the comparison is the same.
Period: as far as the free MSCI interface reaches. The first request showed: requests before 01/1997 are rejected; monthly values are delivered from 12/2000. The 1970s/80s (incl. the Japan bubble, when the world was ahead) are therefore missing.
Metrics: return p.a., largest drawdown, individual decades, share of rolling 10- and 20-year periods with the world ahead.
Criterion as in the FTSE test: the world replaces the S&P 500 as the core only if return p.a. is higher AND higher in BOTH halves AND the largest drawdown is not larger. Otherwise the S&P 500 stays; the result is displayed.

### Result "World vs USA" (2026-11-21, worldlong.py)
Period 12/2000 to 10/2026 (almost 26 years), MSCI gross total return in dollars. USA 9.0 %/yr, World 8.0 %, ACWI 7.9 %. Halves (split 11/2013): until 2013 USA 4.5 % vs World 4.8 % / ACWI 5.1 % (world ahead); from 2013 13.7 vs 11.3 / 10.7 % (USA ahead). Largest drawdown USA 50.6 %, World 53.7 %, ACWI 54.6 % (the world fell deeper, not less). Decades: 2000s USA 0.0 % p.a., World 1.8 %, ACWI 2.7 %; 2010s 13.6 vs 10.1 / 9.4 %; 2020s so far 15.0 vs 13.3 / 12.7 %. Rolling: 10 years world ahead in 36 (World) or 43 (ACWI) of 191 periods (19-23 %), 20 years in 0 of 71.
Criterion NOT met (first half narrowly ahead, but total return, second half and drawdown missed). The S&P 500 remains the core. The lost US decade 2000-2009 is included: the world was ahead there, but only by 2 to 3 percentage points p.a. and with a deeper drawdown. Still not included: the 1970s/80s.

## 2026-11-21: Elite season review (explicit decision)
From now on the Elite is reviewed at EVERY season end (season = 63 trading days as in the test bench; first season end around late January 2027). Automatic in the nightly data run (elitecheck.py, elite_review.py) as soon as a new season begins.
Checked: the hard rules with current prices, same method as the screening: beta < 1.15 (5 years daily, in euros against the S&P 500 in euros) AND 10-year return >= 17 % p.a. (incl. dividends). Whoever fails is dropped, no exceptions (as decided on 2026-11-18). Vacant places are NOT refilled automatically; admission only via screening and explicit decision.
Shadow book: continues chained (value at the time of removal = new base, the remaining stocks equally weighted from the review date). The final verdict in November 2031 is unchanged.
Admission values are re-frozen on the review date. Every review is entered here automatically. The soft rules (margin around 50 % with 1 point tolerance, market position, cyclicality, debt) are not checked automatically.
Status at introduction (prices Nov 20, 2026): all 6 pass (Ferrari 0.90 / 23.0 %; Mastercard 0.88 / 20.1 %; Visa 0.81 / 18.1 %; Cintas 0.76 / 24.0 %; Microsoft 1.09 / 24.5 %; IDEXX 1.09 / 19.0 %). Close: Microsoft and IDEXX on beta (1.09 of 1.15), Visa on return (18.1 of 17 %).

## 2026-11-21: Elite season review changed: two seasons in a row (explicit decision)
Reason: a single review is a snapshot; borderline cases (e.g. Visa 18.1 % against a limit of 17 %) could be dropped through noise, with no automatic re-entry. An annual review would also be just a snapshot, only less frequent.
New: a stock that fails a season review is warned. A stock that fails two season reviews IN A ROW is dropped (no exceptions). A stock that passes again after a warning is back to zero. Real decline is thus detected after about half a year. Everything else from the previous entry is unchanged. Change made before the first review, i.e. without knowledge of any result.

## 2026-11-21: Elite as its own index with bench and substitution (explicit decision)
Universe (renewed every season): current S&P 500 members (with GICS industry) + a fixed European list (data/elite_universe.json). Cyclical industries are excluded beforehand and not calculated at all (frozen on Nov 21, 2026, approved):
- Entire sectors: Energy, Materials, Real Estate.
- Industries: Advertising, Broadcasting, Publishing; automobile manufacturers and parts, homebuilding, home improvement retail, homefurnishing retail, hotels/cruise lines, casinos, leisure products, apparel/accessories/luxury, footwear, computer & electronics retail, consumer electronics; banks (diversified and regional), investment banking/brokerage, consumer finance, asset management/custody banks; agricultural machinery, air freight/logistics, building products, cargo ground transportation, construction/engineering, construction machinery/heavy trucks, electrical components, heavy electrical equipment, industrial machinery, passenger airlines, rail, trading companies/distributors, industrial conglomerates, human resource services, passenger ground transportation; semiconductors, semiconductor equipment, electronic components, electronic manufacturing services, technology hardware/storage, communications equipment, technology distributors, electronic equipment/instruments.
- Europe non-cyclical: Ferrari, Hermès, L'Oréal, EssilorLuxottica, Dassault Systèmes, Wolters Kluwer, SAP, Deutsche Börse, Munich Re, Novo Nordisk, LSEG, RELX, Experian, Diageo, Unilever, Nestlé, Lindt, Constellation Software. Cyclical (excluded): LVMH, Schneider Electric, Air Liquide, ASML, DSV, Atlas Copco, Investor AB, Sika, Partners Group, Evolution.
Admission criteria (all, automatic): beta < 1.15 (5 yrs daily, euros vs S&P 500 in euros); 10-year return >= 17 % p.a. (home currency, incl. dividends); gross margin >= 49 % (around 50 %, 1 point tolerance); debt/equity < 1 (margin and debt from Yahoo fundamentals).
Bench: whoever passes all admission criteria in two season reviews in a row. Size of the Elite: 6 places. When a place becomes free, the bench player with the highest 10-year return is proposed privately via Telegram; only the operator's private chat can confirm or reject (after a rejection the next one follows). After confirmation: admission, shadow book chained (all equally weighted from that day), entry here automatically. Without an answer the place stays free; reminder after 7 days.
Staying: unchanged under the two hard rules (beta, 10-year return), failed two season reviews in a row = out. Margin and debt apply only to admission.
First screening: Nov 21, 2026 (counts as season 38). Bench at the earliest after the next season review (around late January 2027).
Limitation: the universe consists of today's large companies; selection by past returns.

## 2026-11-21: Elite 6 becomes the "Crown Jewels" (explicit decision)
Reason: in the first screening 12 companies met all admission rules; a fixed limit of 6 would be arbitrary (places 6 and 7 differ only in past return) and invites back and forth.
New:
1. Dynamic index: whoever meets all rules is in, equally weighted. No fixed size. Replaces "6 places" and "bench" from the previous entry.
2. Same rules for admission AND staying (four rules): beta < 1.15; 10-year return >= 17 % p.a.; gross margin >= 49 %; net debt/EBITDA < 2 (debt minus cash divided by operating profit). Replaces debt/equity < 1: that ratio is distorted by share buybacks (Mastercard 3.5, MSCI/AbbVie/HCA negative equity) although the companies are soundly financed. Negative or missing EBITDA = not passed.
3. Beta from weekly closing prices (5 years = 260 weeks) instead of daily prices: daily prices distort the beta of European stocks because of different trading hours (Deutsche Börse daily 0.05). Recalculated (prices Nov 20, 2026): Ferrari 0.84, Mastercard 0.81, Visa 0.75, Cintas 0.69, Microsoft 1.05, IDEXX 1.11.
4. In: passed all four rules in two season reviews in a row, then a proposal via Telegram (private), admission after confirmation; a rejection holds until the next season review. Out: failed two season reviews in a row (automatic). On every change the shadow book is chained, all equally weighted (rebalancing only on changes, i.e. at most at season ends).
5. Start: the existing six stocks. Further admissions at the earliest after the next season review (around late January 2027). The final verdict of the shadow book (November 2031) stays.

## 2026-11-21: Crown Jewels: automatic admission, equal weight (explicit decision)
Admission without confirmation: whoever passes all four rules in two season reviews in a row is admitted automatically at the season review (index logic, no individual decision). Telegram reports admissions, removals and warnings privately, for information only. Replaces point 4 ("proposal via Telegram, admission after confirmation") of the previous entry.
Equal weighting stays: the ranking by 10-year return is the past and not a measure of quality; weighting by it would be a bet on continuation. Weighting by market value would be dominated by Microsoft, Visa and Mastercard. Equal weight is the neutral rule without estimation. The ranking is only displayed.

## 2026-11-21: Test "Buffer for the Crown Jewels" (fixed before computing; buffertest.py)
Question: which gap between the admission and removal limits prevents back and forth without costing return? Background: replicated privately as a savings-plan index that never sells (removed stocks get no new money but stay held).
Data: the non-cyclical companies of the screening of Nov 21, 2026, daily prices (Yahoo, incl. dividends) from 2006, in euros. Review every quarter from 2016 (63 trading days). In: beta < 1.15 (weekly prices, 5 years) AND 10-year return >= 17 %, two reviews in a row.
Variants (out after two reviews in a row outside): no buffer (beta > 1.15 or < 17 %), narrow (> 1.20 or < 15 %), medium (> 1.25 or < 14 %), wide (> 1.30 or < 12 %).
Savings plan: €100 per month, equally split across current members, never sell. Comparison: the same savings plan on the S&P 500.
Metrics: changes per year; "returners" (out and back in within 8 quarters); final value and return p.a. (internal rate of return).
Criterion: the buffer with the fewest returners whose savings-plan return is at most 0.5 points p.a. below "no buffer"; plateau: at least one neighbour similar. Otherwise no buffer.
Limits: margin and debt not available historically, only beta and return tested. Today's company list (bankruptcies missing, return too high); uncritical for comparing the variants with each other.

### Result "Buffer for the Crown Jewels" (2026-11-21, buffertest.py)
254 companies with data, 44 quarterly reviews 01/2016 to 10/2026, savings plan €100/month (€12,700 paid in), never sell. No buffer: 40 changes/yr, 55 returners, savings plan 11.3 % p.a. Narrow: 32, 25, 11.3 %. Medium: 28, 13, 11.3 %. Wide: 23, 1, 11.3 %. Return practically the same in all variants (11.25-11.30 %).
Criterion met for "wide" (fewest returners, same return; neighbour "medium" also with few returners and the same return).
Side finding (important): the same savings plan on the S&P 500 over the same period returned 13.9 % p.a. (€27,499 instead of €23,700). The rule with only beta and 10-year return was 2.6 points p.a. behind the index, despite today's company list (bankruptcies missing, result rather too good). Without margin and debt the index becomes very large (59 to 89 stocks on average). Whether the two additional filters change this cannot be tested historically; only the shadow book will show.

## 2026-11-21: Crown Jewels as a savings-plan index with buffer (explicit decision)
1. Buffer "wide": admission only when all strict rules are met (beta < 1.15; 10-year return >= 17 %; gross margin >= 49 %; net debt/EBITDA < 2), two reviews in a row. Removal only on a clear miss, two reviews in a row: beta > 1.30 or 10-year return < 12 %. Set analogously for margin and debt, NOT tested: margin < 45 % or net debt/EBITDA >= 2.5 (or EBITDA negative/missing).
2. Savings-plan index, never sell: every month the same amount, equally split across current members. Removed stocks get no new money but stay held. Returners get money again. The shadow book calculates exactly this (€100 per month from Nov 17, 2026, against the same savings plan on the S&P 500; metric value per euro paid in). The lump-sum shadow book also continues (both side by side, explicit decision): equally weighted, rebalanced only on changes. Final verdict November 2031: proven if the savings-plan return (internal rate of return) is at least 2 points p.a. above the S&P 500 savings plan; failed if below.
3. Telegram messages (private) on every change with concrete steps (start / stop savings plan, do not sell).
4. Labelled on the site as an experiment with the result of the buffer test (rule 2.6 points p.a. behind the S&P 500 in hindsight). The core does not change: the S&P 500 remains the foundation.

### Supplement to the buffer test: lump sum (fixed before computing)
Same setup, additionally: lump sum from the first review with members, equally weighted, rebalanced (sold and redistributed equally) only when members change; against a lump sum in the S&P 500 from the same day. Metric return p.a. Question: is the shortfall due to the savings plan?
Result lump sum (2026-11-21): start Apr 5, 2016, S&P 500 14.3 % p.a. No buffer 12.7 %, narrow 13.1 %, medium 13.6 %, wide 14.0 % (38 rebalances). With a lump sum the shortfall is much smaller than in the savings plan (wide: 0.3 instead of 2.6 points p.a.); the buffer also helps here (fewer sales of stocks that later return). The S&P 500 is not beaten in any variant. The "wide" buffer is confirmed.

## 2026-11-21: Crown Jewels start: previous season review recalculated (fixed before computing; eliteretro.py)
Reason: the candidates only had streak 1 because the calculation was first made on Nov 21, not because they had failed before.
Rule: the previous season review (start of the current season) is recalculated. Beta (weekly prices, 5 yrs, euros) and 10-year return from prices up to the reference date; margin and net debt/EBITDA with today's values (assumption: practically unchanged within three months; not freely available historically). The screening of Nov 21 counts as the review of the current season.
Consequence: whoever meets all rules on the reference date AND on Nov 21 is admitted now (change in both shadow books from Nov 20, the last price day). Members that would have clearly missed on the reference date (buffer limits) get a warning; with a clear miss on both dates they are dropped. One-off at the start.

## 2026-11-20: Crown Jewels admission (start: season reviews 2026-10-27 and 2026-11-20 passed)
Lilly (Eli) (LLY): 10 yrs 35.2 % p.a., beta 0.65, gross margin 83.6 %, net debt 0.96x EBITDA, passed all rules 2 seasons in a row. From now on new money equally split across 7 stocks.

## 2026-11-20: Crown Jewels admission (start: season reviews 2026-10-27 and 2026-11-20 passed)
Veeva Systems (VEEV): 10 yrs 20.4 % p.a., beta 0.99, gross margin 75.0 %, net debt -6.59x EBITDA, passed all rules 2 seasons in a row. From now on new money equally split across 8 stocks.

## 2026-11-20: Crown Jewels admission (start: season reviews 2026-10-27 and 2026-11-20 passed)
Cboe Global Markets (CBOE): 10 yrs 19.5 % p.a., beta 0.15, gross margin 53.9 %, net debt -0.53x EBITDA, passed all rules 2 seasons in a row. From now on new money equally split across 9 stocks.

## 2026-11-20: Crown Jewels admission (start: season reviews 2026-10-27 and 2026-11-20 passed)
Vertex Pharmaceuticals (VRTX): 10 yrs 19.2 % p.a., beta 0.54, gross margin 54.8 %, net debt 0.03x EBITDA, passed all rules 2 seasons in a row. From now on new money equally split across 10 stocks.

## 2026-11-20: Crown Jewels admission (start: season reviews 2026-10-27 and 2026-11-20 passed)
Moody's Corporation (MCO): 10 yrs 17.6 % p.a., beta 0.97, gross margin 74.6 %, net debt 1.48x EBITDA, passed all rules 2 seasons in a row. From now on new money equally split across 11 stocks.

## 2026-11-21: News archive (explicit decision)
Homepage: latest report, below it collapsible only the last 7 days. Reports older than 30 days are moved by the nightly run into monthly files (site/archive/news-YYYY-MM.json, archive_news.py); nothing is deleted. Archive page archiv.html with month selection, daily reports and monthly/annual reports. The 60-entry limit in the news monitor is dropped.

## 2026-11-21: Site restructured (explicit decision)
Order by priority: Current (news compact with collapsible details, reports, buy, three cards, calculator, market conditions, bitcoin power law), Evidence (the evidence, King of Kings with FTSE test, world vs USA and factor ETFs as collapsible details, S&P 500 since 1928), Experiments (Crown Jewels, savings-plan shadow book, team test bench). History tables (team, Crown Jewels, savings plan) on the homepage: last 7 days (as with the news); all daily shadow-book values in the archive by month. Menu top left with the same groups. Content and figures unchanged.

## 2026-11-21: Rule book and log separated (explicit decision)
The rule book (REGELBUCH.en.md, page regeln.html) shows only what applies today, by topic, with a "since" date per rule. This file is now the log (page protokoll.html, newest entries first). Every rule change: update the rule book AND add an entry here. Automatic season reviews write only to the log.

## 2026-11-21: Telegram filter corrected (review)
The Crown Jewels section of the monthly report was accidentally filtered out in Telegram (filter dated from the internal Elite 6). Now: Crown Jewels lines go neutrally to the channel; shadow-book lines stay internal; savings-plan steps privately only.

## 2026-11-21: Names sharpened (explicit decision)
"Savings plan shadow book" is now "S&P 500 savings plan shadow book". "Team model" is now "Tactical model 3 Kings": each season it chooses the strategy per asset (trend, for bitcoin from candidates) and allocates capital by volatility, so it is more than a pure trend model. Content unchanged.

## 2026-11-21: Tactical model: signal stays visible, private message (bug fix)
Bug: the night run executes several times. The first run applied the signal in the shadow book; later runs the same night saw no deviation and showed "Do nothing". So the sale of Nov 20 (S&P 500 49 % → 0 %) was never visible on the site. Now: a data day's signal stays visible until the next data day ("Signal at the close of …, to be carried out on the next trading day"); each new signal triggers a private Telegram message. Open point (unchanged): the shadow book applies the rebalancing at the signal day's close; in practice only the next trading day is possible.

## 2026-11-21: Tactical model: execution on the next trading day (explicit decision)
Previously the shadow book applied a rebalancing at the close of the same day the signal arose (one day too optimistic: in practice the signal is only seen the next morning). New: signal at the close of day D, execution in the shadow book at the close of the next trading day; the old holdings apply until then. Applied retroactively to the signal of Nov 20, 2026 (S&P 500 49 % → 0 %): executed only on the next trading day; shadow book 0.9674 → 0.9676 (trading costs reversed). The site shows the open signal and afterwards "Carried out at the close of … (signal of …)".

## 2026-11-21: Crown Jewels: execution on the next trading day (explicit decision)
As with the tactical model: changes from the season review (admission, removal) take effect in both shadow books only from the close of the next trading day, not at the close of the review day. Applied retroactively to the five admissions of Nov 20, 2026 (Eli Lilly, Veeva, Vertex, Cboe, Moody's): effective from the next trading day; values up to Nov 20 are unchanged.

## 2026-11-21: Watchdog for the watchdog (explicit decision)
watchdog.py, daily 8:04 UTC (9:04 CET): reports privately via Telegram if the nightly data run or the news monitor has written nothing for more than 26 hours, prices are older than 4 days, or the monthly report is missing at the start of the month. On Sundays a short "all running" message.

## 2026-11-21: Market barometer with traffic lights (explicit decision)
New "At a glance" strip at the top of the page with S&P 500, bitcoin, gold, oil, US yield, ECB rate, euro in dollars, inflation US and euro area, Fear & Greed, VIX. Tiles green, yellow or red by the limits in the rule book (section market barometer). Information only, no signal. Sources: Yahoo, ECB data portal, US Bureau of Labor Statistics, Eurostat (new HICP series from 2026).

## 2026-11-21: Market conditions merged, hypotheses on the barometer (explicit decision)
The old market conditions section further down and the tiles at the top are now one "Market conditions" block at the top. New tiles: Shiller P/E, Buffett indicator, yield curve (limits in the rule book). The old opportunity colour (extreme fear = green) is dropped so there is only one colour logic; the note "was often a buying opportunity" remains as text in the details. Four hypotheses A to D fixed in advance (see rule book); values and colours are recorded daily from today. Start: 10 of 14 tiles red, 1 green.

## 2026-11-21: Backtest of the barometer hypotheses (criteria fixed in code beforehand)
thesen.py, nightly. A (VIX above 30 as proxy for Fear & Greed): S&P 500 12 months later +22.3 % vs +10.2 %, 26 episodes since 1990: confirmed. B (US inflation above 3.5 % and 10-yr yield above 4.75 %): +5.6 % vs +7.3 %, 14 episodes since 1900, gap below 3 points: not confirmed. C (number of red tiles says nothing): refuted, correlation −0.18; 0–1 red about +11 %, 2 red +5 %, 3 red −4 % (from VIX, P/E, inflation, yield). D (crypto fear red and bitcoin below power-law midline): +193 % vs +78 %, 7 episodes since 2018: confirmed, short history. Active today: A, B, D. Context only, buy rule unaffected. New tile bitcoin vs power-law midline (16 tiles, grid 4 × 4 or 2 × 8).

## 2026-11-21: Page reordered (explicit decision, no rule change)
Power law check directly below market conditions. Buy and calculator are one block. New under experiments: "Shadow books overview" with all four books (Crown Jewels lump sum and savings plan, S&P 500 savings plan, tactical model) and the gap to each benchmark.

## 2026-11-21: Note on multiple testing for the barometer hypotheses
Added after an external review: four hypotheses on the same data, one may fit by chance; p-values are not meaningful because of overlapping 12-month windows. No rule change.

## 2026-11-21: Crown Jewels size under observation
No cap on the number of members, no rule change. The size of the index is being observed.
