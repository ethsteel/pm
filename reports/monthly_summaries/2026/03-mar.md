# STEEL Team Recap March 2026

This summary was AI assisted 🤖

## TLDR

March focused on advancing Glamsterdam/BAL devnet readiness, with focus on partial EIP-8037 due to inclusion in Devnet-3, and planning on full EIP-8037 for Devnet-4, static test porting, and benchmarking infrastructure. BAL Devnet-3 is near completion, block building testing was scoped, and the team made meaningful tooling improvements across the board.

### Glamsterdam

- EIP-8037 spec aligned with gas repricing changes ([#2526](https://github.com/ethereum/execution-specs/pull/2526), [#2583](https://github.com/ethereum/execution-specs/pull/2583)); devnet 3 preliminary release with a subset of tests done
- EIP-8038/EIP-2780 ([#2175](https://github.com/ethereum/execution-specs/pull/2175)) implementation advanced and under review to get ahead of potential inclusion in Devnet-4 or beyond
- Static test porting nearly complete via Leo's automated conversion script ([#2563](https://github.com/ethereum/execution-specs/pull/2563))

### Scale the L1

- Amsterdam benchmarks running on updated branches
- Stateful benchmark infrastructure progressed; payload generation underway for Osaka
- Block building benchmarking scoped and assigned to Felipe

### zkEVM

- Guru noted ZKEVM project tracking with current dependencies completed, but further STEEL team involvement expected
- By Ignacio: Witness state validation hardened for malformed trie proofs ([#2589](https://github.com/ethereum/execution-specs/pull/2589)); delayed `get_code` calls in CALL-like opcodes in progress ([#2473](https://github.com/ethereum/execution-specs/pull/2473))

### Priorities for Next Month

- Increase BAL Devnet-3 test coverage and begin BAL Devnet 4 release planning: Full EIP-8037, with potentially EIP-2780 + EIP-8037
- Complete block building correctness testing proof of concept
- Finalize benchmark payloads and unblock Rafael's benchmarker image swap

---

## Glamsterdam

### Specs and Tests

**New implementations in March:**

- EIP-8037: Gas repricing spec changes aligned; Spencer raising PRs ([#2526](https://github.com/ethereum/execution-specs/pull/2526), [#2583](https://github.com/ethereum/execution-specs/pull/2583)) to EIP branch; 2D block gas validity tests added ([#2581](https://github.com/ethereum/execution-specs/pull/2581)); static tests being ported and updated ([#2563](https://github.com/ethereum/execution-specs/pull/2563))
- EIP-7928: Worst-case BAL read test added ([#2033](https://github.com/ethereum/execution-specs/pull/2033))
- Post-state verification added to static test fixtures, fixing absent account validation

**Devnet EIPs**

- Devnet-3: Client status mixed, with Geth/Besu/Nimbus/Erigon passing most tests. Geth exception mapper updated ([#2575](https://github.com/ethereum/execution-specs/pull/2575)); reth exception mappings in progress ([#2574](https://github.com/ethereum/execution-specs/pull/2574)). Static tests were the main blocker; Leo's porting script ([#2563](https://github.com/ethereum/execution-specs/pull/2563)) provided meaningful progress although manual fixes are still required for EIP-8037. Additional static test ports in progress ([#2481](https://github.com/ethereum/execution-specs/pull/2481), [#2388](https://github.com/ethereum/execution-specs/pull/2388))
- Devnet-4 candidates: Full EIP-8037 testing updates planned, with the door open to also include EIP-8038 and EIP-2780 ([#2175](https://github.com/ethereum/execution-specs/pull/2175))
- Proposal raised to update Devnet EIPs to SFI status in EIPs repo, needs ACD-E discussion
- 21,000 gas minimum for execute raised by EIP-8037; default bumped to ~200,000 as interim fix, but plan for a more durable solution ongoing

### Releases

#### Test Vectors

##### bal-devnet-3

- [bal@v5.3.0](https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v5.3.0)
- [bal@v5.4.0](https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v5.4.0)
- [bal@v5.5.0](https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v5.5.0)
- [bal@v5.5.1](https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v5.5.1)

## Hegota

### Specs and Tests

- Inclusion Lists (EIP-7805): Testing strategy scoped with Jihoon: blockchain test format extension, transition tool modifications, and new Hive simulator identified as needed

---

## Benchmarking (Scale the L1)

- Account access benchmark nearly complete; storage operations PR ([#2400](https://github.com/ethereum/execution-specs/pull/2400)) the last remaining item; uncacheable precompile benchmark in progress ([#2600](https://github.com/ethereum/execution-specs/pull/2600)); BAL contract chase benchmark in progress ([#2588](https://github.com/ethereum/execution-specs/pull/2588))
- Stateful benchmark infrastructure: Louis working on stub files, address stub CLI parameters ([#2512](https://github.com/ethereum/execution-specs/pull/2512)), and private key inclusion. Additional benchmark improvements by Louis: repricing marker support ([#2430](https://github.com/ethereum/execution-specs/pull/2430)), test collection refactor to use testpath ([#2496](https://github.com/ethereum/execution-specs/pull/2496)), transaction status verification ([#2527](https://github.com/ethereum/execution-specs/pull/2527)), precompile cache fix ([#2415](https://github.com/ethereum/execution-specs/pull/2415)), SSTORE benchmark fix ([#2487](https://github.com/ethereum/execution-specs/pull/2487)), and `target_opcode` metadata in test fixtures ([#2520](https://github.com/ethereum/execution-specs/pull/2520))
- Block building benchmark scoped: two-tier approach (consensus correctness + performance benchmarking), [#2560](https://github.com/ethereum/execution-specs/issues/2560)
- Execute speed optimization: Mario reduced deterministic address contract deployment from 2 minutes to 20 seconds via batched RPC queries; execute remote unit tests added ([#2485](https://github.com/ethereum/execution-specs/pull/2485))
- Genesis config standardization: Rahul's extract config PR ([#2511](https://github.com/ethereum/execution-specs/pull/2511)) creates common genesis interface for benchmarker and hive

### Gas Repricing

- Carson's PR sequence for gas constant unification ([#2383](https://github.com/ethereum/execution-specs/pull/2383), [#2396](https://github.com/ethereum/execution-specs/pull/2396)) merged/in progress. Affects ~250 files, enables easier gas repricing test filling

---

## Tooling and Libraries

- **Fork architecture refactoring**: Mario's EIP splitting of `forks.py` PR ([#2571](https://github.com/ethereum/execution-specs/pull/2571)); reduces rebase conflicts to single-line resolution
- **Python devnet workflow**: Felix developed single-command local branch creation with selective EIP inclusion, eliminating GitHub Actions dependency; CLI flag rename (`--bin` to `--evm-bin`) in progress ([#2548](https://github.com/ethereum/execution-specs/pull/2548))
- **Build system proposal**: Dan implemented switching from `tox` to `just` ([#2555](https://github.com/ethereum/execution-specs/pull/2555)) for better CLI ergonomics and argument pass-through
- **Stale PR management**: Auto-labeling issues/PRs as "stale" after 60 days merged ([#2408](https://github.com/ethereum/execution-specs/pull/2408)); auto-close rejected due to contributor concerns ([#2470](https://github.com/ethereum/execution-specs/pull/2470))
- **CI improvements**: Spencer fixed 40+ red merge commits on flux amsterdam ([#2072](https://github.com/ethereum/execution-specs/pull/2072)); added caching ([#2546](https://github.com/ethereum/execution-specs/pull/2546)) and parallel fork-range runners ([#2529](https://github.com/ethereum/execution-specs/pull/2529)) to address 3x slowdown from static test port
- **PyPy support maintained**: PyPy 7.9 is 2x faster than CPython 3.14 for Frontier sync; CI tests reduced to minimized set ([#2482](https://github.com/ethereum/execution-specs/pull/2482))