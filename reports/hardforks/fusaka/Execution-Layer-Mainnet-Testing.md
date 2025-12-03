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

<!-- Link to the commit used for testing -->
https://github.com/ethereum/execution-specs/tree/forks/osaka/

### - EIP-7823: Set upper bounds for MODEXP

#### Description

Execute pre-compile at the exact boundary and above the boundary.

#### Command

```
uv run execute remote --fork=Osaka -m mainnet tests/osaka/eip7823_modexp_upper_bounds/test_eip_mainnet.py --rpc-seed-key $MAINNET_RPC_SEED_KEY --rpc-endpoint $MAINNET_RPC_ENDPOINT --chain-id $MAINNET_CHAIN_ID
```

#### Transaction Hashes

<!-- Hashes of the transactions that executed the test logic, excluding account funding or contract creation. -->

`tests/.../test_eip_mainnet.py::test_...`: [0x01234...cdef](https://etherscan.io/tx/0x01234...cdef)

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
uv run execute remote --fork=Osaka -m mainnet tests/... --rpc-seed-key $MAINNET_RPC_SEED_KEY --rpc-endpoint $MAINNET_RPC_ENDPOINT --chain-id $MAINNET_CHAIN_ID
```

#### Transaction Hashes

<!-- Hashes of the transactions that executed the test logic, excluding account funding or contract creation. -->

`tests/.../test_eip_mainnet.py::test_...`: [0x01234...cdef](https://etherscan.io/tx/0x01234...cdef)

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

<!-- General description of the tests to be executed. -->

#### Command

<!-- Command used to execute the tests. -->

```
uv run execute remote --fork=Osaka -m mainnet tests/... --rpc-seed-key $MAINNET_RPC_SEED_KEY --rpc-endpoint $MAINNET_RPC_ENDPOINT --chain-id $MAINNET_CHAIN_ID
```

#### Transaction Hashes

<!-- Hashes of the transactions that executed the test logic, excluding account funding or contract creation. -->

`tests/.../test_eip_mainnet.py::test_...`: [0x01234...cdef](https://etherscan.io/tx/0x01234...cdef)

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

<!-- General description of the tests to be executed. -->

#### Command

<!-- Command used to execute the tests. -->

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

<!-- General description of the tests to be executed. -->

#### Command

<!-- Command used to execute the tests. -->

```
uv run execute remote --fork=Osaka -m mainnet tests/... --rpc-seed-key $MAINNET_RPC_SEED_KEY --rpc-endpoint $MAINNET_RPC_ENDPOINT --chain-id $MAINNET_CHAIN_ID
```

#### Transaction Hashes

<!-- Hashes of the transactions that executed the test logic, excluding account funding or contract creation. -->

`tests/.../test_eip_mainnet.py::test_...`: [0x01234...cdef](https://etherscan.io/tx/0x01234...cdef)

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

<!-- General description of the tests to be executed. -->

#### Command

<!-- Command used to execute the tests. -->

```
uv run execute remote --fork=Osaka -m mainnet tests/... --rpc-seed-key $MAINNET_RPC_SEED_KEY --rpc-endpoint $MAINNET_RPC_ENDPOINT --chain-id $MAINNET_CHAIN_ID
```

#### Transaction Hashes

<!-- Hashes of the transactions that executed the test logic, excluding account funding or contract creation. -->

`tests/.../test_eip_mainnet.py::test_...`: [0x01234...cdef](https://etherscan.io/tx/0x01234...cdef)

#### Outcome

✅ PASS / ❌ FAIL

<!-- Summary of the command output. -->
```
================================================================= test session starts ==================================================================
...
============================================================ X passed in Xs (X:XX:XX) =============================================================
```

<!-- Details if necessary. -->