# Proposed Checklist Criteria

Derived from the [Amsterdam calibration](README.md). EIP-7928 is the only mature
Amsterdam EIP the current checklist materially mis-scores, and the reason is
coverage and *structure*, not evaluator error.

---

## 1. The evidence that this is a coverage gap

Back-solving each EIP's score from its measured work (`TEU = 0.38 × S^1.63`):

| EIP | Scored | Implied by measured work | Gap |
|---|---:|---:|---:|
| **7928** | **29** | **40** | **+11** |
| 8037 | 28 | 26 | −2 |
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
> spec-framework concern, not a behavior change in the criterion's sense.

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
Holding the new criterion's *score* fixed and changing only how it enters the total:

| How the same criterion enters the total | S(7928) | 7928 predicted out-of-sample | vs 150.3 actual |
|---|---:|---:|---:|
| not scored at all (today) | 29 | 60 | 0.39× |
| additive 0–3 row | 32 | 67 | 0.43× |
| additive row at 3× weight | 38 | 79 | 0.50× |
| additive row at 5× weight | 44 | 89 | 0.57× |
| **multiplier `× 2^(score/2)`** | **82** | **154** | **0.98×** |

*(Fitted on the other eight mature EIPs only, then asked to predict 7928.)*

Even at 5× weight — 15 additive points, more than a fifth of the whole 72-point
scale — an additive row gets to 0.57×. This is not a tuning problem: a sum cannot
approximate a product over this range.

The evaluators already knew this: EIP-8037's checklist is written as `2 + 2 + 3 + 1`
and `3 + 3 + 3`, hand-rolling multiplication because the form doesn't support it.

**The arithmetic above is sound. What it does *not* establish is that the
state-access ordering row is the multiplier — see the next section.**

## 2b. Why the data cannot identify *which* row is the multiplier

Running the same test with every existing criterion as the multiplier
(`S_eff = (base − row) × 2^(row/2)`, so the row isn't double-counted):

| Criterion used as multiplier | 7928's score | Other EIPs scoring >0 | 7928 out-of-sample |
|---|---:|---:|---:|
| Security risks | 3 | 0 | 1.34× |
| Engine API changes | 3 | 1 | 1.29× |
| New block / header fields | 3 | 1 | **1.05×** |
| Block syncing changes | 2 | 0 | **0.89×** |
| Performance risks | 3 | 3 | 0.73× |
| Transition-tool interface | 2 | 2 | 0.72× |
| Cross-EIP interactions | 3 | 1 | 0.65× |
| Edge/boundary conditions | 3 | 7 | 0.36× |
| EVM Gas rule changes | 3 | 5 | 0.20× |
| Patterns affecting pre-existing tests | 2 | 6 | 0.15× |

**Six existing rows work about as well as the proposed one, and they work for a
bad reason.** Look at the third column: the rows that "land" 7928 are exactly the
rows 7928 scores high on and nobody else scores at all. Made multiplicative, such
a row is a 7928 indicator variable — it identifies 7928 rather than explaining it.
Rows that many EIPs score (edge/boundary: 7 others; pre-existing tests: 6; gas
rules: 5) all fail, because multiplying them lifts everyone and the refit absorbs
the change.

So the out-of-sample test in §2 is weaker evidence than it looks. It guards
against fitting 7928's *measured TEU*, but not against having chosen a variable
that happens to single 7928 out. With one high-cost EIP in the sample, **no
statistical test can distinguish a mechanism from a label.**

### And you cannot simply make several rows multiplicative

Independent multipliers compound:

| EIP | base | product over 4 dimensional rows | S_eff |
|---|---:|---:|---:|
| 7928 | 29 | 5.7× | 164 |
| 8037 | 28 | **45.3×** | **1267** |
| 8038 | 20 | 8.0× | 160 |

8037 explodes because its "pre-existing tests" cell is written `3 + 3 + 3` = 9, and
`2^4.5` = 22.6. Nor can the axis count be recovered by re-reading the existing
rows as dimensions: try it and almost every EIP saturates at the cap, because
those rows encode *severity*, not dimensionality.

The resolution is arithmetic: axes **add in the exponent**
(`2^(a/2) × 2^(b/2) = 2^((a+b)/2)`). So the only stable form is **one** multiplier
whose score counts axes, scored independently of the severity rows — not N
individually multiplicative rows.

## 3. Proposed criteria

### 3.1 State-access ordering within opcode execution — additive

> Changes *where inside an opcode's execution* state is accessed, or where gas is
> charged relative to that access.

**Worded for the world after EIP-7928, not for the transition into it.** Since the
BAL, every state access is consensus-observable — an address or slot appears only
if execution had enough gas to reach it — so the ordering of gas charges and state
accesses inside an opcode is consensus rather than a client implementation detail.
Introducing that observability was a one-time event that has already happened; what
recurs is EIPs *moving* the ordering.

- **0.** No change to where state is accessed, or to where gas is charged relative to a state access, within any opcode.
- **1.** A single opcode's state-access or gas-charge ordering changes.
- **2.** Multiple opcodes' ordering changes, or a new state-accessing operation is introduced whose position in the order must be settled.
- **3.** The ordering rule changes for a whole class of state-accessing opcodes at once, or what counts as a recordable state access is redefined — requiring existing BAL vectors to be re-derived across opcodes and forks.

> Do not confuse this with **Modified opcodes**. That row asks whether an
> opcode's *result* changed. This row asks about the *path to the result*, now
> observable even when the result is identical. 7928 is 0 on the former and 3 on
> the latter — which is why the most expensive part of the work scored zero.

The reframing does not disturb the scores used below: 7928 remains a 3 (it
reordered gas-charge sites across an entire class of opcodes), 8037 and 8038
remain 1 (each moves where gas is charged relative to a state write).

This is the row whose absence is best evidenced (§1), independent of any argument
about multipliers. Add it additively now.

### 3.1b Test-matrix dimensionality — **the multiplier**, if one is adopted

Per §2b, a multiplier cannot be one of the severity rows, and there cannot be
several. If a multiplier is adopted it has to be a single row that asks directly
for the axis count, scored independently of everything else:

> How many **independent axes** does this EIP add to the test matrix — dimensions
> across which every other case must be re-run to get a different answer?

- **0.** No new axis. Cases are enumerable as a list.
- **1.** One new axis (e.g. every case must be run warm and cold).
- **2.** Two independent new axes.
- **3.** Three or more independent new axes.

`S_eff = additive_subtotal × 2^(axes / 2)`. The base 2 and the `/2` are chosen so
three axes give ≈2.8× rather than 8×, on the assumption that axes are partly
redundant in practice. **Neither the base nor the exponent is measured** — only the
`axes = 3` endpoint is, from one EIP.

For 7928 the three axes are: the intra-opcode gas boundary (§3.1), the 12-EIP cross
product, and the BAL expectation attaching to every existing test. For 8037, one:
the gas boundary re-run across the static suite.

**Recommendation: do not adopt this yet.** Add rows 3.1–3.6 additively, and record
the axis count on assessments as an *unscored observation* for a fork or two.
When a second EIP scores 2 or 3 on it, there will be enough data to tell whether
the multiplier is real and what its base should be. Adopting it now means
hard-coding a curve fitted to a single point.

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

### 3.5 New invariant on pre-existing tests — additive

> Tests that are **not about this EIP** must nonetheless check something this EIP
> produces. Their logic doesn't change; they gain a new thing to assert.
>
> Deliberately named to sit alongside **Patterns affecting pre-existing tests**.
> That row asks whether existing tests must be *reworked*; this one asks whether
> they must *additionally assert something new*. 7928 is a 2 on the first and a 3
> on the second.

- **0.** Pre-existing tests assert nothing new.
- **1.** A narrow, contrived category of pre-existing tests gains a new assertion.
- **2.** A broad category gains a new assertion, applied mechanically.
- **3.** Every test in the fork gains the assertion regardless of what it tests, and pre-fork vectors must be re-derived to satisfy it.

7928 scored only 2 on the "pre-existing tests" row — correctly, since little was
*reworked*. But every Amsterdam-filled test now generates and validates a BAL
whether or not it has anything to do with access lists, and Osaka's BAL checks had
to be moved. That is a different cost, and it had nowhere to be recorded.

### 3.6 Uncap Cross-EIP interactions

The existing row saturates at 3. 7928's rationale names **12** interacting EIPs
(2929, 2930, 1559, 6780, 7702, 4895, 2935, 4788, 7002, 7251, 1153, 214); 8038
names 6; everyone else names 0. Let level 3 scale with the count — e.g. `3 + 1`
per additional 4 EIPs beyond the first 3 — in the same style the 8037 assessment
already uses.

## 4. Validation

Scoring all 12 Amsterdam EIPs on the proposals and refitting. **Read rows 3 and 4
of this table together with §2b** — the fit statistics do not discriminate between
the state-access ordering row and six other candidate multipliers, so they are shown to
document the arithmetic, not to validate the choice of row.

| Model | r | exponent k | LOO error | 7928 ratio | 8037 ratio |
|---|---:|---:|---:|---:|---:|
| current checklist | 0.913 | 1.63 | 22 % | 1.72 | 0.90 |
| + the four additive rows only (U, P, R, G) | 0.909 | 1.56 | 33 % | 1.70 | 0.85 |
| + state-access ordering as multiplier | 0.997 | 1.13 | 13 % | 0.99 | 1.18 |
| **+ multiplier + state gas row** | **0.999** | **1.12** | **13 %** | **1.02** | **1.10** |

Note the second row: **the four additive criteria on their own make the fit
slightly worse** (r 0.913 → 0.909, LOO 22 % → 33 %). They add points to 7928, but
they add points to almost everything else too, so the refitted curve moves with
them and 7928's ratio barely budges (1.72 → 1.70). Only the multiplier changes
the shape. The additive rows are worth adding for coverage — they let evaluators
record costs that currently have nowhere to go — but they are not what closes the
gap on EIP-7928.

```
S_eff = (base + underdetermination + framework + new_invariant + state_gas) × 2^(state_access_ordering / 2)
TEU   = 0.81 × S_eff^1.12
```

Per EIP, with `add` = additive subtotal and `O` = the multiplier row:

| EIP | base | U | P | R | G | add | O | S_eff | TEU | pred | ratio |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 7928 | 29 | 3 | 3 | 3 | 0 | 38 | 3 | 107.5 | 156.7 | 153.0 | **1.02** |
| 8037 | 28 | 2 | 2 | 3 | 3 | 38 | 1 | 53.7 | 77.7 | 70.4 | 1.10 |
| 8038 | 20 | 2 | 0 | 2 | 2 | 26 | 1 | 36.8 | 7.7 | 46.1 | 0.17 † |
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

The 1.63 exponent in the current calibration behaves like **a power law
compensating for a missing multiplicative term**. Introduce a multiplicative term
of roughly the right size and the residual super-linearity nearly vanishes — cost
becomes close to linear in the effort-weighted score.

This is suggestive rather than conclusive, and for the same reason as everything
else here: any of the six candidate rows from §2b produces a similar collapse
(exponents 1.08–1.36). What the collapse supports is the *shape* of the model —
that some multiplicative term is missing — not the identity of the row supplying
it. "Complexity is mysteriously super-linear" is probably the wrong reading; "the
score is missing a product term" is the better one, and which product is still
open.

## 5. Tier rescaling

**As adopted in the template** (additive rows only, no multiplier): the criterion set
goes 24 → 28 rows — five added, **Engine API encoding changes** removed — so the
nominal ceiling is 72 → 84, and **Cross-EIP interactions** is uncapped on top of
that. Thresholds scale by 84/72: 🟢 `<12`, 🟡 `12–22`, 🔴 `≥23`. Amsterdam tier
membership is unchanged except EIP-7778, which moves 🟡 → 🟢 at 11 points.

> Engine API encoding changes described a JSON → RLP/SSZ migration at the Engine
> API layer. Those are coordinated outside the EIP process, so the row has no use
> in an EIP-scoped assessment. It was scored 0 or blank in all 28 assessments on
> the previous revision, and never had level definitions, so removing it changes
> no historical total. **Encoding changes (RLP/SSZ)** already covers the
> "interfaces level" if an EIP ever carries one.

**If the deferred multiplier (§3.1b) were also adopted**, `S_eff` could reach
`84 × 2.83 = 238` and the thresholds would instead be:

| Tier | On `S_eff` | Amsterdam members |
|---|---|---|
| 🟢 Low | < 12 | 7997, 7976, 7981, 8024, 7843, 8070, 7708, 7778 |
| 🟡 Medium | 12 – 33 | 2780 |
| 🔴 High | ≥ 34 | 8038, 8037, 7928 |

Also chosen to preserve tier populations. Under this variant 7928 lands at 107 —
visibly 3× the next-worst EIP rather than sitting one point above it, which
matches what actually happened. This is the variant to revisit once a second fork
supplies a second observation on the axis-count row.

## 6. Caveats

1. **`r = 0.998` is not a credible accuracy claim.** Nine points and a
   hand-assigned four-level variable can fit almost anything.
2. **The out-of-sample test is weaker than it appears.** Fitting without 7928 and
   predicting it (0.39× → 0.98×) rules out fitting to 7928's measured TEU. It does
   *not* rule out having picked a variable that singles 7928 out — and §2b shows
   six existing rows do just as well when made multiplicative, purely because
   7928 is the only EIP that scores them. With one high-cost EIP in the sample, no
   statistical test can separate a mechanism from a label.
3. **The multiplier is therefore a design proposal, not a finding.** What the data
   supports is the *negative* result: a sum cannot approximate a product, so no
   additive row at any weight closes the gap. Which row multiplies, and with what
   base, is unidentified. Hence the recommendation in §3.1b to record the axis
   count unscored until a second fork provides a second observation.
4. **All proposed scores are assigned in hindsight**, by reading the repo. The
   real test is whether an evaluator can score these rows *at CFI time*, before
   the work. Rows 3.2–3.5 look assessable a priori. Row 3.1 is the risky one:
   recognising that an EIP makes an execution detail newly observable is exactly
   the insight 7928's original evaluation missed.
5. **The state gas row changes nothing retroactively** except 8037, which
   introduced the mechanism. Its value is forward-looking: any Amsterdam+ EIP
   touching state gas costs now has a row to be scored on.
6. **Independent evidence for the additive rows is thin.** 3.3 (spec
   underdetermination) is scored above 0 for only four EIPs, 3.5 (new invariant on
   pre-existing tests) for six. They improve the fit but each rests on a handful
   of observations.

## 7. Reproducing

The scoring tables and every figure above come from `proposed-criteria.py`, which
reads `amsterdam-dataset.json`. Re-run after Amsterdam ships — 8038, 8070 and
7997 are still truncated and will change the picture.
