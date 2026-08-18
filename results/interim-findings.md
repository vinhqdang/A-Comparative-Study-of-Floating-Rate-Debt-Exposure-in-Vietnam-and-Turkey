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
