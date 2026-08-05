#!/usr/bin/env python3
"""Evaluate proposed checklist anchors against measured Amsterdam work.

Reads amsterdam-dataset.json (produced by calibrate.py) and reproduces every
figure in proposed-anchors.md. Stdlib only.

    python3 proposed-anchors.py

The proposed scores below are assigned in hindsight from repo evidence -- see
proposed-anchors.md §6 for why that limits what the fit statistics can claim.
"""

from __future__ import annotations

import json
import math
import re
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCORE_RE = re.compile(r"\|\s*\*\*Total Score\*\*\s*\|[^|]*\|\s*\**`?(\d+)`?\**\s*\|")
MATURE_WEEKS = 10.0

# ---------------------------------------------------------------------------
# Proposed anchor scores. Evidence for each is cited in proposed-anchors.md §3.
#
#   O  sub-opcode failure-point observability  -- MULTIPLIER, x 2^(O/2)
#   G  state gas accounting changes            -- additive
#   U  specification underdetermination        -- additive
#   P  test-framework primitives required      -- additive
#   R  retroactive expectation obligation      -- additive
# ---------------------------------------------------------------------------
O = {"7928": 3, "8037": 1, "8038": 1}
G = {"8037": 3, "8038": 2}
U = {"7928": 3, "8037": 2, "8038": 2, "2780": 1}
P = {"7928": 3, "8037": 2, "8070": 2, "7778": 1, "7708": 1, "7843": 1,
     "8024": 1, "7976": 1, "7981": 1}
R = {"7928": 3, "8037": 3, "8038": 2, "2780": 2, "7708": 1, "7843": 1, "8024": 1}

MULT_BASE = 2.0  # multiplier is MULT_BASE ** (O / 2)


def g(d: dict, eip: str) -> int:
    return d.get(eip, 0)


# ------------------------------------------------------------------ load data
data = json.loads((HERE / "amsterdam-dataset.json").read_text())
scores: dict[str, int] = {}
for f in sorted((HERE.parent / "EIPs").glob("EIP-*.md")):
    if m := SCORE_RE.search(f.read_text()):
        scores[f.stem.split("-")[1]] = int(m.group(1))

for r in data["eips"]:
    r["TEU"] = round(r["prs"] + r["review_load"] / 10, 1)
    r["base"] = scores.get(r["eip"])
rows = [r for r in data["eips"] if r["base"]]
mature = [r for r in rows if r["weeks"] >= MATURE_WEEKS]
BASE = {r["eip"]: r["base"] for r in rows}


# ---------------------------------------------------------------------- stats
def ols(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    b = sum((a - mx) * (c - my) for a, c in zip(xs, ys)) / sum((a - mx) ** 2 for a in xs)
    return my - b * mx, b


def pearson(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    return (sum((a - mx) * (b - my) for a, b in zip(xs, ys))
            / (math.sqrt(sum((a - mx) ** 2 for a in xs))
               * math.sqrt(sum((b - my) ** 2 for b in ys))))


def fit(subset, score_of):
    a, k = ols([math.log(score_of(r["eip"])) for r in subset],
               [math.log(r["TEU"]) for r in subset])
    return math.exp(a), k


def loo(subset, score_of):
    errs = []
    for held in subset:
        A, k = fit([r for r in subset if r is not held], score_of)
        errs.append(abs(A * score_of(held["eip"]) ** k - held["TEU"]) / held["TEU"] * 100)
    return statistics.median(errs)


def out_of_sample(subset, score_of, eip="7928"):
    """Fit without `eip`, then predict it. The honest test of a proposal."""
    A, k = fit([r for r in subset if r["eip"] != eip], score_of)
    actual = next(r["TEU"] for r in subset if r["eip"] == eip)
    return A * score_of(eip) ** k, actual


# --------------------------------------------------------------- §1 back-solve
print("=" * 74)
print("1. WHAT SCORE WOULD EACH EIP NEED TO LAND ON THE MEASURED CURVE?")
print("=" * 74)
A0, K0 = fit(mature, lambda e: BASE[e])
print(f"\ncurrent calibration: TEU = {A0:.2f} * S^{K0:.2f}\n")
print(f"{'EIP':>6}{'scored':>8}{'implied':>9}{'gap':>7}   note")
for r in sorted(rows, key=lambda r: -r["TEU"]):
    imp = (r["TEU"] / A0) ** (1 / K0)
    note = "" if r["weeks"] >= MATURE_WEEKS else "in flight, ignore"
    star = "  <--" if abs(imp - r["base"]) > 5 and r["weeks"] >= MATURE_WEEKS else ""
    print(f"{r['eip']:>6}{r['base']:>8}{imp:>9.0f}{imp - r['base']:>+7.0f}   {note}{star}")

# ------------------------------------------------- §2 additive vs multiplier
print("\n" + "=" * 74)
print("2. THE SAME ANCHOR, ADDED vs MULTIPLIED")
print("=" * 74)
print("\nO scored identically in every row; only how it enters the total changes.")
print("Fit on the 8 other mature EIPs, then predict 7928.\n")
print(f"{'structure':40}{'S(7928)':>9}{'predicted':>11}{'vs actual':>12}{'LOO':>7}")
print("-" * 79)
STRUCTURES = [
    ("not scored at all (today)", lambda e: BASE[e]),
    ("additive 0-3 row", lambda e: BASE[e] + g(O, e)),
    ("additive row at 3x weight", lambda e: BASE[e] + 3 * g(O, e)),
    ("additive row at 5x weight", lambda e: BASE[e] + 5 * g(O, e)),
    ("multiplier  x 2^(O/2)", lambda e: BASE[e] * MULT_BASE ** (g(O, e) / 2)),
]
for label, fn in STRUCTURES:
    pred, actual = out_of_sample(mature, fn)
    print(f"{label:40}{fn('7928'):>9.0f}{pred:>11.0f}{pred / actual:>11.2f}x"
          f"{loo(mature, fn):>6.0f}%")

# ------------------------------------------------------------- §4 validation
print("\n" + "=" * 74)
print("4. VALIDATION OF THE FULL PROPOSAL")
print("=" * 74 + "\n")

MODELS = [
    ("current checklist", lambda e: BASE[e]),
    ("+ four additive rows only",
     lambda e: BASE[e] + g(U, e) + g(P, e) + g(R, e) + g(G, e)),
    ("+ sub-opcode multiplier",
     lambda e: (BASE[e] + g(U, e) + g(P, e) + g(R, e)) * MULT_BASE ** (g(O, e) / 2)),
    ("+ multiplier + state gas row",
     lambda e: (BASE[e] + g(U, e) + g(P, e) + g(R, e) + g(G, e))
     * MULT_BASE ** (g(O, e) / 2)),
]
print(f"{'model':32}{'r':>7}{'k':>6}{'LOO':>7}{'7928':>8}{'8037':>8}")
print("-" * 68)
for label, fn in MODELS:
    A, k = fit(mature, fn)
    ratios = {r["eip"]: r["TEU"] / (A * fn(r["eip"]) ** k) for r in mature}
    print(f"{label:32}{pearson([fn(r['eip']) for r in mature], [r['TEU'] for r in mature]):>7.3f}"
          f"{k:>6.2f}{loo(mature, fn):>6.0f}%{ratios['7928']:>8.2f}{ratios['8037']:>8.2f}")

final = MODELS[-1][1]
A, k = fit(mature, final)
print(f"\nS_eff = (base + U + P + R + G) x {MULT_BASE:.0f}^(O/2)")
print(f"TEU   = {A:.2f} * S_eff^{k:.2f}\n")
print(f"{'EIP':>6}{'base':>6}{'U':>3}{'P':>3}{'R':>3}{'G':>3}{'add':>6}{'O':>3}"
      f"{'S_eff':>8}{'TEU':>8}{'pred':>8}{'ratio':>7}{'tier':>6}")
for r in sorted(rows, key=lambda r: -final(r["eip"])):
    e = r["eip"]
    add = BASE[e] + g(U, e) + g(P, e) + g(R, e) + g(G, e)
    se = final(e)
    tier = "🔴" if se >= 34 else ("🟡" if se >= 12 else "🟢")
    flag = "" if r["weeks"] >= MATURE_WEEKS else "  in flight"
    print(f"{e:>6}{BASE[e]:>6}{g(U, e):>3}{g(P, e):>3}{g(R, e):>3}{g(G, e):>3}{add:>6}"
          f"{g(O, e):>3}{se:>8.1f}{r['TEU']:>8}{A * se ** k:>8.1f}"
          f"{r['TEU'] / (A * se ** k):>7.2f}{tier:>5}{flag}")

print(f"\nexponent: {K0:.2f} (current) -> {k:.2f} (with the multiplier)")
print("The 1.6 exponent was the power law compensating for a missing product term.")

# ------------------------------------------------------------------- §5 tiers
print("\n" + "=" * 74)
print("5. TIER MEMBERSHIP UNDER S_eff")
print("=" * 74 + "\n")
for tier, lo, hi in (("🟢 Low", 0, 12), ("🟡 Medium", 12, 34), ("🔴 High", 34, 1e9)):
    members = sorted((r["eip"] for r in rows if lo <= final(r["eip"]) < hi),
                     key=lambda e: final(e))
    print(f"{tier:12} S_eff {lo:>3}-{hi if hi < 1e9 else '':<4}  {' '.join(members)}")
print(f"\nadditive ceiling 72 -> 84 (four new rows); S_eff ceiling "
      f"84 * {MULT_BASE ** 1.5:.2f} = {84 * MULT_BASE ** 1.5:.0f}")
