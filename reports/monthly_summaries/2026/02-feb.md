# STEEL Team Recap February 2026

## TLDR

### Glamsterdam

- Substantial implementation progress on 6 new Amsterdam EIPs this month, with EIP-8024 wrapping up from January and EIP-8038 queued for March. EIP-8037 (state gas reservoir) emerged as the most disruptive change, breaking most legacy tests and requiring a framework design overhaul for gas limit handling.
- [`bal-devnet-3`](https://notes.ethereum.org/@ethpandaops/bal-devnet-3) [test release shipped Feb 28](https://github.com/ethereum/execution-spec-tests/releases/tag/bal@v5.2.0) after scope expanded beyond initial estimates. Includes EIP-7954 and EIP-8037, which uses a `cost_per_state_byte` of 1174 for devnet-3. ~700 static tests temporarily skipped as the YAML-to-Python port is required to add 8037 logic; these will land in devnet-4.
- Benchmark filling is transitioning from evmone to Geth since evmone does not support Amsterdam. Spencer's opcode-count tracer PR merged into Geth, unblocking Amsterdam benchmark generation. Migration is still in progress.

### Scale the L1

- Benchmark release infrastructure stabilized after CI issues (OOM and worker starvation failures).
- Benchmark release generation time reduced from a full day to ~3 hours (Felipe, Mario, Louis, Dan). Mario's pre-alloc deduplication ([ethereum/execution-specs#2139](https://github.com/ethereum/execution-specs/pull/2139)) cut account count from ~500K to ~50K.
- Rafael (PandaOps) deployed benchmarker with S3 publishing, authentication, and CRIU-based process checkpointing for cache-free test isolation (~1s overhead per test).

### zkEVM

- Kev (@kevaundray) and Ignacio (@jsign) from the zkEVM team made significant contributions to execution-specs this month, driving improvements across the board. Big thanks to Kev and Ignacio!
- Guru's state tracker prototype completed and updated for Amsterdam/BALS compatibility. Architecture designed by Peter, implemented by Guru.
- Ignacio added zkEVM test fixture release support to the repo. First release is pending imminently.

### Priorities for Next Month

- Follow-up releases for [`bal-devnet-3`](https://notes.ethereum.org/@ethpandaops/bal-devnet-3) as needed.
- Begin `bal-devnet-4` preparation: Restore full static test coverage via the YAML-to-Python port, resolve BAL security check (EIP-7928), and integrate EIP-2780.
- Assist delivery of repricing benchmark data for state access EIPs using redesigned cold/warm methodology. Implement the [internal repricing tool](https://github.com/ethereum/execution-specs/pull/2331) for rapid gas cost iteration.
- Build and fill BAL-specific benchmark tests to measure client optimization impact under block-level access lists.

---

## Glamsterdam

### Specs and Tests

February was dominated by Amsterdam EIP implementation and the push toward [`bal-devnet-3`](https://notes.ethereum.org/@ethpandaops/bal-devnet-3). EIP-8037 consumed the most effort due to its fundamental change to gas accounting. By month's end, all EIP branches except 8037 were rebased and in good shape, with the [`bal-devnet-3`](https://notes.ethereum.org/@ethpandaops/bal-devnet-3) [test release shipping Feb 28](https://github.com/ethereum/execution-spec-tests/releases/tag/bal@v5.2.0).

Felix shipped the getBlobsV3 PR (reviewed by Dan).

**New implementation in February:**

- EIP-7976 — Floor Call Data Cost (Felix).
- EIP-7981 — Excess List Cost Increase (Felix).
- EIP-8037 — State Gas Reservoir (Spencer).
- EIP-7954 — Contract Size Increase (Rahul, Prototyping).
- EIP-7904 — Gas Cost Renaming (Carson).
- EIP-2780 — Variable Intrinsic Gas (Guru), not included in devnet-3, WIP.

**Finishing from January:**

- EIP-8024 — Encoding/Decoding Rules (Felix).

**Starting March:**

- EIP-8038 — State Access Gas (Dan).

**Block-Level Access Lists (Headliner)**

- Felipe developed BAL-specific benchmark tests covering pre-fetching and parallel execution scenarios, building on Jochem's (Prototyping) [initial PR](https://github.com/jochem-brouwer/execution-specs/pull/1) and iterating with ~20 review comments.
- A spec ambiguity was discovered in EIP-7928's security consideration: the check that rejects blocks when access list elements exceed a gas-derived threshold is unclear about "gas remaining" semantics. Empty blocks with system contract items trigger the exception at low gas limits. Three tests fail for early-implementing clients. Guru assigned to drive resolution with Toni (Prototyping, spec author).
- Guru flagged that EIP-2780 worsens worst-case BALS by reducing account access cost. Toni is investigating.
- Sam refactored and simplified the BALs implementation.

**[`bal-devnet-3`](https://notes.ethereum.org/@ethpandaops/bal-devnet-3) EIPs**

- **EIP-8037** (State Gas Reservoir): Spencer led implementation. This EIP splits transaction gas into compute and state paths with a reservoir mechanism, breaking most Frontier-through-Shanghai tests due to insufficient hardcoded gas limits. Spencer addressed Sam Wilson's 27-comment review, added state gas tracing, and built a script to auto-convert ~700 YAML static tests to Python (hasher-verified). A sub-call bug was found where reservoir gas returns zero. Raised at ACDT to flag the testing burden. Non-static tests resolved; static tests temporarily skipped for the devnet-3 release.
- **EIP-7976** (Floor Call Data Cost): Felix implemented with Toni's spec assistance. Toni wrote his own spec PR and was always available for questions. CI failures from hardcoded gas values in shared tests identified and fixed.
- **EIP-7981** (Excess List Cost Increase): Felix implemented; merged to EIP branch. Same hardcoded gas test issue as 7976 surfaced and addressed.
- **EIP-7954** (Contract Size Increase): Rahul (raxhvl, Prototyping) volunteered and implemented. A simple constants change where most tests auto-update via fork inheritance. Felipe reviewed and merged.
- **EIP-8024** (Encoding/Decoding Rules): Felix assessed as doable quickly. Picked up after 7981 merge, with Felipe assigned as reviewer.
- **EIP-8038** (State Access Gas): Reassigned from Spencer/Felipe to Dan after Spencer became overloaded with 8037 and Felipe went on PTO. Dan starting implementation in early March.
- **EIP-7904** (Gas Cost Renaming): Carson's work here fed directly into the repricing tool (see Gas Repricing below). A new tool to list mappings between gas constants, opcodes, and forks was also added.

**Postponed until devnet-4**

- **EIP-2780** (Variable Intrinsic Gas): Guru led with draft PR, basic tests, and legacy test fixes. Open spec questions about EIP-7702 and EIP-7928 interactions drove a clarification PR on the EIPs repo. Confirmed not required for [`bal-devnet-3`](https://notes.ethereum.org/@ethpandaops/bal-devnet-3) but will be ready for `bal-devnet-4`.

### Gas Repricing

Six repricing EIPs were targeted for February per Maria's (Robust Incentives Group) timeline. Four have open PRs (some merged), but EIP-8038 and EIP-7904 specs are still incomplete. The end-of-February deadline was acknowledged as impossible given [`bal-devnet-3`](https://notes.ethereum.org/@ethpandaops/bal-devnet-3) demands and has shifted to end of March, which now also includes block-level access list optimizations.

- Louis led coordination with the gaslighting committee through weekly calls. He completed refactoring all benchmark tests (stateful and compute) to use the bytecode gas calculator, a prerequisite for automated repricing.
- Spencer migrated existing benchmark tests to Mario's automatic bytecode gas cost calculator, using an LLM for refactoring and verifying correctness with the hasher tool.
- Carson completed gas constant renaming between forks.py and specs, which was the bottleneck for the repricing command. Also implemented the repricing mechanism on the test side.
- The team designed a repricing command workflow: a JSON config file at repo root that overrides gas constants at import time, enabling local repricing iteration without dirty commits. Mario created a GitHub issue documenting the design ([ethereum/execution-specs#2200](https://github.com/ethereum/execution-specs/issues/2200)). This machinery will be reused for zkEVM and stateless repricing rounds.
- Critical data collection gap identified: the cold-versus-warm benchmarking methodology was producing unreliable data because access-list-based warming does not work consistently across clients. The committee agreed on a new approach: warm via SLOAD/BALANCE in setup phase (for "cached" variant) and adopt "cached" vs. "non-cached" terminology to avoid confusion with EVM gas-accounting semantics. A coordination tracker for repricing tooling requirements was opened ([ethereum/execution-specs#2340](https://github.com/ethereum/execution-specs/issues/2340)) to define how tests express cache behavior to benchmarking tools.
- Account access and storage operation benchmarks (SLOAD/SSTORE) identified as the biggest bottleneck. Jochem (Prototyping) has PRs for storage operation benchmarks and will create another for account access. Tests must differentiate cached vs. non-cached scenarios and use deterministic bloated contract slots.

### Releases

#### Packages

- **BPO2 release**: PyPI release for the `ethereum-execution` package.

#### Test Vectors

- **Osaka benchmark release**: Published after resolving OOM issues that had blocked the build.
- [`bal-devnet-3`](https://notes.ethereum.org/@ethpandaops/bal-devnet-3) [test release shipped Feb 28](https://github.com/ethereum/execution-spec-tests/releases/tag/bal@v5.2.0) with ~700 static tests temporarily skipped pending the YAML-to-Python port (devnet-4). New EIPs included: EIP-7954 ([PR](https://github.com/ethereum/execution-specs/pull/2276)) and EIP-8037 ([PR](https://github.com/ethereum/execution-specs/pull/2363), [EIP change](https://github.com/ethereum/EIPs/pull/11328)).

**Fixture directory layout change** ([PR](https://github.com/ethereum/execution-specs/pull/2134)): Future execution-spec-tests fixture releases will follow a new directory layout (fixture formats themselves are unchanged). Previously, fixture JSON files accumulated test cases for every target fork in a single file, growing with each new fork. Fixtures are now split into per-fork sub-directories, keeping file sizes bounded and letting runners target exactly the fork they need. See the [ACDT announcement](https://github.com/ethereum/pm/issues/1948#issuecomment-3971527094) for details.

## Benchmarking (Scale the L1)

The benchmarking efforts made significant infrastructure progress this month. The release pipeline was stabilized after persistent OOM failures, benchmark artifact sizes were dramatically reduced, and Rafael's (PandaOps) benchmarker gained production-ready features including S3 publishing and process checkpointing.

- **Benchmark release stabilization**: The fill process had been failing ~300 tests before completion due to worker starvation on heavy parameterized tests. Felipe reduced max workers from 48 to 30 and added duration tracking. Dan discovered work-steal mode was not enabled and tested it successfully. Fill time dropped from a full day to ~3 hours.
- **Artifact size reduction**: One benchmark test file was 2 GB (down from 15 GB). Culprits identified: entire post-allocation and full transaction receipts were included unnecessarily. Both removed for benchmark tests. Dmytro (Nethermind) flagged that 31 GB of total artifacts came from essentially two tests, which Mario resolved in [ethereum/execution-specs#2226](https://github.com/ethereum/execution-specs/pull/2226) with feedback from Jochem.
- **Fixture directory restructuring**: Fixtures are now split into per-fork sub-directories, with benchmark fixtures additionally organized by gas limit and opcode count. See Releases section above ([PR](https://github.com/ethereum/execution-specs/pull/2134)).
- **Amsterdam benchmark filling**: Since evmone does not support Amsterdam, the team is migrating to Geth for benchmark filling. Spencer's opcode-count tracer PR merged into Geth. Felipe rebased onto Geth's BALS `bal-devnet-2` branch and added T8N serialization for the BALS format. This migration is still in progress.
- **Benchmarker infrastructure (Rafael, PandaOps)**: S3 bucket publishing for results, API authentication, and scheduled CI runs deployed. CRIU-based process checkpointing implemented for cache-free test isolation: takes a memory snapshot after client startup, restores for each test with ~1 second overhead. Tested on perfnet-2 and mainnet snapshots for all clients.
- **Stateful testing**: Mario wrote specs for a new stateful testing tool using `testing_buildBlock` against live clients.
- **Repricing benchmark pipeline (Kamil, Nethermind)**: Test generation now fully automated on CI. Benchmarks run 24/7 across four test sets (two networks, two test types), ~3 runs per day. Database restructured into separate tables per test type and network. ZFS support replacing OverlayFS to address disk space issues.
- **State Actor tool (Jochem, Prototyping)**: New tool to initialize clients with predetermined state via genesis, bypassing slow bloating. Supports Geth, Erigon, and partially Reth. Would solve the bottleneck where changing test requirements means re-bloating and taking new snapshots.

## Tooling and Libraries

The team shipped several improvements with measurable impact on developer velocity and CI performance.

- **Fill speed improvements (Felipe and Dan)**: Felipe greatly reduced `fill` test generation by fixing file locking, index generation, state route computation inefficiencies and other optimizations. Dan implemented transition tool call caching to avoid redundant calls. Combined; total fill speed more thaWn doubled.
- **EngineX fixture pre-alloc deduplication (Mario)**: Mario implemented account hashing/deduplication, reducing pre-allocated accounts from ~500K to ~50K by deduplicating accounts with identical initial state. Accounts are now deployed at the hash of their contents with a per-test salt for isolation. Applies to all test fillings.
- **Blob test explosion resolved (Dan)**: Amsterdam blob tests were generating 21,000 combinations. Dan's PR reduced total test count from ~110K to under 90K (a reduction of 20K+ tests).
- **Batch RPC requests (Mario)**: Post-state checking now sends storage checks as a single batch instead of thousands of individual requests, making execution much faster.
- **Static test auto-converter (Spencer)**: Claude-assisted script that converts YAML static tests to Python with EVM bytes/opcode translation, hasher verification, and filler verification. 700 files converted with hash match confirmed. Handed off to Leo for continuation.
- **PR review context-extraction script (Felix)**: Bash function using the GitHub API to extract all PR context (comments, quoted lines, suggestions) into a condensed JSON for LLM consumption.
- **CI failure analysis script (Felix)**: Script to help debug CI failures, shared with team.
- **PR review load-tracking script (Mario)**: Shows backlog of open PRs assigned to each team member for better review distribution.
- **Auto-merge on approval (Spencer)**: PR reviewed by Sam that enables auto-merge when approved and all CI passes.
- **EVM bytes improvement (Mario)**: Merged improvement to make EVM bytes more readable when porting static tests.
- **Reliable EELS Sync (Sam)**: Retry sync on server-side errors.
