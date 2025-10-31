# STEEL Team Recap October 2025

TLDR:

- The Weld™ has been successfully completed.
- All testing source code from [ethereum/execution-spec-tests](https://github.com/ethereum/execution-spec-tests) has been moved into the [execution-specs](https://github.com/ethereum/execution-specs) repository.
- The [ethereum/execution-spec-tests](https://github.com/ethereum/execution-spec-tests) repository will still contain the filled test fixtures that the clients and Hive can directly consume, first in the form of releases, the way it has been in the past and in the same format, but later it will have branches that contain the test fixtures uncompressed, and with that the clients will be able to git-clone to obtain the consumable fixtures.
- Contributors for both specifications and tests should now commit into the [execution-specs](https://github.com/ethereum/execution-specs) repository. New EIPs can include their executable specifications and their respective tests in the same PRs and branches.

## The Weld™

Challenges:
- Coalesce both repos' tooling, ci-checks, workflows, was a major challenge due to small differences in their coding standards, which required multiple PRs to get fixed:
  - Enable ruff, mypy rules that were only enforced by EELS: [#2291](https://github.com/ethereum/execution-spec-tests/pull/2291), [#2290](https://github.com/ethereum/execution-spec-tests/pull/2290), [#2285](https://github.com/ethereum/execution-spec-tests/pull/2285), [#2281](https://github.com/ethereum/execution-spec-tests/pull/2281)
- Project organization required properly separating and packaging (1) Ethereum specification source code, (2) Ethereum specification tests, (3) testing infrastructure source code:
  - [#1633](https://github.com/ethereum/execution-specs/pull/1633), [#1449](https://github.com/ethereum/execution-specs/pull/1449)

What now works:
- Filling, executing, producing test releases is all now fully functional.
- Writing new tests is open for any external contributors: https://github.com/ethereum/execution-specs/tree/HEAD/tests

Remaining open tasks:
- Fix test reference documentation generation. For the time being, users can still refer to the previously generated documentation for reference: https://eest.ethereum.org/main/tests/
- CI workflows to provide up-to-date built fixtures in branches of the [ethereum/execution-spec-tests](https://github.com/ethereum/execution-spec-tests) repository.

## Fusaka

- Sync simulator has been fixed after being flaky in the past months through a series of PRs: [#2272](https://github.com/ethereum/execution-spec-tests/pull/2272), [#1670](https://github.com/ethereum/execution-specs/pull/1670)

## Glamsterdam

### Block-level Access Lists
- Kept up with breakout conversations by updating specs and test vectors for clients and cutting releases.
- New test releases: https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v1.2.0, https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v1.3.0
- Following release is expected to contain every `execution-specs` (prev. `execution-spec-tests`) test filled with BAL functionality enabled (previously they only contained targeted tests).
- Multiple test cases, fixes, and improvements added: [#2297](https://github.com/ethereum/execution-spec-tests/pull/2297), [#2293](https://github.com/ethereum/execution-spec-tests/pull/2293), [#2280](https://github.com/ethereum/execution-spec-tests/pull/2280), [#2212](https://github.com/ethereum/execution-spec-tests/pull/2212)

## Consensus Specs

- Progress has been made in pytest-ifying the vector generation process, with a prototype now available: https://github.com/ethereum/consensus-specs/pull/4709. This helps to align the way all specification repos work when they generate tests for client implementations to consume.

## Benchmarking Support

- Released benchmark@v0.0.5 using this new release method: https://github.com/ethereum/execution-spec-tests/releases/tag/benchmark%40v0.0.5
- Updated most tests to use the new benchmarking wrapper (which should be used by all new benchmark tests): https://github.com/ethereum/execution-spec-tests/pull/2160, [#1708](https://github.com/ethereum/execution-specs/pull/1708)
- Reorganization of the benchmark folder for client benchmarkings to be more clear: [#1681](https://github.com/ethereum/execution-specs/pull/1681)
- Carlos from the stateless team contributed to benchmarking tests targeted to aid benchmarking the stateless efforts: [#1697](https://github.com/ethereum/execution-specs/pull/1697)

## Infra

- Updated our full and feature release workflow to publish test fixture releases to EEST from EELS as part of the Weld: https://github.com/ethereum/execution-specs/pull/1608
- Kamil from Nethermind implemented a new feature for `execute` to make tx poll intervals configurable: [#2286](https://github.com/ethereum/execution-spec-tests/pull/2286)

## Hive

- Consolidated on remaining Fusaka EEST hive failures, fixing consume sync and adding ethrex as a client: https://hive.ethpandaops.io/#/group/fusaka
- Created a BAL hive workflow: https://hive.ethpandaops.io/#/group/bal

## Comms

- The STEEL Discord server has now incorporated channels with every EL+CL team to help coalesce all comms between testing teams (ethpandaops+steel) and the clients into a single place (instead of multiple Telegram channels or Discord chat groups).

## Sessions

No sessions this month due to the amount of work that the Weld required.
