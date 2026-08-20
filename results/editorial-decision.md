# Editorial Decision Package — Borsa Istanbul Review (simulated review committee)

## Decision: Major Revision

Panel: EIC, Methodology (measurement-error econometrics), Domain (applied EM
corporate finance), Practitioner (IAS 29 / accounting), Devil's Advocate.
All four scoring reviewers independently returned Major Revision; the Devil's
Advocate found CRITICAL issues, which under this committee's own rule means
the decision cannot be Accept regardless.

## CONSENSUS-4 (all or nearly all reviewers converge)

1. **Internal numerical inconsistency in the reliability/decomposition
   results.** Methodology and Devil's Advocate independently found the same
   thing: Table `tab:decomp` reports Turkish sampling-noise-implied
   reliability of 0.898 and transitory share 89.8%, but four prose passages
   (lines 516, 567, 1035, 1387) still cite the pre-correction 0.78/78.0%.
   Independently verified — confirmed present.
2. **Incomplete country-exclusion disclosure.** Domain and Devil's Advocate
   both flag that the footnote names only Brazil and Chile as scoped-and-
   excluded, when Hungary, Mexico, and a failed Thailand fetch are also
   absent from the disclosed record. Independently verified against
   `src/analysis_dose.py` and `src/multi_build.py`.
3. **Undisclosed survivorship bias.** Methodology raises this as a first-order
   threat given the outcome is default/distress risk; confirmed by direct
   search — zero mentions of survivorship, delisting, or attrition anywhere
   in the manuscript.
4. **A confirmed factual error in the Turkish policy-rate narrative.** Domain
   flags that CBRT's true 2024 peak was 50% (held March–November), not the
   47.5% year-end figure the paper calls "the peak." Independently verified
   against BIS's monthly (not annual) series. This also affects the 33.5pp/
   38.5pp dose and pass-through figures used elsewhere, which use two
   different, unreconciled baselines.

## CONSENSUS-3 / cross-corroborated

- **R² figures for two different regressions (full-sample T≈10-11 vs.
  split-half T≈6) are cited without disambiguation on first mention**
  (Methodology, Devil's Advocate).
- **Reproducibility gap**: no committed script generates the split-half
  correlations or the variance-decomposition table (Methodology; confirmed —
  the computation exists only in this session's scratch files, never
  committed to `src/`).
- **Overclaiming of novelty in Propositions 1-3/6**, which largely restate
  classical errors-in-variables/reliability-theory results (EIC, Devil's
  Advocate, independently).

## DA-CRITICAL findings requiring explicit author response

1. **Negative split-half correlations fall outside the [0,1] support that
   Proposition 2's own variance-ratio formula implies.** This is a genuine
   logical gap: Corollary `cor:uninformative` treats "zero or negative" as
   interchangeable evidence for λ≈0, but a population ratio of variances
   cannot be negative — an empirically negative value is finite-sample
   noise around a true value at or near zero, which needs to be argued
   explicitly (via a standard error/CI), not glossed over.
2. **Split-half correlation (half-length windows) is asserted, not proven,
   to equal the full-sample attenuation factor** — Methodology independently
   raised the identical gap, given the paper's own sampling-variance formula
   is explicit about T-dependence.
3. **The paper's null may reflect sample selection rather than unmeasurable
   exposure** — DA's strongest counter-argument: Şengül & Çinko's effect
   concentrates in weak-rating/low-liquidity/high-exposure firms, which
   listing requirements structurally screen out. The paper never tests
   whether its own *reliable* proxies (short-term debt share, FX exposure,
   export share — Table `tab:split` lower rows) show restricted range
   relative to a registry-style population. This is not fixed by editing;
   it requires either a new analysis or an explicit acknowledgment of the
   alternative explanation and why it's judged less likely.
4. **The dose-response correlation is fragile beyond the disclosed caveat**:
   reconstructing the fuller assembled sample, DA reports the correlation
   collapses to ~0.64 among the seven non-anchor countries, and Brazil/
   Mexico at an *identical* nominal dose (5.75pp) produce a fivefold
   divergence in outcome. This bears on the "constructive half" of the
   paper's contribution, not just the exposure null.

## Specialist finding requiring author judgment (not consensus, single
reviewer, but high-confidence and specific)

- **Practitioner (IAS 29):** the stylized restatement model omits the net
  monetary position gain/loss, a firm-specific (leverage-correlated) income
  line with no historical-cost analog, that likely sits inside the same
  "Financial Expenses" field the paper already distrusts. If correct, this
  means Proposition 8 (flow invariance) is not as clean as claimed for EBIT
  margin/interest coverage specifically. Requires either new data work to
  isolate the line, or an explicit caveat weakening the "prefer flows"
  prescription.

## Missing references (Domain)

Hausman (2001, JEP); Bound, Brown & Mathiowetz (2001, Handbook of
Econometrics); the completed Eichengreen-Hausmann-Panizza "original sin"
trilogy (2003/2005) alongside the 1999 NBER precursor already cited; Salomao
& Varela (2022, RES); Jeenas (2019); at least one Vietnam-specific
monetary-transmission or 2022 corporate-bond-crisis reference.

## Revision roadmap

**P1 — must fix (confirmed, mechanical, no judgment call):**
- Reconcile all reliability/decomposition figures to the corrected values
  (0.898/89.8% for Türkiye) throughout — 4 locations.
- Fix duplicate `\label{}` targets (EIC finding) — `sec:lit`, `sec:data`,
  `sec:results`, `sec:conclusion`.
- Correct the CBRT 2024 peak to 50% and reconcile the 33.5/38.5pp figures on
  one consistent, stated convention; recompute the five-country dose-response
  analysis with the corrected Turkish dose.
- Disclose all excluded countries (Hungary, Mexico, Thailand), not only
  Brazil/Chile.
- Add an explicit survivorship-bias limitation.
- Disambiguate the two R² figures on first mention.
- Commit a reproducible script for the split-half/decomposition computation.

**P2 — should fix (substantive, some judgment required):**
- Add inferential uncertainty (SE/CI) to the split-half λ̂ estimates and
  restate Corollary `cor:uninformative` as a statistical test rather than a
  point comparison.
- Add one paragraph explicitly ruling out an errors-in-variables/IV
  correction on weak-instrument grounds (both Methodology and DA raised
  this).
- Add the missing references.
- Address the practitioner's IAS 29 monetary-gain/loss point, at minimum as
  a stated limitation.

**P3 — author's call (reframing, not correctness):**
- Whether to foreground Propositions 7-8 as the genuinely novel content and
  de-emphasize 1-3/6 as applications of known results.
- Whether/how to engage DA's sample-selection alternative explanation for
  the null.
- Whether the dose-response result should be presented with less headline
  confidence given DA's fuller-sample fragility finding.
