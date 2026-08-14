#!/usr/bin/env python3
"""Calibrate EIP complexity-assessment scores against measured execution-specs work.

Measures, per EIP, the testing work that landed in ethereum/execution-specs, then
fits it against the Total Score from complexity_assessments/EIPs/EIP-<n>.md.

    python3 calibrate.py --specs-repo ~/src/execution-specs

Needs `gh` authenticated (PR metadata). Pass --collect to recount filled test
cases via the execution-specs venv; otherwise cached counts in the dataset are
reused. See README.md for the model and its caveats. Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import subprocess
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSESSMENTS = HERE.parent / "EIPs"

SCORE_RE = re.compile(r"\|\s*\*\*Total Score\*\*\s*\|[^|]*\|\s*\**`?(\d+)`?\**\s*\|")
ROW_RE = re.compile(r"^\|\s*\*\*(.+?)\*\*\s*\|([^|]*)\|", re.M)
PR_RE = re.compile(r"\(#(\d+)\)\s*$")
REVISION_RE = re.compile(r"Checklist revision:\s*\*\*(\d+)\*\*")
EIP_TEXT_RE = re.compile(r"eip[-_ ]?(\d{4})", re.IGNORECASE)
GIT_TS = "%Y-%m-%dT%H:%M:%SZ"

# Machine-ported trees. ~2.3M lines of churn in Amsterdam alone; including them
# would swamp every hand-written signal.
GENERATED_PREFIXES = ("tests/ported_static/", "tests/static/")
# The EEST -> execution-specs weld. Before this there is no `tests/` tree here.
WELD_DATE = "2025-10-21"
# EIPs whose work started fewer than this many weeks ago are measured but held
# out of the fit: their totals are truncated, not small.
MATURE_WEEKS = 10.0


# --------------------------------------------------------------- assessments
def read_assessments(revision: int) -> tuple[dict[str, int], dict[str, dict[str, int]]]:
    """Return {eip: total_score} and {eip: {anchor: score}} for one checklist revision.

    Scores are not comparable across checklist revisions -- revision 2 added five
    anchors and uncapped one -- so pooling them into a single regression silently
    contaminates the fit. Assessments with no revision line predate the marker and
    count as revision 1.
    """
    scores: dict[str, int] = {}
    anchors: dict[str, dict[str, int]] = {}
    skipped: dict[int, list[str]] = defaultdict(list)
    for path in sorted(ASSESSMENTS.glob("EIP-*.md")):
        eip = path.stem.split("-")[1]
        text = path.read_text()
        m_rev = REVISION_RE.search(text)
        found = int(m_rev.group(1)) if m_rev else 1
        if found != revision:
            if SCORE_RE.search(text):
                skipped[found].append(eip)
            continue
        if m := SCORE_RE.search(text):
            scores[eip] = int(m.group(1))
        start = text.find("### Checklist")
        if start < 0:
            continue
        end = text.find("#### Special", start)
        rows = {}
        for name, value in ROW_RE.findall(text[start : end if end > 0 else len(text)]):
            # Cells read "3 + 3 + 3" when an anchor is counted more than once.
            if nums := [int(x) for x in re.findall(r"\d+", value)]:
                rows[name.strip()] = sum(nums)
        if rows:
            anchors[eip] = rows
    for rev, eips in sorted(skipped.items()):
        print(f"skipped {len(eips)} scored assessment(s) on revision {rev}: "
              f"{', '.join(sorted(eips))}", file=sys.stderr)
    return scores, anchors


# ------------------------------------------------------------------ git side
def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True, check=True).stdout


def resolve_rev(repo: Path, rev: str) -> str:
    """Pin the measurement to one commit.

    Everything -- churn, PR set, and the file measures below -- is read from this
    sha, so a re-run with the same --rev is byte-identical. Do not bound the log
    by date instead: --until filters on committer date, which rebases mutate, and
    it cannot exclude a commit rebased into the window later.
    """
    try:
        return git(repo, "rev-parse", "--verify", f"{rev}^{{commit}}").strip()
    except subprocess.CalledProcessError:
        sys.exit(f"cannot resolve --rev {rev!r} in {repo}")


def tip_date(repo: Path, rev: str) -> date:
    """Commit date of the pinned rev, used as 'today' for the maturity cutoff."""
    return date.fromisoformat(git(repo, "log", "-1", "--format=%ad",
                                  "--date=short", rev).strip())


def suites_at(repo: Path, fork: str, rev: str) -> dict[str, str]:
    """{eip: dirname} for the EIP test suites present at `rev`."""
    out = git(repo, "ls-tree", "-d", "--name-only", rev, f"tests/{fork}/")
    found = {}
    for line in out.splitlines():
        if m := re.search(rf"tests/{fork}/(eip(\d+)_\S*)", line.strip()):
            found[m.group(2)] = m.group(1)
    return found


def git_log(repo: Path, rev: str) -> list[dict]:
    """One entry per squash-merged commit, with numstat per file."""
    out = git(repo, "log", rev, f"--since={WELD_DATE}", "--numstat",
              "--no-merges", "--format=__C__%H|%ad|%an|%s", "--date=short")
    commits: list[dict] = []
    cur: dict | None = None
    for line in out.splitlines():
        if line.startswith("__C__"):
            sha, day, author, subject = line[5:].split("|", 3)
            cur = {"sha": sha, "date": day, "author": author, "subject": subject, "files": []}
            commits.append(cur)
        elif cur is not None and "\t" in line:
            parts = line.split("\t")
            if len(parts) == 3:
                add, dele, path = parts
                cur["files"].append((int(add) if add.isdigit() else 0,
                                     int(dele) if dele.isdigit() else 0, path))
    return commits


def classify(path: str, fork: str) -> tuple[str, str | None]:
    """Bucket a changed path, returning (kind, owning_eip_or_None)."""
    if m := re.search(rf"tests/{fork}/eip(\d+)_", path):
        return "own", m.group(1)
    if path.startswith(GENERATED_PREFIXES):
        return "generated", None
    if path.startswith("src/ethereum/forks/"):
        return "eels", None
    # The test framework lives in packages/testing/ post-reorg; src/ethereum_test*
    # no longer exists. src/ethereum_spec_tools is the t8n/b11r tooling.
    if path.startswith(("packages/testing", "packages/tests", "src/ethereum_spec_tools",
                        "src/ethereum_optimized", "scripts/")):
        return "framework", None
    if path.startswith("tests/"):
        return "existing_tests", None
    return "meta", None


def group_units(commits: list[dict]) -> dict[tuple[str, object], list[dict]]:
    """Squash merges make one commit per PR; anything else is its own unit."""
    units: dict[tuple[str, object], list[dict]] = defaultdict(list)
    for c in commits:
        m = PR_RE.search(c["subject"])
        units[("pr", int(m.group(1))) if m else ("sha", c["sha"])].append(c)
    return units


def owners_of(unit: list[dict], fork: str, suites: set[str]) -> set[str]:
    """EIPs named in the subject win over EIPs whose directory was touched.

    A PR titled "merge EIP-8037 to forks/amsterdam" repairs eight other EIPs'
    tests as collateral. That is 8037's cost, not a cost shared eight ways.

    Titles are intersected with `suites` first. Without that, any 4-digit EIP
    mentioned in a subject becomes an owner -- 17 of them on forks/amsterdam,
    e.g. "EIP-7825 test fix to avoid failures on EIP-7976 ci run". Such phantoms
    have no row to be written to, so their units vanish from both the per-EIP
    rows and the baseline (22 units), and they inflate `n = len(owners)`, which
    dilutes the real owners' credit (EIP-7928 lost 2.0 PRs).
    """
    titled: set[str] = set()
    touched: set[str] = set()
    for c in unit:
        titled |= {m.group(1) for m in EIP_TEXT_RE.finditer(c["subject"])}
        for _, _, path in c["files"]:
            kind, eip = classify(path, fork)
            if kind == "own":
                touched.add(eip)
    return (titled & suites) or touched


# ------------------------------------------------------------- github side
def fetch_prs(numbers: list[int], repo: str, batch: int = 25) -> dict[int, dict]:
    """Batch PR metadata over GraphQL aliases. Requires an authenticated `gh`."""
    owner, name = repo.split("/")
    meta: dict[int, dict] = {}
    for i in range(0, len(numbers), batch):
        chunk = numbers[i : i + batch]
        fields = ("number createdAt mergedAt additions deletions changedFiles "
                  "comments{totalCount} reviews{totalCount} reviewThreads{totalCount}")
        aliases = " ".join(f"p{n}: pullRequest(number:{n}) {{ {fields} }}" for n in chunk)
        query = f'query {{ repository(owner:"{owner}", name:"{name}") {{ {aliases} }} }}'
        res = subprocess.run(
            ["gh", "api", "graphql", "-f", f"query={query}"],
            capture_output=True, text=True,
        )
        if res.returncode != 0:
            sys.exit(f"gh failed: {res.stderr.strip()[:400]}")
        for pr in json.loads(res.stdout)["data"]["repository"].values():
            if pr:
                meta[pr["number"]] = pr
        print(f"  fetched {min(i + batch, len(numbers))}/{len(numbers)} PRs", file=sys.stderr)
    return meta


# ------------------------------------------------------------------ measure
def measure(repo: Path, fork: str, rev: str, gh_repo: str, today: date,
            collect: bool, cached_cases: dict[str, int | None]) -> dict:
    commits = git_log(repo, rev)
    units = group_units(commits)
    suite_dirs = suites_at(repo, fork, rev)
    suites = set(suite_dirs)

    pr_numbers = sorted({n for kind, n in units if kind == "pr"
                         and owners_of(units[(kind, n)], fork, suites)})
    print(f"{len(commits)} commits, {len(units)} work units, "
          f"{len(pr_numbers)} EIP-owned PRs", file=sys.stderr)
    pr_meta = fetch_prs(pr_numbers, gh_repo)

    acc: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    owned: dict[str, set] = defaultdict(set)
    authors: dict[str, set] = defaultdict(set)
    days: dict[str, set] = defaultdict(set)
    lifetimes: dict[str, list[float]] = defaultdict(list)
    baseline: dict[str, float] = defaultdict(float)

    for key, unit in units.items():
        # Direct churn belongs to the directory's EIP regardless of who wrote it.
        for c in unit:
            for add, dele, path in c["files"]:
                kind, eip = classify(path, fork)
                if kind == "own":
                    acc[eip]["direct_churn"] += add + dele

        owners = owners_of(unit, fork, suites)
        if not owners:
            for c in unit:
                for add, dele, path in c["files"]:
                    baseline[classify(path, fork)[0]] += add + dele
            continue

        n = len(owners)
        for eip in owners:
            owned[eip].add(key)
            for c in unit:
                authors[eip].add(c["author"])
                days[eip].add(c["date"])

        for c in unit:
            for add, dele, path in c["files"]:
                kind, eip = classify(path, fork)
                churn = add + dele
                if kind == "own" and eip in owners:
                    continue  # already booked above
                bucket = "generated" if kind == "generated" else f"ripple_{kind}"
                for o in owners:
                    acc[o][bucket] += churn / n
                    if kind != "generated":
                        acc[o]["ripple_churn"] += churn / n

        if key[0] == "pr" and (pr := pr_meta.get(key[1])):
            load = (pr["reviews"]["totalCount"] + pr["reviewThreads"]["totalCount"]) / n
            for eip in owners:
                acc[eip]["review_load"] += load
                acc[eip]["changed_files"] += pr["changedFiles"] / n
            if pr.get("mergedAt"):
                span = (datetime.strptime(pr["mergedAt"], GIT_TS)
                        - datetime.strptime(pr["createdAt"], GIT_TS)).days
                for eip in owners:
                    lifetimes[eip].append(span)

    if collect:
        cases, cases_source = collect_cases(repo, fork, rev), "collected"
    else:
        cases, cases_source = dict(cached_cases), "inherited"

    rows = []
    for eip, dirname in sorted(suite_dirs.items(), key=lambda kv: kv[1]):
        sources = read_sources(repo, rev, f"tests/{fork}/{dirname}")
        a = acc[eip]
        first = min(days[eip]) if days[eip] else None
        rows.append({
            "eip": eip,
            "dir": dirname,
            "prs": len(owned[eip]),
            "authors": len(authors[eip]),
            "active_days": len(days[eip]),
            "first": first,
            "last": max(days[eip]) if days[eip] else None,
            "weeks": round((today - date(*map(int, first.split("-")))).days / 7, 1)
            if first else 0.0,
            "direct_churn": int(a["direct_churn"]),
            "ripple_churn": int(a["ripple_churn"]),
            "ripple_eels": int(a["ripple_eels"]),
            "ripple_framework": int(a["ripple_framework"]),
            "ripple_existing_tests": int(a["ripple_existing_tests"]),
            "generated": int(a["generated"]),
            "review_load": round(a["review_load"], 1),
            "changed_files": int(a["changed_files"]),
            "median_pr_days": statistics.median(lifetimes[eip]) if lifetimes[eip] else None,
            "loc": sum(len(s.splitlines()) for s in sources),
            "test_funcs": sum(len(re.findall(r"^def test_", s, re.M)) for s in sources),
            "py_files": len(sources),
            # None, not 0, when the count is genuinely unknown -- a fabricated
            # zero would silently produce a plausible-looking `filled cases` row.
            "cases": cases.get(eip),
        })
    return {"eips": rows, "baseline": {k: int(v) for k, v in baseline.items()},
            "n_units": len(units), "n_commits": len(commits),
            "cases_source": cases_source}


def read_sources(repo: Path, rev: str, prefix: str) -> list[str]:
    """Python sources under `prefix` as of `rev`, read from git rather than disk.

    Reading the working tree here would blend two repo states into one dataset:
    churn and PR metrics come from `rev`, so the file measures must too.
    """
    names = [n for n in git(repo, "ls-tree", "-r", "--name-only", rev,
                            f"{prefix}/").splitlines() if n.endswith(".py")]
    if not names:
        return []
    # --batch sizes are byte counts, so the stream must be walked as bytes.
    spec = "".join(f"{rev}:{n}\n" for n in names).encode()
    out = subprocess.run(["git", "-C", str(repo), "cat-file", "--batch"],
                         input=spec, capture_output=True, check=True).stdout
    sources, pos = [], 0
    for _ in names:
        nl = out.index(b"\n", pos)
        header = out[pos:nl].split()
        if len(header) < 3:
            sys.exit(f"unexpected cat-file header: {out[pos:nl]!r}")
        size = int(header[2])
        sources.append(out[nl + 1 : nl + 1 + size].decode(errors="replace"))
        pos = nl + 1 + size + 1  # trailing newline after each blob
    return sources


def collect_cases(repo: Path, fork: str, rev: str) -> dict[str, int]:
    """Count filled test cases per EIP. Reported for completeness only -- see
    README §5: vector counts track parametrization style, not work.

    `fill` runs against the checkout, not against `rev`, so this is the one
    measure that cannot be read from git; require the two to agree.
    """
    fill = repo / ".venv/bin/fill"
    if not fill.exists():
        sys.exit(f"--collect requires {fill}\n"
                 "run `uv sync` in the specs repo, or drop --collect to inherit "
                 "cached counts")
    head = git(repo, "rev-parse", "HEAD").strip()
    if head != rev:
        sys.exit(f"--collect needs the checkout to match the measured rev\n"
                 f"  HEAD {head[:12]} != rev {rev[:12]}\n"
                 f"run `git -C {repo} checkout {rev[:12]}` or drop --collect")
    out = subprocess.run(
        [str(fill), "--collect-only", "-q", f"--until={fork.capitalize()}", f"tests/{fork}"],
        cwd=repo, capture_output=True, text=True,
    ).stdout
    counts: dict[str, int] = defaultdict(int)
    for line in out.splitlines():
        if m := re.match(rf"tests/{fork}/eip(\d+)_", line):
            counts[m.group(1)] += 1
    return dict(counts)


# ---------------------------------------------------------------------- stats
def pearson(xs, ys) -> float:
    n = len(xs)
    if n < 3:
        return float("nan")
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    dx = math.sqrt(sum((a - mx) ** 2 for a in xs))
    dy = math.sqrt(sum((b - my) ** 2 for b in ys))
    return num / (dx * dy) if dx and dy else float("nan")


def ols(xs, ys) -> tuple[float, float]:
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    slope = (sum((a - mx) * (b - my) for a, b in zip(xs, ys))
             / sum((a - mx) ** 2 for a in xs))
    return my - slope * mx, slope


def power_fit(rows, key) -> tuple[float, float]:
    """effort = A * score^k, via OLS in log space."""
    a, k = ols([math.log(r["score"]) for r in rows],
               [math.log(max(r[key], 0.5)) for r in rows])
    return math.exp(a), k


def loo_error(rows, key, power=True) -> float:
    """Median leave-one-out |% error|, the only honest accuracy figure at n<15."""
    errs = []
    for held in rows:
        train = [r for r in rows if r is not held]
        actual = max(held[key], 0.5)
        if power:
            A, k = power_fit(train, key)
            pred = A * held["score"] ** k
        else:
            b = (sum(r["score"] * r[key] for r in train)
                 / sum(r["score"] ** 2 for r in train))
            pred = b * held["score"]
        errs.append(abs(pred - actual) / actual * 100)
    return statistics.median(errs)


def teu(row) -> float:
    return round(row["prs"] + row["review_load"] / 10, 1)


# --------------------------------------------------------------------- report
MEASURES = [("TEU", "TEU"), ("merged PRs", "prs"), ("review load", "review_load"),
            ("test functions", "test_funcs"), ("suite LoC", "loc"),
            ("total churn", "churn"), ("filled cases", "cases")]


def report(data: dict, scores: dict, anchors: dict) -> None:
    for r in data["eips"]:
        r["score"] = scores.get(r["eip"])
        r["churn"] = r["direct_churn"] + r["ripple_churn"]
        r["TEU"] = teu(r)

    scored = [r for r in data["eips"] if r["score"]]
    mature = [r for r in scored if r["weeks"] >= MATURE_WEEKS]
    if len(mature) < 4:
        sys.exit("not enough mature EIPs to fit")

    print(f"\n{'=' * 72}\nMEASURED WORK PER EIP\n{'=' * 72}\n")
    head = (f"{'EIP':>6}{'score':>6}{'TEU':>7}{'PRs':>5}{'revw':>6}{'funcs':>6}"
            f"{'LoC':>7}{'direct':>8}{'ripple':>8}{'gener':>7}{'wks':>5}")
    print(head + "\n" + "-" * len(head))
    for r in sorted(data["eips"], key=lambda r: -r["TEU"]):
        flag = "" if r["weeks"] >= MATURE_WEEKS else "  in flight"
        print(f"{r['eip']:>6}{str(r['score'] or '-'):>6}{r['TEU']:>7}{r['prs']:>5}"
              f"{r['review_load']:>6.0f}{r['test_funcs']:>6}{r['loc']:>7}"
              f"{r['direct_churn']:>8}{r['ripple_churn']:>8}{r['generated']:>7}"
              f"{r['weeks']:>5.0f}{flag}")
    print(f"\nunattributed baseline churn: {data['baseline']}")

    print(f"\n{'=' * 72}\nWHICH WORK MEASURE TRACKS THE SCORE?\n{'=' * 72}")
    print(f"(mature n={len(mature)}, all scored n={len(scored)})\n")
    print(f"{'measure':18}{'r(all)':>9}{'r(mature)':>11}{'LOO%':>7}{'exponent k':>12}")
    print("-" * 57)
    for label, key in MEASURES:
        # An unknown measure is omitted, never defaulted to 0: a fabricated row
        # here would look exactly like a real one.
        if any(r[key] is None for r in scored):
            missing = sum(1 for r in scored if r[key] is None)
            print(f"{label:18}{f'-- unknown for {missing}/{len(scored)} EIPs':>39}")
            continue
        print(f"{label:18}"
              f"{pearson([r['score'] for r in scored], [r[key] for r in scored]):>9.3f}"
              f"{pearson([r['score'] for r in mature], [r[key] for r in mature]):>11.3f}"
              f"{loo_error(mature, key):>7.0f}{power_fit(mature, key)[1]:>12.2f}")

    A, K = power_fit(mature, "TEU")
    lin = loo_error(mature, "TEU", power=False)
    print(f"\n{'=' * 72}\nCALIBRATION\n{'=' * 72}\n")
    print("  TEU = merged_PRs + (review_submissions + review_threads) / 10\n")
    print(f"  TEU = {A:.2f} * S^{K:.2f}"
          f"      r = {pearson([r['score'] for r in mature], [r['TEU'] for r in mature]):.3f}"
          f"   LOO = {loo_error(mature, 'TEU'):.0f}%")
    print(f"  linear model for comparison: LOO = {lin:.0f}%  "
          f"(power law {lin / loo_error(mature, 'TEU'):.1f}x better)")
    print(f"\n  doubling the score multiplies the work by 2^{K:.2f} = {2 ** K:.1f}x")

    print(f"\n{'EIP':>6}{'score':>6}{'TEU':>7}{'predicted':>11}{'ratio':>7}   note")
    for r in sorted(scored, key=lambda r: -r["score"]):
        pred = A * r["score"] ** K
        note = "" if r["weeks"] >= MATURE_WEEKS else f"held out ({r['weeks']:.0f}w in flight)"
        print(f"{r['eip']:>6}{r['score']:>6}{r['TEU']:>7}{pred:>11.1f}"
              f"{r['TEU'] / pred:>7.2f}   {note}")
    for r in sorted(data["eips"], key=lambda r: -r["TEU"]):
        if not r["score"]:
            print(f"{r['eip']:>6}{'-':>6}{r['TEU']:>7}{'':>11}{'':>7}   "
                  f"no assessment; back-solved S ~ {(r['TEU'] / A) ** (1 / K):.0f}")

    print(f"\n{'=' * 72}\nPLANNING TABLE\n{'=' * 72}\n")
    fits = {k: power_fit(mature, k) for _, k in MEASURES
            if not any(r[k] is None for r in mature)}
    cols = [("TEU", "TEU"), ("PRs", "prs"), ("review", "review_load"),
            ("tests", "test_funcs"), ("LoC", "loc"), ("churn", "churn")]
    print(f"{'S':>4}{'tier':>5}" + "".join(f"{h:>9}" for h, _ in cols) + f"{'vs S=5':>9}")
    print("-" * 68)
    base = fits["TEU"][0] * 5 ** fits["TEU"][1]
    for s in (3, 5, 8, 10, 13, 16, 20, 25, 30, 36):
        tier = "🟢" if s < 10 else ("🟡" if s < 20 else "🔴")
        vals = "".join(f"{fits[k][0] * s ** fits[k][1]:>9.0f}" for _, k in cols)
        print(f"{s:>4}{tier:>5}{vals}"
              f"{fits['TEU'][0] * s ** fits['TEU'][1] / base:>8.1f}x")

    total = sum(r["TEU"] for r in data["eips"])
    per_eip = sum(A * (r["score"] or 0) ** K for r in data["eips"])
    summed = A * sum(r["score"] or 0 for r in data["eips"]) ** K
    print(f"\nfork total: {total:.0f} TEU measured across {len(data['eips'])} suites")
    print(f"  sum of per-EIP predictions: {per_eip:.0f} TEU   <- apply the curve per EIP")
    print(f"  curve applied to summed score: {summed:.0f} TEU   <- wrong, {summed / per_eip:.1f}x too high")

    if anchors:
        print(f"\n{'=' * 72}\nPER-ANCHOR SIGNAL\n{'=' * 72}\n")
        eips = [r["eip"] for r in scored if r["eip"] in anchors]
        by_eip = {r["eip"]: r for r in scored}
        names = sorted({k for e in eips for k in anchors[e]})
        print(f"{'anchor':46}{'n>0':>5}{'r:churn':>9}{'r:funcs':>9}")
        print("-" * 69)
        table = []
        for name in names:
            xs = [anchors[e].get(name, 0) for e in eips]
            if not any(xs):
                continue
            table.append((
                sum(1 for v in xs if v > 0), name,
                pearson(xs, [by_eip[e]["churn"] for e in eips]),
                pearson(xs, [by_eip[e]["test_funcs"] for e in eips]),
            ))
        for nz, name, rc, rf in sorted(table, key=lambda t: -t[2]):
            warn = "  (single observation)" if nz <= 2 else ""
            print(f"{name[:45]:46}{nz:>5}{rc:>9.2f}{rf:>9.2f}{warn}")
        xs = [sum(anchors[e].values()) for e in eips]
        print(f"{'TOTAL (all rows)':46}{len(eips):>5}"
              f"{pearson(xs, [by_eip[e]['churn'] for e in eips]):>9.2f}"
              f"{pearson(xs, [by_eip[e]['test_funcs'] for e in eips]):>9.2f}")
        unused = [n for n in names if not any(anchors[e].get(n, 0) for e in eips)]
        if unused:
            print(f"\nnever scored above 0 in this fork (no evidence either way):")
            for n in unused:
                print(f"  - {n}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--specs-repo", type=Path, required=True,
                    help="clone of ethereum/execution-specs")
    ap.add_argument("--fork", default="amsterdam", help="fork name under tests/")
    ap.add_argument("--rev", default=None,
                    help="commit or ref to measure; default: upstream/forks/<fork>. "
                         "Reproduce a dataset by passing its recorded `rev`.")
    ap.add_argument("--gh-repo", default="ethereum/execution-specs")
    ap.add_argument("--collect", action="store_true",
                    help="recount filled test cases; needs the checkout to be at --rev")
    ap.add_argument("--today", default=None,
                    help="YYYY-MM-DD; default: the commit date of --rev")
    ap.add_argument("--revision", type=int, default=1,
                    help="checklist revision to fit; assessments on other revisions "
                         "are skipped, since scores are not comparable across them")
    ap.add_argument("--out", type=Path, default=None,
                    help="default: <fork>-dataset.json beside this script")
    args = ap.parse_args()

    repo = args.specs_repo.expanduser()
    rev = resolve_rev(repo, args.rev or f"upstream/forks/{args.fork}")
    out = args.out or HERE / f"{args.fork}-dataset.json"
    today = date.fromisoformat(args.today) if args.today else tip_date(repo, rev)
    print(f"rev {rev[:12]}  as-of {today}  revision {args.revision}", file=sys.stderr)

    # `cases` cannot be derived from git (see collect_cases), so it is inherited
    # from the dataset being replaced. Absent means unknown, not zero.
    cached: dict[str, int | None] = {}
    if out.is_file() and not args.collect:
        try:
            prior = json.loads(out.read_text())
        except (ValueError, OSError):
            prior = {}
            print(f"note: {out} is not a readable dataset; `cases` will be "
                  "unknown", file=sys.stderr)
        cached = {r["eip"]: r.get("cases") for r in prior.get("eips", [])}
        if prior.get("rev") and prior["rev"] != rev:
            print(f"note: inheriting `cases` from a dataset measured at "
                  f"{prior['rev'][:12]}", file=sys.stderr)

    scores, anchors = read_assessments(args.revision)
    print(f"{len(scores)} assessments with a Total Score", file=sys.stderr)

    data = measure(repo, args.fork, rev, args.gh_repo, today, args.collect, cached)
    data["rev"] = rev
    data["generated_on"] = today.isoformat()
    data["fork"] = args.fork
    data["checklist_revision"] = args.revision
    report(data, scores, anchors)
    out.write_text(json.dumps(data, indent=1) + "\n")
    print(f"\nwrote {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
