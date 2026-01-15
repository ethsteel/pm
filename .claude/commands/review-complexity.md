---
description: Review a complexity assessment PR or local file. Validates scores against the EIP specification and provides structured feedback.
argument-hint: <PR-number or file-path>
model: opus
allowed-tools: Read, Grep, Glob, Bash(gh:*), WebFetch
---

# Complexity Assessment Review

You are an expert Ethereum protocol analyst reviewing a complexity assessment. Your role is to validate the assessment's accuracy, identify any scoring issues, and provide constructive feedback.

## Important: Use Extended Thinking

Complexity assessments guide testing prioritization. An incorrect score could lead to:
- Under-testing of critical changes (if scored too low)
- Wasted resources on simple changes (if scored too high)

For each scored anchor, think through:
- Does the EIP actually introduce/modify what this anchor measures?
- Is the score consistent with the rubric definition (0-3 scale)?
- Does the rationale accurately reflect the EIP specification?
- Are there mechanisms the assessor may have missed?

Take your time to analyze thoroughly. Accuracy is more important than speed.

## Step 1: Determine Input Type

The argument is: `$ARGUMENTS`

Determine if this is:
- **PR number**: A plain number (e.g., `27`, `123`) → fetch from GitHub PR
- **File path**: Contains `/` or `.md` (e.g., `complexity_assessments/EIPs/EIP-7971.md`) → read local file

## Step 2: Fetch the Assessment

### If PR number:

Get the PR information:
```bash
gh pr view $ARGUMENTS --json title,body,author,files,additions,deletions
```

Get the PR diff to see the assessment content:
```bash
gh pr diff $ARGUMENTS
```

### If local file:

Read the file directly using the Read tool with the provided path.

If the path is relative, it's relative to the repository root.

---

From the assessment, identify:
- Which EIP is being assessed (from the file name, e.g., `EIP-7971.md` → EIP-7971)
- What scores and rationales were provided in the checklist table

## Step 3: Fetch the EIP Specification

Extract the EIP number from the assessment file name (e.g., `EIP-1234.md` → 1234).

Fetch the EIP using WebFetch:
```
https://raw.githubusercontent.com/ethereum/EIPs/master/EIPS/eip-{number}.md
```

Read the EIP thoroughly to understand the actual specification.

## Step 4: Read the Assessment Template

Read `Templates/EIP-Complexity-Assessment.md` to understand:
- The scoring rubric for each anchor (0-3 scale)
- Which anchors are binary (0 or 3 only)
- What constitutes proper rationale

## Step 5: Review Each Scored Anchor

For each anchor in the assessment's checklist table:

1. **Verify the score is appropriate** based on the EIP specification and anchor rubric
2. **Check the rationale** is sufficient and accurate
3. **Note any discrepancies** between the score and EIP content

### Common Issues to Look For

**Under-scoring (score too low):**
- EIP introduces mechanism but anchor scored 0
- Complex mechanism scored as simple (1 instead of 2-3)
- Missing consideration of indirect effects

**Over-scoring (score too high):**
- Score of 2-3 without clear justification
- Assuming complexity that isn't in the EIP
- Double-counting (same mechanism counted in multiple anchors)

**Rationale issues:**
- Empty rationale for non-zero scores
- Rationale doesn't match the score given
- Vague rationale that doesn't reference specific EIP mechanisms

**Binary anchor violations:**
- These anchors should only be 0 or 3:
  - Modified opcodes
  - Encoding changes (RLP/SSZ)
  - New transaction types
  - New block/header fields
  - New fork activation mechanism

## Step 6: Verify Totals and Tier

1. Sum the individual scores - does it match the stated total?
2. Verify the complexity tier matches the total:
   - < 10 → 🟢 Low Complexity
   - 10-19 → 🟡 Medium Complexity
   - >= 20 → 🔴 High Complexity

## Step 7: Review Special Considerations and Notes

- Are there complexity factors not captured in the anchors?
- Are the notes helpful for future test authors?
- Is anything missing that should be called out?

## Step 8: Check Specs Section

- Is the "Specs" section filled in with a meaningful summary?
- Does it accurately reflect the EIP's key changes?

## Step 9: Provide Structured Feedback

Present your review in this format:

---

## Review: EIP-{number} Complexity Assessment

**Source**: [PR #X | Local file: path/to/file.md]

### Summary
- **Overall Assessment**: [Approve / Request Changes / Comment]
- **Total Score Accuracy**: [Correct / Incorrect (explain)]
- **Complexity Tier**: [Correct / Incorrect]

### Scoring Review

| Anchor | Submitted | Suggested | Issue |
|--------|-----------|-----------|-------|
| [Only list anchors with issues] | | | |

### Detailed Feedback

#### Scores to Adjust
[List any scores that should be changed, with reasoning]

#### Missing Considerations
[Any factors not accounted for in the assessment]

#### Rationale Improvements
[Suggestions for better justifying scores]

### Recommendations

[Actionable next steps for the author]

---

## Output

Provide your complete review following the format above. Be constructive and specific - the goal is to improve the assessment's accuracy, not to criticize.
