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
uv run execute eth-config ...
```

#### Transaction Hashes

N/A

#### Outcome

✅ PASS / ❌ FAIL

<!-- Summary of the command output. -->
```
================================================================= test session starts ==================================================================
...
============================================================ X passed in Xs (X:XX:XX) =============================================================
```

<!-- Details if necessary. -->

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