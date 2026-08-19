# What Financial Statements Can and Cannot Reveal About Monetary Transmission to Corporate Balance Sheets: Evidence from Vietnam and Türkiye

## Abstract

Recent work using administrative credit registries finds that firms with
floating-rate debt bear the brunt of monetary tightening. Whether that finding
can be reproduced — or extended to countries without such registries — using
published financial statements is an open and consequential question, because
statements are the only firm-level data available in most emerging markets. We
assemble harmonised panels for 693 Vietnamese and 585 Turkish listed
non-financial firms spanning 2010–2025, each cross-validated against an
independent source, and ask what the exercise can support. Three results are
constructive. First, a simple implied borrowing cost, interest expense over
average debt, recovers each central bank's policy path without being given it:
the Turkish series peaks in 2024 at 31.2% as policy peaks at 47.5%, and the
Vietnamese series traces the 2011 inflation crisis and the 2023 tightening.
Second, pass-through is large but incomplete — a 38-percentage-point Turkish
policy move produces a 13.4-point move in realised borrowing costs while median
interest coverage halves. Third, we document that a widely used Turkish data
field bundles currency revaluation into interest expense, so that measures
built on it recover lira crises and mislabel them as monetary transmission.
Against these, three results are cautionary. Firm-level pass-through
sensitivities estimated from annual data fail split-half reliability, with
correlations of −0.22 and −0.08 across sample halves and in-sample fit
indistinguishable from noise. Turkish inflation accounting from 2023 restates
non-monetary assets while leaving monetary debt nominal, and because asset
vintage differs across firms this enters as an exposure-by-post interaction
that fixed effects cannot absorb. Once contaminated outcomes are removed,
exposure is measured before restatement, and the pre-period is extended far
enough to test the identifying assumption, no exposure gradient survives in
either country: the apparent relationships are persistent level differences
that predate treatment by years. We conclude that the contractual object these
designs require is not recoverable from published statements, and set out what
can be measured instead.

**Keywords:** monetary transmission; corporate default; measurement error;
inflation accounting; emerging markets; financial statements

**JEL classification:** E52; G32; M41; C23

---

## 1. Introduction

A firm that borrows at a floating rate feels a policy tightening immediately.
One that borrowed long and fixed does not. This simple asymmetry has become the
organising idea of a productive literature on how monetary policy reaches the
corporate sector, and the empirical work behind it has been built almost
entirely on supervisory data. Ippolito, Ozdagli, and Perez-Orive (2018)
identify a floating rate channel using matched loan-level records. Şengül and
Çinko (2026), studying the June 2023 reversal in Türkiye, use a large
administrative dataset and a two-part Double Machine Learning design, finding
that the average effect is modest but concentrated in firms with weak internal
risk ratings, low liquidity and high exposure shares, while exporters and
manufacturers are relatively insulated.

The common ingredient is a credit registry that records, loan by loan, whether
the contract reprices. Most of the world's emerging markets have no such
registry available to researchers. What they do have is published financial
statements. The natural question — and the one this paper takes seriously — is
whether the accounting record is a workable substitute. If it is, the
literature's reach expands enormously. If it is not, a great deal of effort is
being spent on designs that cannot deliver, and it is worth knowing precisely
where and why they fail.

We approach this as a measurement problem, and we approach it comparatively.
Vietnam and Türkiye share the structural features that make the floating-rate
channel plausible: bank-dominated corporate finance, thin corporate bond
markets, heavy reliance on short-maturity credit, and a substantial listed
non-financial sector. What they do not share is the monetary experience of
2021–2025. Türkiye executed one of the most severe tightenings of the decade,
from 9% to 47.5%, under inflation that exceeded 60%. Vietnam tightened mildly
in late 2022 and reversed within a year. A measurement strategy that works
should register both, in proportion. That contrast is what makes the pair
useful: it provides a strong dose and a weak one, and any method that cannot
distinguish them is not measuring what it claims to.

Our answer has two halves, and we regard both as findings.

The constructive half is that the *price* of corporate debt is recoverable, and
recoverable well. A firm's implied borrowing cost — interest expense divided by
average debt — aggregates to a series that reproduces each central bank's
policy path without being told it. This is not a trivial diagnostic. It
establishes that ordinary audited statements contain a legible signal of
monetary transmission, and it provides the validation on which any further
measurement must rest. We use it to quantify pass-through, and we use it to
expose a data problem that would otherwise be invisible: İş Yatırım's widely
used financial-expense field bundles foreign-exchange revaluation into interest,
and measures built on it peak in Türkiye's currency crises of 2018 and 2021
rather than at the policy peak of 2024.

The cautionary half is that *exposure* is not recoverable. This is the object
the literature needs, and it defeats every strategy we try. Firm-level
pass-through sensitivities, estimated in the natural way from annual data, do
not survive a split-half reliability test: betas estimated on one half of the
sample correlate at −0.22 and −0.08 with those estimated on the other, and
in-sample fit is indistinguishable from what pure noise would produce. Nor do
balance-sheet proxies help. The short-maturity share, the obvious candidate,
proxies creditworthiness as much as repricing risk — firms that roll short-term
paper cheaply are frequently the strongest borrowers, and in Vietnam that effect
dominates and inverts the ordering.

Layered on top is a problem specific to high-inflation settings that we believe
deserves wider attention. From fiscal 2023, Turkish listed companies restate
their statements under inflation accounting. Non-monetary assets are indexed;
monetary debt is not. Because asset vintage differs across firms, the
restatement effect is *heterogeneous in any exposure variable built from the
balance sheet*, and therefore enters the regression as an exposure-by-post
interaction — precisely where the coefficient of interest sits. Country-by-year
fixed effects, the natural defence, absorb the common level shift and leave the
contamination untouched. We show that this is not hypothetical: a specification
using FX exposure produces highly significant coefficients with the wrong sign,
whose post-treatment path grows monotonically as the restatement compounds.

When we strip out the contaminated outcomes, measure exposure before the
restatement takes effect, and extend the pre-period far enough that the
identifying assumption can actually be tested, nothing survives. The
exposure-outcome relationships that appear significant turn out to be
persistent level differences that predate the treatment by years and do not
shift when policy moves.

We regard this null as informative rather than empty, for a specific reason.
Over the course of the analysis, three separate significant results appeared and
were each subsequently shown to be artefacts — small-sample noise, accounting
restatement, and pre-existing trend — by diagnostics that a conventional
specification would not have run. A design that produces three false positives
before producing a null is telling us something about the design, and the
diagnostics that caught them are transferable.

The paper contributes in three directions. To the monetary transmission
literature, it delimits where statement-based designs can and cannot substitute
for registry data, and it supplies a validated price measure that survives the
transition. To empirical work on Türkiye, it documents two data hazards — one in
a commonly used vendor field, one in the accounting standard itself — that
threaten a broad class of post-2023 studies. To research on Vietnam, it
introduces a firm-level statement panel that has not previously been used for
questions of this kind, harmonised against a Turkish counterpart and validated
throughout.

## 2. Institutional setting

### 2.1 Two monetary regimes

Türkiye's tightening is the sharper of the two by an order of magnitude. The
one-week repo rate stood at 9.0% at the end of 2022, reached 42.5% by the end of
2023, peaked at 47.5% in 2024, and stood at 38.0% at the end of 2025. Inflation
exceeded 60% at its height. Vietnam's State Bank raised policy rates in late
2022 in response to stress in the domestic bond market and reversed course
through 2023; the average lending rate rose from 8.0% in 2022 to 9.3% in 2023,
against 17.0% at the peak of the 2011 inflation episode.

The comparison is therefore not between a treatment and a control, but between
a large dose and a small one, and the appropriate prediction is proportional
rather than binary.

### 2.2 Inflation accounting in Türkiye

From fiscal 2023, Turkish listed companies apply inflation accounting.
Non-monetary items — property, plant and equipment, inventories, equity — are
restated by a general price index tied to each item's acquisition date.
Monetary items — debt, cash, receivables — are already expressed in
period-end purchasing power and are not restated. Income-statement items are
restated to period-end purchasing power by a common factor.

The consequences for empirical work are direct and, in our reading,
underappreciated. Any ratio with a non-monetary stock in it moves mechanically
at the transition. Any ratio of two flows is largely unaffected, because both
are scaled by a common factor that year effects absorb. And critically, the
magnitude of the restatement depends on the vintage of a firm's assets, which
varies across firms — so the distortion is not a common shock. Section 6
develops the implication.

## 3. Data

### 3.1 Sources and coverage

The Vietnamese panel is drawn from an item-level dataset of statements filed by
companies listed on the Ho Chi Minh City and Hanoi exchanges, distributed
through a public repository. It yields 9,893 firm-years for 693 firms over
2011–2025, with non-missing coverage of 94.5% for total assets, 94.7% for total
debt, 91.2% for interest expense, 93.2% for EBIT and 96.8% for equity.

The Turkish panel is drawn from a brokerage data service that redistributes
filings made to the Public Disclosure Platform. A single request returns the
balance sheet, income statement, cash-flow statement and a block of
supplementary items with bilingual labels, for four annual periods. The
resulting panel covers 585 firms over 2010–2025. It carries two items with no
Vietnamese counterpart and considerable analytical value: export sales and net
foreign-currency position.

Both panels are restricted to non-financial firms. Banks, insurers and brokers
file on incompatible templates and their liability structure is not comparable
to that of non-financial borrowers.

### 3.2 Cross-validation against an independent source

Because the paper's subject is measurement, we validate each national source
against an independent commercial aggregator that normalises the same filings
and retains four to five annual periods. Agreement is not assumed; it is
tested, and the pattern of disagreement is as informative as the agreement.

Where the two should agree, they agree closely. Total assets reconcile at a
median relative difference of 0.0000, with correlations of 1.0000 in Vietnam
and 0.9960 in Türkiye; revenue reconciles at 0.0000 with correlations of 0.9999
and 0.9935. Vietnamese interest expense reconciles at a median difference of
0.00% on absolute values, with a correlation of 0.991 and 78% of firm-years
agreeing within two percent.

Three discrepancies are systematic and each is definitional. Equity differs by
roughly four percent in Vietnam because the aggregator reports parent-only
shareholders' equity where the national source consolidates minority interest.
EBIT differs by about 21–23% in both countries because the aggregator derives it
from pretax income plus interest rather than taking reported operating profit.
The third discrepancy is not definitional in the benign sense, and we treat it
separately in Section 4.3.

## 4. Measuring the price of corporate debt

### 4.1 Construction

For firm *i* in year *t* we define the implied borrowing cost as interest
expense divided by the average of beginning- and end-of-year debt:

  r_it = |interest expense_it| / ½(D_it + D_i,t−1)

Averaging the denominator prevents the ratio from being driven mechanically by
borrowing undertaken during the year. The measure has an important property in
the Turkish context: numerator and denominator are both monetary, so it is
invariant to the inflation restatement discussed in Section 2.2.

### 4.2 Validation against policy paths

The measure is not calibrated to any policy series. Whether it recovers one is
therefore a genuine test, and it passes in both countries.

**Table 1. Median implied borrowing cost and the policy path**

| Vietnam | Implied cost | | Türkiye | Implied cost | CBRT policy (year-end) |
|---|---|---|---|---|---|
| 2011 | 11.1% | | 2022 | 17.8% | 9.0% |
| 2015 | 5.8% | | 2023 | 25.4% | 42.5% |
| 2023 | 7.2% | | 2024 | **31.2%** | **47.5%** |
| 2025 | 5.8% | | 2025 | 25.8% | 38.0% |

The Turkish series peaks in 2024, the year policy peaks. The Vietnamese series
peaks in 2011, at the height of that country's inflation crisis, falls through
the easing cycle to 5.8% by 2015, rises to 7.2% in the 2023 tightening and
subsides again. Median interest coverage moves in the mirror image, reaching its
sample minimum of 2.05 in Vietnam in exactly 2023.

That an accounting ratio constructed from published statements traces a policy
path it was never shown is the paper's foundational result. It establishes that
the price side of monetary transmission is legible in ordinary filings.

### 4.3 Pass-through is large but far from complete

The Turkish episode allows a quantification that registry studies rarely
report. Policy moved 38 percentage points between end-2022 and the 2024 peak.
Realised borrowing costs moved 13.4 points, from 17.8% to 31.2% — a pass-through
of roughly 35%. Over the same window median interest coverage halved, from 3.36
to 1.66.

Vietnam's mild cycle produces a proportionally mild response: costs move 0.8
points and coverage dips from 3.11 to 2.05 before recovering to 2.70 as policy
reverses. The dose-response contrast is clear in aggregate, which makes the
firm-level null of Section 7 the more striking.

Incomplete pass-through is itself economically meaningful. It is consistent with
maturity structure delaying repricing, with credit rationing substituting for
price adjustment, and with directed or subsidised lending, all of which are
plausible in the Turkish setting and none of which we can separate here.

### 4.4 A data hazard: bundled financial expense

The Turkish source's `4BB` field is labelled *Financial Expenses* and is the
natural candidate for an interest measure over the long history. It should not
be used as one. Against the independent aggregator's interest expense, it runs
roughly three times larger — a median relative difference of −68.8%, with a
correlation of 0.727 on absolute values, against Vietnam's 0.991 and 0.00%.

The field bundles foreign-exchange revaluation losses with interest. The
consequence is not a modest attenuation but a change in what the measure
tracks. Built on `4BB`, the Turkish implied cost peaks in **2018 and 2021** —
the two lira crisis years. Built on a clean interest figure, it peaks in **2024**
with policy. A researcher using the bundled field to study monetary
transmission would recover currency shocks and report them as interest-rate
effects.

We accordingly take Turkish interest-based quantities from the aggregator and
reserve the national source for balance-sheet characteristics and for outcomes
that require no interest figure.

## 5. Measuring exposure

### 5.1 The object the literature needs is not in the data

Contractual floating-rate status is not disclosed in published statements. No
estimator recovers it. The question is whether something adequate can be
constructed, and we consider the two natural candidates.

### 5.2 Revealed repricing sensitivity fails reliability testing

The most appealing candidate infers exposure from behaviour. For each firm we
estimate, over a window ending before treatment,

  Δr_it = a_i + β_i ΔPolicy_t + γ_i Δln(FX)_t + ε_it

where β_i is the firm's repricing sensitivity. The FX term is included jointly
rather than as a nuisance control, since in Türkiye a large part of the movement
in realised borrowing cost comes from currency revaluation.

The estimates are well behaved on the surface. Roughly 72% of firms in both
countries return a positive β, and the mean Vietnamese pass-through implies that
a one-point rise in the lending rate raises a firm's own cost of funds by about
0.79 points — economically sensible for a corporate sector funded predominantly
at short maturity.

They do not survive validation. We subject them to two tests.

**Split-half reliability.** Betas estimated on 2012–2017 are compared with betas
estimated on 2018–2022 for firms present in both windows. A measure of a stable
firm characteristic should correlate strongly across halves.

**Table 2. Split-half reliability of candidate exposure measures**

| Measure | Türkiye | Vietnam |
|---|---|---|
| Repricing beta | **−0.219** | **−0.080** |
| FX beta | +0.147 | +0.094 |
| Short-term debt share | +0.438 | +0.628 |
| Export share | +0.838 | — |

The estimated betas correlate at zero or below. The *measured* balance-sheet
characteristics, by contrast, are stable traits. The failure is specific to
regression-estimated quantities, not to the data.

**Fit against a noise benchmark.** With a median of six usable annual
observations and two regressors, the R² expected from pure noise is
approximately 0.40. The observed Vietnamese median is 0.396.

The diagnosis is straightforward. Year-to-year variation in a firm's implied
cost reflects changes in debt composition, the timing of drawdowns and one-off
charges, and at annual frequency this idiosyncratic component overwhelms the
common policy signal. Roughly a decade of annual observations is not enough to
estimate a firm-specific slope.

**A first-stage test confirms it.** Neither country's β predicts the firm's
actual change in borrowing cost across the tightening: R² of 0.035 in Türkiye
and 0.002 in Vietnam, with the most-exposed Turkish tercile recording the
*smallest* increase.

### 5.3 Balance-sheet proxies are stable but do not identify repricing

The measured characteristics in Table 2 are reliable, which makes them the
natural fallback. They fail for a different reason: none predicts the actual
change in borrowing cost. Regressing that change on standardised pre-period
characteristics yields R² below 0.02 for the short-term debt share, leverage,
the current ratio, size and interest coverage, in both countries.

The short-maturity share illustrates the underlying confound. It is
simultaneously a measure of repricing exposure and of credit quality, because
firms that can roll short-term paper cheaply tend to be strong borrowers. In
Türkiye the two effects align and coverage falls monotonically across terciles.
In Vietnam the credit-quality effect dominates and the ordering inverts, with
the most short-funded tercile the healthiest in most years.

## 6. Identification and its failure modes

### 6.1 Inflation accounting as an exposure-by-post confound

Section 2.2 described the mechanics of the Turkish restatement. Its empirical
signature is unmistakable.

**Table 3. Turkish median balance-sheet aggregates**

| Year | Equity / assets | Debt / assets |
|---|---|---|
| 2017 | 0.472 | 0.217 |
| 2019 | 0.419 | 0.226 |
| 2021 | 0.462 | 0.189 |
| 2022 | 0.558 | 0.138 |
| 2023 | 0.614 | 0.111 |
| 2024 | 0.646 | 0.100 |

Median leverage more than halves between 2019 and 2024 and equity-to-assets
rises by more than twenty points. No real deleveraging of that magnitude
occurred; the movement is restatement.

The identification problem is sharper than a level break. Because the
restatement factor applied to a firm's assets depends on their vintage, and
vintage varies across firms, the distortion is heterogeneous in exactly the
dimension that any balance-sheet exposure measure captures. It therefore enters
the estimating equation as an exposure-by-post interaction — the coefficient of
interest — and country-by-year fixed effects, which absorb only the common
component, provide no protection.

This is demonstrable rather than conjectural. Estimating the standard design
with FX exposure as the treatment yields coefficients that are highly
significant and wrongly signed: firms with more foreign-currency debt appear to
*improve* on every balance-sheet outcome after 2023 (implied rate −0.108,
p < 0.0001; Altman Z″ +0.813, p = 0.004). The event-study path grows
monotonically — +0.32, +0.83, +1.18 across 2023–2025 — as the restatement
compounds, and pre-treatment coefficients are large and significant. The result
is an accounting artefact wearing the clothes of a causal estimate.

### 6.2 The specification that survives

Three restrictions follow. Outcomes must be flows, since a ratio of two
restated flows is scaled by a common factor that year effects absorb: we retain
the implied rate (monetary over monetary), interest coverage, EBIT margin and
debt growth, and discard Altman Z″, leverage, equity ratios and return on
assets. Exposure must be measured before the restatement, which we take at
2021. And the pre-period must be long enough to test parallel trends — for the
two outcomes requiring no interest figure, EBIT margin and debt growth, the
national source supplies history back to 2015.

## 7. Results

Under this specification the exposure gradient does not appear.

Four coefficients reach conventional significance — Turkish FX exposure on EBIT
margin (+0.023, p = 0.041) and on debt growth (−0.055, p = 0.054), Vietnamese
short-maturity share on EBIT margin (−0.016, p = 0.0001) and on debt growth
(+0.059, p = 0.002). The event studies show that none is a treatment effect.

**Table 4. Event study: Turkish short-maturity share on debt growth (base 2022)**

| Year | Coefficient | | Year | Coefficient |
|---|---|---|---|---|
| 2015 | −0.138** | | 2021 | −0.232*** |
| 2016 | −0.187*** | | 2022 | base |
| 2017 | −0.162*** | | **2023** | **−0.220*** |
| 2019 | −0.252*** | | 2024 | −0.069 |
| 2020 | −0.211*** | | 2025 | −0.191*** |

Firms with more short-term debt grow debt more slowly in every year from 2015
onward, and nothing whatever happens at treatment. The Vietnamese EBIT-margin
result has the same character: a coefficient that drifts from +0.020 (p < 0.01)
in 2015 to −0.011 (p < 0.10) in 2025, passing smoothly through the treatment
year without a discontinuity. These are persistent differences between firm
types, not responses to monetary policy.

The null is credible in proportion to the diagnostics behind it. Three earlier
significant results in this project were each shown to be artefacts: a Turkish
effect of +0.886 (p = 0.045) that vanished when the sample doubled; the FX
results of Section 6.1, which were restatement; and the coefficients above,
which are pre-trend. A specification that reports only the first of these — as a
conventional short-window design would — would have published a false positive.

## 8. Implications for practice

For firm-level work on monetary transmission in emerging markets we draw four
practical conclusions.

*Validate the price measure against the policy path before using it.* The
implied borrowing cost passes this test in both countries, and the test is what
exposed the bundled-expense problem in Section 4.4.

*Do not estimate firm-specific sensitivities from annual data.* Roughly a decade
of annual observations cannot support a firm-level slope. Split-half reliability
is a cheap and decisive check, and we recommend it be reported whenever an
estimated firm characteristic is used as a regressor.

*In inflation-accounting regimes, treat every stock-based ratio as suspect and
prefer flows.* The heterogeneity of the restatement across firms means the
contamination enters as an interaction, so the usual fixed-effects reasoning
does not apply.

*Extend the pre-period until parallel trends can be tested, even at the cost of
outcomes.* Restricting to outcomes with long history revealed that our
significant coefficients were decade-long trends. A one- or two-year pre-period
would have concealed this.

## 9. Conclusion

Published financial statements support a genuine and validated measure of the
price of corporate debt, and that measure recovers monetary policy paths in two
very different regimes. They do not support a measure of which firms are
contractually exposed to repricing. That object — the treatment variable of the
floating-rate literature — is absent from the accounting record, cannot be
estimated reliably from annual observations, and is not adequately proxied by
the balance-sheet characteristics that are measured well.

The implication is not that the channel does not operate. Our aggregate
evidence is entirely consistent with its operating: Turkish borrowing costs rose
13 points and coverage halved. The implication is narrower and more useful. The
cross-sectional question — *which* firms bear the adjustment — requires
contractual data, and researchers without registry access should direct their
effort toward the aggregate and price-side questions that statements can answer,
or toward obtaining the contractual data that the cross-sectional question
demands.

---

## References

*Note to co-authors: the following are verified. The list requires expansion —
in particular on emerging-market corporate FX mismatch, inflation accounting
under IAS 29, and recent 2025–2026 work on monetary transmission — before
submission. Every added entry must be verified against the publisher record.*

Altman, E. I. (2005). An emerging market credit scoring system for corporate
bonds. *Emerging Markets Review*, 6(4), 311–323.

Ippolito, F., Ozdagli, A. K., & Perez-Orive, A. (2018). The transmission of
monetary policy through bank lending: The floating rate channel. *Journal of
Monetary Economics*, 95, 49–71.

Şengül, A., & Çinko, L. (2026). Monetary tightening and corporate default risk:
Evidence from floating-rate debt exposure. *Borsa Istanbul Review*, 26(4),
100837. https://doi.org/10.1016/j.bir.2026.100837
