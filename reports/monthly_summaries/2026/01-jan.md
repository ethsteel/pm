# STEEL Team Recap January 2026

## TLDR

### Glamsterdam

- Completed EIP complexity assignments to help evaluate EIP CFI status.
- The BAL dev branch ([`eips/amsterdam/eip-7928`](https://github.com/ethereum/execution-specs/commits/eips/amsterdam/eip-7928/)) was [merged into the main `forks/amsterdam` branch](https://github.com/ethereum/execution-specs/pull/1719); specs and tests continue to be refined and extended.
- Added spec implementations and test coverage for the EIPs scoped for [bal-devnet-2](https://notes.ethereum.org/@ethpandaops/bal-devnet-2): [EIP-7778](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7778.md), [EIP-7708](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7708.md), [EIP-7843](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7843.md) and [EIP-8024](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-8024.md).
- Released 5 test vector updates for client teams; as of [bal@v4.0.0](https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v4.0.0) these target the full [bal-devnet-2](https://notes.ethereum.org/@ethpandaops/bal-devnet-2) spec.
- Client support: STEEL contributed a [SELFDESTRUCT OOG fix for Nethermind](https://github.com/NethermindEth/nethermind/pull/10064) and the [Amsterdam instruction set to Geth](https://github.com/ethereum/go-ethereum/pull/33643) to facilitate testing.

### Scale the L1

- Significant improvements added for the gas benchmarking infrastructure, including:
  - Added opcode counting verification in the test framework and CI to help validate benchmark test correctness.
  - Improved gas accounting infrastructure to greatly reduce implementation burden for test writers.

### zkEVM

- Started work on an improved state tracking implementation in EELS, which is a prerequisite to prototype the Execution Witness.

### "New" Team Member

- As of 1st January, [@LouisTsai-Csie](https://github.com/LouisTsai-Csie) (officially) joins the team full-time! Louis has contributed to and driven STEEL's benchmarking efforts since June 2025.
- This month, Louis started facilitating the weekly Gas-Lighting Committee Call that coordinates Glamsterdam Gas Repricing and Benchmarking efforts between research and client teams!

### Priorities for the next month

- Glamsterdam bal-devnet-2 releases and client support.
- Supporting Benchmarking and Gas-Repricing efforts.

## Glamsterdam

### Specs and Tests

Initial implementations and test coverage for the Execution-Layer EIPs included in `bal-devnet-2`:

- [ethereum/execution-specs#1719](https://github.com/ethereum/execution-specs/pull/1719): feat(specs,tests): Implement EIP-7928 Block-Level Access Lists.
- [ethereum/execution-specs#2023](https://github.com/ethereum/execution-specs/pull/2023): feat(spec-specs): EIP-7708 ETH Transfers Emit a Log.
- [ethereum/execution-specs#2074](https://github.com/ethereum/execution-specs/pull/2074): feat(spec-tests): Add EIP-7778 tests with multiple refund types.
- [ethereum/execution-specs#2007](https://github.com/ethereum/execution-specs/pull/2007): feat(src): EIP-7843 (SLOTNUM).

Additionally:

- [ethereum/consensus-specs#4696](https://github.com/ethereum/consensus-specs/pull/4696): Add tests for `get_validators_custody_requirement`.
- [ethereum/consensus-specs#4810](https://github.com/ethereum/consensus-specs/pull/4810) and [ethereum/consensus-specs#4830](https://github.com/ethereum/consensus-specs/pull/4830): Implement test_process_withdrawal for Gloas.
- Refactored EIP-7928 (BALs) net-zero filtering implementation.
- Enabled EIP-7934 tests to run with BAL releases.
- Client support: STEEL contributed a [SELFDESTRUCT OOG fix for Nethermind](https://github.com/NethermindEth/nethermind/pull/10064) and the [Amsterdam instruction set to Geth](https://github.com/ethereum/go-ethereum/pull/33643) to facilitate testing.

### Test Vector Releases

Continued BAL devnet and bal-devnet-2 releases ([bal@v2.0.0](https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v2.0.0), [bal@v3.0.0](https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v3.0.0), [bal@v3.0.1](https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v3.0.1), [bal@v4.0.0](https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v4.0.0), [bal@v5.0.0](https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v5.0.0)):

- [bal@v4.0.0](https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v4.0.0) (and newer) target the evolving bal-devnet-2 spec that includes EIP-7928, EIP-7708, EIP-7778, EIP-7843, EIP-8024.
- Releases will be continuously deployed as specs are updated and test coverage increases.

## Benchmarking (Scale the L1)

TLDR:

- Extended gas benchmark suite with precompile counting, fuzzy-compute configs, and worst-case trie depth attacks.
- Fixed gas constant calculations across multiple benchmark tests.
- Significant infra improvements that assist test implementation and verification.

### Infra

Major CI infrastructure improvements: benchmark workflows, hive-consume rate limiting, devnet workflows.

- [ethereum/execution-specs#1853](https://github.com/ethereum/execution-specs/pull/1853): enhance(ci): improve benchmark workflows (adds continuous test vector artifact deployment).
- [ethereum/execution-specs#1869](https://github.com/ethereum/execution-specs/pull/1869): feat(test-benchmark): implement opcode count verification (for test verification).
- [ethereum/execution-specs#1934](https://github.com/ethereum/execution-specs/pull/1934): feat(test-execute): Implement `pre.deterministic_deploy_contract`.
- [ethereum/execution-specs#2002](https://github.com/ethereum/execution-specs/pull/2002): feat(testing/forks): Implement bytecode.gas_cost(fork) (gas accounting helper).
- [ethereum/execution-specs#1996](https://github.com/ethereum/execution-specs/pull/1996): feat(test-benchmark): Introduce create2 helper for address computation.
- [ethereum/execution-specs#1907](https://github.com/ethereum/execution-specs/pull/1907): feat(test-execute): tx batching for execute remote.

## Tooling and Libraries

- [Reduced test vector generation](https://github.com/ethereum/execution-specs/pull/2079) (`fill` runtime) by ~35% in CI!
- Fixed Hive BPO defaults configuration.

## Comms & Community

- Contributed to EIPs/ERCs process improvements.
