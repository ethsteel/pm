# Execution Layer [HARDFORK] Mainnet Testing

## Summary

- Test transactions will be sent to mainnet for each EIP using [EELS's `execute remote` command](https://eest.ethereum.org/main/running_tests/execute/remote/), with the exception of the EIPs in the next bullet point.
- Approximately ~[EXECUTE DRY-RUN ETH] Eth gas required for these tests.

## EIPs

### Included

 <!-- List of all the EIPs that will be included in this testing round. -->

### Excluded

 <!-- List of all the EIPs that will be excluded from this testing round, along with reasoning to exclusion. -->

## Schedule

- Fork Epoch: [HARDFORK EPOCH] ([HARDFORK EPOCH DATE])
- Fork Expected Finalization Epoch: [HARDFORK EPOCH + 2] ([HARDFORK EPOCH + 2 DATE])
- Testing will commence at the fork finalization epoch when the chain finalizes successfully without intervention.

## Test Spec

#### EELS Commit

<!-- Link to the commit used for testing -->
https://github.com/ethereum/execution-specs/tree/forks/osaka/

### - EIP-XXXX

#### Description

<!-- General description of the tests to be executed. -->

#### Command

<!-- Command used to execute the tests. -->

```
uv run execute remote --fork=[HARDFORK] -m mainnet tests/... --rpc-seed-key $RPC_SEED_KEY --rpc-endpoint $RPC_URL --chain-id $RPC_CHAIN_ID
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