# Execution Layer Fusaka Mainnet Testing

## Summary

- Test transactions will be sent to mainnet for each EIP using [EELS's `execute remote` command](https://eest.ethereum.org/main/running_tests/execute/remote/), with the exception of the EIPs in the next bullet point.
- Approximately ~0.0001 Eth gas required for these tests.

## EIPs

### Included

- EIP-7823: Set upper bounds for MODEXP
- EIP-7825: Transaction Gas Limit Cap
- EIP-7883: ModExp Gas Cost Increase
- EIP-7910: eth_config JSON-RPC Method
- EIP-7939: Count leading zeros (CLZ) opcode
- EIP-7951: Precompile for secp256r1 Curve Support

### Excluded

- EIP-7594: PeerDAS

Networking related, not testable via EL transactions.

- EIP-7642: eth/69

Networking related, not testable via EL transactions.

- EIP-7892: Blob Parameter Only ('BPO') Hardforks

Requires many blob transactions included in the same block, not easily achievable via `execute` command.

- EIP-7917: Deterministic proposer lookahead

CL only change.

- EIP-7918: Blob base fee bounded by execution cost

Environment dependent, not testable via `execute` command.

- EIP-7934: RLP Execution Block Size Limit

Environment dependent, not testable via `execute` command.

- EIP-7935: Set default gas limit to 60M

Environment dependent, not testable via `execute` command.

## Schedule

- Fork Epoch: 411392 (Dec-03-2025 09:49:11 PM)
- Fork Expected Finalization Epoch: 411394 (Dec-03-2025 10:01:59 PM)
- Testing will commence at the fork finalization epoch when the chain finalizes successfully without intervention.

## Test Spec

#### EELS Commit

https://github.com/ethereum/execution-specs/commit/2b7dc12d89bc9daa45a0737ab36c14fe55eaad5b

### - EIP-7823: Set upper bounds for MODEXP

#### Description

Execute pre-compile at the exact boundary and above the boundary.

#### Command

```
uv run execute remote --fork=Osaka -m mainnet tests/osaka/eip7823_modexp_upper_bounds/test_eip_mainnet.py --rpc-seed-key $MAINNET_RPC_SEED_KEY --rpc-endpoint $MAINNET_RPC_ENDPOINT --chain-id $MAINNET_CHAIN_ID
```

#### Transaction Hashes

- `test_modexp_boundary[fork_Osaka-state_test-base-boundary-1024-bytes]`: [0x5be8356abea4466ad03a1821d34b437b0b45e1b38c03b09cc545ddb36a0548b1](https://etherscan.io/tx/0x5be8356abea4466ad03a1821d34b437b0b45e1b38c03b09cc545ddb36a0548b1)
- `test_modexp_over_boundary[fork_Osaka-state_test-base-over-boundary-1025-bytes]`: [0x1eaf26a250f50411888a11d227dbdfeecb51a273613cac9a9fa097b64b102b0f](https://etherscan.io/tx/0x1eaf26a250f50411888a11d227dbdfeecb51a273613cac9a9fa097b64b102b0f)
        
#### Outcome

✅ PASS

```
================================================================================================ test session starts =================================================================================================
platform linux -- Python 3.11.2, pytest-8.4.2, pluggy-1.6.0
Generating fixtures for: Osaka
Start seed for EOA: 0x384b848c34a36cd05735668f429cfc5311aa53058a5c51467b14505bb15969d
Log file: logs/execute-remote-20251203-220332-main.log
rootdir: /home/marioevz/Development/Eth/execution-specs
configfile: packages/testing/src/execution_testing/cli/pytest_commands/pytest_ini_files/pytest-execute.ini
plugins: regex-0.2.0, custom-report-1.0.1, cov-4.1.0, metadata-3.1.1, xdist-3.8.0, html-4.1.1, json-report-1.5.0
collecting ...  pytest-regex selected 2 tests to run for regex: .*
collected 2 items

tests/osaka/eip7823_modexp_upper_bounds/test_eip_mainnet.py ..                                                                                                                                                  [2/2]

================================================================================================== warnings summary ==================================================================================================
.venv/lib/python3.11/site-packages/_pytest/config/__init__.py:812
  /home/marioevz/Development/Eth/execution-specs/.venv/lib/python3.11/site-packages/_pytest/config/__init__.py:812: PytestAssertRewriteWarning: Module already imported so cannot be rewritten; execution_testing.cli.pytest_commands.plugins.shared.execute_fill
    self.import_plugin(arg, consider_entry_points=True)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
------------------------------------------------------- Log file: /home/marioevz/Development/Eth/execution-specs/logs/execute-remote-20251203-220332-main.log --------------------------------------------------------
====================================================================================== 2 passed, 1 warning in 165.43s (0:02:45) ======================================================================================
```

### - EIP-7825: Transaction Gas Limit Cap

#### Description

Send a transaction with the gas limit cap and above.

#### Command

```
uv run execute remote --fork=Osaka -m mainnet tests/osaka/eip7825_transaction_gas_limit_cap/test_eip_mainnet.py --rpc-seed-key $MAINNET_RPC_SEED_KEY --rpc-endpoint $MAINNET_RPC_ENDPOINT --chain-id $MAINNET_CHAIN_ID
```

#### Transaction Hashes

`test_tx_gas_limit_cap_at_maximum[fork_Osaka-state_test]`: [0x952750833f1dab54ea088dc936f37c6064c0fb3678985d4351f17cca9b0c5ece](https://etherscan.io/tx/0x952750833f1dab54ea088dc936f37c6064c0fb3678985d4351f17cca9b0c5ece)
`test_tx_gas_limit_cap_exceeded[fork_Osaka-state_test]`: No direct transaction executed (expected), accound funding[0xc5ac11315053776ac903235ef71f97deabe4ae9d5a4bd18b645e97699ecec2f6](https://etherscan.io/tx/0xc5ac11315053776ac903235ef71f97deabe4ae9d5a4bd18b645e97699ecec2f6), acccount refund after no tx execution [0x46d32a995a7934d268bc264c7a6e1c15308a73a07cc7c12e50a9ed21a383941b](https://etherscan.io/tx/0x46d32a995a7934d268bc264c7a6e1c15308a73a07cc7c12e50a9ed21a383941b)

#### Outcome

✅ PASS

<!-- Summary of the command output. -->
```
================================================================================================ test session starts =================================================================================================
platform linux -- Python 3.11.2, pytest-8.4.2, pluggy-1.6.0 -- /home/marioevz/Development/Eth/execution-specs/.venv/bin/python3
Generating fixtures for: Osaka
Start seed for EOA: 0xb4ae073b73d321e92255a8b83fa8ffe18ffc65d4dc01fd066f89cc9af3bfa05e
cachedir: .pytest_cache
Log file: logs/execute-remote-20251203-220718-main.log
metadata: {'Python': '3.11.2', 'Platform': 'Linux-6.1.0-41-cloud-amd64-x86_64-with-glibc2.36', 'Packages': {'pytest': '8.4.2', 'pluggy': '1.6.0'}, 'Plugins': {'regex': '0.2.0', 'custom-report': '1.0.1', 'cov': '4.1.0', 'metadata': '3.1.1', 'xdist': '3.8.0', 'html': '4.1.1', 'json-report': '1.5.0'}, 'Command-line args': '<code>execute -c /home/marioevz/Development/Eth/execution-specs/packages/testing/src/execution_testing/cli/pytest_commands/pytest_ini_files/pytest-execute.ini --rootdir . --fork=Osaka -m mainnet tests/osaka/eip7825_transaction_gas_limit_cap/test_eip_mainnet.py --rpc-seed-key ** --rpc-endpoint ** --chain-id 1 -vv</code>', 'Senders': {}}
rootdir: /home/marioevz/Development/Eth/execution-specs
configfile: packages/testing/src/execution_testing/cli/pytest_commands/pytest_ini_files/pytest-execute.ini
plugins: regex-0.2.0, custom-report-1.0.1, cov-4.1.0, metadata-3.1.1, xdist-3.8.0, html-4.1.1, json-report-1.5.0
collecting ...  pytest-regex selected 2 tests to run for regex: .*
collected 2 items

tests/osaka/eip7825_transaction_gas_limit_cap/test_eip_mainnet.py::test_tx_gas_limit_cap_at_maximum[fork_Osaka-state_test] PASSED                                                                               [1/2]
tests/osaka/eip7825_transaction_gas_limit_cap/test_eip_mainnet.py::test_tx_gas_limit_cap_exceeded[fork_Osaka-state_test] PASSED                                                                                 [2/2]

================================================================================================== warnings summary ==================================================================================================
.venv/lib/python3.11/site-packages/_pytest/config/__init__.py:812
  /home/marioevz/Development/Eth/execution-specs/.venv/lib/python3.11/site-packages/_pytest/config/__init__.py:812: PytestAssertRewriteWarning: Module already imported so cannot be rewritten; execution_testing.cli.pytest_commands.plugins.shared.execute_fill
    self.import_plugin(arg, consider_entry_points=True)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
------------------------------------------------------- Log file: /home/marioevz/Development/Eth/execution-specs/logs/execute-remote-20251203-220718-main.log --------------------------------------------------------
====================================================================================== 2 passed, 1 warning in 72.24s (0:01:12) =======================================================================================
```

<!-- Details if necessary. -->

### - EIP-7883: ModExp Gas Cost Increase

#### Description

Trigger the gas cost changes in the ModExp precompile.

#### Command

```
uv run execute remote --fork=Osaka -m mainnet tests/osaka/eip7883_modexp_gas_increase/test_eip_mainnet.py --rpc-seed-key $MAINNET_RPC_SEED_KEY --rpc-endpoint $MAINNET_RPC_ENDPOINT --chain-id $MAINNET_CHAIN_ID
```

#### Transaction Hashes

`test_modexp_different_base_lengths[fork_Osaka-state_test-32-bytes-long-base]`: [0x26d0f8b580d735ac74755030f8e4a52ed02814888887e64097c81c7d0f6dd2e0](https://etherscan.io/tx/0x26d0f8b580d735ac74755030f8e4a52ed02814888887e64097c81c7d0f6dd2e0)
`test_modexp_different_base_lengths[fork_Osaka-state_test-33-bytes-long-base]`: [0x71470510279c1006e84fc65c3977983ecdf9658a3aaca0f0e98b90914333e4e7](https://etherscan.io/tx/0x71470510279c1006e84fc65c3977983ecdf9658a3aaca0f0e98b90914333e4e7)
`test_modexp_different_base_lengths[fork_Osaka-state_test-1024-bytes-long-exp]`: [0xca67e591a6f4d4f995ede0927c13e3713d9393660ff9b710fec548bbe6863a51](https://etherscan.io/tx/0xca67e591a6f4d4f995ede0927c13e3713d9393660ff9b710fec548bbe6863a51)
`test_modexp_different_base_lengths[fork_Osaka-state_test-nagydani-1-pow0x10001]`: [0x10d904c6c5d7f3e1f1f527b8871176faac26f4ebc92bdf4a767799fa0e446083](https://etherscan.io/tx/0x10d904c6c5d7f3e1f1f527b8871176faac26f4ebc92bdf4a767799fa0e446083)
`test_modexp_different_base_lengths[fork_Osaka-state_test-zero-exponent-64bytes]`: [0xf2ae6f732cea8ff243d394790c68150118de7a13edcb3c839a848d1043e63189](https://etherscan.io/tx/0xf2ae6f732cea8ff243d394790c68150118de7a13edcb3c839a848d1043e63189)


#### Outcome

✅ PASS

```
================================================================================================ test session starts =================================================================================================
platform linux -- Python 3.11.2, pytest-8.4.2, pluggy-1.6.0 -- /home/marioevz/Development/Eth/execution-specs/.venv/bin/python3
Generating fixtures for: Osaka
Start seed for EOA: 0xe56456f2bd2b240023047d69255f77a5323f97ba36520172051b3b4faa6aaa3a
cachedir: .pytest_cache
Log file: logs/execute-remote-20251203-221125-main.log
metadata: {'Python': '3.11.2', 'Platform': 'Linux-6.1.0-41-cloud-amd64-x86_64-with-glibc2.36', 'Packages': {'pytest': '8.4.2', 'pluggy': '1.6.0'}, 'Plugins': {'regex': '0.2.0', 'custom-report': '1.0.1', 'cov': '4.1.0', 'metadata': '3.1.1', 'xdist': '3.8.0', 'html': '4.1.1', 'json-report': '1.5.0'}, 'Command-line args': '<code>execute -c /home/marioevz/Development/Eth/execution-specs/packages/testing/src/execution_testing/cli/pytest_commands/pytest_ini_files/pytest-execute.ini --rootdir . --fork=Osaka -m mainnet tests/osaka/eip7883_modexp_gas_increase/test_eip_mainnet.py --rpc-seed-key ** --rpc-endpoint ** --chain-id 1 -vv</code>', 'Senders': {}}
rootdir: /home/marioevz/Development/Eth/execution-specs
configfile: packages/testing/src/execution_testing/cli/pytest_commands/pytest_ini_files/pytest-execute.ini
plugins: regex-0.2.0, custom-report-1.0.1, cov-4.1.0, metadata-3.1.1, xdist-3.8.0, html-4.1.1, json-report-1.5.0
collecting ...  pytest-regex selected 5 tests to run for regex: .*
collected 5 items

tests/osaka/eip7883_modexp_gas_increase/test_eip_mainnet.py::test_modexp_different_base_lengths[fork_Osaka-state_test-32-bytes-long-base] PASSED                                                                [1/5]
tests/osaka/eip7883_modexp_gas_increase/test_eip_mainnet.py::test_modexp_different_base_lengths[fork_Osaka-state_test-33-bytes-long-base] PASSED                                                                [2/5]
tests/osaka/eip7883_modexp_gas_increase/test_eip_mainnet.py::test_modexp_different_base_lengths[fork_Osaka-state_test-1024-bytes-long-exp] PASSED                                                               [3/5]
tests/osaka/eip7883_modexp_gas_increase/test_eip_mainnet.py::test_modexp_different_base_lengths[fork_Osaka-state_test-nagydani-1-pow0x10001] PASSED                                                             [4/5]
tests/osaka/eip7883_modexp_gas_increase/test_eip_mainnet.py::test_modexp_different_base_lengths[fork_Osaka-state_test-zero-exponent-64bytes] PASSED                                                             [5/5]

================================================================================================== warnings summary ==================================================================================================
.venv/lib/python3.11/site-packages/_pytest/config/__init__.py:812
  /home/marioevz/Development/Eth/execution-specs/.venv/lib/python3.11/site-packages/_pytest/config/__init__.py:812: PytestAssertRewriteWarning: Module already imported so cannot be rewritten; execution_testing.cli.pytest_commands.plugins.shared.execute_fill
    self.import_plugin(arg, consider_entry_points=True)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
------------------------------------------------------- Log file: /home/marioevz/Development/Eth/execution-specs/logs/execute-remote-20251203-221125-main.log --------------------------------------------------------
====================================================================================== 5 passed, 1 warning in 242.22s (0:04:02) ======================================================================================
```


### - EIP-7910: eth_config JSON-RPC Method

#### Description

Run `execute eth-config` after the fork to validate remaining BPO forks.

#### Command

```
uv run execute eth-config --network Mainnet --rpc-endpoint $MAINNET_RPC_ENDPOINT --chain-id=1
```

#### Transaction Hashes

This is a regular call to a node's JSON RPC to request information; it does not require sending a transaction. 

#### Outcome

✅ PASS

```
================================================= test session starts ==================================================
platform darwin -- Python 3.13.2, pytest-8.4.2, pluggy-1.6.0
collected 7 items

test_eth_config_current[rpc.srv1.snapshotter.mainnet.ethpandaops.io] .
test_eth_config_current_fork_id[rpc.srv1.snapshotter.mainnet.ethpandaops.io] .
test_eth_config_next[rpc.srv1.snapshotter.mainnet.ethpandaops.io] .
test_eth_config_next_fork_id[rpc.srv1.snapshotter.mainnet.ethpandaops.io] .
test_eth_config_last[rpc.srv1.snapshotter.mainnet.ethpandaops.io] .
test_eth_config_last_fork_id[rpc.srv1.snapshotter.mainnet.ethpandaops.io] .

============================================= 6 passed in 1.33s =============================================
```

Tested against 5 mainnet RPC endpoints for Geth, Reth, Nethermind, Erigon, and Besu. All returned consistent results.

#### eth_config Response

```json
{
  "current": {
    "activationTime": 1764798551,
    "blobSchedule": {
      "baseFeeUpdateFraction": 5007716,
      "max": 9,
      "target": 6
    },
    "chainId": "0x1",
    "forkId": "0x5167e2a6",
    "precompiles": {
      "BLAKE2F": "0x0000000000000000000000000000000000000009",
      "BLS12_G1ADD": "0x000000000000000000000000000000000000000b",
      "BLS12_G1MSM": "0x000000000000000000000000000000000000000c",
      "BLS12_G2ADD": "0x000000000000000000000000000000000000000d",
      "BLS12_G2MSM": "0x000000000000000000000000000000000000000e",
      "BLS12_MAP_FP2_TO_G2": "0x0000000000000000000000000000000000000011",
      "BLS12_MAP_FP_TO_G1": "0x0000000000000000000000000000000000000010",
      "BLS12_PAIRING_CHECK": "0x000000000000000000000000000000000000000f",
      "BN254_ADD": "0x0000000000000000000000000000000000000006",
      "BN254_MUL": "0x0000000000000000000000000000000000000007",
      "BN254_PAIRING": "0x0000000000000000000000000000000000000008",
      "ECREC": "0x0000000000000000000000000000000000000001",
      "ID": "0x0000000000000000000000000000000000000004",
      "KZG_POINT_EVALUATION": "0x000000000000000000000000000000000000000a",
      "MODEXP": "0x0000000000000000000000000000000000000005",
      "P256VERIFY": "0x0000000000000000000000000000000000000100",
      "RIPEMD160": "0x0000000000000000000000000000000000000003",
      "SHA256": "0x0000000000000000000000000000000000000002"
    },
    "systemContracts": {
      "BEACON_ROOTS_ADDRESS": "0x000f3df6d732807ef1319fb7b8bb8522d0beac02",
      "CONSOLIDATION_REQUEST_PREDEPLOY_ADDRESS": "0x0000bbddc7ce488642fb579f8b00f3a590007251",
      "DEPOSIT_CONTRACT_ADDRESS": "0x00000000219ab540356cbb839cbe05303d7705fa",
      "HISTORY_STORAGE_ADDRESS": "0x0000f90827f1c53a10cb7a02335b175320002935",
      "WITHDRAWAL_REQUEST_PREDEPLOY_ADDRESS": "0x00000961ef480eb55e80d19ad83579a64c007002"
    }
  },
  "next": {
    "activationTime": 1765290071,
    "blobSchedule": {
      "baseFeeUpdateFraction": 8346193,
      "max": 15,
      "target": 10
    },
    "chainId": "0x1",
    "forkId": "0xcba2a1c0",
    "precompiles": { "..." },
    "systemContracts": { "..." }
  },
  "last": {
    "activationTime": 1767747671,
    "blobSchedule": {
      "baseFeeUpdateFraction": 11684671,
      "max": 21,
      "target": 14
    },
    "chainId": "0x1",
    "forkId": "0x07c9462e",
    "precompiles": { "..." },
    "systemContracts": { "..." }
  }
}
```

The response shows the next scheduled BPO (Blob Parameter Only) forks, and that Osaka is the current fork:

- **current**: The active Osaka fork with blob target=6, max=9
- **next**: First BPO fork (BPO1) increasing blob parameters to target=10, max=15
- **last**: Final scheduled BPO fork (BPO2) with target=14, max=21

All clients return consistent configurations, confirming correct `eth_config` implementation.

### - EIP-7939: Count leading zeros (CLZ) opcode

#### Description

Execute the opcode with different inputs.

#### Command

<!-- Command used to execute the tests. -->

```
uv run execute remote --fork=Osaka -m mainnet tests/osaka/eip7939_count_leading_zeros/test_eip_mainnet.py --rpc-seed-key $MAINNET_RPC_SEED_KEY --rpc-endpoint $MAINNET_RPC_ENDPOINT --chain-id $MAINNET_CHAIN_ID
```

#### Transaction Hashes

`test_clz_mainnet[fork_Osaka-state_test-clz-8-leading-zeros]`: [0x9ec7c2d94378ce3eaa9c794ce70d2f6f0288918d008bc8de79f167a008cb6437](https://etherscan.io/tx/0x9ec7c2d94378ce3eaa9c794ce70d2f6f0288918d008bc8de79f167a008cb6437)
`test_clz_mainnet[fork_Osaka-state_test-clz-all-zeros]`: [0x7f9ea62cf3490a0080523c056fb0327ee3de2d9a854e297b8fe86442d5126bb0](https://etherscan.io/tx/0x7f9ea62cf3490a0080523c056fb0327ee3de2d9a854e297b8fe86442d5126bb0)

#### Outcome

✅ PASS

```
================================================================================================ test session starts =================================================================================================
platform linux -- Python 3.11.2, pytest-8.4.2, pluggy-1.6.0 -- /home/marioevz/Development/Eth/execution-specs/.venv/bin/python3
Generating fixtures for: Osaka
Start seed for EOA: 0xb455ab3f3dfcc6979e5d38b44798a23efb59966d457747dbbfe5c98885ef5f39
cachedir: .pytest_cache
Log file: logs/execute-remote-20251203-221638-main.log
metadata: {'Python': '3.11.2', 'Platform': 'Linux-6.1.0-41-cloud-amd64-x86_64-with-glibc2.36', 'Packages': {'pytest': '8.4.2', 'pluggy': '1.6.0'}, 'Plugins': {'regex': '0.2.0', 'custom-report': '1.0.1', 'cov': '4.1.0', 'metadata': '3.1.1', 'xdist': '3.8.0', 'html': '4.1.1', 'json-report': '1.5.0'}, 'Command-line args': '<code>execute -c /home/marioevz/Development/Eth/execution-specs/packages/testing/src/execution_testing/cli/pytest_commands/pytest_ini_files/pytest-execute.ini --rootdir . --fork=Osaka -m mainnet tests/osaka/eip7939_count_leading_zeros/test_eip_mainnet.py --rpc-seed-key ** --rpc-endpoint ** --chain-id 1 -vv</code>', 'Senders': {}}
rootdir: /home/marioevz/Development/Eth/execution-specs
configfile: packages/testing/src/execution_testing/cli/pytest_commands/pytest_ini_files/pytest-execute.ini
plugins: regex-0.2.0, custom-report-1.0.1, cov-4.1.0, metadata-3.1.1, xdist-3.8.0, html-4.1.1, json-report-1.5.0
collecting ...  pytest-regex selected 2 tests to run for regex: .*
collected 2 items

tests/osaka/eip7939_count_leading_zeros/test_eip_mainnet.py::test_clz_mainnet[fork_Osaka-state_test-clz-8-leading-zeros] PASSED                                                                                 [1/2]
tests/osaka/eip7939_count_leading_zeros/test_eip_mainnet.py::test_clz_mainnet[fork_Osaka-state_test-clz-all-zeros] PASSED                                                                                       [2/2]

================================================================================================== warnings summary ==================================================================================================
.venv/lib/python3.11/site-packages/_pytest/config/__init__.py:812
  /home/marioevz/Development/Eth/execution-specs/.venv/lib/python3.11/site-packages/_pytest/config/__init__.py:812: PytestAssertRewriteWarning: Module already imported so cannot be rewritten; execution_testing.cli.pytest_commands.plugins.shared.execute_fill
    self.import_plugin(arg, consider_entry_points=True)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
------------------------------------------------------- Log file: /home/marioevz/Development/Eth/execution-specs/logs/execute-remote-20251203-221638-main.log --------------------------------------------------------
====================================================================================== 2 passed, 1 warning in 145.33s (0:02:25) ======================================================================================
```


### - EIP-7951: Precompile for secp256r1 Curve Support

#### Description

Execute the precompile with different inputs.

#### Command

<!-- Command used to execute the tests. -->

```
uv run execute remote --fork=Osaka -m mainnet tests/osaka/eip7951_p256verify_precompiles/test_eip_mainnet.py --rpc-seed-key $MAINNET_RPC_SEED_KEY --rpc-endpoint $MAINNET_RPC_ENDPOINT --chain-id $MAINNET_CHAIN_ID
```

#### Transaction Hashes

`test_valid[fork_Osaka-state_test--valid_r1_sig-]`: [0x6911ce5860e375b70c35a5b7d4860a85481e2c4e3db057196cd8089dc7434b92](https://etherscan.io/tx/0x6911ce5860e375b70c35a5b7d4860a85481e2c4e3db057196cd8089dc7434b92)
`test_invalid[fork_Osaka-state_test--invalid_r1_sig_but_valid_k1_sig-]`: [0x63e3c33f556f13df928c994cbe97e0cb7f5994912fc1c355d128027461d005de](https://etherscan.io/tx/0x63e3c33f556f13df928c994cbe97e0cb7f5994912fc1c355d128027461d005de)

#### Outcome

✅ PASS

<!-- Summary of the command output. -->
```
================================================================================================ test session starts =================================================================================================
platform linux -- Python 3.11.2, pytest-8.4.2, pluggy-1.6.0 -- /home/marioevz/Development/Eth/execution-specs/.venv/bin/python3
Generating fixtures for: Osaka
Start seed for EOA: 0xecf3a0a57edc9824fec2f3edc6eb91700dbf87b2e0a6f6ac39766859d818621c
cachedir: .pytest_cache
Log file: logs/execute-remote-20251203-221945-main.log
metadata: {'Python': '3.11.2', 'Platform': 'Linux-6.1.0-41-cloud-amd64-x86_64-with-glibc2.36', 'Packages': {'pytest': '8.4.2', 'pluggy': '1.6.0'}, 'Plugins': {'regex': '0.2.0', 'custom-report': '1.0.1', 'cov': '4.1.0', 'metadata': '3.1.1', 'xdist': '3.8.0', 'html': '4.1.1', 'json-report': '1.5.0'}, 'Command-line args': '<code>execute -c /home/marioevz/Development/Eth/execution-specs/packages/testing/src/execution_testing/cli/pytest_commands/pytest_ini_files/pytest-execute.ini --rootdir . --fork=Osaka -m mainnet tests/osaka/eip7951_p256verify_precompiles/test_eip_mainnet.py --rpc-seed-key ** --rpc-endpoint ** --chain-id 1 -vv</code>', 'Senders': {}}
rootdir: /home/marioevz/Development/Eth/execution-specs
configfile: packages/testing/src/execution_testing/cli/pytest_commands/pytest_ini_files/pytest-execute.ini
plugins: regex-0.2.0, custom-report-1.0.1, cov-4.1.0, metadata-3.1.1, xdist-3.8.0, html-4.1.1, json-report-1.5.0
collecting ...  pytest-regex selected 2 tests to run for regex: .*
collected 2 items

tests/osaka/eip7951_p256verify_precompiles/test_eip_mainnet.py::test_valid[fork_Osaka-state_test--valid_r1_sig-] PASSED                                                                                         [1/2]
tests/osaka/eip7951_p256verify_precompiles/test_eip_mainnet.py::test_invalid[fork_Osaka-state_test--invalid_r1_sig_but_valid_k1_sig-] PASSED                                                                    [2/2]

================================================================================================== warnings summary ==================================================================================================
.venv/lib/python3.11/site-packages/_pytest/config/__init__.py:812
  /home/marioevz/Development/Eth/execution-specs/.venv/lib/python3.11/site-packages/_pytest/config/__init__.py:812: PytestAssertRewriteWarning: Module already imported so cannot be rewritten; execution_testing.cli.pytest_commands.plugins.shared.execute_fill
    self.import_plugin(arg, consider_entry_points=True)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
------------------------------------------------------- Log file: /home/marioevz/Development/Eth/execution-specs/logs/execute-remote-20251203-221945-main.log --------------------------------------------------------
====================================================================================== 2 passed, 1 warning in 91.81s (0:01:31) =======================================================================================
```

<!-- Details if necessary. -->