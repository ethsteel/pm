# STEEL Team Recap September, 2025

TLDR:

- Fusaka hardening and testing continued.
- First EEST full releases for Osaka including all `GeneralStateTests` from ethereum/tests adhering to EIP-7825 Transaction Gas Limit Cap [v5.0.0](https://github.com/ethereum/execution-spec-tests/releases/tag/v5.0.0), [v5.1.0](https://github.com/ethereum/execution-spec-tests/releases/tag/v5.1.0) [v5.2.0](https://github.com/ethereum/execution-spec-tests/releases/tag/v5.2.0).
- [Glamsterdam](https://forkcast.org/upgrade/glamsterdam/) efforts ramped up with 2 [EIP-7928](https://forkcast.org/upgrade/glamsterdam/#eip-7928) Block-level Access Lists test vector [pre-releases](https://eest.ethereum.org/main/running_tests/releases/#pre-release-and-devnet-releases): [v1.0.0](https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v1.0.0), [v1.0.1](https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v1.0.1).
- Scale the L1: Bloatnet testing gained momentum [ethereum/execution-spec-tests#2090](https://github.com/ethereum/execution-spec-tests/pull/2090) and benchmarking infra improvements to abstract the tx gas limit and ease test case implementation [ethereum/execution-spec-tests#1945](https://github.com/ethereum/execution-spec-tests/pull/1945).
- [ethereum/py-evm](https://github.com/ethereum/py-evm) was [sunsetted](https://snakecharmers.ethereum.org/sunsetting-support-for-py-evm/).
- STEEL Team website launch: [steel.ethereum.foundation](https://steel.ethereum.foundation/home/main/).
- The Weld public announcement [via ACDE](https://www.youtube.com/live/wc40rKbl2LY?&t=2302) ([slides](https://notes.ethereum.org/@danceratopz/weld-announcement#/)), [via blog](https://steel.ethereum.foundation/blog/blog_posts/2025-09-11_weld-announcement/).
- STEEL's Discord server dedicated to team-internal and client team discussions reaches 44 members.
- Hive debugging session, [recording](https://drive.google.com/file/d/14EzwceHRmjVA8_bKW9cUmjDMofqzNUB6/view?usp=drive_web) and [notes](https://drive.google.com/file/d/14EzwceHRmjVA8_bKW9cUmjDMofqzNUB6/view?usp=drive_web).
- EEST's `execute` command session, [recording](https://drive.google.com/file/d/1UfX4rGds3tWfYGRbjbh5CcFZJuI8xnuu/view?usp=sharing) and [notes](https://docs.google.com/document/d/1ukyI0x95K-5p9-ymFID8rwuo66xZR2ehupbLrMRxlyU/edit?usp=sharing).

## Fusaka

- EEST command [`execute eth-config`](https://eest.ethereum.org/main/running_tests/execute/eth_config/) was used to [verify client release config for devnet-5](https://steel.ethereum.foundation/blog/blog_posts/2025-09-15_eth-config/) and Holesky (WIP) using `eth_config` JSON RPC from [EIP-7910](https://eips.ethereum.org/EIPS/eip-7910).
- The new EEST simulator [`consume sync`](https://eest.ethereum.org/main/running_tests/running/#sync) is now running in the Fusaka Hiveview CI dashboard. Currently used to verify correct verification of [EIP-7934, RLP Execution Block Size Limit](https://eips.ethereum.org/EIPS/eip-7934) during sync.

## The Weld™

## Glamsterdam

## Scale The L1

## Infra

## Sessions

- Hive debugging session: How to debug client test failures in hive locally, parse the client's logs, dos and don'ts when trying to fix on the side of tests, potential causes of common problems, and more! [Recording](https://drive.google.com/file/d/14EzwceHRmjVA8_bKW9cUmjDMofqzNUB6/view?usp=drive_web), [Notes](https://drive.google.com/file/d/14EzwceHRmjVA8_bKW9cUmjDMofqzNUB6/view?usp=drive_web).
- EEST's execute command overview: What's the `execute` command's purpose and how to use it. [Recording](https://drive.google.com/file/d/1UfX4rGds3tWfYGRbjbh5CcFZJuI8xnuu/view?usp=sharing), [Notes](https://docs.google.com/document/d/1ukyI0x95K-5p9-ymFID8rwuo66xZR2ehupbLrMRxlyU/edit?usp=sharing)