# STEEL Team Recap November 2025

TLDR:

- 🎉 7 STEEL team members happily hacked and enjoyed time together at Devconnect ARG: @marioevz, @fselmo, @gurukamath, @klcowes, @leolara, @LouisTsai-Csie, @danceratopz.
- 🚀 6 EIP-7928 Block-level Access client test releases due to fast iterations on specs and tests by @fselmo, @nerolation and @raxhvl.
- 📊 1 Benchmarking release, @LouisTsai-Csie.
- 🔥 Gas repricing efforts ramped up! @LouisTsai-Csie.
- 🧩 Glamsterdam PFI'd EIP complexity evaluations: [ethsteel/pm#7](https://github.com/ethsteel/pm/issues/7).
- 🛠️ Fusaka mainnet live on-chain testing preparations @felix314159, @spencer-tb.
- 📝 2 blog posts:
  - 🏗️ "The Weld is Complete" by @gurukamath.
  - 🧪 (WIP) "Osaka Mainnet Testing" by @felix314159.
- 🎤 Devconnect talk: "Code is Law: Avoiding Spec-ulation for Faster Forks" at the EIP Summit by @danceratopz and @raxhvl, [slides](https://docs.google.com/presentation/d/1IBBfYqNlkE7r3YBWrQr9MZaN4SUfvaOX-mjeZ4Y4h_k/edit?usp=sharing), [recording](https://www.youtube.com/watch?v=3mU5r4LW_ik).
- 🌐 Team website makeover: [steel.ethereum.foundation](https://steel.ethereum.foundation/), @danceratopz.

- ⚡ Test infra optimization efforts started to increase Benchmarking release frequency as requested by @kamilchodola, Nethermind.

**Note:** Many contributions below were made by external contributors, including EFers from the Prototyping, Stateless Consensus Team.

## Fusaka

- **[WIP]** ethereum/execution-specs#1806: Add mainnet tests for Osaka. @felix314159 - Preparation for Fusaka mainnet on-chain testing (as [done for Prague](https://notes.ethereum.org/@marioevz/pectra-mainnet-testing))..
- ethereum/execution-specs#1752: Added Osaka mainnet configuration info to the specs, @SamWilsn.
- ethereum/execution-specs#1789: Create blob parameter-only hardforks on the fly, @SamWilsn.

## Glamsterdam

### Block-level Access Lists

- ethereum/execution-specs#1737: Removed BAL checks in Osaka fork; opted for the EIP-7928 branch approach for block access list handling, @fselmo.
- ethereum/execution-specs#1743: Fixed early issues from the BALs release v1.4.0 — addressed specification bugs discovered shortly after the block access list release, @fselmo.
- ethereum/execution-specs#1759: EIP-7928 larger refactoring — moved the state tracker into the block environment and introduced proper check-gas/charge-gas sequencing. Ensures account access costs are charged before marking accounts as accessed, @nerolation.
- ethereum/execution-specs#1809: Added BAL exception mapping for Erigon client, @felix314159.
- ethereum/execution-specs#1742: Refactored test types to always validate t8n BAL (block access list) if present. Separates static validation checks from expectation validation, catching duplicate entries during test filling, @fselmo.
- **[WIP]** ethereum/execution-specs#1751: Split `charge_gas` around account access in specs, @fselmo.
- **[WIP]** ethereum/execution-specs#1815: Add more EIP-7928 test descriptions, @nerolation.
- **[WIP]** ethereum/execution-specs#1812: Add BAL test cases, @qu0b.

BAL releases:

- [bal@v1.8.0](https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v1.8.0) (Nov 25) — Front-loads more static gas checks in call opcodes ahead of state access; removes named forks from `blobSchedule` in hive config.
- [bal@v1.7.0](https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v1.7.0) (Nov 22)
- [bal@v1.6.0](https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v1.6.0) (Nov 17)
- [bal@v1.5.0](https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v1.5.0) (Nov 13)
- [bal@v1.4.1](https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v1.4.1) (Nov 12)
- [bal@v1.4.0](https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v1.4.0) (Nov 3)

### Gas Repricing

- **[WIP]** ethereum/execution-specs#1748: Implement EIP-7904 gas repricing in specs and tests, @LouisTsai-Csie.
- **[WIP]** ethereum/execution-specs#1785: Define reference test for gas repricing, @LouisTsai-Csie.
- **[WIP]** ethereum/execution-specs#1776: Unify gas cost variable across tests, @LouisTsai-Csie.
- **[WIP]** ethereum/execution-specs#1810: Refactor repricing filter logic, @LouisTsai-Csie.
- **[WIP]** ethereum/execution-specs#1769: Add gas-repricings SLOAD tests, @jochem-brouwer.
- **[WIP]** ethereum/execution-specs#1738: Tests for ecadd/ecmul/ecpairing constant gas repricing, @pdobacz.

## Benchmarking Support

- ethereum/execution-specs#1747: Added support for `--fixed-opcode-count` flag and corresponding tests - enables running benchmarks with a fixed number of opcode executions, @LouisTsai-Csie.
- ethereum/execution-specs#1768: Added missing benchmark scenarios and optimizations, @LouisTsai-Csie.
- ethereum/execution-specs#1767: Updated docstrings for supported benchmark operations, @LouisTsai-Csie.
- ethereum/execution-specs#1770: Fixed benchmark gas limit configuration, @LouisTsai-Csie.
- ethereum/execution-specs#1771: Added setup and execution transaction labels to benchmarks for better categorization, @LouisTsai-Csie.
- ethereum/execution-specs#1780: Fixed failing benchmark test cases, @LouisTsai-Csie.
- ethereum/execution-specs#1791: Skipped benchmark `test_blockhash` temporarily due to issues (marked urgent), @marioevz.
- ethereum/execution-specs#1799: Separated BLOCKHASH into its own pre-alloc group to avoid benchmark interference, @LouisTsai-Csie.
- ethereum/execution-specs#1700: Updated benchmark wrapper for execute mode compatibility, @LouisTsai-Csie.
- ethereum/execution-specs#1800: Fixed benchmark genesis generation in GitHub Actions, @marioevz.
- ethereum/execution-specs#1794: Added more SLOAD/SSTORE combination tests for gas repricing analysis, @jochem-brouwer.
- ethereum/execution-specs#1778: Generate genesis files for benchmark releases automatically in CI, @danceratopz, @marioevz.
- **[WIP]** ethereum/execution-specs#1790: Use config file for fixed opcode count scenarios, @spencer-tb.
- **[WIP]** ethereum/execution-specs#1787: Optimize benchmark cases, @LouisTsai-Csie.
- **[WIP]** ethereum/execution-specs#1784: Add benchmark test & layout for MLOAD & MSTORE, @gitToki.
- **[WIP]** ethereum/execution-specs#1774: Add extra SSTORE benchmark cases, @LouisTsai-Csie.
- **[WIP]** ethereum/execution-specs#1734: Add vector storage benchmarks for EVM storage operations, @CPerezz.
- **[WIP]** ethereum/execution-specs#1766: Add XEN tests, @jochem-brouwer.

Releases:

- [benchmark@v0.0.6](https://github.com/ethereum/execution-spec-tests/releases/tag/benchmark%40v0.0.6) (Nov 12) — Additional SLOAD/SSTORE cases, folder restructuring, doc string updates, and execute mode wrapper fixes. Includes genesis file.

## Consensus Specs

- **WIP** ethereum/consensus-specs#4709, Prototype of generating vectors from pytest, @leolara.

## Tests

- ethereum/execution-specs#1702: Additional tests for header validation rules, @pdobacz.
- ethereum/execution-specs#1728: Added opcode tests for stack overflow and BLOCKHASH edge cases, @pdobacz.
- ethereum/execution-specs#1729: Improved modexp tests — covers more widths and parities of moduli, @pdobacz.
- ethereum/execution-specs#1731: Added tests checking that minimum gas limit (5000) is validated, @pdobacz.
- ethereum/execution-specs#1736: Added tests for zero gasprice transactions vs account touch behavior, @pdobacz.
- ethereum/execution-specs#1746: Added test for bad withdrawals root validation, @pdobacz.
- ethereum/execution-specs#1754: Added tests verifying typed transactions are invalid and void before their fork, @pdobacz.
- **[WIP]** ethereum/execution-specs#1781: Tests for even modexp with long trailing zeros, @chfast.
- **[WIP]** ethereum/execution-specs#1732: Add a case for RIPEMD OOGing in early forks, @pdobacz.

## Infra

- Reducing execution-specs CI workflow times for smoother devex, @gurukamath, @kclowes, @marioevz.
- **[WIP]** ethereum/execution-specs#1811: Blob sender plugin for execute command, @felix314159.
- **[WIP]** ethereum/execution-specs#1804: Optimize fill performance. @marioevz - Efforts to optimize the `fill` tool started to increase the frequency of benchmark tests, following a request from Nethermind and Camille at Devconnect ARG track.

## Hive

- **WIP** danceratopz/execution-specs#1 `enginex` - a new Hive simulator for much faster test execution.

## Comms

- The STEEL website got a new look [steel.ethereum.foundation](https://steel.ethereum.foundation/).
- Blog posts:
  - [The Weld is Complete](https://steel.ethereum.foundation/blog/2025-11-04_weld_final/) by @gurukamath.
  - **WIP** [Osaka Mainnet Testing](https://steel.ethereum.foundation/blog/2025-11-27_osaka_mainnet_tests/) by @felix314159.

## Sessions/Talks

- "Code is Law: Avoiding Spec-ulation for Faster Forks" at the [EIP Summit](https://luma.com/5lwboseu) by @danceratopz and @raxhvl (Prototyping): Dan and Rahul brainstormed at Devconnect and came up with an idea to make designated "executable spec reviewers" the CODEOWNERS of an SFI'd EIP's markdown in ethereum/EIPs (instead of the authors) in order to enforce a tighter coupling between the markdown and executable specs, [slides](https://docs.google.com/presentation/d/1IBBfYqNlkE7r3YBWrQr9MZaN4SUfvaOX-mjeZ4Y4h_k/edit?usp=sharing), [recording](https://www.youtube.com/watch?v=3mU5r4LW_ik).
