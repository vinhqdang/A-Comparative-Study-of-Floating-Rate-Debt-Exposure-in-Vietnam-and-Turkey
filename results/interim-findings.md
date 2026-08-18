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
