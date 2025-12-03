# Pectra Mainnet Testing

## Summary

- Test transactions will be sent to mainnet for each EIP using [EEST's `execute` command](https://eest.ethereum.org/main/executing_tests/), with the exception of the EIP's in the next bullet point.
    - Approximately ~0.010533462656721374 Eth gas required for these tests.
- EIP-6110 + EIP-7002 + EIP-7251 tests are run using a currently-active mainnet validator:
    - A currently-active mainnet validator, with 0x01 withdrawal credentials, will perform the following tests:
      - Send consolidation request to change withdrawal credentials to 0x02 type to validate EIP-7251.
      - Make a 1 Eth deposit to validate deposit requests in EIP-6110.
      - Send a withdrawal request with a non-zero amount to validate EIP-7002.

## Schedule

- Fork Epoch: 364032 (May 7, 2025 10:05:11 UTC)
- Fork Finalization Epoch: 364034 (May 7, 2025 10:17:59 UTC)
- Testing will commence at the fork finalization epoch if the chain finalizes successfully without intervention.

## Test Spec

##### EEST branch

https://github.com/ethereum/execution-spec-tests/tree/mainnet-marked-tests-defered-eoa-funding

#### - EIP-2537

##### Description

Test using each pre-compile introduced in EIP-2537.

##### Command

```
uv run execute remote --fork=Prague -m mainnet tests/prague/eip2537_bls_12_381_precompiles/test_eip_mainnet.py --rpc-seed-key $RPC_SEED_KEY --rpc-endpoint $RPC_URL --rpc-chain-id $RPC_CHAIN_ID
```

##### Transaction Hashes

`tests/prague/eip2537_bls_12_381_precompiles/test_eip_mainnet.py::test_eip_2537[fork_Prague-state_test-G1ADD]`: [0x5f3ba22a2a7ad9d79492d667de6ad7e60bedca286de3a873cda8db571b8db199](https://etherscan.io/tx/0x5f3ba22a2a7ad9d79492d667de6ad7e60bedca286de3a873cda8db571b8db199)
`tests/prague/eip2537_bls_12_381_precompiles/test_eip_mainnet.py::test_eip_2537[fork_Prague-state_test-G1MSM]`: [0x947ddcc44e3e311efdeb450a531a1d083a369e20445c58baeea67200217974f2](https://etherscan.io/tx/0x947ddcc44e3e311efdeb450a531a1d083a369e20445c58baeea67200217974f2)
`tests/prague/eip2537_bls_12_381_precompiles/test_eip_mainnet.py::test_eip_2537[fork_Prague-state_test-G2ADD]`: [0xa0109267a59c216dae8c09eee3fe898376a331909562579a059e270879aa69f7](https://etherscan.io/tx/0xa0109267a59c216dae8c09eee3fe898376a331909562579a059e270879aa69f7)
`tests/prague/eip2537_bls_12_381_precompiles/test_eip_mainnet.py::test_eip_2537[fork_Prague-state_test-G2MSM]`: [0x971d08f32a25e88e67c369fe3edf394c06c73bb9b6590dbf2e59853815bfb920](https://etherscan.io/tx/0x971d08f32a25e88e67c369fe3edf394c06c73bb9b6590dbf2e59853815bfb920)
`tests/prague/eip2537_bls_12_381_precompiles/test_eip_mainnet.py::test_eip_2537[fork_Prague-state_test-PAIRING]`: [0x242d2e701ff23b8d134215ea4331566fa148e570ddec200fba3190d40fb9eff5](https://etherscan.io/tx/0x242d2e701ff23b8d134215ea4331566fa148e570ddec200fba3190d40fb9eff5)
`tests/prague/eip2537_bls_12_381_precompiles/test_eip_mainnet.py::test_eip_2537[fork_Prague-state_test-fp_map_to_inf0]`: [0x5d4ef6ed292c906b4507acd0a937c81a9c0315e337ad788f74e27361950df638](https://etherscan.io/tx/0x5d4ef6ed292c906b4507acd0a937c81a9c0315e337ad788f74e27361950df638)
`tests/prague/eip2537_bls_12_381_precompiles/test_eip_mainnet.py::test_eip_2537[fork_Prague-state_test-fp_map_to_inf1]`: [0x78bb640a029630b3bcdbec0c829453a9ace6f6987be4852efbcf6d59c4ce5580](https://etherscan.io/tx/0x78bb640a029630b3bcdbec0c829453a9ace6f6987be4852efbcf6d59c4ce5580) (Note: Test ID name mistake, this is actually MAP_FP2_TO_G2)

##### Outcome

✅ PASS

```
================================================================= test session starts ==================================================================
platform linux -- Python 3.10.12, pytest-7.4.4, pluggy-1.5.0
Generating fixtures for: Prague
solc: 0.8.24
Start seed for EOA: * 
Log file: logs/execute-remote-20250507-104236-main.log
rootdir: /home/marioevz/execution-spec-tests
configfile: pytest-execute.ini
plugins: html-4.1.1, json-report-1.5.0, xdist-3.6.1, regex-0.2.0, custom-report-1.0.1, metadata-3.1.1
collecting ...  pytest-regex selected 7 tests to run for regex: .*
collected 7 items                                                                                                                                      

tests/prague/eip2537_bls_12_381_precompiles/test_eip_mainnet.py .......                                                                           [7/7]

------------------------------ Log file: /home/marioevz/execution-spec-tests/logs/execute-remote-20250507-104236-main.log ------------------------------
============================================================ 7 passed in 313.20s (0:05:13) =============================================================
```


#### - EIP-2935

##### Description

Test calling the system contract to obtain a hash and compare against the result of `BLOCKHASH` opcode.

##### Command

```
uv run execute remote --fork=Prague -m mainnet tests/prague/eip2935_historical_block_hashes_from_state/test_eip_mainnet.py --rpc-seed-key $RPC_SEED_KEY --rpc-endpoint $RPC_URL --rpc-chain-id $RPC_CHAIN_ID
```

##### Transaction Hashes

[0x9e01e3ddedd893cc1a78234c1eebe0d670a4be69ff5c15d64185c5038a77f719](https://etherscan.io/tx/0x9e01e3ddedd893cc1a78234c1eebe0d670a4be69ff5c15d64185c5038a77f719)

##### Outcome

✅ PASS

```
================================================================= test session starts ==================================================================
platform linux -- Python 3.10.12, pytest-7.4.4, pluggy-1.5.0
Generating fixtures for: Prague
solc: 0.8.24
Start seed for EOA: * 
Log file: logs/execute-remote-20250507-103800-main.log
rootdir: /home/marioevz/execution-spec-tests
configfile: pytest-execute.ini
plugins: html-4.1.1, json-report-1.5.0, xdist-3.6.1, regex-0.2.0, custom-report-1.0.1, metadata-3.1.1
collecting ...  pytest-regex selected 1 tests to run for regex: .*
collected 1 item                                                                                                                                       

tests/prague/eip2935_historical_block_hashes_from_state/test_eip_mainnet.py .                                                                     [1/1]

------------------------------ Log file: /home/marioevz/execution-spec-tests/logs/execute-remote-20250507-103800-main.log ------------------------------
================================================================== 1 passed in 49.51s ==================================================================
```

#### - EIP-7623

##### Description

Test sending all transaction types with enough data to trigger the data floor cost introduced by EIP-7623.

##### Command

```
uv run execute remote --fork=Prague -m mainnet tests/prague/eip7623_increase_calldata_cost/test_eip_mainnet.py --rpc-seed-key $RPC_SEED_KEY --rpc-endpoint $RPC_URL --rpc-chain-id $RPC_CHAIN_ID
```

##### Transaction Hashes

`tests/prague/eip7623_increase_calldata_cost/test_eip_mainnet.py::test_eip_7623[fork_Prague-state_test----type_0_protected]`: [0x500f0576ddcea4200b07607b792269d920a9cd66df1b8fa3a89ed30809b37e56](https://etherscan.io/tx/0x500f0576ddcea4200b07607b792269d920a9cd66df1b8fa3a89ed30809b37e56)
`tests/prague/eip7623_increase_calldata_cost/test_eip_mainnet.py::test_eip_7623[fork_Prague-state_test----type_1]`: [0x5c6b85d15e9d2b831cbcec3cf4871044eb4cc52e917ebe4e5b734eab998ef8da](https://etherscan.io/tx/0x5c6b85d15e9d2b831cbcec3cf4871044eb4cc52e917ebe4e5b734eab998ef8da)
`tests/prague/eip7623_increase_calldata_cost/test_eip_mainnet.py::test_eip_7623[fork_Prague-state_test----type_2]`: [0xf776872f95f15d6c621c21920d10cdcd15771646e71b9f1e540f44036943013f](https://etherscan.io/tx/0xf776872f95f15d6c621c21920d10cdcd15771646e71b9f1e540f44036943013f)
`tests/prague/eip7623_increase_calldata_cost/test_eip_mainnet.py::test_eip_7623[fork_Prague-state_test----type_4]`: [0x3ff034f0c94c28c7922a2ac1cd9ac70097e0dab04e1369b434ffd5ad6e0c046c](https://etherscan.io/tx/0x3ff034f0c94c28c7922a2ac1cd9ac70097e0dab04e1369b434ffd5ad6e0c046c)

##### Outcome

✅ PASS:
```
================================================================= test session starts ==================================================================
platform linux -- Python 3.10.12, pytest-7.4.4, pluggy-1.5.0
Generating fixtures for: Prague
solc: 0.8.24
Start seed for EOA: * 
Log file: logs/execute-remote-20250507-105140-main.log
rootdir: /home/marioevz/execution-spec-tests
configfile: pytest-execute.ini
plugins: html-4.1.1, json-report-1.5.0, xdist-3.6.1, regex-0.2.0, custom-report-1.0.1, metadata-3.1.1
collecting ...  pytest-regex selected 6 tests to run for regex: .*
collected 6 items                                                                                                                                      

tests/prague/eip7623_increase_calldata_cost/test_eip_mainnet.py .s..s.                                                                            [6/6]

------------------------------ Log file: /home/marioevz/execution-spec-tests/logs/execute-remote-20250507-105140-main.log ------------------------------
======================================================= 4 passed, 2 skipped in 115.98s (0:01:55) =======================================================
```

#### - EIP-7702

##### Description

Test type-4 transaction to set a code delegation for an account, and call the account which sets the storage in the EOA.

##### Command

```
uv run execute remote --fork=Prague -m mainnet tests/prague/eip7702_set_code_tx/test_eip_mainnet.py --rpc-seed-key $RPC_SEED_KEY --rpc-endpoint $RPC_URL --rpc-chain-id $RPC_CHAIN_ID
```

##### Transaction Hashes

`tests/prague/eip7702_set_code_tx/test_eip_mainnet.py::test_eip_7702[fork_Prague-state_test]`: [0x1e89e5fc1622cb58703e3a82d77ceadfb1a45a66e59eb3c595e859185583a0f4](https://etherscan.io/tx/0x1e89e5fc1622cb58703e3a82d77ceadfb1a45a66e59eb3c595e859185583a0f4)

##### Outcome

✅ PASS:
```
================================================================= test session starts ==================================================================
platform linux -- Python 3.10.12, pytest-7.4.4, pluggy-1.5.0
Generating fixtures for: Prague
solc: 0.8.24
Start seed for EOA: * 
Log file: logs/execute-remote-20250507-105724-main.log
rootdir: /home/marioevz/execution-spec-tests
configfile: pytest-execute.ini
plugins: html-4.1.1, json-report-1.5.0, xdist-3.6.1, regex-0.2.0, custom-report-1.0.1, metadata-3.1.1
collecting ...  pytest-regex selected 1 tests to run for regex: .*
collected 1 item                                                                                                                                       

tests/prague/eip7702_set_code_tx/test_eip_mainnet.py .                                                                                            [1/1]

------------------------------ Log file: /home/marioevz/execution-spec-tests/logs/execute-remote-20250507-105724-main.log ------------------------------
================================================================== 1 passed in 49.48s ==================================================================
```

#### - EIP-7251

##### Description

Send a transaction to the EIP-7251 system contract that triggers a consolidation request for an active mainnet validator and converts it to a compounding validator.

Verify the validator is correctly converted to a compounding validator.

Validator: 0x94630ee7300cd57c97c4bc4ccfc434ddc61ed9832b34ae74dfb40b8bcb7c4fddd80d791c5df6b1e31a975198dab631cd

##### Command

N/A

##### Transaction Hashes

[0x3fcd4c90da4df016c666bd571ec35f980ed06aafc96b0399282c584be9cc32a1](https://etherscan.io/tx/0x3fcd4c90da4df016c666bd571ec35f980ed06aafc96b0399282c584be9cc32a1)

##### Outcome

✅ PASS - Validator upgraded to 0x02 withdrawal credentials:
```
{
  "execution_optimistic": false,
  "finalized": false,
  "data": {
    "index": "1011535",
    "balance": "32000017023",
    "status": "active_ongoing",
    "validator": {
      "pubkey": "0x94630ee7300cd57c97c4bc4ccfc434ddc61ed9832b34ae74dfb40b8bcb7c4fddd80d791c5df6b1e31a975198dab631cd",
      "withdrawal_credentials": "0x020000000000000000000000d2f75c89daa9fbf469ec11e8aee102a43a183545",
      "effective_balance": "32000000000",
      "slashed": false,
      "activation_eligibility_epoch": "241057",
      "activation_epoch": "241092",
      "exit_epoch": "18446744073709551615",
      "withdrawable_epoch": "18446744073709551615"
    }
  }
}
```

#### - EIP-6110

##### Description

Send a deposit transaction for 1 Eth to an active validator.

Verify the deposit amount is correctly added to the active validator's balance.

Validator: 0x94630ee7300cd57c97c4bc4ccfc434ddc61ed9832b34ae74dfb40b8bcb7c4fddd80d791c5df6b1e31a975198dab631cd

##### Command

N/A

##### Transaction Hashes

[0x0a25e918602a6dcfc423551921a8c83c19bb0fb004477f8dfe6dd2bd4fd78da6](https://etherscan.io/tx/0x0a25e918602a6dcfc423551921a8c83c19bb0fb004477f8dfe6dd2bd4fd78da6)

##### Outcome

✅ PASS: Pending deposit shows up in the pending deposits queue:
```
{
      "pubkey": "0x94630ee7300cd57c97c4bc4ccfc434ddc61ed9832b34ae74dfb40b8bcb7c4fddd80d791c5df6b1e31a975198dab631cd",
      "withdrawal_credentials": "0x0000000000000000000000000000000000000000000000000000000000000000",
      "amount": "1000000000",
      "signature": "0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
      "slot": "11649134"
    },
```
(Empty signature/withdrawal credentials is expected)

#### - EIP-7002

##### Description

Send a transaction to the EIP-7002 system contract that triggers a partial withdrawal request for an active mainnet validator.

Validator: 0x94630ee7300cd57c97c4bc4ccfc434ddc61ed9832b34ae74dfb40b8bcb7c4fddd80d791c5df6b1e31a975198dab631cd

##### Command

N/A

##### Transaction Hashes

[0x94f23a6bfe0bc26cfc164e19e46a4dd30ef2bc6ae76124255184ffa61d38af61](https://etherscan.io/tx/0x94f23a6bfe0bc26cfc164e19e46a4dd30ef2bc6ae76124255184ffa61d38af61)

##### Outcome

✅ PASS: Partial withdrawal shows up in the pending partial withdrawals queue:
```
{
  "execution_optimistic": false,
  "finalized": false,
  "data": [
    {
      "validator_index": "1011535",
      "amount": "1",
      "withdrawable_epoch": "364301"
    }
  ]
}
```
