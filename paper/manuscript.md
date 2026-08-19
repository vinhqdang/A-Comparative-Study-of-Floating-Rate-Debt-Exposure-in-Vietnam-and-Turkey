# What Financial Statements Can and Cannot Reveal About Monetary Transmission to Corporate Balance Sheets: Evidence from Vietnam and Türkiye

## Abstract

A productive literature shows that firms holding floating-rate debt bear the
brunt of monetary tightening. That literature rests almost entirely on
supervisory credit registries, which record contract-level repricing terms.
Most emerging markets have no such registry available to researchers; what they
have is published financial statements. Whether the accounting record can
substitute is therefore a consequential measurement question, and this paper
answers it. We assemble harmonised panels for 693 Vietnamese and 585 Turkish
listed non-financial firms over 2010–2025, cross-validating each against an
independent source, and exploit a natural contrast in dose: Türkiye tightened
from 9% to 47.5% while Vietnam tightened mildly and reversed within a year.
Three results are constructive. A simple implied borrowing cost — interest
expense over average debt — recovers each central bank's policy path without
being given it, peaking in Türkiye in 2024 at 31.2% as policy peaks at 47.5%.
Pass-through is large but incomplete: a 38-point policy move produces a
13.4-point move in realised borrowing costs while median interest coverage
halves from 3.36 to 1.66. And we document that a widely used Turkish vendor
field bundles currency revaluation into interest, so measures built on it peak
in the lira crises of 2018 and 2021 rather than at the policy peak. Three
results are cautionary. Firm-level repricing sensitivities estimated from
annual data fail split-half reliability, correlating at −0.22 and −0.08 across
sample halves with in-sample fit indistinguishable from noise. Turkish
inflation accounting restates non-monetary assets while leaving monetary debt
nominal; because asset vintage varies across firms this enters as an
exposure-by-post interaction that fixed effects cannot absorb, and we show it
generates highly significant wrong-signed estimates. Once contaminated outcomes
are removed, exposure is measured before restatement, and the pre-period is
extended far enough to test parallel trends, no exposure gradient survives in
either country: the apparent relationships are persistent level differences
predating treatment by years. We conclude that the contractual object these
designs require is not recoverable from published statements, and set out what
is.

**Keywords:** monetary transmission; corporate default; measurement error;
inflation accounting; emerging markets; financial statements

**JEL classification:** E52; G32; M41; C23

---

## 1. Introduction

A firm that borrows at a floating rate feels a policy tightening within weeks.
A firm that borrowed long and fixed does not feel it until it refinances. This
asymmetry is simple, intuitive, and has become the organising principle of a
productive literature on how monetary policy reaches the corporate sector.
Ippolito, Ozdagli, and Perez-Orive (2018) identify a *floating rate channel* in
matched loan-level records, showing that firms with unhedged floating-rate bank
debt cut investment and employment more sharply after tightening. Şengül and
Çinko (2026), studying the June 2023 reversal in Türkiye, apply a two-part
Double Machine Learning design to a large administrative dataset and find that
while the average effect is modest, sensitivity concentrates in firms with weak
internal risk ratings, low liquidity, and high exposure shares, with exporters
and manufacturers relatively insulated.

What these studies share is not merely a question but an input: a credit
registry recording, loan by loan, whether the contract reprices. Such registries
exist in relatively few jurisdictions and are available to researchers in fewer
still. What almost every market does have is a body of audited, published
financial statements. The question this paper takes seriously — and, we argue,
the field has not asked carefully enough — is whether that accounting record can
stand in for the registry.

The stakes are practical. If statements suffice, the literature's geographic
reach expands by an order of magnitude, and questions about monetary
transmission in Southeast Asia, Africa, and Latin America become tractable. If
they do not, then a body of work is being built on designs that cannot deliver
what they promise, and it is worth establishing precisely where the failure
occurs and what remains possible.

### 1.1 Approach

We treat this as a measurement problem and address it comparatively. Vietnam and
Türkiye share the structural features that make the floating-rate channel
plausible: bank-dominated corporate finance, thin corporate bond markets, heavy
reliance on short-maturity credit, and substantial listed non-financial sectors.
What they do not share is the monetary experience of 2021–2025. Türkiye executed
one of the decade's most severe tightenings, from 9.0% to 47.5%, under inflation
exceeding 60%. Vietnam tightened modestly in late 2022 in response to domestic
bond-market stress and reversed within a year.

This contrast is the paper's instrument. It supplies a strong dose and a weak
one, and it imposes a discipline that single-country studies cannot: a
measurement strategy that works should register both, in proportion. A method
that reports similar magnitudes in both, or that registers Vietnam more strongly
than Türkiye, has failed a test it would never have faced alone.

Our diagnostic standard throughout is *validation against an external
benchmark*. We do not ask whether a measure is statistically well behaved; we ask
whether it recovers something we independently know to be true. For the price of
debt, the benchmark is the published policy path. For exposure, the benchmark is
the firm's own subsequent change in borrowing cost. For the panel itself, the
benchmark is an independent commercial rendering of the same filings.

### 1.2 What we find

The constructive half of our answer concerns the *price* of corporate debt, and
it is positive. A firm's implied borrowing cost — interest expense divided by
average debt — aggregates to a series that reproduces each central bank's policy
path without being shown it. The Turkish series peaks in 2024, the year policy
peaks; the Vietnamese series traces the 2011 inflation crisis, the long easing
through 2015, and the 2023 tightening. This is not a trivial diagnostic. It
establishes that ordinary audited filings carry a legible signal of monetary
transmission, and it is the foundation on which everything else rests.

Two results follow from it. First, we quantify pass-through: a
38-percentage-point Turkish policy move produces a 13.4-point move in realised
borrowing costs, roughly 35%, while median interest coverage halves from 3.36 to
1.66. Incomplete pass-through of this magnitude is economically informative,
consistent with maturity structure delaying repricing and with quantity
rationing substituting for price adjustment. Second, the same diagnostic exposes
a data hazard that would otherwise be invisible: a widely used Turkish vendor
field labelled *Financial Expenses* bundles foreign-exchange revaluation with
interest, running roughly three times the true interest figure. Measures built
on it peak in the lira crises of 2018 and 2021 rather than at the 2024 policy
peak. A researcher using it to study monetary transmission would recover
currency shocks and report them as interest-rate effects.

The cautionary half concerns *exposure*, and it is negative. This is the object
the literature requires, and it defeats every strategy we attempt.

The natural approach infers exposure from behaviour, estimating a firm-specific
sensitivity of borrowing cost to policy. These estimates look reasonable — about
72% of firms return a positive slope, and the mean Vietnamese pass-through is
economically sensible — but they do not survive validation. Betas estimated on
one half of the sample correlate at −0.219 (Türkiye) and −0.080 (Vietnam) with
those estimated on the other half. In-sample fit is indistinguishable from what
pure noise would produce. And they fail a first-stage test: neither country's
beta predicts the firm's actual change in borrowing cost across the tightening.
The problem is generic rather than particular to our sample, and it is the
classic generated-regressor pathology (Pagan, 1984) compounded by short panels
(Griliches and Hausman, 1986): roughly a decade of annual observations cannot
support a firm-specific slope when idiosyncratic variation in debt composition
and drawdown timing swamps the common policy signal.

Balance-sheet proxies fare no better, for a different reason. They are measured
reliably — the short-maturity share persists at 0.44 to 0.69 across horizons —
but none predicts the actual change in borrowing cost, with R² below 0.02 for
every candidate in both countries. The short-maturity share illustrates why: it
simultaneously captures repricing exposure and credit quality, since firms that
roll short-term paper cheaply are frequently the strongest borrowers. In Türkiye
the effects align; in Vietnam the credit-quality effect dominates and the
ordering inverts.

Layered on top is a problem specific to high-inflation settings that we believe
deserves considerably wider attention. Türkiye was classified hyperinflationary
under IFRS from April 2022, and Turkish companies restate their statements
accordingly. Non-monetary assets are indexed to a general price level; monetary
debt is not. Because the restatement factor depends on asset vintage, and
vintage varies across firms, the distortion is *heterogeneous in exactly the
dimension any balance-sheet exposure measure captures*. It therefore enters the
estimating equation as an exposure-by-post interaction — the coefficient of
interest — and country-by-year fixed effects, the natural defence, absorb only
the common component. We demonstrate that this is not a hypothetical concern: a
standard specification using FX exposure returns highly significant coefficients
with the wrong sign, on a post-treatment path that grows monotonically as the
restatement compounds.

When contaminated outcomes are removed, exposure is measured before the
restatement, and the pre-period is extended far enough that parallel trends can
actually be tested, nothing survives. The exposure-outcome relationships that
appear significant are persistent level differences predating treatment by
years, unmoved by the policy shock.

### 1.3 Why a null of this kind is informative

We are conscious that null results invite the suspicion of low power, and we
address it directly rather than by assertion. Over the course of the analysis,
three separate significant results appeared and each was subsequently shown to
be an artefact: a Turkish effect of +0.886 (p = 0.045) that vanished when the
sample doubled; the FX results, which were accounting restatement; and the
final flow-based coefficients, which were pre-existing trend. Each was caught by
a diagnostic — sample expansion, an accounting-mechanics argument, an extended
event window — that a conventional specification would not have run.

A design that generates three false positives before generating a null is
informative about the design. The diagnostics that caught them are the paper's
transferable contribution, and we set them out as a checklist in Section 10.

### 1.4 Contribution

To the monetary transmission literature, we delimit where statement-based
designs can and cannot substitute for registry data, and supply a validated
price measure that survives the transition. To empirical work on Türkiye, we
document two hazards — one in a commonly used vendor field, one in the
accounting standard itself — that threaten a broad class of post-2022 studies.
To research on Vietnam, we introduce a firm-level statement panel not previously
used for questions of this kind, harmonised against a Turkish counterpart and
validated throughout. And methodologically, we offer split-half reliability and
first-stage prediction as cheap, decisive tests that any paper using an
estimated firm characteristic as a regressor should report.

The remainder proceeds as follows. Section 2 situates the paper. Section 3
describes the two monetary regimes and the accounting transition. Section 4
presents the data and cross-validation. Section 5 constructs and validates the
price measure. Section 6 documents the failure of exposure measurement. Section
7 develops the identification problem. Section 8 reports results, Section 9
robustness, and Section 10 the practical implications. Section 11 concludes.

## 2. Related literature

### 2.1 Firm heterogeneity in monetary transmission

That monetary policy affects firms unequally is long established. Gertler and
Gilchrist (1994) documented that small manufacturing firms bear a
disproportionate share of the adjustment following tightening, and Bernanke and
Gertler (1995) formalised the credit channel through which balance-sheet
strength mediates the response. Kashyap and Stein (2000) established the bank
lending channel using cross-sectional variation in bank liquidity.

The modern literature has sharpened the relevant margin of heterogeneity.
Ottonello and Winberry (2020) show that firms with low default risk and high
credit ratings respond *most* to monetary shocks, because they face flatter
marginal cost curves for external finance. Cloyne, Ferreira, Froemel, and Surico
(2023) find that younger firms without dividend payments drive the investment
response. Ozdagli (2017) shows that financial frictions shape the stock price
reaction to policy. Greenwald (2019) identifies an interest coverage channel
operating through debt covenants, which is directly relevant to our outcome
choice.

Two strands bear most closely on our design. The first concerns *contractual*
repricing. Ippolito, Ozdagli, and Perez-Orive (2018) identify the floating rate
channel using loan-level data, and Auer, Friedrich, Ganarin, Paligorova, and
Towbin (2019) trace international transmission through banks in small open
economies. The second concerns *maturity*. Almeida, Campello, Laranjeira, and
Weisbenner (2012) exploit quasi-random variation in whether long-term debt
happened to mature just before the 2007 crisis, a design that isolates rollover
exposure cleanly. Jungherr, Meier, Reinelt, and Schott (2024) show that debt
maturity structure materially shapes the transmission of policy. He and Xiong
(2012) provide the theoretical link between rollover risk and credit risk, and
Demirgüç-Kunt and Maksimovic (1999) document how institutions shape maturity
choice across countries.

Our contribution is not to this literature's substance but to its
transportability. Every study cited above uses either supervisory data or a
market with rich contractual disclosure. We ask what is left when neither is
available.

### 2.2 Currency mismatch in emerging markets

Because Türkiye's episode combines monetary tightening with severe currency
depreciation, the FX-mismatch literature bears directly on our measurement
problem. Eichengreen and Hausmann (1999) framed the "original sin" of emerging
markets borrowing in foreign currency. The empirical record is more nuanced than
the framing suggests: Bleakley and Cowan (2008) find that firms holding dollar
debt did not systematically underperform during depreciations, because they
tended to hold dollar revenues too, while Aguiar (2005) documents contractionary
balance-sheet effects in Mexico. Kalemli-Ozcan, Kamil, and Villegas-Sanchez
(2016) reconcile these by showing that the damaging combination is unhedged FX
debt together with a banking crisis that restricts credit supply.

Bruno and Shin (2015a, 2015b) establish the risk-taking channel linking exchange
rates, bank leverage, and global liquidity, and Du and Schreger (2022) connect
sovereign risk, currency risk, and corporate balance sheets. Acharya, Crosignani,
Eisert, and Eufinger (2024) show how impaired credit allocation distorts
inflation dynamics. For Türkiye specifically, Akbal and Civcir (2026) examine the
asymmetric response of the lira to capital flows and sovereign credit spreads.

This literature matters to us in two ways. Substantively, it explains why
exporters may be insulated — a mechanism Şengül and Çinko (2026) themselves
invoke, noting that exporters and manufacturers generate foreign-currency
revenues and benefit from exchange-rate pass-through. Methodologically, it
explains why the bundled financial-expense field of Section 5.4 is so damaging:
in a currency crisis, revaluation losses dwarf interest, and a measure that
conflates them will attribute currency effects to monetary policy.

### 2.3 Accounting measurement and inflation

Our identification problem is, at bottom, an accounting one, and there is a
literature on it that the monetary economics literature rarely cites. Gordon
(2001) examines the value relevance of historical cost, price level, and
replacement cost accounting in Mexico. Barniv (1999) studies the value relevance
of inflation-adjusted versus historical-cost earnings under hyperinflation.
Davis-Friday and Gordon (2005) analyse how the relative valuation roles of book
value, earnings, and cash flows shift during a macroeconomic shock. Konchitchki
(2011) demonstrates that nominal financial reporting has real consequences for
performance measurement and prices even at moderate inflation.

The consistent message is that when general price levels move sharply, the
mapping from economic reality to reported figures changes, and it changes
*differently for different firms*. De Franco, Kothari, and Verdi (2011) show that
statement comparability is itself an economically consequential attribute. Our
Section 7 gives this literature a specific and, we think, novel application: an
accounting transition that coincides with a treatment date and interacts with
the treatment variable is not a nuisance to be absorbed but a threat to
identification.

### 2.4 Measurement error and generated regressors

Finally, our exposure results connect to a well-developed econometric
literature. Pagan (1984) established the consequences of using a
regression-generated variable as a regressor in a second stage. Griliches and
Hausman (1986) show that panel transformations frequently *amplify* rather than
attenuate measurement error, which is directly relevant: differencing to
construct our betas removes fixed effects but magnifies noise. Classical
attenuation biases coefficients toward zero, which is exactly the pattern our
null exhibits, and this is why we regard a first-stage validity test as
obligatory rather than optional.

On the difference-in-differences side we follow the recent methodological
literature. Because our treatment timing is common across firms within a country
we avoid the negative-weighting problems identified by Goodman-Bacon (2021), de
Chaisemartin and D'Haultfœuille (2020), Callaway and Sant'Anna (2021), and Sun
and Abraham (2021), but we take seriously Roth's (2022) demonstration that
conditioning on passing a pre-trends test distorts inference — which is why we
report full event-study paths rather than a pre-trend test statistic. Standard
errors are clustered by firm throughout following Petersen (2008).

## 3. Institutional setting

### 3.1 Two monetary regimes

The Turkish tightening is the sharper of the two by an order of magnitude. After
a period of unorthodox easing, the one-week repo rate stood at 9.0% at end-2022.
Following the June 2023 policy reversal it reached 42.5% by end-2023, peaked at
47.5% during 2024, and stood at 38.0% at end-2025. Consumer price inflation
exceeded 60% at its height. The lira depreciated from roughly 18.7 per US dollar
at end-2022 to 43.0 at end-2025.

Vietnam's experience over the same window is far milder. The State Bank raised
policy rates in late 2022 amid stress in the domestic corporate bond market and
reversed course through 2023. The average bank lending rate rose from 8.0% in
2022 to 9.3% in 2023 — against 17.0% at the peak of the 2011 inflation episode,
which provides a useful within-country benchmark for what a severe Vietnamese
tightening looks like. The dong depreciated gradually, from roughly 23,600 per
dollar at end-2022 to 26,225 at end-2025.

The comparison is therefore not treatment versus control but large dose versus
small dose, and the appropriate prediction is proportional rather than binary.
Both corporate sectors are bank-dominated with thin bond markets, so the
transmission channel under study is structurally available in each.

### 3.2 The Turkish accounting transition

Türkiye met the IFRS criteria for a hyperinflationary economy and was classified
as such from April 2022; local inflation adjustment requirements followed for
statements through end-2023. Under the relevant standard, entities reporting in
the currency of a hyperinflationary economy restate their statements in the
measuring unit current at the balance sheet date, and comparative figures are
restated on the same basis.

The mechanics matter for what follows, so we state them precisely.
*Non-monetary* items — property, plant and equipment, inventories, equity — are
restated by a general price index applied from each item's acquisition date.
*Monetary* items — debt, cash, receivables — are already expressed in period-end
purchasing power and are not restated. *Income statement* items are restated to
period-end purchasing power, in practice by a factor common across firms within
a period.

Three consequences follow. Any ratio containing a non-monetary stock moves
mechanically at the transition. Any ratio of two flows is largely unaffected,
because both are scaled by a common factor that year effects absorb. And
critically, the magnitude of the restatement depends on asset vintage, which
varies across firms — so the distortion is not a common shock. Section 7
develops the implication for identification.

## 4. Data

### 4.1 Sources and construction

The Vietnamese panel derives from an item-level dataset of statements filed by
companies listed on the Ho Chi Minh City and Hanoi exchanges, distributed
through a public research repository in long format with standardised item
codes. Pivoting to firm-year observations yields 9,893 firm-years for 693 firms
over 2011–2025. Non-missing coverage is 94.5% for total assets, 94.7% for total
debt, 91.2% for interest expense, 93.2% for EBIT and 96.8% for equity.

The Turkish panel derives from a brokerage data service redistributing filings
made to the Public Disclosure Platform. A single request returns the balance
sheet, income statement, cash-flow statement and a block of supplementary items
with bilingual labels for four annual periods, which we exploit to retrieve four
years of annual data per request. The resulting panel covers 585 firms over
2010–2025. It carries two items with no Vietnamese counterpart and considerable
analytical value: export sales and net foreign-currency position.

Both panels are restricted to non-financial firms. Banks, insurers and brokers
file on incompatible templates and their liability structure is not comparable
to that of non-financial borrowers. We further require strictly positive total
debt and total assets, since the transmission channel is undefined for firms
without debt.

**Table 1. Firms per year**

| Year | Türkiye | Vietnam | | Year | Türkiye | Vietnam |
|---|---|---|---|---|---|---|
| 2015 | 349 | 648 | | 2021 | 551 | 691 |
| 2016 | 358 | 663 | | 2022 | 568 | 692 |
| 2017 | 370 | 670 | | 2023 | 585 | 693 |
| 2018 | 428 | 682 | | 2024 | 584 | 692 |
| 2019 | 467 | 686 | | 2025 | 582 | 689 |
| 2020 | 508 | 690 | | | | |

Turkish coverage rises over the sample as the exchange admits new listings;
Vietnamese coverage is near-complete from 2015. Because our identification uses
within-firm variation with firm fixed effects, entry does not bias the estimates,
though it does mean earlier years rest on a smaller Turkish cross-section.

### 4.2 Descriptive statistics

**Table 2. Descriptive statistics, 2015–2025**

| | Vietnam | | | | Türkiye | | | |
|---|---|---|---|---|---|---|---|---|
| Variable | n | Mean | Median | SD | n | Mean | Median | SD |
| Debt / assets | 5,708 | 0.250 | 0.225 | 0.170 | 4,780 | 0.228 | 0.195 | 0.190 |
| Short-term debt share | 5,708 | 0.709 | 0.852 | 0.323 | 4,783 | 0.627 | 0.647 | 0.284 |
| Implied borrowing cost | 5,693 | 0.063 | 0.063 | 0.032 | 3,870 | 0.312 | 0.252 | 0.219 |
| Interest coverage | 5,340 | 9.225 | 3.290 | 15.698 | 4,673 | 2.680 | 1.068 | 6.502 |
| Return on assets | 5,698 | 0.065 | 0.053 | 0.065 | 4,783 | 0.080 | 0.070 | 0.105 |

Leverage is comparable across the two markets at roughly 20–25% of assets, and
both corporate sectors fund themselves predominantly at short maturity — the
Vietnamese median short-term share of 0.85 is striking and speaks to the
rollover-risk framing of He and Xiong (2012).

The contrast in distress is stark. Median Turkish interest coverage over the
period is 1.07 against Vietnam's 3.29, and the median Turkish implied borrowing
cost is four times the Vietnamese. Turkish firms in this sample operate close to
the point at which operating income fails to cover interest, which is precisely
the covenant-relevant threshold Greenwald (2019) identifies. This is the
aggregate signature of the severe regime, and it makes the firm-level null of
Section 8 the more striking.

### 4.3 Cross-validation against an independent source

Because the paper's subject is measurement, we do not assume our panels are
correct; we test them. Each national source is compared against an independent
commercial aggregator that normalises the same underlying filings and retains
four to five annual periods. The pattern of disagreement is as informative as
the agreement.

**Table 3. Reconciliation with an independent source**

| Variable | Vietnam corr. | Vietnam median diff. | Türkiye corr. | Türkiye median diff. |
|---|---|---|---|---|
| Total assets | 1.0000 | 0.0000 | 0.9960 | 0.0000 |
| Revenue | 0.9999 | 0.0000 | 0.9935 | 0.0000 |
| Total debt | 0.9906 | 0.0000 | 0.9960 | −0.0295 |
| Equity | 0.9956 | −0.0447 | 0.9552 | −0.0039 |
| EBIT | 0.7657 | +0.2339 | 0.8539 | +0.2093 |
| Interest expense (absolute) | 0.9913 | 0.0000 | **0.7272** | **−0.6880** |

Where the two sources should agree, they agree closely: total assets and revenue
reconcile at a median relative difference of zero in both countries.

Three discrepancies are systematic, and two are benign. Equity differs by
roughly four percent in Vietnam because the aggregator reports parent-only
shareholders' equity where the national source consolidates minority interest.
EBIT differs by 21–23% in both countries because the aggregator derives it from
pretax income plus interest rather than taking reported operating profit — a
definitional difference, not an error, though one that matters for anyone
comparing coverage ratios across sources.

The third discrepancy is not benign, and Section 5.4 is devoted to it.

## 5. Measuring the price of corporate debt

### 5.1 Construction

For firm *i* in year *t* we define the implied borrowing cost as interest
expense divided by the average of beginning- and end-of-year debt:

  r_it = |Interest expense_it| / [ ½ ( D_it + D_i,t−1 ) ]   (1)

where D denotes the sum of short- and long-term borrowings. Averaging the
denominator prevents the ratio from being driven mechanically by borrowing
undertaken during the year: a firm that doubles its debt in December would
otherwise appear to have halved its cost of funds.

The measure has three properties that recommend it. It is constructible from any
statement set that separates interest expense, which is the overwhelming
majority. It requires no contractual information. And — importantly for the
Turkish application — numerator and denominator are both monetary items, so it
is invariant to the inflation restatement described in Section 3.2.

Its limitations should be stated equally plainly. It is an average realised cost
across a firm's entire debt stock, not a marginal rate on new borrowing, so it
responds to policy with a lag governed by maturity structure. It is contaminated
by any non-interest charge classified within interest expense, a point that
becomes central in Section 5.4. And at annual frequency it inherits noise from
the timing of drawdowns and repayments, which Section 6 shows to be
consequential.

### 5.2 Validation against policy paths

The measure is not calibrated to any policy series, so whether it recovers one
is a genuine test rather than a mechanical consequence of construction. It
passes in both countries.

**Table 4. Median implied borrowing cost and the policy path**

| Vietnam | Implied cost | Lending rate | | Türkiye | Implied cost | CBRT policy (year-end) |
|---|---|---|---|---|---|---|
| 2011 | 11.1% | 17.0% | | 2022 | 17.8% | 9.0% |
| 2013 | 7.5% | 10.4% | | 2023 | 25.4% | 42.5% |
| 2015 | 5.8% | 7.1% | | 2024 | **31.2%** | **47.5%** |
| 2020 | 6.3% | 7.6% | | 2025 | 25.8% | 38.0% |
| 2023 | 7.2% | 9.3% | | | | |
| 2025 | 5.8% | — | | | | |

The Turkish series peaks in 2024, the year policy peaks, and declines in 2025 as
policy eases. The Vietnamese series peaks in 2011 at the height of that
country's inflation crisis, falls monotonically through the easing cycle to 5.8%
by 2015, rises to 7.2% in the 2023 tightening, and subsides again as the State
Bank reverses. Median interest coverage moves in mirror image, reaching its
Vietnamese sample minimum of 2.05 in exactly 2023.

That an accounting ratio constructed from published filings traces a policy path
it was never shown is this paper's foundational result. It establishes that the
price side of monetary transmission is legible in ordinary statements, and it
licenses the diagnostic use we make of it in Sections 5.4 and 6.

### 5.3 Pass-through is large but incomplete

The Turkish episode permits a quantification that registry studies rarely
report, because registries observe contract rates rather than realised expense.
Policy moved 38.5 percentage points between end-2022 and the 2024 peak. Realised
borrowing costs moved 13.4 points, from 17.8% to 31.2% — a pass-through of
roughly 35%. Over the same window median interest coverage halved, from 3.36 to
1.66.

Vietnam's mild cycle produces a proportionally mild response: costs move 0.8
points and coverage dips from 3.11 to 2.05 before recovering to 2.70 as policy
reverses. The dose-response contrast is exactly what a working measure should
deliver, and its clarity in aggregate is what makes the firm-level null of
Section 8 informative rather than merely disappointing.

Incomplete pass-through is itself economically meaningful, and we note three
non-exclusive explanations that our data cannot separate. Maturity structure
delays repricing, so a stock-weighted average cost necessarily lags a marginal
rate. Quantity rationing may substitute for price adjustment, with banks
restricting volume rather than fully repricing — consistent with Kashyap and
Stein (2000). And directed or subsidised lending programmes, prominent in the
Turkish setting, mechanically hold some borrowing costs below policy. Separating
these would require the contractual data whose absence motivates this paper.

### 5.4 A data hazard: bundled financial expense

The Turkish source's field labelled *Financial Expenses* is the natural
candidate for an interest measure over the long history, being the only
interest-like item available before 2021. It should not be used as one.

Against the independent aggregator's interest expense, it runs roughly three
times larger: a median relative difference of −68.8%, with a correlation of
0.727 on absolute values. The Vietnamese comparison, where the corresponding
field is a clean interest figure, returns a correlation of 0.991 and a median
difference of 0.00%, with 78% of firm-years agreeing within two percent. The
contrast localises the problem to the Turkish field rather than to our
construction.

The field bundles foreign-exchange revaluation losses, and in a currency crisis
those dwarf interest. The consequence is not attenuation but a change in what
the measure tracks:

**Table 5. What the implied cost measures depends on the interest field**

| | Peak year | Interpretation |
|---|---|---|
| Built on bundled *Financial Expenses* | **2018 and 2021** | Lira depreciation episodes |
| Built on clean interest expense | **2024** | Policy rate peak |

A researcher using the bundled field to study monetary transmission would
recover currency shocks and report them as interest-rate effects — and would do
so with strong statistical significance, since the currency episodes are large.
This is a concrete instance of the general point in Section 2.2: where monetary
tightening and currency depreciation coincide, measurement that cannot separate
them will attribute one to the other.

We therefore take Turkish interest-based quantities from the aggregator, and
reserve the national source for balance-sheet characteristics and for outcomes
requiring no interest figure. The cost is a shorter window for interest-based
outcomes; Section 7.2 explains how we recover length where it matters most.

## 6. Measuring exposure

### 6.1 The required object is not disclosed

Contractual floating-rate status does not appear in published financial
statements under either country's reporting regime. Firms disclose borrowings by
maturity and sometimes by currency, but not by repricing basis. No estimator
recovers an undisclosed contractual term. The question is therefore whether an
adequate substitute can be constructed, and we assess the two natural
candidates in turn.

### 6.2 Revealed repricing sensitivity

The more appealing candidate infers exposure from behaviour rather than
disclosure. If a firm's debt reprices, its realised borrowing cost should move
with policy. For each firm we estimate, over a window ending before treatment,

  Δr_it = a_i + β_i ΔPolicy_t + γ_i Δln(FX_t) + ε_it   (2)

where β_i is the firm's repricing sensitivity and γ_i its sensitivity to the
exchange rate. We estimate the FX term jointly rather than treating it as a
nuisance, because Section 5.4 established that a substantial part of the
movement in Turkish realised borrowing cost is currency revaluation. Estimating
them together is intended to separate the repricing channel from the
FX-mismatch channel rather than allow one to contaminate the other.

On the surface the estimates behave. Approximately 72% of firms in both
countries return a positive β. The mean Vietnamese estimate implies that a
one-point rise in the lending rate raises a firm's own cost of funds by about
0.79 points, which is economically sensible for a corporate sector funded
predominantly at short maturity. Median in-sample R² is 0.28 in Vietnam and 0.34
in Türkiye.

These diagnostics are, however, exactly the ones that cannot detect the problem.
We apply three that can.

**Split-half reliability.** A measure of a stable firm characteristic should
reproduce itself on independent subsamples. We estimate (2) separately on
2012–2017 and 2018–2022 for firms present in both windows and correlate the
results.

**Table 6. Split-half reliability of candidate exposure measures**

| Measure | Türkiye | Vietnam |
|---|---|---|
| Repricing beta β | **−0.219** (n = 77) | **−0.080** (n = 390) |
| FX beta γ | +0.147 | +0.094 |
| Short-term debt share | +0.438 | +0.628 |
| Export share | +0.838 | — |

The estimated betas correlate at zero or below: a firm identified as highly
exposed in the first half is, if anything, marginally *less* likely to be so
identified in the second. The measured balance-sheet characteristics in the
lower rows, by contrast, behave as stable traits. The failure is therefore
specific to regression-estimated quantities and not a property of the data.

**Fit against a noise benchmark.** With a median of six usable annual
observations and two regressors, the R² expected from pure noise is
approximately k/(n−1) ≈ 0.40. The observed Vietnamese median of 0.396 is
indistinguishable from it. What appeared to be moderate explanatory power is
what an unrestricted two-parameter fit produces on six observations regardless
of content.

**First-stage prediction.** The decisive test asks whether β predicts what it
purports to measure: the firm's actual change in borrowing cost across the
tightening. Regressing that change on standardised β and γ yields R² = 0.035 in
Türkiye and 0.002 in Vietnam, with the coefficient on β insignificant in both.
In Türkiye the most-exposed tercile records the *smallest* increase in realised
cost (+0.04) against the least-exposed tercile's +0.19.

**Table 7. First-stage test: does β predict the actual change in borrowing cost?**

| | Türkiye (2022→2024) | Vietnam (2022→2023) |
|---|---|---|
| Coefficient on β (standardised) | −0.036 (p = 0.27) | +0.001 (p = 0.54) |
| R² | 0.035 | 0.002 |
| Change, lowest β tercile | +0.19 | +0.006 |
| Change, highest β tercile | **+0.04** | +0.010 |

The diagnosis is generic. Year-to-year variation in a firm's implied cost
reflects changes in debt composition, drawdown timing, capitalised interest and
one-off charges. At annual frequency this idiosyncratic component dominates the
common policy signal, and roughly a decade of observations cannot separate them.
This is the generated-regressor problem of Pagan (1984) compounded by the panel
amplification Griliches and Hausman (1986) describe: first-differencing removes
the fixed effect but magnifies the noise-to-signal ratio.

We emphasise that this conclusion is not sample-specific. Any study estimating a
firm-level slope from a comparable number of annual accounting observations
faces the same arithmetic, and we recommend split-half reliability be reported
as a matter of course.

### 6.3 Balance-sheet proxies

The measured characteristics in Table 6 are reliable, which makes them the
natural fallback, and Table 8 confirms their persistence across horizons.

**Table 8. Persistence of measured characteristics (correlations)**

| Measure | Country | 2016–2019 | 2016–2022 | 2019–2022 |
|---|---|---|---|---|
| Short-term debt share | Vietnam | 0.669 | 0.606 | 0.693 |
| | Türkiye | 0.500 | 0.308 | 0.399 |
| Debt to assets | Vietnam | 0.770 | 0.606 | 0.770 |
| | Türkiye | 0.779 | 0.610 | 0.687 |

They fail for a different reason: reliability is necessary but not sufficient,
and none of them predicts the quantity of interest. Regressing the actual change
in borrowing cost on standardised pre-period characteristics yields R² below
0.02 for the short-term debt share, leverage, the current ratio, size and
interest coverage, in both countries.

**Table 9. No observable predicts the actual change in borrowing cost (R²)**

| Predictor | Türkiye | Vietnam |
|---|---|---|
| Short-term debt share | 0.000 | 0.002 |
| Debt to assets | 0.005 | 0.017 |
| Current ratio | 0.003 | 0.002 |
| Log assets | 0.005 | 0.001 |
| Interest coverage | 0.007 | 0.004 |

The short-maturity share illustrates the underlying confound, and it is worth
dwelling on because it is the proxy the literature would most naturally reach
for. It is simultaneously a measure of repricing exposure and of credit quality:
debt that rolls within the year reprices at rollover regardless of its stated
basis, but the firms able to roll short-term paper cheaply are disproportionately
the strongest borrowers. The two interpretations carry opposite predictions for
distress. In Türkiye they align and median coverage falls monotonically across
terciles. In Vietnam the credit-quality effect dominates and the ordering
inverts, with the most short-funded tercile the healthiest in most years — 5.02
against 3.45 for the least short-funded in 2021, and 4.05 against 3.41 in 2025.

A proxy whose sign flips across two structurally similar markets is not
measuring a single underlying construct.

## 7. Identification

### 7.1 Inflation accounting as an exposure-by-post confound

Section 3.2 set out the mechanics of the Turkish restatement. Its empirical
signature is unmistakable.

**Table 10. Turkish median balance-sheet aggregates**

| Year | Equity / assets | Debt / assets |
|---|---|---|
| 2017 | 0.472 | 0.217 |
| 2018 | 0.440 | 0.211 |
| 2019 | 0.419 | 0.226 |
| 2020 | 0.421 | 0.219 |
| 2021 | 0.462 | 0.189 |
| **2022** | **0.558** | **0.138** |
| **2023** | **0.614** | **0.111** |
| 2024 | 0.646 | 0.100 |
| 2025 | 0.619 | 0.117 |

Median leverage more than halves between 2019 and 2024 while equity-to-assets
rises by over twenty points. No real deleveraging of that magnitude occurred in
a period of severe monetary tightening and currency depreciation; the movement
is restatement, and it begins in 2022 consistent with the April 2022
classification date and the restatement of comparatives.

The identification problem is sharper than a level break, and this is the point
we wish to press. The restatement factor applied to a firm's assets depends on
their vintage — a firm holding recently acquired assets is indexed less than one
holding assets acquired a decade earlier. Vintage varies across firms and is
correlated with capital intensity, sector, age and, critically, with financing
structure. The distortion is therefore *heterogeneous in exactly the dimension
that any balance-sheet exposure measure captures*.

Formally, suppose the reported outcome is Y*_it = Y_it + δ_i·1[t ≥ 2022]·φ_t,
where φ_t is the common restatement factor and δ_i is the firm-specific loading
that depends on asset vintage. If δ_i is correlated with exposure E_i — and it
is, because both derive from the balance sheet — then the term δ_i·1[t ≥ 2022]
is observationally equivalent to the interaction E_i × Post_t that the design
estimates. Country-by-year fixed effects absorb φ_t. They cannot absorb δ_i·φ_t.

This is demonstrable rather than conjectural. Estimating the standard design
with FX exposure as treatment and stock-based outcomes returns coefficients that
are highly significant and wrongly signed: firms with more foreign-currency debt
appear to *improve* after 2023 on every balance-sheet outcome (implied rate
−0.108, p < 0.0001; Altman Z″ +0.813, p = 0.004; leverage −0.049, p < 0.0001).
The event-study path grows monotonically — +0.32, +0.83, +1.18 across 2023–2025
— as the restatement compounds, and pre-treatment coefficients are large and
significant (2017: +0.83, p < 0.01; 2021: −0.59, p < 0.05). The result has every
outward mark of a strong causal finding and is an accounting artefact.

We regard this as the paper's most consequential warning. A substantial and
growing body of work uses Turkish firm-level balance-sheet data around the
2023 policy reversal. Any such study using stock-based ratios in a
difference-in-differences with an exposure interaction is exposed to this
problem, and the standard fixed-effects defence does not address it.

### 7.2 The surviving specification

Three restrictions follow.

*Outcomes must be flows.* A ratio of two restated flows is scaled by a common
factor that year effects absorb. We retain the implied borrowing rate (monetary
over monetary, hence invariant), interest coverage, EBIT margin, and the log
change in debt. We discard the Altman Z″ score, leverage, equity ratios and
return on assets — every one of which contains a non-monetary stock.

*Exposure must predate the restatement.* We measure it at 2021, before the
transition and before treatment, and standardise within country so coefficients
are interpretable per standard deviation.

*The pre-period must permit a test of parallel trends.* This is where the
data-source decision of Section 5.4 has teeth. Two of our four outcomes — EBIT
margin and debt growth — require no interest figure, so the bundling problem is
irrelevant to them and the national source's full history can be used. That
buys a 2015–2025 window for those outcomes. Section 8 shows that the extra
decade changes the conclusion.

The estimating equations are

  Y_it = β (E_i × Post_t) + α_i + λ_t + ε_it   (3)

  Y_it = Σ_k β_k (E_i × 1[t = k]) + α_i + λ_t + ε_it   (4)

with firm effects α_i, year effects λ_t, 2022 omitted in (4), and standard
errors clustered by firm.

## 8. Results

Under this specification the exposure gradient does not appear.

**Table 11. Main estimates: exposure × post, flow outcomes**

| Country | Exposure | Outcome | Firms | Coef. | SE | p |
|---|---|---|---|---|---|---|
| TR | Short-term share | Implied rate | 466 | 0.018 | 0.016 | 0.27 |
| TR | Short-term share | Interest coverage | 468 | −0.421 | 0.718 | 0.56 |
| TR | Short-term share | EBIT margin | 499 | −0.013 | 0.012 | 0.27 |
| TR | Short-term share | Debt growth | 502 | −0.002 | 0.035 | 0.96 |
| TR | FX exposure | Implied rate | 491 | −0.025 | 0.021 | 0.23 |
| TR | FX exposure | Interest coverage | 498 | 0.176 | 0.733 | 0.81 |
| TR | FX exposure | EBIT margin | 547 | 0.023 | 0.011 | **0.04** |
| TR | FX exposure | Debt growth | 536 | −0.055 | 0.028 | **0.05** |
| VN | Short-term share | Implied rate | 522 | −0.002 | 0.001 | 0.11 |
| VN | Short-term share | Interest coverage | 521 | −0.355 | 0.497 | 0.48 |
| VN | Short-term share | EBIT margin | 522 | −0.016 | 0.004 | **0.00** |
| VN | Short-term share | Debt growth | 522 | 0.059 | 0.019 | **0.00** |

Four coefficients reach conventional significance. The event studies show that
none is a treatment effect.

**Table 12. Event study: Turkish short-maturity share on debt growth (base 2022)**

| Year | Coefficient | SE | | Year | Coefficient | SE |
|---|---|---|---|---|---|---|
| 2015 | −0.138** | 0.068 | | 2021 | −0.232*** | 0.066 |
| 2016 | −0.187*** | 0.065 | | 2022 | base | — |
| 2017 | −0.162*** | 0.062 | | **2023** | **−0.220*** | 0.069 |
| 2018 | −0.189*** | 0.072 | | 2024 | −0.069 | 0.076 |
| 2019 | −0.252*** | 0.070 | | 2025 | −0.191*** | 0.064 |
| 2020 | −0.211*** | 0.057 | | | | |

Firms with more short-term debt grow debt more slowly in every year from 2015
onward. The coefficient at treatment is statistically indistinguishable from
those seven years earlier. Nothing happens in 2023.

The Vietnamese EBIT-margin result has the same character. The coefficient drifts
from +0.020 (p < 0.01) in 2015 through +0.011 (p < 0.05) in 2020 to −0.011
(p < 0.10) in 2025, passing smoothly through the treatment year without
discontinuity. This is a decade-long secular trend in the relative profitability
of short-funded firms, not a response to monetary policy.

What a conventional two-year window would have reported is precisely the
difference between the 2022 base and the 2023–2025 average — a difference that
exists, is statistically significant, and means nothing causal.

## 9. Robustness

### 9.1 Placebo treatment

If the design manufactures effects, it should manufacture them at a false date.
Assigning a placebo treatment at 2018 and restricting the sample to 2015–2021
returns nothing: for Vietnam, coefficients of −0.791 (p = 0.19) on interest
coverage and +0.004 (p = 0.51) on EBIT margin. The design is not mechanically
generating significance, which strengthens the interpretation of Section 8's
significant coefficients as genuine pre-existing trends rather than artefacts of
specification.

### 9.2 Sample expansion as a diagnostic

The Turkish estimates were computed at three sample sizes as data collection
proceeded, which provides an unplanned but informative stability check. At 83
firms the specification returned an effect of +0.886 on the Altman Z″ score
(p = 0.045) together with significant pre-trends. At 158 firms both vanished. At
the full 585-firm sample the estimates are those of Table 11. Roughly a third of
the eventual sample produced a significant result of the wrong sign with
apparent pre-trend violation; two-thirds produced neither.

We report this because it is a realistic depiction of how such analyses proceed
and because the lesson generalises. Sample-size stability is cheap to check and
rarely reported.

### 9.3 Alternative specifications

The results are unchanged under winsorisation at 1%/99% rather than 2%/98%;
under exposure measured at 2020 or as the 2020–2021 mean rather than 2021 alone;
under exclusion of the smallest tercile by assets; and under exclusion of 2022
from the estimation window to guard against the restatement of comparatives.
None alters any conclusion, and none converts a null into an effect.

### 9.4 What would overturn the null

Candour requires stating what evidence would change our reading. Quarterly data
would raise the observation count for equation (2) fourfold and might render
firm-level betas estimable; the Turkish source supplies quarterly statements,
though Vietnam has no comparable source at scale, which would break the
symmetry the comparison rests on. Portfolio sorting, aggregating firms before
estimating sensitivities, would average away the idiosyncratic noise that
defeats firm-level betas at the cost of the heterogeneity that motivates the
exercise. And disclosure of repricing basis in the notes to accounts, were it
machine-readable at scale, would remove the problem entirely.

## 10. Implications for practice

We draw four practical conclusions for firm-level work on monetary transmission
in emerging markets, each of which follows from a specific finding above.

*Validate the price measure against the policy path before using it.* The
implied borrowing cost passes this test in both countries, and it is the test
that exposed the bundled-expense problem of Section 5.4. A measure that cannot
reproduce a known aggregate should not be used to estimate an unknown
cross-section.

*Do not estimate firm-specific sensitivities from annual accounting data.*
Roughly a decade of annual observations cannot support a firm-level slope, and
conventional in-sample diagnostics will not reveal this. Split-half reliability
and a first-stage prediction test are both inexpensive and decisive; we
recommend they be reported whenever an estimated firm characteristic enters as a
regressor.

*In inflation-accounting regimes, treat every stock-based ratio as suspect and
prefer flows.* Because the restatement is heterogeneous across firms, the
contamination enters as an interaction and the usual fixed-effects reasoning
does not apply. This affects any study of Turkish firms spanning 2022, and
equally any study of other economies that have crossed the hyperinflation
threshold.

*Extend the pre-period until parallel trends can genuinely be tested, even at
the cost of outcome variables.* Restricting to outcomes with long history
revealed that our significant coefficients were decade-long trends. A one- or
two-year pre-period would have concealed this and, in our case, would have
produced a publishable false positive.

## 11. Conclusion

Published financial statements support a genuine, validated measure of the price
of corporate debt, and that measure recovers monetary policy paths in two very
different regimes — a severe Turkish tightening and a mild Vietnamese one. Using
it, we document that pass-through is large but far from complete, that median
Turkish interest coverage halved across the tightening while Vietnam's dipped
and recovered, and that a commonly used data field conflates currency shocks
with interest costs.

Statements do not support a measure of which firms are contractually exposed to
repricing. That object — the treatment variable of the floating-rate literature
— is absent from the accounting record, cannot be estimated reliably from annual
observations, and is not adequately proxied by the balance-sheet characteristics
that are measured well. When we impose the discipline that the identification
requires, no cross-sectional gradient survives in either country.

The implication is not that the channel fails to operate. Our aggregate evidence
is entirely consistent with its operating forcefully in Türkiye. The implication
is narrower and, we think, more useful: the cross-sectional question — *which*
firms bear the adjustment — requires contractual data. Researchers without
registry access should direct their effort toward the aggregate and price-side
questions that statements can answer, and toward the institutional work of
making repricing terms disclosable, rather than toward proxies that cannot carry
the weight placed on them.

That conclusion is more encouraging than it may appear. The price measure
validated here is available in essentially every market with audited filings,
and the questions it can answer — how much of a policy move reaches corporate
borrowing costs, how quickly, and how far coverage ratios deteriorate — are
first-order for financial stability. They are simply not the questions the
registry literature has taught us to ask.

---

## References

Acharya, V. V., Crosignani, M., Eisert, T., & Eufinger, C. (2024). Zombie credit
and (dis-)inflation: Evidence from Europe. *The Journal of Finance*, 79(3),
1883–1929. https://doi.org/10.1111/jofi.13342

Aguiar, M. (2005). Investment, devaluation, and foreign currency exposure: The
case of Mexico. *Journal of Development Economics*, 78(1), 95–113.
https://doi.org/10.1016/j.jdeveco.2004.06.012

Akbal, E., & Civcir, I. (2026). The asymmetric effect of capital flows and
credit default swap spreads on the US dollar/Turkish lira exchange rate. *Borsa
Istanbul Review*, 26, 100774. https://doi.org/10.1016/j.bir.2025.100774

Almeida, H., Campello, M., Laranjeira, B., & Weisbenner, S. (2012). Corporate
debt maturity and the real effects of the 2007 credit crisis. *Critical Finance
Review*, 1(1), 3–58. https://doi.org/10.1561/104.00000001

Altman, E. I. (2005). An emerging market credit scoring system for corporate
bonds. *Emerging Markets Review*, 6(4), 311–323.

Auer, S., Friedrich, C., Ganarin, M., Paligorova, T., & Towbin, P. (2019).
International monetary policy transmission through banks in small open
economies. *Journal of International Money and Finance*, 90, 34–53.
https://doi.org/10.1016/j.jimonfin.2018.08.008

Barniv, R. (1999). The value relevance of inflation-adjusted and historical-cost
earnings during hyperinflation. *Journal of International Accounting, Auditing
and Taxation*, 8(2), 269–287. https://doi.org/10.1016/S1061-9518(99)00016-6

Bernanke, B. S., & Gertler, M. (1995). Inside the black box: The credit channel
of monetary policy transmission. *Journal of Economic Perspectives*, 9(4),
27–48. https://doi.org/10.1257/jep.9.4.27

Bleakley, H., & Cowan, K. (2008). Corporate dollar debt and depreciations: Much
ado about nothing? *Review of Economics and Statistics*, 90(4), 612–626.
https://doi.org/10.1162/rest.90.4.612

Bruno, V., & Shin, H. S. (2015a). Cross-border banking and global liquidity.
*The Review of Economic Studies*, 82(2), 535–564.
https://doi.org/10.1093/restud/rdu042

Bruno, V., & Shin, H. S. (2015b). Capital flows and the risk-taking channel of
monetary policy. *Journal of Monetary Economics*, 71, 119–132.
https://doi.org/10.1016/j.jmoneco.2014.11.011

Callaway, B., & Sant'Anna, P. H. C. (2021). Difference-in-differences with
multiple time periods. *Journal of Econometrics*, 225(2), 200–230.
https://doi.org/10.1016/j.jeconom.2020.12.001

Cloyne, J., Ferreira, C., Froemel, M., & Surico, P. (2023). Monetary policy,
corporate finance, and investment. *Journal of the European Economic
Association*, 21(6), 2586–2634. https://doi.org/10.1093/jeea/jvad009

Davis-Friday, P. Y., & Gordon, E. A. (2005). Relative valuation roles of equity
book value, net income, and cash flows during a macroeconomic shock: The case of
Mexico and the 1994 currency crisis. *Journal of International Accounting
Research*, 4(1), 1–21. https://doi.org/10.2308/jiar.2005.4.1.1

de Chaisemartin, C., & D'Haultfœuille, X. (2020). Two-way fixed effects
estimators with heterogeneous treatment effects. *American Economic Review*,
110(9), 2964–2996. https://doi.org/10.1257/aer.20181169

De Franco, G., Kothari, S. P., & Verdi, R. S. (2011). The benefits of financial
statement comparability. *Journal of Accounting Research*, 49(4), 895–931.
https://doi.org/10.1111/j.1475-679X.2011.00415.x

Demirgüç-Kunt, A., & Maksimovic, V. (1999). Institutions, financial markets, and
firm debt maturity. *Journal of Financial Economics*, 54(3), 295–336.
https://doi.org/10.1016/S0304-405X(99)00039-2

Du, W., & Schreger, J. (2022). Sovereign risk, currency risk, and corporate
balance sheets. *The Review of Financial Studies*, 35(10), 4587–4629.
https://doi.org/10.1093/rfs/hhac001

Eichengreen, B., & Hausmann, R. (1999). *Exchange rates and financial fragility*
(NBER Working Paper No. 7418). National Bureau of Economic Research.

Gertler, M., & Gilchrist, S. (1994). Monetary policy, business cycles, and the
behavior of small manufacturing firms. *The Quarterly Journal of Economics*,
109(2), 309–340. https://doi.org/10.2307/2118465

Goodman-Bacon, A. (2021). Difference-in-differences with variation in treatment
timing. *Journal of Econometrics*, 225(2), 254–277.
https://doi.org/10.1016/j.jeconom.2021.03.014

Gordon, E. A. (2001). Accounting for changing prices: The value relevance of
historical cost, price level, and replacement cost accounting in Mexico.
*Journal of Accounting Research*, 39(1), 177–200.
https://doi.org/10.1111/1475-679X.00008

Greenwald, D. (2019). *Firm debt covenants and the macroeconomy: The interest
coverage channel* (Working paper). [Publication status to be verified before
submission.]

Griliches, Z., & Hausman, J. A. (1986). Errors in variables in panel data.
*Journal of Econometrics*, 31(1), 93–118.
https://doi.org/10.1016/0304-4076(86)90058-8

He, Z., & Xiong, W. (2012). Rollover risk and credit risk. *The Journal of
Finance*, 67(2), 391–430.
https://doi.org/10.1111/j.1540-6261.2012.01721.x

Ippolito, F., Ozdagli, A. K., & Perez-Orive, A. (2018). The transmission of
monetary policy through bank lending: The floating rate channel. *Journal of
Monetary Economics*, 95, 49–71.

Jungherr, J., Meier, M., Reinelt, T., & Schott, I. (2024). *Corporate debt
maturity matters for monetary policy* (International Finance Discussion Papers
No. 1402). Board of Governors of the Federal Reserve System.

Kalemli-Ozcan, S., Kamil, H., & Villegas-Sanchez, C. (2016). What hinders
investment in the aftermath of financial crises: Insolvent firms or illiquid
banks? *Review of Economics and Statistics*, 98(4), 756–769.
https://doi.org/10.1162/REST_a_00590

Kashyap, A. K., & Stein, J. C. (2000). What do a million observations on banks
say about the transmission of monetary policy? *American Economic Review*,
90(3), 407–428. https://doi.org/10.1257/aer.90.3.407

Konchitchki, Y. (2011). Inflation and nominal financial reporting: Implications
for performance and stock prices. *The Accounting Review*, 86(3), 1045–1085.
https://doi.org/10.2308/accr.00000044

Ottonello, P., & Winberry, T. (2020). Financial heterogeneity and the investment
channel of monetary policy. *Econometrica*, 88(6), 2473–2502.
https://doi.org/10.3982/ECTA15949

Ozdagli, A. K. (2017). Financial frictions and the stock price reaction to
monetary policy. *The Review of Financial Studies*, 31(10), 3895–3936.
https://doi.org/10.1093/rfs/hhx106

Pagan, A. (1984). Econometric issues in the analysis of regressions with
generated regressors. *International Economic Review*, 25(1), 221–247.
https://doi.org/10.2307/2648877

Petersen, M. A. (2009). Estimating standard errors in finance panel data sets:
Comparing approaches. *The Review of Financial Studies*, 22(1), 435–480.
https://doi.org/10.1093/rfs/hhn053

Roth, J. (2022). Pretest with caution: Event-study estimates after testing for
parallel trends. *American Economic Review: Insights*, 4(3), 305–322.
https://doi.org/10.1257/aeri.20210236

Sun, L., & Abraham, S. (2021). Estimating dynamic treatment effects in event
studies with heterogeneous treatment effects. *Journal of Econometrics*, 225(2),
175–199. https://doi.org/10.1016/j.jeconom.2020.09.006

Şengül, A., & Çinko, L. (2026). Monetary tightening and corporate default risk:
Evidence from floating-rate debt exposure. *Borsa Istanbul Review*, 26(4),
100837. https://doi.org/10.1016/j.bir.2026.100837
