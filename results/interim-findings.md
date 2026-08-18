# Interim estimation results

Run on the 2021-2025 window: Vietnam from `vnfinancialdata` (532 firms),
Türkiye from Yahoo Finance (465 firms), 4,290 firm-year observations.

## Headline: the difference-in-differences is null, and the reason is diagnosable

Neither exposure proxy produces a significant effect on interest coverage or
the Altman Z''-score in either country, and the triple-difference term is
insignificant throughout (`results/did_estimates.csv`). Only one coefficient is
both significant and theory-consistent: in Vietnam, a one-standard-deviation
higher pre-period leverage raises the post-2023 implied borrowing rate by
0.45 percentage points (p = 0.001). That is the *first stage* of the channel --
policy passing into the cost of funds -- without a measurable second stage into
default risk.

This is a real result about the current design, not a failed run. Three causes,
in order of importance.

## 1. The exposure proxy is confounded

Median interest coverage by pre-period short-term-debt-share tercile:

**Türkiye** -- monotone, and the ordering holds throughout:

| Year | Low | Mid | High |
|---|---|---|---|
| 2022 | 4.48 | 2.77 | 3.02 |
| 2023 | 3.42 | 2.98 | 2.15 |
| 2024 | 2.44 | 1.60 | **1.30** |
| 2025 | 2.18 | 1.34 | **1.33** |

**Vietnam** -- non-monotone, and the *high* tercile is the healthiest:

| Year | Low | Mid | High |
|---|---|---|---|
| 2021 | 3.45 | 2.62 | **5.02** |
| 2023 | 2.70 | 1.33 | 2.67 |
| 2025 | 3.41 | 2.57 | **4.05** |

The short-maturity share is picking up two opposing things at once: repricing
exposure, and creditworthiness. Firms that can roll short-term paper cheaply
are often the *strongest* borrowers, not the most fragile. In Vietnam the
second effect dominates and the ordering inverts, which mechanically kills the
pooled estimate.

This is precisely why the design note named revealed pass-through sensitivity
as the primary exposure measure and the short-maturity share as a robustness
check only. The substitution was forced by the short window, and the null is
the consequence of that substitution.

## 2. There is effectively no pre-period for Türkiye

Yahoo retains four to five annual periods, and Turkish coverage in 2021 is only
49 firms against 460 in 2022. The Turkish "pre-period" is therefore one usable
year. Pre-trends cannot be tested at all, which on its own would disqualify the
current specification from publication regardless of what the coefficients did.

## 3. Survivorship

The ticker list is currently-listed firms while the outcome is default risk, so
the firms most likely to have failed are absent. The bias runs toward zero.

## What this changes

The İş Yatırım fetch moves back onto the critical path. It was previously
described as a robustness input; that was wrong. It is the only source of
2010-2020 history, and that history is what makes the primary design work:

- a genuine pre-period with testable parallel trends;
- per-firm pass-through betas estimated over 2013-2022, which identify
  repricing exposure from *revealed* cost-of-funds behaviour rather than from
  a balance-sheet ratio that also proxies credit quality.

The aggregate deterioration is not in doubt -- Turkish median coverage halves
from 3.36 to 1.66 across the tightening while Vietnam's dips and recovers. What
the current window cannot yet establish is the cross-sectional gradient, which
is the paper's actual claim.

---

# Primary specification: repricing betas

Exposure is now the revealed repricing beta from `src/exposure.py`, estimated
over 2012-2022 from

    d(implied rate)_it = a_i + b_i d(rate)_t + g_i d(ln FX)_t + e_it

and standardised within country. Treatment begins 2023, so exposure is strictly
pre-determined. Vietnam: 502 firms, median 11 annual observations each.
Türkiye: 83 firms so far and rising as the İş Yatırım fetch completes.

## A cross-country contrast that stands on its own

| | Vietnam | Türkiye |
|---|---|---|
| Mean repricing beta | 0.0079 | 0.0023 |
| Mean FX beta | **-0.0002** | **0.347** |
| Share with positive repricing beta | 72.5% | 71.4% |

Vietnamese firms' realised borrowing costs are essentially insensitive to the
exchange rate. Turkish firms' costs load heavily on it. The two corporate
sectors transmit monetary conditions through different balance-sheet channels,
which is a result in its own right and is only visible because the two betas
are estimated jointly.

## Vietnam: a clean, well-identified null

| Outcome | Coef | SE | p |
|---|---|---|---|
| Interest coverage | 0.187 | 0.676 | 0.78 |
| Altman Z'' | 0.023 | 0.089 | 0.80 |
| ROA | -0.002 | 0.002 | 0.28 |

The event study is flat on both sides of 2023 -- no pre-trend, no post-treatment
divergence. For Altman Z'' the 95% interval is roughly [-0.15, +0.20] against a
median of about 6.7, so this is a reasonably tight null rather than an
uninformative one.

**This is the predicted result, not a failure.** Vietnam's tightening moved
realised borrowing costs by under one percentage point. The hypothesis is that
the channel bites under large tightening and not small; a null in the mild
regime is what that hypothesis implies. It becomes evidence only in
combination with a positive Turkish result.

## Türkiye: not yet identified

The DiD reports +0.886 on Altman Z'' (p = 0.045), which is the wrong sign for
the hypothesis and should not be believed, because the event study rejects the
identifying assumption outright:

| Year | Altman Z'' coef | SE |
|---|---|---|
| 2018 | **-1.437** | 0.723 ** |
| 2019 | **-1.555** | 0.691 ** |
| 2020 | -0.380 | 0.579 |
| 2021 | **-1.343** | 0.735 * |
| 2022 | 0 (base) | |
| 2023 | +0.563 | 0.325 * |
| 2024 | +0.418 | 0.450 |
| 2025 | +0.213 | 0.457 |

High-beta Turkish firms were already diverging well before treatment. The
positive post-2023 coefficients are consistent with mean reversion toward the
2022 base year, not with a treatment effect. Parallel trends fails.

Two things must happen before this is interpretable: the fetch must finish
(83 of a possible ~500 firms are in), and if the pre-trend survives the full
sample the design needs to address it directly -- pre-trend-adjusted estimation,
matching on pre-period trajectories, or restricting the exposure window.

## Status of the claim

Half the design is established. The Vietnamese null is clean and its event
study supports the identifying assumption. The Turkish side is not yet
identified, and the claim cannot be asserted until it is.

---

# Re-check on the expanded Turkish sample: the exposure measure fails validation

Rebuilding with 1,979 cached files (489 Turkish firms in the panel, 172 with
estimated betas, up from 83) overturns both of the previous Turkish readings.

## Both earlier Turkish results were small-sample artefacts

| | 83-firm sample | 158-firm sample |
|---|---|---|
| DiD, Altman Z'' | **+0.886 (p = 0.045)** | +0.151 (p = 0.53) |
| Event study 2018 | **-1.437 (p < 0.05)** | -0.170 (ns) |
| Event study 2019 | **-1.555 (p < 0.05)** | -0.130 (ns) |
| Event study 2021 | **-1.343 (p < 0.10)** | +0.098 (ns) |

The apparent effect and the apparent parallel-trends violation both vanish.
Neither was real. Türkiye now looks like Vietnam: a null with a flat event
study.

## But the null is uninformative, because the measure does not work

Three diagnostics, each independently damning.

**First stage.** Does the repricing beta predict the firm's *actual* change in
borrowing cost across the tightening? Türkiye, against the clean Yahoo-based
implied rate, 2022 to 2024: coefficient -0.036 (p = 0.27), R^2 = 0.035, and the
top beta tercile records the *smallest* increase (+0.04) against the bottom
tercile's +0.19. Vietnam, 2022 to 2023: coefficient 0.001 (p = 0.54),
R^2 = 0.002. The measure has no out-of-sample predictive content in either
country.

**Split-half reliability.** Betas estimated on 2012-2017 versus 2018-2022, for
firms present in both windows. A stable firm characteristic should correlate
strongly across halves:

| | Repricing beta | FX beta |
|---|---|---|
| Türkiye (n = 77) | **-0.219** | +0.147 |
| Vietnam (n = 390) | **-0.080** | +0.094 |

Zero or negative. The betas do not measure a persistent firm trait.

**R-squared against a noise benchmark.** With a median of six usable annual
observations and two regressors, pure noise yields an expected R^2 of about
0.40. Vietnam's median observed R^2 is 0.396 -- indistinguishable from noise.

## No observable proxy passes either

Regressing the actual change in borrowing cost on standardised pre-period
characteristics:

| Predictor | Türkiye R^2 | Vietnam R^2 |
|---|---|---|
| Short-term debt share | 0.000 | 0.002 |
| Debt to assets | 0.005 | 0.017 |
| Current ratio | 0.003 | 0.002 |
| Log assets | 0.005 | 0.001 |
| Interest coverage | 0.007 | 0.004 |

Nothing reaches an R^2 of 0.02. Cross-firm variation in how much a firm's
borrowing cost actually reprices is close to unpredictable from annual
financial statements.

## What this means

The paper's firm-level design cannot be executed with annual accounting data.
Both nulls reflect a measurement failure, not the absence of a transmission
channel. This is also the honest reason Şengül & Çinko needed administrative
data: a contractual floating-rate flag is not recoverable from published
statements, and accounting proxies do not stand in for it. That is a finding
worth stating plainly rather than a gap to paper over.

What survives untouched: the aggregate comparison (Turkish median coverage
halving from 3.36 to 1.66 while Vietnam dips and recovers), the demonstration
that `4BB` bundles FX revaluation, and the cross-country channel contrast in
which Turkish borrowing costs load heavily on the exchange rate and Vietnamese
costs do not.

## Options

1. **Quarterly estimation.** İş Yatırım serves periods 3/6/9/12, so the Turkish
   beta window grows from ~11 annual observations to ~44. This is the direct
   fix for the noise problem, but Vietnam has no quarterly source at comparable
   scale, so it breaks the symmetry the comparison rests on.
2. **Portfolio sorting.** Aggregate firms into portfolios on observables and
   analyse portfolio-level repricing. Averaging is exactly what kills the
   idiosyncratic noise that defeats firm-level betas, at the cost of
   statistical power and of the heterogeneity story.
3. **Reframe to the aggregate comparison** the data does support, accepting a
   more descriptive contribution.

---

# Is the data adequate for a theoretically strong paper?

Short answer: not for the Türkiye-2023 firm-level design. Three independent
problems compound, and the third is decisive.

## 1. The treatment variable is unobservable

Contractual floating-rate status is not recoverable from published statements.
This is why Şengül & Çinko needed administrative data, and no econometric
technique substitutes for it.

## 2. Estimated exposure is noise; measured exposure is not

Persistence across 2018-2022:

| Measure | Correlation | Verdict |
|---|---|---|
| Repricing beta (TR / VN) | -0.22 / -0.08 | noise |
| Short-term debt share (TR / VN) | +0.44 / +0.63 | stable |
| FX exposure (TR) | +0.52 | stable |
| Export share (TR) | +0.84 | stable |

Balance-sheet characteristics *are* well-measured firm traits. Only the
regression-estimated betas fail. So exposure can be measured -- just not
floating-rate exposure.

## 3. Inflation accounting contaminates every Turkish balance-sheet ratio at
the treatment date

Turkish median balance-sheet aggregates:

| Year | Equity / assets | Debt / assets |
|---|---|---|
| 2017 | 0.472 | 0.217 |
| 2019 | 0.419 | 0.226 |
| 2021 | 0.462 | 0.189 |
| **2022** | **0.558** | **0.138** |
| **2023** | **0.614** | **0.111** |
| 2024 | 0.646 | 0.100 |

Leverage more than halves between 2019 and 2024. No real deleveraging of that
size occurred. TMS-29 indexes non-monetary assets and equity upward while
monetary debt stays nominal, so the ratios move mechanically -- and the break
lands on 2022-23, exactly at treatment.

This is fatal for the FX design in a way fixed effects cannot repair. Firms
differ in their ratio of monetary debt to non-monetary assets, so the
restatement effect is itself *heterogeneous in the exposure variable*. It
enters as an exposure-by-post interaction, which is the coefficient of
interest. Country-by-year effects absorb the common level shift and leave the
contamination untouched.

The FX results show exactly this signature: highly significant coefficients
with the wrong sign (FX-indebted firms appearing to *improve* -- implied rate
-0.108, p < 0.0001; Altman Z'' +0.813, p = 0.004), post-treatment coefficients
growing monotonically (+0.32, +0.83, +1.18 across 2023-25) as restatement
compounds, and event studies with large significant pre-trends
(2017 +0.83***, 2018 +0.54**, 2021 -0.59**). None of it is causal.

## What the data can support

**The 2018 Turkish currency crisis.** The lira fell from 3.8 to 5.3 against the
dollar in 2018. It is a sharp, well-identified shock; FX exposure is measurable
and persistent; and it sits entirely *before* TMS-29, so the accounting basis is
consistent across the window. Our panel starts in 2010, giving ample pre-period.
The theory is well developed -- original sin, and the Bruno-Shin risk-taking
channel -- and the prediction is directional and testable.

**Vietnam as the clean laboratory.** No inflation accounting, 693 firms over
2011-2025, and validated against an independent source. Whatever design is
chosen, the Vietnamese side is sound.

## Recommendation

Move the treatment event rather than patch the specification. A paper built on
the 2023 tightening must defend every balance-sheet outcome against a
mechanical accounting artefact that moves with the treatment; a paper built on
2018, or on a currency shock in general, does not. The comparative VN/TR
structure and all the data infrastructure carry over unchanged.

---

# Main specification, flow outcomes only

Implemented as recommended: treatment at 2023, exposure measured at 2021
(pre-treatment and pre-restatement), outcomes restricted to flows. Turkish
interest-based outcomes come from Yahoo; EBIT margin and debt growth use the
İş Yatırım history, since neither needs an interest figure and the `4BB`
bundling is therefore irrelevant to them. That buys a 2015-2025 window and a
genuinely testable event study.

## Result: no treatment effect on any flow outcome, in either country

All twelve difference-in-differences coefficients are insignificant
(`results/did_flow.csv`); the smallest p-value is 0.15. This holds for both
exposure measures and both countries.

## The long pre-period is what makes the result interpretable

With only 2021 available as a pre-year the event studies looked flat and the
nulls looked underpowered. Extending to 2015 shows something different: the
exposure-outcome relationships are *persistent level differences* that predate
treatment by years and do not shift at 2023.

Türkiye, short-term-debt share to debt growth:

| Year | Coef | | Year | Coef |
|---|---|---|---|---|
| 2015 | -0.138** | | 2021 | -0.232*** |
| 2016 | -0.187*** | | 2022 | base |
| 2017 | -0.162*** | | **2023** | **-0.220*** |
| 2019 | -0.252*** | | 2024 | -0.069 |
| 2020 | -0.211*** | | 2025 | -0.191*** |

Firms with more short-term debt persistently grow debt more slowly, in every
year from 2015 onward, and nothing happens at treatment. The same pattern holds
for Turkish FX exposure (2020 +0.180***, 2021 +0.279*** before treatment) and
for Vietnamese EBIT margin, where a downward drift begins well before 2023.

These are pre-existing differences between firm types, not responses to
monetary tightening. A specification with one pre-year would have reported some
of them as treatment effects.

## Conclusion

With contaminated outcomes removed, exposure measured before restatement, and a
pre-period long enough to test the identifying assumption, there is no
detectable firm-level exposure gradient in listed non-financial firms in either
country. The earlier significant coefficients were, in order: small-sample
noise, inflation-accounting artefact, and pre-existing trend.

The honest reading is that the listed-firm universe cannot deliver the result
Şengül & Çinko obtain from administrative data, for reasons that are now
documented rather than suspected: the contractual treatment is unobservable,
regression-estimated proxies are noise, stock-based outcomes are mechanically
contaminated in Türkiye, and the flow-based outcomes that survive show only
persistent heterogeneity.

Limitations that qualify the null: annual frequency, listed firms only, and
survivorship in a sample whose outcome is distress.
