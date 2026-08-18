# Floating-Rate Debt Exposure and Corporate Default Risk: Vietnam vs Türkiye

Working design note. Target venue: *Borsa Istanbul Review* (Elsevier, open access).

---

## 1. What the target journal has just published, and why that is an opportunity

Şengül & Çinko, "Monetary tightening and corporate default risk: Evidence from
floating-rate debt exposure," *Borsa Istanbul Review* (in press,
S2214845026000578), estimate how balance-sheet exposure to floating-rate debt
transmits monetary tightening into corporate default risk. They exploit the
June 2023 policy reversal in Türkiye, use a large **administrative** dataset,
and apply a two-part Double Machine Learning design to separate selection from
causation. Their headline: the *average* effect is modest — aggregate
resilience — but treatment effects are sharply heterogeneous, concentrated in
firms with weak internal risk ratings, low liquidity and high exposure shares,
while exporters and manufacturers are relatively insulated.

Two features of that paper define our opening.

**First, it is a single-country, single-episode result.** The estimate is
identified off one tightening cycle — arguably the most extreme in any
sizeable economy this decade, roughly 8.5% to 50% in twelve months, under
inflation above 60%. That is a superb setting for *detecting* the channel and a
poor one for telling us how much of the result is the channel and how much is
the extremity of the episode. A referee-proof way to state the gap: their
design cannot separate *floating-rate exposure matters* from *floating-rate
exposure matters when rates quadruple*.

**Second, its data cannot be replicated, which paradoxically helps us.** We
have no credit registry. Competing on Turkish administrative data would lose.
Instead we change the question from "how large is the effect in Türkiye" to
"does the mechanism generalise across monetary regimes," and answer it with the
one data type that exists in comparable form in both countries: audited
listed-company financial statements.

## 2. The comparison, and why Vietnam is the right counterfactual

Vietnam and Türkiye share the structural preconditions that make the
floating-rate channel operative: bank-dominated corporate finance, thin
corporate bond markets, high reliance on short-maturity credit, and a large
listed non-financial sector. What they do not share is the monetary regime over
2021–2025.

| | Türkiye | Vietnam |
|---|---|---|
| Policy stance 2022–23 | Extreme, abrupt tightening from June 2023 | Mild tightening late 2022, reversed through 2023 |
| Inflation | >60% peak | Contained, single digit |
| Accounting regime | Inflation accounting (TMS-29) from FY2023 | Unchanged historical cost |

This is close to a natural experiment in *dose*. If the exposure gradient of
default risk is a general property of leveraged emerging-market firms, it
should be visible in Vietnam too, scaled down. If it appears only in Türkiye,
the channel is a crisis phenomenon rather than a business-cycle one. Either
result is publishable, and the second is the more interesting.

## 3. Data — both sides verified working

**Vietnam.** `vnfinancialdata` (PyPI 0.1.1) → Hugging Face dataset
`thanhnp-uel/vietnam-listed-companies-financial-statements` v1.0.0. Long-format
item-level statements for HSX and HNX. Built panel: **9,893 firm-years, 693
firms, 2011–2025**, with non-missing coverage of 94.5% (total assets), 94.7%
(total debt), 91.2% (interest expense), 93.2% (EBIT), 96.8% (equity).

**Türkiye.** İş Yatırım's public `MaliTablo` endpoint, 798 BIST companies from
KAP. One request returns balance sheet, income statement, cash flow and a
supplementary block with bilingual item labels, for four annual periods at
once. Note the endpoint refuses connections from most non-Turkish IPs; the
fetcher routes through a proxy, with a `FETCH_DIRECT=1` switch for use from a
Turkish IP.

The Turkish source is in one respect **richer** than the Vietnamese one, and it
maps directly onto the heterogeneity Şengül & Çinko report:

| Item | Code | Enables |
|---|---|---|
| Short/Long-Term Financial Loans | `2AA`, `2BA` | Debt structure, exposure share |
| Financial Expenses | `4BB` | Implied cost of debt |
| Export Sales | `4BD` | **The exporter-insulation channel, directly** |
| Net FX Position (incl. hedge) | `4BE`, `4BEB` | FX-mismatch channel |
| Depreciation & Amortisation | `4B` | EBITDA, coverage ratios |

Harmonised core (available both sides): total assets, current assets, cash,
total and current liabilities, equity, retained earnings, short- and long-term
borrowings, net sales, operating profit, interest/financial expense, D&A.

## 4. The measurement problem, and the proposed answer

Neither dataset flags a loan as contractually floating. Şengül & Çinko had that
field administratively; we must infer it. We propose three measures, treating
the first as primary and the others as robustness.

**(a) Revealed repricing sensitivity — preferred.** For each firm, estimate the
pass-through of the policy rate into its own realised borrowing cost over a
pre-treatment window:

  Δ(implied rate)_it = α_i + β_i · Δ(policy rate)_t + ε_it,
  where implied rate_it = |interest expense_it| / average debt_it.

β_i is a *revealed* exposure measure: it captures whatever combination of
contractual floating terms, short rollover and renegotiation actually causes a
firm's cost of funds to move with policy. It is superior to any balance-sheet
share precisely because it does not require knowing the contract.

**(b) Short-maturity share.** short-term debt / total debt. Debt that rolls
within the year reprices at rollover whatever its stated coupon. Vietnamese
listed firms sit near 70% on this measure — unusually high, and a large part of
why the channel should operate there at all.

**(c) Bank-loan share (Türkiye only).** `2AA`+`2BA` are bank credit, which in
Türkiye reprices far faster than the thin corporate bond market.

**This measure is already validated on the Vietnamese panel.** The median
implied rate reproduces the SBV policy path without being told it: 11.1% in
2011 at the peak of the inflation crisis, falling to 5.8% by 2015, rising to
7.2% in the 2023 tightening, easing to 5.8% by 2025 — while median interest
coverage bottoms out at 2.05 in exactly 2023, its lowest value in the sample.
The transmission from policy to firm cost of funds to debt-servicing capacity
is legible in ordinary audited statements. That is the methodological bridge
that makes a registry-free comparison credible.

### 4.1 Two independent sources per country, and what disagreement taught us

Each country panel is built from a national source and cross-checked against an
independent Yahoo Finance pull of the same filings (`src/validate.py`). Yahoo
retains only four to five annual periods, so it cannot replace the national
sources, but it normalises the same statements independently — which makes
agreement evidence that our item mapping is right, and disagreement a precise
diagnostic.

**Where they agree, they agree exactly.** Total assets reconcile at a median
relative difference of 0.0000 in both countries (Vietnam corr 1.0000, Türkiye
0.9960); revenue likewise (0.9999 / 0.9935). Total debt agrees to 0.000%
median in Vietnam and −2.9% in Türkiye, the latter a lease-classification
difference. Equity differs by about −4% in Vietnam because Yahoo reports
parent-only stockholders' equity where the national source includes minority
interest. EBIT differs by roughly +21-23% in both countries because Yahoo
derives EBIT from pretax income plus interest rather than taking reported
operating profit. These are definitional and documented, not errors.

**Where they disagree, the disagreement is the finding.** On absolute values,
Vietnamese interest expense reconciles almost perfectly — corr 0.991, median
difference 0.00%, 78% of firm-years within 2%. (The two sources use opposite
sign conventions, which is why raw correlations appear negative; the
construction takes absolute values.) Türkiye does not reconcile: corr 0.727 and
a median difference of **−68.8%**, meaning İş Yatırım's `4BB` runs roughly
three times Yahoo's interest expense. `4BB` is *Financial Expenses*, a bundled
line that carries FX revaluation losses and other financing charges alongside
interest.

That is not a nuisance to be footnoted, because it changes the numbers that
matter. Built on `4BB`, the Turkish implied rate peaks in **2018 and 2021** —
the two lira crisis years. Built on Yahoo's interest expense, it tracks the
CBRT path monotonically:

| Year | Implied rate | CBRT 1-week repo (year-end) | Median ICR |
|---|---|---|---|
| 2022 | 17.8% | 9.0% | 3.36 |
| 2023 | 25.4% | 42.5% | 3.16 |
| 2024 | **31.2%** | **47.5%** | 1.84 |
| 2025 | 25.8% | ~39.5% | 1.66 |

The implied rate peaks in 2024, exactly when policy peaked, and median interest
coverage halves from 3.36 to 1.66 across the tightening. The pass-through is
incomplete — a 38-point policy move produces a 13-point move in realised
borrowing costs — which is itself informative about repricing frictions and
maturity structure.

**Resulting source strategy.** Yahoo interest expense is primary for the
Turkish implied rate over 2021-2025, the identification window. İş Yatırım
supplies the long pre-trend history (2010-2020) and the Türkiye-specific items
that Yahoo does not carry — export sales `4BD` and net FX position `4BE` — which
drive the exporter and FX-mismatch heterogeneity. `4BB` is retained as a
*measure of total financing cost including FX*, which lets us decompose the two
channels rather than conflate them.


## 5. Identification

Continuous-treatment difference-in-differences, then a triple difference across
countries:

  Y_ict = β · (Exposure_i × Post_t) + γ · (Exposure_i × Post_t × Türkiye_c)
          + firm FE + country×year FE + controls + ε

`Post` is 2023 onward in both countries. Firm fixed effects absorb permanent
differences in riskiness; country×year fixed effects absorb every
macroeconomic and accounting shock common within a country-year. Identification
therefore comes from the *cross-firm exposure gradient within a country-year* —
never from cross-country level comparisons, which would be meaningless given
different currencies, price levels and accounting bases.

γ is the parameter of interest: it asks whether the exposure gradient is
steeper under extreme tightening than under mild tightening.

Outcomes: Altman Z''-score (emerging-market variant, Altman 2005 — already
computed on the Vietnamese panel), interest coverage, and a distress indicator
(coverage below one for two consecutive years).

## 6. The main threat to identification, and how it is handled

**Turkish inflation accounting.** From FY2023, Turkish listed companies restate
financial statements under TMS-29. Non-monetary items (fixed assets,
inventories, equity) are indexed; monetary items (debt, cash, receivables) are
not. This lands *exactly on the treatment date* and mechanically moves several
of our variables — debt-to-assets falls, equity rises — for reasons that have
nothing to do with monetary transmission. A referee at this journal will raise
it, and it is a genuine problem, not a formality.

Three defences, in order of strength:

1. **Country×year fixed effects absorb it.** The restatement is common to all
   Turkish firms in a given year. Since identification runs off the within-
   country-year cross-firm gradient, a common level shift cannot drive γ.
   This is the primary defence and it is structural, not cosmetic.
2. **Prefer monetary-to-monetary ratios.** The implied rate is financial
   expense over debt — both monetary, both unindexed — so it is
   restatement-invariant by construction. This is a further reason to make
   measure (a) primary rather than a balance-sheet share.
3. **Placebo and sensitivity.** Re-estimate on Vietnam alone, where no
   restatement occurred; re-estimate excluding FY2023; report results with
   inflation-adjusted Turkish series where reconstructible.

Second-order threats to address: survivorship (delisted firms — the 798-ticker
KAP list includes currently listed companies, so the sample tilts toward
survivors, and default is our outcome; we will discuss the resulting
conservative bias explicitly); non-financial screen (banks, insurers and
brokers use different statement templates and are excluded on both sides);
annual frequency on the Vietnamese side, which limits us to annual
identification even though Turkish data is available quarterly.

## 7. Contribution, stated plainly

1. First cross-country test of the floating-rate transmission channel across
   *sharply different monetary regimes*, which is precisely the external-
   validity question the single-country administrative literature cannot
   answer.
2. A registry-free, fully reproducible measurement strategy — revealed
   repricing sensitivity from audited statements — validated against the
   Vietnamese policy path, which lets researchers without administrative
   access study this channel in any market with listed-company filings.
3. First application of the Vietnamese listed-company statement panel to a
   monetary-transmission question, and a harmonised VN–TR firm panel released
   with the paper.

## 8. Status

- [x] Vietnam panel built and validated — 9,893 firm-years, 693 firms
- [x] Turkish data access solved; taxonomy mapped; fetch running
- [x] Turkish panel via Yahoo: 2,762 firm-years, 586 firms, 2021-2025
- [x] Both panels cross-validated against an independent source (src/validate.py)
- [x] Turkish implied rate resolved and validated against the CBRT path
- [ ] Full Is Yatirim fetch for 2010-2020 pre-trends (running, resumable)
- [ ] Policy-rate series (SBV; CBRT via EVDS)
- [ ] Exposure estimation, DiD, triple difference
- [ ] Robustness: TMS-29, survivorship, placebo
- [ ] Check *BIR* author guidelines before drafting (format, structure, blinding)
