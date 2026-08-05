# Complexity Score Calibration — Test Effort Units (TEU)

Links the **complexity assessment score** of an EIP to the **measured testing work** it
generated in [`ethereum/execution-specs`](https://github.com/ethereum/execution-specs).

Calibrated against Amsterdam, 2025-10-21 (the EEST → execution-specs weld) through
2026-08-05. 917 squash-merged commits on `forks/amsterdam`, 15 EIP test suites,
12 of which have a complexity assessment on file.

---

## 1. The metric

**Test Effort Units (TEU)** — the observable cost of testing one EIP:

```
TEU = merged_PRs + (review_submissions + review_threads) / 10
```

One TEU ≈ one merged PR's worth of work. The review term adds the PRs that
were expensive to land, which PR count alone misses.

Both components come from PRs *owned* by the EIP (see [attribution](#4-attribution-model)).
Neither depends on how tests happen to be written, which is why they beat the
obvious alternatives — see [§5](#5-why-not-the-obvious-measures).

## 2. The calibration

```
TEU  =  0.38 × S^1.62
```

where `S` is the assessment's Total Score.

| | |
|---|---|
| Fit sample | n = 9 (EIPs ≥ 10 weeks in flight) |
| Pearson r | **0.920** |
| Leave-one-out median error | **21 %** |
| Same fit, linear model | 148 % LOO error — the power law is **7× more accurate** |
| Fork-level closure | Σ per-EIP predictions = **320 TEU** vs **328 measured** (2.5 % off) |

### The headline: cost is super-linear in score

**Doubling the complexity score triples the work** (2^1.62 ≈ 3.1×).

Every measure of work independently shows an exponent above 1:

| Work measure | Exponent |
|---|---:|
| Review load (submissions + threads) | 2.02 |
| Diff churn (lines added + deleted) | 1.88 |
| **TEU** | **1.62** |
| Test functions written | 1.48 |
| Merged PRs | 1.46 |
| Final test-suite LoC | 1.32 |

Review attention scales worst of all. Test-writing volume grows roughly with
`S^1.5`; the *arguing about it* grows with `S^2`.

**What the data actually shows is a cliff at the red tier, not a smooth curve.**
Fit only the seven mature 🟢/🟡 EIPs (scores 5–13) and the exponent collapses to
**0.78** — inside that band, cost is flat to slightly sub-linear in score. The
1.62 exponent is produced entirely by the jump to EIP-7928 (29) and EIP-8037 (28).
So read the power law as a smooth interpolation across a step, not as evidence
that each additional point costs more than the last. Both readings give the same
planning numbers at the anchors; they disagree in the 16–25 gap, where Amsterdam
has no observations at all.

## 3. Planning table

Fitted on mature Amsterdam EIPs. Read across for the workload a score implies.

| Score | Tier | TEU | PRs | Review items | Test funcs | Suite LoC | Churn | vs. a 5-pt EIP |
|---:|:--:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 🟢 | 2.3 | 1.8 | 4 | 6 | 600 | 630 | 0.4× |
| 5 | 🟢 | 5.2 | 3.7 | 12 | 12 | 1 180 | 1 660 | 1.0× |
| 8 | 🟢 | 11.1 | 7.3 | 32 | 24 | 2 200 | 4 010 | 2.1× |
| 10 | 🟡 | 16.0 | 10.2 | 50 | 34 | 2 960 | 6 100 | 3.1× |
| 13 | 🟡 | 24.5 | 14.9 | 85 | 50 | 4 180 | 9 990 | 4.7× |
| 16 | 🟡 | 34.2 | 20.2 | 129 | 68 | 5 510 | 14 750 | 6.6× |
| 20 | 🔴 | 49.2 | 28.0 | 203 | 95 | 7 400 | 22 440 | 9.4× |
| 25 | 🔴 | 70.6 | 38.8 | 319 | 132 | 9 930 | 34 130 | 13.6× |
| 30 | 🔴 | 95.0 | 50.7 | 462 | 172 | 12 640 | 48 090 | 18.2× |
| 36 | 🔴 | 127.4 | 66.2 | 668 | 226 | 16 090 | 67 740 | 24.5× |

**A single 🔴 EIP at the top of the range costs more than the entire 🟢 tier of a
fork combined.** In Amsterdam, EIP-7928 and EIP-8037 were 39 % of the score
total but **70 % of the measured TEU**.

### Using it for a fork

Apply the curve **per EIP, then sum**. Never apply it to a summed score — the
super-linearity is a property of one EIP's internal interactions, not of a fork's
EIP list. Amsterdam: per-EIP sum gives 320 TEU (correct); the summed-score
shortcut gives 1 217 TEU (~4× too high).

## 4. Attribution model

Each squash-merged commit on `forks/amsterdam` is one work unit, assigned to
owner EIPs:

```
owners = EIPs named in the commit subject
         else EIPs whose tests/amsterdam/eipNNNN_* directory the unit touched
```

Title takes precedence on purpose. PR #2901 (*"merge EIP-8037 to
`forks/amsterdam`"*, 910 files, 159 review submissions) touched 8 EIPs' test
directories because a gas-cost change breaks everyone's tests. It is 8037's
cost, not a cost smeared across its victims. Multi-owner units split `1/n`.

Three churn classes are tracked separately:

- **direct** — inside the EIP's own `tests/amsterdam/eipNNNN_*` directory
- **ripple** — anywhere else, from units the EIP owns (EELS, framework, other forks' tests)
- **generated** — `tests/ported_static/`, `tests/static/`; machine-ported, 2.3 M lines of
  unattributed churn that would otherwise swamp every real signal

Ripple churn matters: EIP-7928 wrote 19 k lines inside its own directory and
caused **68 k lines** of change everywhere else.

## 5. Why not the obvious measures

| Measure | r (mature) | Verdict |
|---|---:|---|
| Review load alone | 0.969 | Best single predictor, but noisy on quiet EIPs |
| Final suite LoC | 0.961 | Excellent, but rewards verbose test code |
| Test functions | 0.932 | Style-dependent (see below) |
| **TEU (PRs + review/10)** | **0.920** | **Chosen** — lowest LOO error, style-independent |
| Diff churn | 0.882 | Highest churn-side LOO error (59 %); rebases and moves inflate it |
| **Filled test cases** | **0.674** | **Do not use** — 72 % LOO error, exponent 0.80 |

**Filled test cases are actively misleading.** Spearman ρ = 0.36 — barely
better than chance. EIP-8246 (trivial, 2 test functions, no assessment)
generates 1 302 cases; EIP-7778 (score 10) generates 54. One
`@pytest.mark.parametrize` decorator can produce a thousand vectors for free,
so vector count measures parametrization style, not work.

Test-function counts have a milder version of the same problem — EIP-8024 wrote
68 functions on a score of 6, EIP-7976 wrote 10 on a score of 5 while generating
1 598 cases. TEU avoids both by counting process events instead of code.

## 6. Which anchors are actually earning their keep

Per-anchor scores parsed from all 12 assessments and correlated against measured
work. *The total beats every individual row and every thematic group* — the
checklist as a whole is the signal, which is the strongest possible endorsement
of its current design.

| Anchor / group | r vs churn | r vs test funcs | n>0 |
|---|---:|---:|---:|
| **TOTAL (all rows)** | **0.83** | **0.91** | 12 |
| Edge/boundary conditions | 0.63 | 0.77 | 9 |
| Cross-EIP interactions | 0.73 | 0.75 | 3 |
| Patterns affecting pre-existing tests | 0.36 | 0.76 | 9 |
| EVM Gas rule changes | 0.46 | 0.77 | 7 |
| *group:* risk & edges | 0.70 | 0.56 | — |
| *group:* blast radius | 0.54 | 0.85 | — |
| *group:* gas & metering | 0.31 | 0.68 | — |

Notes:

- **"Patterns affecting pre-existing tests" is a volume driver, not a churn
  driver** (0.76 vs test functions, 0.36 vs churn). Breaking existing tests means
  writing many more cases, not rewriting more lines than usual.
- **"Edge/boundary conditions"** is the best-populated high-signal row and the
  single most broadly useful anchor.
- Six anchors were **never scored above 0** in Amsterdam: added precompiles,
  modified precompiles, cryptography-related testing, new transaction types,
  encoding changes (RLP/SSZ), Engine API encoding changes. No evidence either
  way — Amsterdam simply has no precompile or encoding work. Do not prune them
  on this data.
- Rows with `n>0 ≤ 2` (block syncing at r = 0.93, modified system contracts,
  new header fields) are single-observation artifacts. Ignore the numbers.

## 7. Caveats

1. **n = 12, one fork, and two points carry the exponent.** Every number here is
   Amsterdam-shaped. Drop EIP-7928 and EIP-8037 and the exponent falls from 1.62
   to **0.78**. The power law is the better *model* by a wide margin (7× better
   LOO error than linear), but that verdict rests on two observations at the top
   of the range. Treat the curve as reliable *at* the tier anchors and
   provisional *between* them until a second fork is measured.
2. **Discrimination is poor within a tier.** Score vs PRs is r = 0.80 over the
   full range but only **r = 0.36** once the two reds are removed. The assessment
   reliably separates 🔴 from 🟢; it does not reliably rank a 5 against a 7. Use
   the tier, not the point value, for anything below 20.
3. **Truncation.** EIP-8038 (score 20, 4.7 weeks in flight), EIP-8070 (7,
   0.9 weeks) and EIP-7997 (5, 4.9 weeks) are excluded from the fit — their work
   has barely started, and they are exactly the three largest
   under-predictions. Re-run after Amsterdam ships.
4. **Score inflation risk.** These are the *original* assessment scores. If
   scores are ever revised after test work begins, the correlation becomes
   self-fulfilling. Freeze the score at CFI time and record the frozen value.
5. **TEU is not engineer-hours.** Squash merges collapse each PR to one commit,
   so per-author-day counts degenerate to PR counts and no honest
   effort-in-hours figure is recoverable from git. TEU is a workload *index*,
   comparable across EIPs but not convertible to headcount without time tracking.
6. **Three Amsterdam suites have no assessment on file** — EIP-7954, EIP-8282,
   EIP-8246. Their measured TEU back-solves to scores of ~6, ~5 and ~4.

## 8. Reproducing

```sh
# from a clone of ethereum/execution-specs with `upstream` pointing at the repo
python3 calibrate.py --specs-repo ~/path/to/execution-specs --fork amsterdam
```

`calibrate.py` regenerates `amsterdam-dataset.json` (per-EIP raw measures) and
every table above. It needs `gh` authenticated for PR metadata, and the
`execution-specs` venv only if you pass `--collect` to recount filled cases.
