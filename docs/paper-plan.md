# Paper plan: what can be measured, and what cannot

Working title (to be sharpened):
*Measuring monetary transmission to corporate balance sheets in emerging
markets: what financial statements can and cannot reveal. Evidence from
Vietnam and Türkiye.*

The project set out to test whether floating-rate debt exposure transmits
monetary tightening into corporate default risk, comparing a severe tightening
(Türkiye) with a mild one (Vietnam). That test cannot be run on listed-firm
data. Rather than abandon the work, the paper reports *why* -- which turns out
to be a set of results that are useful to anyone attempting this class of
measurement, and several of which are, as far as we can find, undocumented.

## The positive results the paper is built on

Every number below is from the final panels: Vietnam 693 firms 2011-2025
(vnfinancialdata), Türkiye 585 firms 2010-2025 (Is Yatirim) plus 586 firms
2021-2025 (Yahoo).

**1. Implied borrowing cost recovers the policy path from ordinary statements.**
Firm-level interest expense over average debt, aggregated to a median,
reproduces each central bank's path without being given it.

| Vietnam | | Türkiye | |
|---|---|---|---|
| 2011 | 11.1% | 2022 | 17.8% |
| 2015 | 5.8% | 2023 | 25.4% |
| 2023 | 7.2% | 2024 | **31.2%** |
| 2025 | 5.8% | 2025 | 25.8% |

Turkish policy peaked in 2024 at 47.5% and the measure peaks in 2024. Vietnam's
2011 peak coincides with the inflation crisis and the 2023 uptick with the SBV
tightening. This validates the measure and is the foundation for everything
after it.

**2. Pass-through is large but far from complete.** A 38-percentage-point
Turkish policy move produces a 13.4-point move in realised borrowing costs,
roughly 35% pass-through, while median interest coverage halves from 3.36 to
1.66. Vietnam's mild cycle moves costs 0.8 points and coverage dips from 3.11
to 2.05 before recovering to 2.70. The dose-response contrast is clear in
aggregate even though it cannot be identified across firms.

**3. A widely used Turkish data source bundles FX into interest.** Is Yatirim's
`4BB` "Financial Expenses" runs about three times Yahoo's interest expense
(median difference -68.8%, correlation on absolute values 0.727). Built on
`4BB` the Turkish implied rate peaks in 2018 and 2021 -- the lira crisis years.
Built on a clean interest measure it peaks in 2024 with policy. Anyone using
`4BB` as an interest proxy will recover currency shocks and call them monetary
transmission.

**4. Regression-estimated exposure is noise; balance-sheet exposure is not.**
Split-half reliability across 2012-2017 versus 2018-2022:

| Measure | Correlation |
|---|---|
| Repricing beta (TR / VN) | **-0.22 / -0.08** |
| Short-term debt share (TR / VN) | +0.44 / +0.63 |
| FX exposure (TR) | +0.52 |
| Export share (TR) | +0.84 |

With a median of six usable annual observations and two regressors, the
expected R-squared from pure noise is about 0.40; Vietnam's observed median is
0.396. Per-firm pass-through betas from annual accounting data do not measure a
firm trait. This is a general warning, not a quirk of our sample.

**5. Turkish inflation accounting contaminates stock-based outcomes in a way
fixed effects cannot absorb.** Median leverage falls from 0.226 (2019) to 0.100
(2024) and equity-to-assets rises from 0.419 to 0.646, driven by TMS-29
restating non-monetary assets while monetary debt stays nominal. Because asset
vintage differs across firms, the restatement effect is *heterogeneous in the
exposure variable*: it enters as an exposure-by-post interaction, exactly where
the coefficient of interest sits. Country-by-year effects absorb the common
level shift and leave the contamination in place. The FX specification shows
the signature precisely -- highly significant wrong-signed coefficients whose
post-treatment path grows monotonically (+0.32, +0.83, +1.18 across 2023-25).
Every study using Turkish post-2023 balance-sheet ratios in a
difference-in-differences is exposed to this.

**6. Two independent sources agree where they should.** Total assets reconcile
at a median relative difference of 0.0000 (Vietnam correlation 1.0000, Türkiye
0.9960) and revenue likewise. Vietnamese interest expense reconciles at 0.00%
median on absolute values. Disagreements are all definitional and identified:
equity (parent versus including minority interest), EBIT (reported operating
profit versus pretax plus interest), and `4BB` above.

## The null, properly identified

With contaminated outcomes removed, exposure measured at 2021 before
restatement, and a 2015-2025 window that makes the identifying assumption
testable, no exposure gradient is detectable in either country on any flow
outcome. The event studies show why: the exposure-outcome relationships are
persistent level differences predating treatment by years. Turkish short-term
debt share against debt growth is significantly negative in *every* year from
2015 and does not shift at 2023.

The null is credible precisely because three earlier significant results were
each shown to be artefacts -- small-sample noise, inflation-accounting
restatement, and pre-existing trend -- by diagnostics the paper documents.

## Structure

1. **Introduction** - the question, why administrative data answers it and
   statements do not, what the paper contributes instead.
2. **Institutional setting** - the two monetary regimes; TMS-29.
3. **Data** - two countries, two sources each, harmonisation, cross-validation.
4. **Measuring the cost of debt** - construction and validation against policy
   paths (results 1, 2, 3, 6).
5. **Measuring exposure** - what is and is not a stable firm trait (result 4).
6. **Identification and its failure modes** - TMS-29 as an exposure-by-post
   confound (result 5); pre-trends.
7. **Results** - the identified null and the diagnostics behind it.
8. **Implications for practice** - a checklist for firm-level monetary
   transmission work in emerging markets.
9. **Conclusion** - what would be needed to answer the original question.

## Open decisions

- Framing emphasis: measurement paper with a null, or null result with
  measurement contributions. Affects title and introduction.
- Whether to release the harmonised panel as a dataset citation (must be
  masked for double anonymized review).
- Reference set must be current to 2026 per project convention.
