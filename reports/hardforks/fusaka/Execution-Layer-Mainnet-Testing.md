# Execution Layer Fusaka Mainnet Testing

## Summary

- Test transactions will be sent to mainnet for each EIP using [EELS's `execute remote` command](https://eest.ethereum.org/main/running_tests/execute/remote/), with the exception of the EIPs in the next bullet point.
- Approximately ~[EXECUTE DRY-RUN ETH] Eth gas required for these tests.

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

`test_modexp_boundary[fork_Osaka-state_test-base-boundary-1024-bytes]`: 
`test_modexp_over_boundary[fork_Osaka-state_test-base-over-boundary-1025-bytes]`: 
        
#### Outcome

✅ PASS / ❌ FAIL

<!-- Summary of the command output. -->
```
================================================================= test session starts ==================================================================
...
============================================================ X passed in Xs (X:XX:XX) =============================================================
```

<!-- Details if necessary. -->

### - EIP-7825: Transaction Gas Limit Cap

#### Description

Send a transaction with the gas limit cap and above.

#### Command

```
uv run execute remote --fork=Osaka -m mainnet tests/osaka/eip7825_transaction_gas_limit_cap/test_eip_mainnet.py --rpc-seed-key $MAINNET_RPC_SEED_KEY --rpc-endpoint $MAINNET_RPC_ENDPOINT --chain-id $MAINNET_CHAIN_ID
```

#### Transaction Hashes

`test_tx_gas_limit_cap_at_maximum[fork_Osaka-state_test]`: 
`test_tx_gas_limit_cap_exceeded[fork_Osaka-state_test]`: 

#### Outcome

✅ PASS / ❌ FAIL

<!-- Summary of the command output. -->
```
================================================================= test session starts ==================================================================
...
============================================================ X passed in Xs (X:XX:XX) =============================================================
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

`test_modexp_different_base_lengths[fork_Osaka-state_test-32-bytes-long-base]`: 
`test_modexp_different_base_lengths[fork_Osaka-state_test-33-bytes-long-base]`: 
`test_modexp_different_base_lengths[fork_Osaka-state_test-1024-bytes-long-exp]`: 
`test_modexp_different_base_lengths[fork_Osaka-state_test-nagydani-1-pow0x10001]`: 
`test_modexp_different_base_lengths[fork_Osaka-state_test-zero-exponent-64bytes]`: 


#### Outcome

✅ PASS / ❌ FAIL

<!-- Summary of the command output. -->
```
================================================================= test session starts ==================================================================
...
============================================================ X passed in Xs (X:XX:XX) =============================================================
```

<!-- Details if necessary. -->

### - EIP-7910: eth_config JSON-RPC Method

#### Description

Run `execute eth-config` after the fork to validate remaining BPO forks.

#### Command

```
uv run execute eth-config --network Mainnet --rpc-endpoint $MAINNET_RPC_ENDPOINT --chain-id=1
```

#### Transaction Hashes

N/A

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

`test_clz_mainnet[fork_Osaka-state_test-clz-8-leading-zeros]`: 
`test_clz_mainnet[fork_Osaka-state_test-clz-all-zeros]`: 

#### Outcome

✅ PASS / ❌ FAIL

<!-- Summary of the command output. -->
```
================================================================= test session starts ==================================================================
...
============================================================ X passed in Xs (X:XX:XX) =============================================================
```

<!-- Details if necessary. -->

### - EIP-7951: Precompile for secp256r1 Curve Support

#### Description

Execute the precompile with different inputs.

#### Command

<!-- Command used to execute the tests. -->

```
uv run execute remote --fork=Osaka -m mainnet tests/osaka/eip7951_p256verify_precompiles/test_eip_mainnet.py --rpc-seed-key $MAINNET_RPC_SEED_KEY --rpc-endpoint $MAINNET_RPC_ENDPOINT --chain-id $MAINNET_CHAIN_ID
```

#### Transaction Hashes

`test_valid[fork_Osaka-state_test--valid_r1_sig-]`: 
`test_invalid[fork_Osaka-state_test--invalid_r1_sig_but_valid_k1_sig-]`: 

#### Outcome

✅ PASS / ❌ FAIL

<!-- Summary of the command output. -->
```
================================================================= test session starts ==================================================================
...
============================================================ X passed in Xs (X:XX:XX) =============================================================
```

<!-- Details if necessary. -->