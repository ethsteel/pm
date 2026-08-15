---
description: Create an EIP complexity assessment using the standard template. Analyzes the EIP specification and scores 24 anchors for testing complexity.
argument-hint: <EIP-number>
model: opus
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(gh:*), WebFetch
---

# EIP Complexity Assessment

You are an expert Ethereum protocol analyst with deep knowledge of the EVM, consensus mechanisms, transaction types, system contracts, and the execution-specs testing framework. Your task is to create a comprehensive complexity assessment for EIP-$ARGUMENTS.

## Important: Think Deeply

This is a critical assessment that will guide testing efforts. Before scoring each anchor, think through:
- What specific mechanisms does this EIP introduce or modify?
- How does this interact with existing protocol components?
- What edge cases and boundary conditions exist?
- What is the testing burden for this change?

Take your time to analyze thoroughly. Accuracy is more important than speed.

## Step 1: Fetch the EIP Specification

Use WebFetch to retrieve the EIP markdown from:
`https://raw.githubusercontent.com/ethereum/EIPs/master/EIPS/eip-$ARGUMENTS.md`

Read the EIP carefully, noting:
- The abstract and motivation
- Specification details (new opcodes, precompiles, transaction types, etc.)
- Security considerations
- Backwards compatibility notes

## Step 2: Check for Open PRs to this EIP

Run this command to find open PRs that may modify this EIP:
```bash
gh api "search/issues?q=repo:ethereum/EIPs+is:pr+is:open+$ARGUMENTS+in:title" --jq '.items[] | "PR #\(.number): \(.title)"'
```

Note any open PRs for the final assessment.

## Step 3: Read the Template and Examples

Read the template:
- `Templates/EIP-Complexity-Assessment.md`

Read 2-3 existing assessments for reference on scoring patterns and rationale style:
- `complexity_assessments/EIPs/EIP-7805.md` (medium complexity example)
- `complexity_assessments/EIPs/EIP-7708.md` (low complexity example)

## Step 4: Create the Assessment

For each of the 24 anchors in the checklist, analyze the EIP and determine:
1. **Score (0-3)**: Based on the anchor definitions in the template
2. **Rationale**: Brief justification referencing specific EIP mechanisms

### Anchors to Score

Score each anchor systematically:

1. **EVM Gas rule changes** - New gas accounting rules?
2. **Blob gas accounting changes** - Blob-related gas changes?
3. **New EVM gas refund** - New refund mechanisms?
4. **Patterns affecting pre-existing tests** - Will existing tests need updates?
5. **Transition-tool interface changes** - New t8n fields/mechanisms?
6. **Cryptography** - New crypto primitives or algorithms?
7. **Edge/boundary conditions** - Boundary-prone mechanisms?
8. **Block syncing changes** - RLP validation changes?
9. **Engine API changes** - New fields or endpoints?
10. **Added system contracts** - New system contracts?
11. **Modified system contracts** - Changes to existing contracts?
12. **Added opcodes** - New EVM opcodes?
13. **Modified opcodes** - Changes to existing opcodes?
14. **Added precompiles** - New precompiled contracts?
15. **Modified precompiles** - Changes to existing precompiles?
16. **Encoding changes (RLP/SSZ)** - Encoding format changes?
17. **New transaction types** - New tx type introduced?
18. **New or modified transaction validity** - Validity rule changes?
19. **New block/header fields** - New header fields?
20. **New fork activation mechanism** - State changes at fork activation?
21. **Performance risks** - Performance validation needed?
22. **Security risks** - Security-sensitive mechanisms?
23. **Cross-EIP interactions** - Dependencies on other EIPs?

### Scoring Guidelines

- **0**: No impact in this category
- **1**: Minor/simple change, limited testing scope
- **2**: Moderate change, affects multiple components
- **3**: Major/complex change, extensive testing required
- **4**: Exceptional circumstances only (document why)

Some anchors only allow 0 or 3 (binary impact):
- Modified opcodes
- Encoding changes
- New transaction types
- New block/header fields
- New fork activation mechanism

## Step 5: Fill in the Specs Section

Under "Execution Specs > Specs", write a brief summary of the key specification changes this EIP introduces. Focus on what changes in the protocol, not the full EIP text.

## Step 6: Calculate Total and Determine Tier

Sum all anchor scores for the total (max 72).

Determine complexity tier:
- **< 10**: 🟢 Low Complexity
- **10-19**: 🟡 Medium Complexity
- **>= 20**: 🔴 High Complexity

## Step 7: Write Special Considerations and Notes

- **Special Considerations**: Factors that make this EIP particularly complex beyond the checklist
- **Notes**: Points for test authors that don't affect scoring

## Step 8: Handle Open PRs

If there are open PRs to this EIP, append a section at the end:

```markdown
---

## Open PRs Notice

At the time of writing this complexity assessment, EIP-$ARGUMENTS had the following open PRs to its specification:

- [List the PRs found in Step 2]

**Impact Assessment**: [Brief assessment of whether these PRs would materially change the complexity scores if merged]
```

## Step 9: Write the Assessment File

Write the complete assessment to:
`complexity_assessments/EIPs/EIP-$ARGUMENTS.md`

The file should follow the exact structure of the template, with all sections filled in.

## Output

After writing the file, provide a brief summary:
- Total score and complexity tier
- Key drivers of complexity (highest-scoring anchors)
- Any special considerations worth highlighting
