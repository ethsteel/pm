# EIP-NNNN: EIP Title

Link: https://eips.ethereum.org/EIPS/eip-NNNN

# Execution Specs

## Specs

TBD

## Testing

### Anchors

All anchors are scored on a 0–3 scale. A score of 4 may be used in exceptional circumstances where the complexity or impact exceeds the defined anchors.

#### EVM Gas rule changes

New EVM gas accounting rules 

- 0. No gas accounting changes.
- 1. Existing gas accounting mechanism is updated.
- 2. A new gas accounting mechanism is introduced but it does not affect existing mechanisms nor it affects existing tests.
- 3. A new gas accounting mechanism is introduced and affects existing mechanisms which affects existing tests.

#### Blob gas accounting changes

New Blob gas accounting rules which potentially affect pre-existing tests

- 0. No blob gas accounting changes.
- 1. Existing blob gas accounting mechanism is updated.
- 2. A new blob gas accounting mechanism is introduced but it does not affect existing mechanisms nor it affects existing tests.
- 3. A new blob gas accounting mechanism is introduced and affects existing mechanisms which affects existing tests.

#### New EVM gas refund

New gas-refund mechanism 

- 0. No new gas-refund mechanisms are introduced.
- 1. A new simple gas-refund mechanism is introduced that does not affect either existing tests or existing gas-refund mechanisms.
- 2. A new complex gas-refund mechanism is introduced or a simple mechanism that affects existing tests or existing gas-refund mechanisms.
- 3. A new complex gas-refund mechanism is introduced that affects existing tests or existing gas-refund mechanisms.

#### Patterns affecting pre-existing tests

Implements a new validation mechanism or rule that translates in reworking pre-existing tests 

- 0. No pre-existing tests are affected by this change.
- 1. Minor subset of existing tests are affected by this change.
- 2. Considreable subset of existing tests are affected by this change but involves a contrived category of tests.
- 3. Major subset of existing tests are affected, including diverse category of tests (benchmarks, static, multiple forks, etc.).

#### Transition-tool interface changes

Modifies or adds new fields to the transition tool interface. 

- 0. No modifications to the transition tool interface are required.
- 1. A single new field needs to be introduced to the transition tool interface. 
- 2. Multiple new fields or a new mechanism has to be introduced to the transition tool interface.
- 3. Multiple new fields and a new mechanism has to be introduced to the transition tool interface.

*Special consideration must be paid to this section if the EIP introduces a mechanism that requires the state transition tool to be aware whether the block it is processing is the fork-activation block.

#### Cryptography

Introduces new cryptography mechanisms or modifies existing functionality that involves cryptography 

- 0. No cryptography mechanisms are introduced.
- 1. A new cryptography mechanism is introduced but it is a well known mechanism that is known to have vast resources to aid on its testing.
- 2. Multiple new cryptography mechanisms are introduced that are well-known or a single but novel mechanism is introduced that it's either untested or has limited resources.
- 3. Multiple new cryptography mechanisms are introduced and at least one of them is a novel mechanism.

#### Edge/boundary conditions

Feature contains edge/boundary conditions.

- 0. No discernible edge cases or boundary conditions are introduced.
- 1. A single edge-case or boundary-condition prone mechanism is introduced.
- 2. Multiple edge-case or boundary-condition prone mechanisms are introduced, but none of them requires an elevated number of cases to test.
- 3. Multiple edge-case or boundary-condition prone mechanisms are introduced and at least one of them requires an elevated number of cases to test.

#### Block syncing changes

Modifies block RLP validation mechanisms that requires test client syncing.

- 0. No new RLP validation mechanism is introduced.
- 1. A single new simple RLP validation mechanism is introduced.
- 2. Multiple simple RLP validation mechanisms are introduced or a single complex one.
- 3. Multiple RLP validation mechanisms are introduced and at least one of them is deemed complex.

#### Engine API changes

Introduces new fields to the Engine API directives

- 0. No new fields or communication mechanisms are introduced to the Engine API.
- 1. A single new field is introduced in one of the Engine API end-points.
- 2. Multiple fields are introduced to one or multiple Engine API end points, or a new Engine API end-point is introduced.
- 3. Multiple fields are introduced to one or multiple Engine API end points and a new Engine API end-point is introduced.

#### Added system contracts

Introduces new system contract, stateful or not 

- 0. No new system contracts are introduced.
- 1. A new system contract is introduced that is not stateful nor does it trigger a new system action (e.g. requests to the consensus layer).
- 2. Multiple new system contracts are introduced or a single new system contract that is either stateful or triggers a new system action (e.g. requests to the consensus layer).
- 3. Multiple new system contracts are introduced and at least one of them is either stateful or triggers a new system action (e.g. requests to the consensus layer).

#### Modified system contracts

Modifies pre-existing system contracts 

- 0. No modifications to pre-existing system contracts are introduced.
- 3. At least one pre-existing system contract is modified, which would involve irregular state transition or a similary complex transition methodology.

#### Added opcodes

Introduces new opcodes 

- 0. No new opcodes are introduced.
- 1. A new simple opcode is introduced (no data portion, no complex stack mechanics, and a constant gas cost).
- 2. Multiple new simple opcodes are introduced, or a single new complex opcode is introduced (has data portion, or complex stack mechanics, or a dynamic gas cost).
- 3. Multiple new opcodes are introduced, and at least one of them is complex (has data portion, or complex stack mechanics, or a dynamic gas cost).

*Cryptography opcodes are not considered complex by default. Refer to the "Cryptography" for a separate assessment.

#### Modified opcodes

Modifies pre-existing opcodes 

- 0. No pre-existing opcode modifications are introduced.
- 3. At least one pre-existing opcode's behavior is modified (not including gas changes).

#### Added precompiles

Introduces new precompiles 

- 0. No new precompiles are introduced.
- 1. A new simple precompile is introduced (constant input length, constant gas cost).
- 2. Multiple new simple precompiles are introduced, or a single new complex precompile is introduced (dynamic input length or dynamic gas cost).
- 3. Multiple new precompiles are introduced, and at least one of them is complex (dynamic input length or dynamic gas cost).

*Cryptography precompiles are not considered complex by default. Refer to the "Cryptography" for a separate assessment.

#### Modified precompiles

Modifies pre-existing precompiles logic or gas-accounting 

- 0. No pre-existing precompiles are modified.
- 1. At least one pre-existing precompile has its gas schedule modified.
- 2. Multiple pre-existing precompiles have their gas schedule modified, or a single pre-existing precompile has its behavior modified.
- 3. Multiple pre-existing precompiles have their behavior modified.

#### Encoding changes (RLP/SSZ)

Introduces encoding changes at the transaction/block/interfaces level 

- 0. No encoding changes are introduced at the transaction, block, or interfaces levels.
- 3. An encoding change is introduced at transaction, block or interfaces level (e.g. RLP -> SSZ).

#### New transaction types

Introduces a new transaction type 

- 0. No new transaction types are introduced.
- 3. A new transaction type is introduced.

#### New transaction validity mechanisms

Modifies pre-existing transaction types' validation mechanisms 

- 0. No changes are introduced to the validity rules of existing transaction types or to their intrinsic gas cost calculation.
- 1. Minor adjustments are introduced to validity rules or intrinsic gas cost calculation, but they do not significantly affect existing tests.
- 2. Changes to validity rules or intrinsic gas cost calculation affect existing tests, but require only limited updates to test cases and no redesign of the testing infrastructure.
- 3. Changes to validity rules or intrinsic gas cost calculation require extensive rework or redesign of the testing infrastructure.

#### New block / header fields

Introduces new block or block header fields 

- 0. No new block or header fields are introduced.
- 3. A new block or header field is introduced.

#### New fork activation mechanism

Modifies state, internal variables, or similar, at the fork activation block 

- 0. No state modifications, internal variables or similar are modified at the fork activation block.
- 3. Either a state modification or an internal variable is modified at the fork activation block.

*Initialization of new internal variable is not considered modification.

#### Performance risks

Introduces or modifies mechanisms and requires performance validation.

- 0. No new mechanisms are introduced that require performance validation.
- 1. The introduced mechanisms can be benchmarked in isolation and do not affect existing performance behavior.
- 2. The introduced mechanisms cannot be fully benchmarked in isolation, or they have a limited impact on existing performance benchmarks.
- 3. The introduced mechanisms cannot be benchmarked in isolation and have a substantial impact on existing performance benchmarks or have complex interactions with existing mechanisms.

### Checklist

| Anchor | Score (0–3) |
|---|---:|
| **EVM Gas rule changes** |   |
| **Blob gas accounting changes** |   |
| **New EVM gas refund** |   |
| **Patterns affecting pre-existing tests** |   |
| **Transition-tool interface changes** |   |
| **Cryptography-related testing** |   |
| **Edge/boundary conditions** |   |
| **Block syncing changes** |   |
| **Engine API changes** |   |
| **Engine API encoding changes** |   |
| **Added system contracts** |   |
| **Modified system contracts** |   |
| **Added opcodes** |   |
| **Modified opcodes** |   |
| **Added precompiles** |   |
| **Modified precompiles** |   |
| **Encoding changes (RLP/SSZ)** |   |
| **New transaction types** |   |
| **New transaction validity mechanisms** |   |
| **New block / header fields** |   |
| **New fork activation mechanism** |   |
| **Performance risks** |   |

**Total: X**

### Special Considerations

> Evaluator must write here special considerations that make the EIP particularly complex to test due to reasons not directly included in this checklist.

### Final Assessment

| Category | Description | Value |
|-----------|--------------|:----:|
| **Total Score** | Sum of all anchor scores (0–66) | **`XX`** |
| **Complexity Tier** | Computed from total score | 🟢 / 🟡 / 🔴 |

#### Tier Interpretation

| Tier | Range | Meaning |
|------|--------|----------|
| 🟢 **Low Complexity** | **< 10** | Minor feature or localized change. Existing tests are largely unaffected. Does not require intensive cross-EIP testing. |
| 🟡 **Medium Complexity** | **>= 10<20** | Moderate change affecting multiple components. Requires moderate cross-EIP testing. |
| 🔴 **High Complexity** | **>=20** | Broad or deep impact on protocol behavior; high regression risk; and/or requiring intensive cross-EIP testing. |


# Consensus Specs

## Specs

## Testing

## Notes
