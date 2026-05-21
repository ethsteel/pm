# STEEL Team Recap April 2026

## TLDR

### Soldøgn Interop

- **7 STEEL members participated in Soldøgn and the preceding STEEL Team co-work week in Oslo**. Mario, Spencer, Felipe, Louis, Carson, Dan joined core devs in Svalbard (Apr 27 to May 1), while Peter joined the pre-interop co-work week in Oslo (Apr 20 to 24). Peter's Oslo deep dive on EIP-8037 produced an alternative state-gas-accounting proposal that seeded the Monday 8037 breakout on the trip.
- **Rapid iterations on EIP-8037 specs**. During daily working sessions ([pt1](https://notes.ethereum.org/@protocolsupport/8037-spec-breakout), [pt2](https://hackmd.io/@nixorokish/8037p2-summary), [pt3](https://hackmd.io/@nixorokish/8037p3-summary)) **Spencer, Felipe and Mario** worked intensively with Maria (RIG) and other core developers, notably Dragan (Reth), Ben Adams (Nethermind), Pawel (Erigon) and Marius (Geth) to converge the EIP-8037 State Gas spec, arriving at a fixed cost-per-state-byte and, after prototyping end-of-call accounting, decided that in-opcode accounting remained the best approach.
- **Repricing Goals Achieved**: **Louis** collaborated intensively with Maria (RIG), Jochem (Prototyping), Raffael (EthPandaOps) and client teams to ensure that repricing benchmarking data could be gathered. This result in a conservative estimate of a 200M gas limit for Glamsterdam!
- **Carson led an [EIP-7708 breakout session](https://hackmd.io/@nixorokish/eip7708-summary)** which further clarified spec (priority fees, base-fee burn, withdrawals out of scope).
- **STEEL-led [EL Client breakout session](https://hackmd.io/@nixorokish/EL-hardening-summary).** Following up from in-person discussions with client teams, **Dan** led an EL-focussed testing session. Teams agreed that moving the primary testing methodology from a system test (Hive) to a module test (Spencer's recently proposed `enginetest` interface) could accelerate developement. Other topics included how to better handle EL exceptions and invalid tests and branching strategies.
- On 3 of 5 days STEEL members won one of the daily Panda Prizes!
- Louis made his first snowman with help from rest of the team.

### Glamsterdam

- Leading up to the Interop, Spencer, Keri and other team members added ~200 tests to allow direct launch of  bal-devnet-5 pre-interop.
- Shipped 10 test vector releases including `bal@v6.0.0` (snobal-devnet-4) and the rapid-iteration `snobal-devnet-5`/`snobal-devnet-6` series during the final five days of the month at the Soldogn Interop.
- Adopted Mario's `fork.is_eip_enabled(EIP)` cross-EIP testing pattern team-wide and merged Felix's Python DevNet merger script for conflict-free composition of EIPs 7976, 7981, 8024, and 8037.

### Benchmarking

- Validated the cached/non-cached benchmarking methodology, which surfaced P256 verify as needing repricing (over-optimistic caching previously hid this).
- Presented the first preliminary EIP-7904 and EIP-8038 worst-case multipliers at the April 21 gaslighting call (storage write 50x, account write 32x, storage access 86x flagged as suspicious by Besu).
- Felipe's Geth T8N streaming fix cut peak memory on benchmark fills from ~12 GB to 2 to 3 GB, unlocking the benchmark release path.

### Bogota

- FOCIL: Felix added the first set of FOCIL tests in [PR #2643] and a new simulator to test the new `engine_getInclusionListV1` endpoint and remotely helped Besu test their implementation remotely during the interop.

### Client Support

- Spencer drafted an `enginetest` direct interface to all mainnet clients. Nethermind used this interface during the interop to accelerate testing, successfully detecting regressions. Additional commitments from Geth, Besu, Reth, Nimbus, Ethrex and Erigon to adopt the interface at the Soldogn EL hardening breakout (see [HackMD summary](https://hackmd.io/@nixorokish/EL-hardening-summary)).

### Priorities for Next Month

- Finalize the EIP-8037 EELS spec and tests ready for a bal-devnet-7 release.
- Push to SFI all `bal-devnet-6` EIPs and merge their respective `eips/amsterdam/eip-*` branch to `forks/amsterdam`.
- Stand up the new N+1 (Hegota) call (Fridays 14:00 UTC, Peter leading) and define the process so red-complexity EIPs get earlier STEEL involvement.

---

## Glamsterdam

### Specs and Tests

April was dominated by EIP-8037 spec convergence. The team iterated through three different state-gas accounting models across the month and ultimately landed on inline op-code-level accounting at Soldogn. Four bal-devnets shipped between April 1 and April 30, capped by `bal-devnet-6` stabilizing the final form just as the interop wrapped.

**BALS (Headliner)**

- Felipe extended invalid-BAL coverage in [PR #2653](https://github.com/ethereum/execution-specs/pull/2653) and refactored the block access index to `uint32` in [PR #2730](https://github.com/ethereum/execution-specs/pull/2730).
- Mario added EIP-7708 cross-checks against EIP-6780 in [PR #2743](https://github.com/ethereum/execution-specs/pull/2743) and pushed the gas-limit-aware `Fork` and fork-aware `Environment` plumbing in [PR #2690](https://github.com/ethereum/execution-specs/pull/2690).
- BAL workflows pointed at bal-devnet-4 (Spencer, [hive-tests #46](https://github.com/ethpandaops/hive-tests/pull/46), [hive-ui #64](https://github.com/ethpandaops/hive-ui/pull/64)) and bumped to snobal-devnet-5 ([hive-tests #49](https://github.com/ethpandaops/hive-tests/pull/49)).

**DevNet 4 / DevNet 5 / DevNet 6 EIPs**

- **EIP-8037** (State Gas Reservoir): Spencer drove the "second unofficial headliner" EIP all month, contributing 17 execution-specs PRs two EIP updates ([EIPs #11532](https://github.com/ethereum/EIPs/pull/11532), [EIPs #11548](https://github.com/ethereum/EIPs/pull/11548)). Major test additions covered blockchain header gas used cases ([PR #2611](https://github.com/ethereum/execution-specs/pull/2611)), CREATE state gas charge ordering ([PR #2608](https://github.com/ethereum/execution-specs/pull/2608)), nested child frame refunds (Felipe, [PR #2733](https://github.com/ethereum/execution-specs/pull/2733)), per-dimension block gas limit checks (Keri, [PR #2703](https://github.com/ethereum/execution-specs/pull/2703)), CALL with value to selfdestructed accounts (Keri, [PR #2646](https://github.com/ethereum/execution-specs/pull/2646)), zero execution state gas on top-level failure (Keri, [PR #2689](https://github.com/ethereum/execution-specs/pull/2689)), CREATE failure refunds ([PR #2704](https://github.com/ethereum/execution-specs/pull/2704)), SELFDESTRUCT same-tx refunds ([PR #2707](https://github.com/ethereum/execution-specs/pull/2707)), immutable intrinsic state gas for EIP-7702 ([PR #2711](https://github.com/ethereum/execution-specs/pull/2711)), calldata floor on sender refund ([PR #2728](https://github.com/ethereum/execution-specs/pull/2728)), SSTORE refund clamp ([PR #2729](https://github.com/ethereum/execution-specs/pull/2729)), and alignment with the GasCosts refactor ([PR #2737](https://github.com/ethereum/execution-specs/pull/2737)). Roughly 200 unique tests added; 19 PRs in bal-devnet-4 alone.
- **EIP-7976** (Floor Call Data Cost): Champion-side rebase on latest 47 (Mario) shipped in bal-devnet-4.
- **EIP-7981** (Excess List Cost Increase): Felix improved test robustness in [PR #2696](https://github.com/ethereum/execution-specs/pull/2696); shipped in bal-devnet-4.
- **EIP-7708** (logs for ETH transfers): Spencer added finalization burn log ordering and the coinbase fee no-log case in [PR #2717](https://github.com/ethereum/execution-specs/pull/2717). Carson and Peter Miller worked on an alternate gas-accounting proposal; Pawel returned with a new approach. Soldogn working session (May 1, Carson hosted) clarified scope: priority fees, base fee burn, and withdrawals are out of scope, and log cost is provisionally bundled with CALL repricing pending EIP-2780 clarity.
- **EIP-2780** (Variable Intrinsic Gas): Guru landed the implementation in [PR #2175](https://github.com/ethereum/execution-specs/pull/2175) plus an EIPs clarification ([EIPs #11332](https://github.com/ethereum/EIPs/pull/11332)). Treated as nice-to-have for interop; static-test port remains a follow-up.
- **EIP-8024** (Encoding/Decoding Rules): Mario fixed cross-EIP failures with EIP-8037 in [PR #2656](https://github.com/ethereum/execution-specs/pull/2656).
- Felipe extended Geth's `testing_buildBlockV1` to wire up `slotnum` ([go-ethereum #34721](https://github.com/ethereum/go-ethereum/pull/34721)) and respect slot num when specified in payload attributes ([go-ethereum #34722](https://github.com/ethereum/go-ethereum/pull/34722))
- **EIPS class refactor**: Mario added EIP classes ([PR #2571](https://github.com/ethereum/execution-specs/pull/2571)) and enabled multiple EIPs to be specified in `fork.is_eip_enabled` ([PR #2676](https://github.com/ethereum/execution-specs/pull/2676)). The latter became the team's standard cross-EIP testing pattern.

### Gas Repricing

Gas repricing work matured significantly across April. The cached/non-cached methodology validated mid-month, the first preliminary EIP-7904 and EIP-8038 numbers were presented April 21, and Maria's pre-trip handoff at the gaslighting call gave the team a concrete starting point for the Soldogn working sessions.

- **EIP-7904** (Compute Gas Cost Renaming / repricing): Carson and Sam landed a large repricing tool refactor (including [PR #2396](https://github.com/ethereum/execution-specs/pull/2396) for opcode gas constants and the formatting fix in [PR #2763](https://github.com/ethereum/execution-specs/pull/2763)). Preliminary numbers from Maria Silva on April 21: mod/div lower than originally proposed, mulmod 8 to 12, addmod unchanged, and P256 verify newly identified as needing repricing.
- **EIP-8038** (State Access Gas): Spec considered done; benchmark data near-complete. Preliminary worst-case multipliers presented April 21 (storage write 50x, account write 32x, storage access 86x, account access 3x with no code, 7x with code). Erigon and Reth are worst-case for storage; Besu is worst-case for account access. The 86x storage access result was flagged as suspicious by Besu (Ameziane committed to local reproduction).
- **Gas repricing call expansion**: Reth and Erigon client devs welcomed as new gaslighting attendees on April 21, broadening the cross-client conversation beyond the existing core.
- **Pain point slides**: Spencer contributed [Add testing pain point slides](https://github.com/misilva73/evm-gas-repricings/pull/3) to the gas repricings working group.

### Test Vector Releases

Ten test vector releases shipped this month, all driven by snobal devnet preparation and the Soldogn interop. The release cadence accelerated dramatically into the trip (four devnet releases in the final five days).

- [bal@v5.6.0](https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v5.6.0) (Apr 2)
- [bal@v5.6.1](https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v5.6.1) (Apr 2)
- [zkevm@v0.3.3](https://github.com/ethereum/execution-spec-tests/releases/tag/zkevm%40v0.3.3) (Apr 6)
- [bal@v5.7.0-alpha](https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v5.7.0) (Apr 21)
- [bal@v6.0.0 / snobal-devnet-4](https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v6.0.0) (Apr 27): major release. EIP-8037 (with the cost-per-state-byte block-gas-limit workaround), EIP-7976, EIP-7981, BAL index width change (`uint64` to `uint32`, [EIPs #11550](https://github.com/ethereum/EIPs/pull/11550) / [execution-specs #2730](https://github.com/ethereum/execution-specs/pull/2730)). ~200 new unique tests, 7 spec changes, 19 PRs for EIP-8037.
- [zkevm@v0.3.4](https://github.com/ethereum/execution-spec-tests/releases/tag/zkevm%40v0.3.4) (Apr 28)
- [snobal-devnet-5@v8037.0.0](https://github.com/ethereum/execution-spec-tests/releases/tag/snobal-devnet-5%40v8037.0.0) (Apr 29)
- [snobal-devnet-5@v8037.0.1](https://github.com/ethereum/execution-spec-tests/releases/tag/snobal-devnet-5%40v8037.0.1) (Apr 29)
- [snobal-devnet-6@v1.0.0](https://github.com/ethereum/execution-spec-tests/releases/tag/snobal-devnet-6%40v1.0.0) (Apr 30)
- [snobal-devnet-6@v1.1.0](https://github.com/ethereum/execution-spec-tests/releases/tag/snobal-devnet-6%40v1.1.0) (Apr 30): final inline-op-code-level EIP-8037 design.

## Road to Soldogn (Svalbard) Interop

Seven STEEL members participated in Soldøgn and the preceding STEEL co-work week in Oslo. Six joined core devs in Svalbard from April 27 to May 1, 2026 (Mario, Spencer, Felipe, Louis, Carson, Dan); Peter joined the pre-interop co-work week in Oslo (April 20 to 24), where his deep dive on EIP-8037 produced the alternative state-gas-accounting proposal that seeded the Monday emergency breakout on the trip. Felix, Sam, Keri, Guru, and Leo participated remotely. The team brought four headline goals into the trip: convergence on the EIP-8037 spec, EL hardening alignment with major client teams, EIP-7708 scope clarification, and gas repricing alignment for EIP-7904 and EIP-8038. April was structured deliberately around making those goals reachable.

### Preparation timeline

April was structured as six concerted efforts, each removing a known bottleneck before the team met researchers, prototypers and clients in person on Svalbard.

#### 1. Speed up the release pipeline

The Soldogn cadence (four bal-devnet releases in five days at month-end) was greatly facilitated due to the team attacking release latency on two fronts before leaving.

- **Normal releases (Dan)**: Split fixture generation across multiple runners by fork ([PR #2592](https://github.com/ethereum/execution-specs/pull/2592)) which brought releae generation time down from ~3 hours to ~1 hour. Spencer additionally temporarily disabled `enginex` fixtures in release generation which brought release time down to ~30 minutes. Further improvements for releases are planned, see the tracking issue: [execution-specs #2736 "Faster, More Targeted Test Fixture Releases"](https://github.com/ethereum/execution-specs/issues/2736).
- **Benchmark releases (Felipe)**: Diagnosed peak memory in both Python and Geth and landed paired fixes: t8n file streaming optimizations on the EELS side ([execution-specs #2751](https://github.com/ethereum/execution-specs/pull/2751)) and streaming t8n alloc to ease heavy memory cases on the Geth side ([go-ethereum #34785](https://github.com/ethereum/go-ethereum/pull/34785)). Peak memory on benchmark fills dropped from ~12 GB to 2 to 3 GB, unlocking the benchmark release path in time for the interop.

#### 2. Firm up the EIP-8037 spec for bal-devnet-5 pre-interop

Getting a stable 8037 spec and matching test fixtures into client hands before the trip was the headline goal. Spencer iterated through three cost-per-state-byte models in April, with bal-devnet-3 (Apr 1) acting as a DevNet 3 spec freeze and [bal-devnet-4](https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v6.0.0) (Apr 21) shipping EIP-8037 plus EIP-7976, EIP-7981, and the BAL index width change (`uint64` to `uint32`) with ~200 unique tests and 19 PRs for EIP-8037 alone. The April 23 Testing emergency call escalated EIP-8037 to ACDE for a temperature check (Peter posted; three options on the table: rewrite, ship as-is, drop), deliberately surfacing the concern publicly before the trip rather than ambushing client teams on-site.

#### 3. Cross-EIP composability tooling

Iterating EIP-8037 weekly without breaking EIP-7976, EIP-7981 and EIP-8024 tests required a coordinated tooling effort.

- **Mario's `fork.is_eip_enabled(EIP)` cross-EIP testing pattern** ([PR #2676](https://github.com/ethereum/execution-specs/pull/2676)): Replaces TODO comments with explicit conditional logic in tests, making cross-EIP fixes self-documenting. Adopted team-wide in mid-April.
- **Mario's EIP classes and forks composition** ([PR #2571](https://github.com/ethereum/execution-specs/pull/2571)): Split monolithic `forks.py` into per-EIP files, easing rebases and reducing merge conflicts.
- **Felix's DevNet merger Python script** ([PR #2663](https://github.com/ethereum/execution-specs/pull/2663)): Replaces the old shell builder with conflict-free composition of EIPs 8024, 8037, 7976, and 7981 into Fork Amsterdam.

#### 4. In-EELS benchmarking and methodology validation

Pre-trip benchmarking work focused on landing the methodology, the numbers, and reproducible state tooling that the in-person team could put in front of client devs at the Soldogn benchmarker workshop.

- **Cached/non-cached methodology validated** April 14, then applied to pre-compiles April 21 (which surfaced P256 verify as needing repricing).
- **Maria Silva's preliminary EIP-7904 and EIP-8038 multipliers** handed off at the April 21 gaslighting call, giving the in-person team concrete numbers for the Soldogn working sessions.
- **Jochem's reproducible-state tooling** (Apr 14 and Apr 21 gaslighting): a mainnet-snapshot replay path that executes pre-state transactions on top of a mainnet snapshot (with 20 GB, 10 GB, and 1 GB contract variants for state-heavy benchmarks), plus a mid-sized-state proposal that runs initialization payloads on top of empty state to produce contracts ~2x mainnet size for local iteration. Together these unblock client teams from needing the multi-TB bloatnet snapshot just to start optimizing, with full bloatnet runs reserved for final benchmark validation. Louis and Jochem hosted a benchmarker setup workshop at the trip on this foundation.

#### 5. The `enginetest` direct interface for client teams

Spencer drafted a new direct interface (`enginetest`) for client teams to run engine fixtures without going through Hive. Bringing this to the trip as a credible alternative to Hive made the EL hardening breakout possible.

- **Spencer's `enginetest` direct runner**: Nethermind and Besu engine tests dropped from "up to a day" to ~5 minutes, with Erigon at ~8 minutes.
- **Cross-client adoption tracker**: [execution-specs #2650 "consume direct support for all EL clients with engine fixture runners"](https://github.com/ethereum/execution-specs/issues/2650).
- Together these set up the cross-client `enginetest` commitments secured at the Apr 30 EL hardening breakout (see [HackMD summary](https://hackmd.io/@nixorokish/EL-hardening-summary)).

#### 6. Documentation push for in-person knowledge sharing

A coordinated push moved the team's spec and tooling docs onto a single, current site for use during Soldogn.

- Combined HTML and spec doc artifact published (Dan, [PR #2638](https://github.com/ethereum/execution-specs/pull/2638)).
- README and top-level docs rewritten in standard open-source style; specs section added to HTML docs (Dan, [PR #2677](https://github.com/ethereum/execution-specs/pull/2677)); EIP author's manual moved into HTML docs (Dan, [PR #2662](https://github.com/ethereum/execution-specs/pull/2662)).
- Result: <https://steel.ethereum.foundation/docs/> served as the single source of truth at the interop, with current spec content per devnet branch.

### Outcomes at the trip

- **Three rapid EIP-8037 working sessions converged the spec.** Spencer, Felipe, and Mario worked alongside Maria (RIG), Dragan (Reth), Ben Adams (Nethermind), Pawel (Erigon), and Marius (Geth) across three sessions ([pt1](https://notes.ethereum.org/@protocolsupport/8037-spec-breakout), [pt2](https://hackmd.io/@nixorokish/8037p2-summary), [pt3](https://hackmd.io/@nixorokish/8037p3-summary)) to lock a fixed cost-per-state-byte at 1,174 (with broad consensus including Vitalik to keep the EIP). After prototyping end-of-call accounting following Peter's Oslo proposal, multi-client pushback (Reth, Erigon, Geth) prompted a Thursday revert to in-opcode accounting. bal-devnet-6 stabilized just as the trip wrapped.
- **Repricing goals achieved.** Louis collaborated intensively with Maria (RIG), Jochem (Prototyping), Rafael (EthPandaOps), and client teams to make repricing benchmarking data gatherable, resulting in a conservative 200M post-Glamsterdam gas-limit floor agreement.
- **Carson hosted the [EIP-7708 working session](https://hackmd.io/@nixorokish/eip7708-summary)** (May 1) which clarified scope: priority fees, base-fee burn, and withdrawals are out of scope; log cost provisionally bundled with CALL repricing pending EIP-2780 clarity.
- **Dan led the STEEL [EL Client breakout session](https://hackmd.io/@nixorokish/EL-hardening-summary) (Apr 30)** following up from in-person discussions with client teams. Teams agreed to move the primary testing methodology from a system test (Hive) to a module test (Spencer's recently proposed `enginetest` interface) to accelerate development. Other topics: better handling of EL exceptions, invalid tests, and per-EIP branching strategies. Nethermind put `enginetest` to use during the interop and successfully detected regressions.
- **Hands-on client work**: Felipe and Guillaume (Geth) merged the T8N data-streaming PR ([go-ethereum #34785](https://github.com/ethereum/go-ethereum/pull/34785)) on-site; Felipe and Guillaume also fixed the long-broken Erigon T8N for Amsterdam plus EVM tracing. Felix remotely helped a Besu engineer integrate FOCIL, after which Besu passes all FOCIL tests except 4 (limited only by the EIP-8037 fixture toggle).
- **Lighter notes**: STEEL members took home daily Panda Prizes on three of five days. Louis built his first snowman with help from the rest of the team.
- **Future Fork Development Pipelining** The team decided to establish a new "N+1" (e.g., Hegota) coordination call. Peter accepted leadership of the EELS side and to moderate the call. The first priority is to define the N+1 process itself so red-complexity EIPs get earlier attention.

#### References

- [EF blog recap](https://blog.ethereum.org/2026/05/02/soldogn-interop-recap).
- [EL hardening summary](https://hackmd.io/@nixorokish/EL-hardening-summary).
- EIP-8037 working sessions ([pt1](https://notes.ethereum.org/@protocolsupport/8037-spec-breakout), [pt2](https://hackmd.io/@nixorokish/8037p2-summary), [pt3](https://hackmd.io/@nixorokish/8037p3-summary)).
- [EIP-7708 summary](https://hackmd.io/@nixorokish/eip7708-summary).

## Bogota

- **FOCIL** (Bogota / next-fork prep): Felix added FOCIL src features and the first set of FOCIL tests in [PR #2643](https://github.com/ethereum/execution-specs/pull/2643), and built a new simulator for the `engine_getInclusionListV1` endpoint.

## Client Support

April's client engagement happened largely through in-person conversation at Soldogn. The `enginetest` direct interface agreement set up a structural shift toward catching client bugs in modular tests rather than in Hive.

- **`enginetest` direct interface adoption** (cross-client commitment, [HackMD EL hardening summary](https://hackmd.io/@nixorokish/EL-hardening-summary)): Spencer drafted the `enginetest` direct interface to all mainnet clients. Nethermind put the interface to use during the interop and successfully detected regressions; Geth, Besu, Reth, Nimbus, Ethrex, and Erigon committed to adopt it at the Apr 30 EL hardening breakout. Spencer's tracking issue: [execution-specs #2650](https://github.com/ethereum/execution-specs/issues/2650). Reported performance gains: Nethermind from ~20 hours to minutes; Reth from 14 minutes to 1.5 minutes on Shanghai (10x).
- **FOCIL Besu integration support** (Felix, remotely during Soldogn): Felix helped a Besu engineer integrate FOCIL, including a brief explainer on creating a branch to fill the tests. Besu fixed all bugs and now passes all non-8037 FOCIL tests.
- **Besu BAL race condition** (Jochem, Apr 14 gaslighting): Besu passes all Glamsterdam benchmarks in sequential mode but fails some tests in optimized BAL plus parallel mode, with different tests failing across runs. Elevates BAL benchmarks to consensus-test status. Besu team aware.
- **EIP-8037 multi-client implementation feedback** drove the April 30 spec revert: Reth, Erigon, and Geth all flagged issues with end-of-call-frame state gas accounting, prompting the impromptu morning breakout.
- **Geth T8N for Amsterdam plus EVM tracing fix** (Felipe with Guillaume on-site at Soldogn): fixes long-broken EVM tracing.
- **Geth T8N streaming** (Felipe): peak memory cut from ~12 GB to 2 to 3 GB on unchunked bytecode tests, prototyped April 21 ([PR #34785](https://github.com/ethereum/go-ethereum/pull/34785)) and merged at Soldogn by Guillaume. This was the biggest unlock for benchmark releases.

## Benchmarking (Scale the L1)

Two structural shifts and a methodology validation defined April's benchmarking work. The cached/non-cached methodology was finally validated mid-month, the in-house EELS-based payload generation replaced the old man-in-the-middle script, and Felipe's Geth T8N streaming fix unlocked the chronic benchmark release OOM.

- **Cached/non-cached methodology validated** (Apr 14 gaslighting; Maria, Yoav, Louis, Carlos): The new S-load/S-store test set resolves a long-standing anomaly where re-writing the same value measured faster than an actual update. State writes now correctly more expensive than no-op writes; storage repricing numbers are looking good. Methodology applied to pre-compiles April 21, surfacing P256 verify as needing repricing.
- **EELS-based payload generation** (Felipe, Mario, Apr 7 gaslighting): Felipe's PoC replaces the gas-benchmarks man-in-the-middle script via the [`testing_buildBlock_v1`](https://github.com/NethermindEth/nethermind/pull/9901) endpoint. Kev's competing state-DB T8N PR closed in favor of this path. Ongoing work in execution-spec-tests plus benchmarker PRs.
- **Geth T8N streaming PR merged at Soldogn** (Felipe, [PR #34785](https://github.com/ethereum/go-ethereum/pull/34785)): peak memory 12 GB to 2 to 3 GB on unchunked bytecode tests. With this Geth change alone the team can release benchmarks reliably.
- **Stateful benchmark suite work** (Louis): nine PRs across the month including precompile macro for precompile benchmarks ([PR #2591](https://github.com/ethereum/execution-specs/pull/2591)), uncacheable precompile benchmark ([PR #2600](https://github.com/ethereum/execution-specs/pull/2600)), cache strategy in storage benchmark ([PR #2628](https://github.com/ethereum/execution-specs/pull/2628)), `EOA` pkey support for stub accounts ([PR #2624](https://github.com/ethereum/execution-specs/pull/2624)), parametrized stateful benchmark stubs ([PR #2562](https://github.com/ethereum/execution-specs/pull/2562)), the `ecpairing` zero tx fix ([PR #2749](https://github.com/ethereum/execution-specs/pull/2749)), and the storage benchmark gas-limit refactor ([PR #2771](https://github.com/ethereum/execution-specs/pull/2771)).
- **Trace verification comparators** (Leo): Verify-traces flag with gas-agnostic, OOG-location, and stack-ignoring comparators landed in [PR #2535](https://github.com/ethereum/execution-specs/pull/2535) and aggregation across xdist workers in [PR #2664](https://github.com/ethereum/execution-specs/pull/2664).
- **Benchmarker infrastructure walkthrough** (Louis, Rafael, Apr 21 gaslighting): Three-component picture (execution-spec-tests benchmarks, Nethermind-maintained `gas-benchmarks` tool, `benchmarker` test runner) presented to new Reth and Erigon attendees. Local benchmarker setup support committed for Andrew Ashikhmin (Erigon) as first external user.
- **Benchmarker workshop at Soldogn** (Louis, Jochem): held during the trip; Louis played a valuable role driving community alignment.
- **Block-building benchmarking added to scope** (Felipe): currently only re-execution is benchmarked; the Amsterdam slowdown plus BALS-induced payload growth motivated adding the build path.
- **EIP-8037 benchmark integration solution** (Mario, Carlos, Louis at Soldogn): Walked through the full benchmark life cycle and found a solution compatible with the converged 8037 design; Louis implementing.

## Tooling and Libraries

The team made structural tooling investments that paid off in the Soldogn release cadence and will compound through Glamsterdam.

- **`tox` to `just` migration** (Dan, [PR #2555](https://github.com/ethereum/execution-specs/pull/2555)): Foundational tooling migration that triggered downstream changes throughout the month (recipes for `tests`, `static`, `fix`, `coverage`, `test_pyspec`, `test_bench`; parallelized static; tab completion; arg pass-through). Full team approval. The shift propagated externally with Felipe's `leanEthereum/leanSpec` issue suggesting `just` over `tox` ([leanSpec #634](https://github.com/leanEthereum/leanSpec/issues/634)).
- **Felix's DevNet merger script** ([PR #2663](https://github.com/ethereum/execution-specs/pull/2663)): conflict-free merge of EIPs 8024, 8037, 7976, 7981 into Fork Amsterdam. Supports local-branch merging and detects the ethereum repo by URL.
- **Cross-EIP testing pattern** (Mario, [PR #2676](https://github.com/ethereum/execution-specs/pull/2676)): `fork.is_eip_enabled(EIP)` adopted across the team. Replaces TODO comments and DevNet fix branches with explicit conditional logic.
- **EIP classes and forks composition** (Mario, [PR #2571](https://github.com/ethereum/execution-specs/pull/2571)): split monolithic `forks.py` into per-EIP files. Eases EIP rebases and reduces merge conflicts.
- **`pytest.mark.valid_before`** (Mario, [PR #2647](https://github.com/ethereum/execution-specs/pull/2647)): paired with the gas-limit-aware `Fork` and fork-aware `Environment` ([PR #2690](https://github.com/ethereum/execution-specs/pull/2690)) to make EIP-aware test conditions cleaner.
- **CI restructure** (Dan): split release builds across multiple runners, deleted `develop`, made `stable` map to `mainnet` ([PR #2592](https://github.com/ethereum/execution-specs/pull/2592)); enabled phase-1-only pre-alloc generation ([PR #2720](https://github.com/ethereum/execution-specs/pull/2720)); generate-all-formats for mainnet fixture releases ([PR #2781](https://github.com/ethereum/execution-specs/pull/2781)).
- **Documentation pipeline modernization** (Sam, 12 PRs): Six PRs in `SamWilsn/docc` (whitespace, anchors, directory listings, listing source hooks, `__init__.py` PythonSource, dark mode) plus three downstream `execution-specs` PRs ([#2658](https://github.com/ethereum/execution-specs/pull/2658), [#2756](https://github.com/ethereum/execution-specs/pull/2756), [#2779](https://github.com/ethereum/execution-specs/pull/2779)) modernized the spec docs publishing pipeline.
- **`execution-specs` README and docs site rewrite** (Dan, [PRs #2662](https://github.com/ethereum/execution-specs/pull/2662), [#2677](https://github.com/ethereum/execution-specs/pull/2677), [#2638](https://github.com/ethereum/execution-specs/pull/2638)): combined HTML and spec doc artifact published, README rewritten in standard open-source style, EIP author's manual moved into HTML docs.
- **t8n streaming optimizations** (Felipe, [PR #2751](https://github.com/ethereum/execution-specs/pull/2751)): execution-specs-side complement to the Geth fix.
- **Static test port progress** (Leo): `@manually-enhanced` skip in filler-to-python ([PR #2630](https://github.com/ethereum/execution-specs/pull/2630)), dynamic addresses in ported static tests ([PR #2695](https://github.com/ethereum/execution-specs/pull/2695)), and missing trace file tolerance ([PR #2709](https://github.com/ethereum/execution-specs/pull/2709)).
