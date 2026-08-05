# Proposed Checklist Anchors

Derived from the [Amsterdam calibration](README.md). EIP-7928 is the only mature
Amsterdam EIP the current checklist materially mis-scores, and the reason is
coverage and *structure*, not evaluator error.

---

## 1. The evidence that this is a coverage gap

Back-solving each EIP's score from its measured work (`TEU = 0.38 × S^1.62`):

| EIP | Scored | Implied by measured work | Gap |
|---|---:|---:|---:|
| **7928** | **29** | **40** | **+11** |
| 8037 | 28 | 27 | −1 |
| 2780 | 13 | 11 | −2 |
| 7778 | 10 | 9 | −1 |
| 7843 | 7 | 6 | −1 |
| 7981 | 6 | 6 | 0 |
| 8024 | 6 | 7 | +1 |
| 7976 | 5 | 7 | +2 |
| 7708 | 9 | 6 | −3 |

Every mature EIP lands within ±3 of its score. EIP-7928 is off by +11. That is
not noise — it is one EIP whose dominant cost has no row to be written on.

**7928 was already at the ceiling of what the checklist can express.** It scored
3 on seven rows and 2 on three more: 29 out of a maximum 33 across the ten
applicable rows. The remaining rows are genuinely N/A (no precompiles, no new
opcodes, no cryptography, no new transaction types). There was no room left.

### The smoking gun

7928's assessment scored **Modified opcodes: 0**, with this rationale:

> Final EVM semantics (gas charged, state changes, reverts) are unchanged. Only
> the observation order for BAL inclusion is constrained, which is a
> spec-framework concern, not a behavior change in the anchor's sense.

That is the checklist applied *correctly*, and it assigns zero to the single most
expensive part of the work. Whether an opcode runs out of gas **before or after**
it touches state became consensus-observable, and clients had to agree on where
that line falls for every state-accessing opcode. In the repo this shows up as:

- `fix(spec-specs): Calculate all gas we can before accessing state`
- `fix(spec-specs): Early static check for SSTORE before any reads`
- `feat(test-tests): Expand BAL CALL opcode OOG boundary test cases`
- 16 spec-side `fix`/`refactor` iterations — 3.2× the next highest EIP (8037, 5)
- 23 026 lines of EELS churn — 3.6× the next highest

## 2. The structural problem: the checklist is additive, the cost is a product

7928's test surface is a Cartesian product:

```
(state-accessing opcodes) × (cold / warm)
  × (OOG-before-access / OOG-after-access / success−1 / success)
  × (static / non-static) × (7702-delegated / direct)
```

An additive 0–3 checklist cannot express a product. Adding rows does not fix it.
Holding the new anchor's *score* fixed and changing only how it enters the total:

| How the same anchor enters the total | S(7928) | 7928 predicted out-of-sample | vs 150.3 actual |
|---|---:|---:|---:|
| not scored at all (today) | 29 | 61 | 0.40× |
| additive 0–3 row | 32 | 67 | 0.45× |
| additive row at 3× weight | 38 | 79 | 0.52× |
| additive row at 5× weight | 44 | 89 | 0.59× |
| **multiplier `× 2^(score/2)`** | **82** | **154** | **1.03×** |

*(Fitted on the other eight mature EIPs only, then asked to predict 7928. The
multiplier is the only structure that lands it.)*

Even at 5× weight — 15 additive points, more than a fifth of the whole 72-point
scale — an additive row gets to 0.59×. This is not a tuning problem.

The evaluators already knew this: EIP-8037's checklist is written as `2 + 2 + 3 + 1`
and `3 + 3 + 3`, hand-rolling multiplication because the form doesn't support it.
Formalise what they were already doing.

## 3. Proposed anchors

### 3.1 Sub-opcode failure-point observability — **MULTIPLIER**

> Makes it consensus-observable *where inside an opcode's execution* a failure
> occurred — in particular whether gas ran out before or after a state access.
> Previously only the final state mattered.

- **0.** Failure points inside an opcode are not observable; only final state matters.
- **1.** A single opcode or narrow family gains an observable internal failure point, with one gas boundary to settle.
- **2.** Multiple opcodes gain observable internal failure points, but the same rule fixes the boundary in each case.
- **3.** Every state-accessing opcode gains an observable internal failure point, and the boundary must be settled per-opcode because the gas-charge site differs.

**This row multiplies the additive subtotal by `2^(score/2)`** rather than adding
to it. Justification: each such boundary must be re-tested across every other
dimension that can change the answer, so it scales the existing matrix instead of
extending it.

> Do not confuse this with **Modified opcodes**. That row asks whether an
> opcode's *result* changed. This row asks whether the *path to the result*
> became observable. 7928 is 0 on the former and 3 on the latter.

### 3.2 State gas accounting changes — additive

Amsterdam introduced a second metering dimension via EIP-8037 — the cost of
*writing* state, distinct from accessing it: `StateGasCosts`
(`STORAGE_SET`, `NEW_ACCOUNT`, `AUTH_BASE`), `COST_PER_STATE_BYTE`,
`state_gas_reservoir`, block-level `block_state_gas_used`, and a `state_gas_spilled`
spill path into execution gas. The checklist has a row for blob gas and none for
this.

- **0.** No state gas accounting changes.
- **1.** An existing state gas cost or `STATE_BYTES_PER_*` rate is adjusted.
- **2.** A new state-gas-charging site is introduced, or the block-level state gas budget or reservoir allocation is modified.
- **3.** A new state gas charging mechanism is introduced, or the spill interaction between state gas and execution gas is modified, affecting existing gas tests.

Worse to test than blob gas: the spill path means state gas is **not**
independently meterable, and `NEW_ACCOUNT` is state-dependent.

### 3.3 Specification underdetermination — additive

> The EIP text does not determine the answer; clients must agree on a previously
> unspecified detail before tests can be baselined. The cost is coordination and
> re-baselining, not typing.

- **0.** The EIP text determines the answer for every case a test could construct.
- **1.** A few details are unspecified but have an obvious intended reading.
- **2.** Details require client agreement before tests can be written, but are localized.
- **3.** A previously unspecified *and previously unobservable* behaviour becomes consensus-critical; expect test re-baselining on each round of EIP amendment.

Evidence: 7928's `uint32 → uint64 → uint32` index-width reversal, BAL moved out of
the payload, `max bal item` check added late. Each round re-baselined tests.

### 3.4 Test-framework primitives required — additive

- **0.** Existing test primitives suffice.
- **1.** Existing primitives need minor extension.
- **2.** New expectation or modifier primitives are required, reusable within this EIP's suite.
- **3.** New framework-level primitives are required that become a permanent part of the framework and are used by other EIPs' tests.

Evidence: 7928 added ~2.4 KLOC of `BlockAccessListExpectation`,
`BalAccountExpectation`, `BalAccountAbsentValues` and a modifier DSL — 9 framework
units and 9 801 lines of framework churn, 6.8× the next highest.

### 3.5 Retroactive expectation obligation — additive

> Existing tests must *carry a new validated artifact*. Distinct from
> **Patterns affecting pre-existing tests**, which asks whether they must be
> reworked.

- **0.** Existing tests are unaffected.
- **1.** A contrived subset of existing tests must carry a new expectation.
- **2.** A broad category must carry a new expectation, mechanically.
- **3.** Every test for the fork carries a new validated artifact, and pre-fork vectors need re-derivation.

7928 scored only 2 on the existing "pre-existing tests" row — correctly, since
little was *reworked*. But every Amsterdam-filled test now generates and validates
a BAL, and Osaka's BAL checks had to be moved. That is a different cost.

### 3.6 Uncap Cross-EIP interactions

The existing row saturates at 3. 7928's rationale names **11** interacting EIPs
(2929, 2930, 1559, 6780, 7702, 4895, 2935, 4788, 7002, 7251, 1153, 214); 8038
names 6; everyone else names 0. Let level 3 scale with the count — e.g. `3 + 1`
per additional 4 EIPs beyond the first 3 — in the same style the 8037 assessment
already uses.

## 4. Validation

Scoring all 12 Amsterdam EIPs on the proposals and refitting:

| Model | r | exponent k | LOO error | 7928 ratio | 8037 ratio |
|---|---:|---:|---:|---:|---:|
| current checklist | 0.920 | 1.62 | 21 % | 1.68 | 0.92 |
| + the four additive rows only (U, P, R, G) | 0.916 | 1.55 | 31 % | 1.66 | 0.86 |
| + sub-opcode multiplier | 0.996 | 1.12 | 13 % | 0.97 | 1.20 |
| **+ multiplier + state gas row** | **0.998** | **1.11** | **13 %** | **1.01** | **1.12** |

Note the second row: **the four additive anchors on their own make the fit
slightly worse** (r 0.920 → 0.916, LOO 21 % → 31 %). They add points to 7928, but
they add points to almost everything else too, so the refitted curve moves with
them and 7928's ratio barely budges (1.68 → 1.66). Only the multiplier changes
the shape. The additive rows are worth adding for coverage — they let evaluators
record costs that currently have nowhere to go — but they are not what fixes
7928.

```
S_eff = (base + underdetermination + framework + retro + state_gas) × 2^(sub_opcode / 2)
TEU   = 0.83 × S_eff^1.11
```

Per EIP, with `add` = additive subtotal and `O` = the multiplier row:

| EIP | base | U | P | R | G | add | O | S_eff | TEU | pred | ratio |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 7928 | 29 | 3 | 3 | 3 | 0 | 38 | 3 | 107.5 | 150.3 | 149.3 | **1.01** |
| 8037 | 28 | 2 | 2 | 3 | 3 | 38 | 1 | 53.7 | 77.7 | 69.2 | 1.12 |
| 8038 | 20 | 2 | 0 | 2 | 2 | 26 | 1 | 36.8 | 7.7 | 45.4 | 0.17 † |
| 2780 | 13 | 1 | 0 | 2 | 0 | 16 | 0 | 16.0 | 18.6 | 18.0 | 1.03 |
| 7778 | 10 | 0 | 1 | 0 | 0 | 11 | 0 | 11.0 | 13.5 | 11.9 | 1.14 |
| 7708 | 9 | 0 | 1 | 1 | 0 | 11 | 0 | 11.0 | 7.4 | 11.9 | 0.62 |
| 7843 | 7 | 0 | 1 | 1 | 0 | 9 | 0 | 9.0 | 7.9 | 9.5 | 0.83 |
| 8070 | 7 | 0 | 2 | 0 | 0 | 9 | 0 | 9.0 | 1.1 | 9.5 | 0.12 † |
| 8024 | 6 | 0 | 1 | 1 | 0 | 8 | 0 | 8.0 | 8.3 | 8.4 | 0.99 |
| 7981 | 6 | 0 | 1 | 0 | 0 | 7 | 0 | 7.0 | 6.5 | 7.2 | 0.90 |
| 7976 | 5 | 0 | 1 | 0 | 0 | 6 | 0 | 6.0 | 9.9 | 6.1 | 1.63 |
| 7997 | 5 | 0 | 0 | 0 | 0 | 5 | 0 | 5.0 | 3.5 | 5.0 | 0.71 |

† still in flight; held out of the fit.

### The exponent collapses to ~1.1

This is the most interesting result and the best argument that the proposals
describe something real. The 1.62 exponent in the current calibration was **the
power law compensating for a missing multiplicative term**. Express the product
structure explicitly and the residual super-linearity nearly vanishes — cost
becomes close to linear in the effort-weighted score. "Complexity is mysteriously
super-linear" was the wrong conclusion; "the score was missing a multiplier" is
the right one.

## 5. Tier rescaling

The additive ceiling rises from 72 to 84 (four new 0–3 rows), and `S_eff` can
reach `84 × 2.83 = 238`.

| Tier | On `S_eff` | Amsterdam members |
|---|---|---|
| 🟢 Low | < 12 | 7997, 7976, 7981, 8024, 7843, 8070, 7708, 7778 |
| 🟡 Medium | 12 – 33 | 2780 |
| 🔴 High | ≥ 34 | 8038, 8037, 7928 |

Thresholds chosen to preserve the current tier populations. Note 7928 at 107 is
now visibly 3× the next-worst EIP rather than sitting one point above it — which
matches what actually happened.

## 6. Caveats

1. **`r = 0.998` is not a credible accuracy claim.** Nine points and a
   hand-assigned four-level variable can fit almost anything. The credible
   evidence is the out-of-sample test in §2 (fit without 7928, predict 7928:
   0.40× → 1.03×), the LOO error dropping 21 % → 13 %, and the exponent
   collapsing to ~1.1.
2. **The multiplier's calibration rests on one observation.** 7928 is the only
   EIP scoring 3 on it. `2^(score/2)` is a plausible shape, not a measured one —
   only the endpoint is measured. A second fork with a 2 or 3 on this row is
   needed before the intermediate levels mean anything.
3. **All proposed scores are assigned in hindsight**, by reading the repo. The
   real test is whether an evaluator can score these rows *at CFI time*, before
   the work. Rows 3.2–3.5 look assessable a priori. Row 3.1 is the risky one:
   recognising that an EIP makes an execution detail newly observable is exactly
   the insight 7928's original evaluation missed.
4. **The state gas row changes nothing retroactively** except 8037, which
   introduced the mechanism. Its value is forward-looking: any Amsterdam+ EIP
   touching state gas costs now has a row to be scored on.
5. **Independent evidence for the additive rows is thin.** 3.3 (spec
   underdetermination) is scored above 0 for only four EIPs, 3.5 (retro
   expectations) for six. They improve the fit but each rests on a handful of
   observations.

## 7. Reproducing

The scoring tables and every figure above come from `proposed-anchors.py`, which
reads `amsterdam-dataset.json`. Re-run after Amsterdam ships — 8038, 8070 and
7997 are still truncated and will change the picture.
