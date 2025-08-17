# EIP-NNNN: EIP Title

Link: https://eips.ethereum.org/EIPS/eip-NNNN

## Execution Spec Tests

### Complexity Assessment

**Scoring rubric per row (0–3):**
- **0**: Not applicable, this spec change does not affect this area at all  
- **1**: Introduces a new but simple mechanism that does not affect existing mechanisms  
- **2**: Introduces a new and complex mechanism **or** affects existing mechanisms  
- **3**: Introduces a new and complex mechanism **and** affects existing mechanisms  


| Dimension | What to verify (system-level tests) | Multiplier | Score (0–3) | Total |
|---|---|---:|:---:|:---:|
| **EVM Gas rule changes** | New EVM gas accounting rules | 1.0 | [ ] | [ ] |
| **Blob gas accounting changes** | New Blob gas accounting rules which potentially affect pre-existing tests | 1.0 | [ ] | [ ] |
| **New EVM gas refund** | New gas-refund mechanism (0 or 3) | 0.5 | [ ] | [ ] |
| **Patterns affecting pre-existing tests** | Implements a new validation mechanism or rule that translates in reworking pre-existing tests | 2.0 | [ ] | [ ] |
| **Transition-tool interface changes** | Modifies or adds new fields to the transition tool interface. | 2.0 | [ ] | [ ] |
| **Cryptography-related testing** | Introduces new cryptography mechanisms or modifies existing functionality that involves cryptography | 1.0 | [ ] | [ ] |
| **Edge/boundary conditions** | Feature contains edge/boundary conditions | 1.5 | [ ] | [ ] |
| **Block syncing changes** | Modifies block RLP validation mechanisms that requires test client syncing | 1.5 | [ ] | [ ] |
| **Engine API changes** | Introduces new fields to the Engine API directives | 1.5 | [ ] | [ ] |
| **Engine API encoding changes** | Introduces changes to the encoding or communication mechanism in the Engine API | 2.0 | [ ] | [ ] |
| **Added system contracts** | Introduces new system contract, stateful or not | 1.0 | [ ] | [ ] |
| **Modified system contracts** | Modifies pre-existing system contracts | 1.0 | [ ] | [ ] |
| **Added opcodes** | Introduces new opcodes | 1.0 | [ ] | [ ] |
| **Modified opcodes** | Modifies pre-existing opcodes | 1.0 | [ ] | [ ] |
| **Added precompiles** | Introduces new precompiles | 1.0 | [ ] | [ ] |
| **Modified precompiles** | Modifies pre-existing pre-compiles logic or gas-accounting | 1.0 | [ ] | [ ] |
| **Encoding changes (RLP/SSZ)** | Introduces encoding changes at the transaction/block/interfaces level | 2.0 | [ ] | [ ] |
| **New transaction types** | Introduces a new transaction type | 1.5 | [ ] | [ ] |
| **New transaction validity mechanisms** | Modifies pre-existing transaction types' validation mechanisms | 1.5 | [ ] | [ ] |
| **New block / header fields** | Introduces new block or block header fields | 1.5 | [ ] | [ ] |
| **New fork activation mechanism** | Modifies state, internal variables, or similar, at the fork activation block | 2.5 | [ ] | [ ] |
| **Performance risks** | Introduces or modifies mechanisms and requires performance validation | 1.0 | [ ] | [ ] |

> **Weighted total** = Σ(Multiplier × score).
> **Maximum total** = 90.

**Subtotal (Σ weights × scores):** **[ ]**

### Notes

### Gates
Any of the following gates results in automatic complexity increment.

- [ ] EIP affects 20% or more of the pre-existing tests.

#### Legend:

✅: Gate is not triggered
❌: Gate is triggered

### Color thresholds (by weighted subtotal)
- **🟢**: ≤ 10% of max (and all Gates ✅)
- **🟡**: 10–25% of max (and all Gates ✅)
- **🟠**: 25–50% of max **or** any Gate ❌
- **🔴**: > 50% of max **or** any Gate ❌

## Consensus Spec Tests

TBD