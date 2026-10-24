"""design_ledger.py - enforce the HARD RULE: a new design for every post every week.

Every lane picks its per-post art-directions ("worlds") THROUGH this ledger instead
of a fixed weekly rotation. The ledger records which worlds each lane used each week
and, when picking, EXCLUDES any world used in the recent lookback window. If the
bank is too shallow, the build fails instead of silently shipping stale creative.
Set IW_ALLOW_STALE_DESIGN=1 only for an explicit emergency fallback.

  worlds = design_ledger.pick("quote", QUOTE_WORLDS, 5, "week16")   # choose + reserve
  design_ledger.record("quote", "week16", worlds)                    # commit after render

Kept deliberately tiny and file-based (matches the education topic-dedup pattern).
"""
from __future__ import annotations
import hashlib
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
SM = os.path.dirname(HERE)
LEDGER = os.path.join(SM, "content", "design_ledger.json")
DEFAULT_AVOID_WEEKS = 2
ALLOW_STALE_ENV = "IW_ALLOW_STALE_DESIGN"


class DesignFreshnessError(RuntimeError):
    """Raised when a lane cannot satisfy the weekly fresh-direction rule."""



def _weeknum(wid):
    try:
        return int("".join(c for c in str(wid) if c.isdigit()))
    except ValueError:
        return -1


def _load():
    try:
        return json.load(open(LEDGER))
    except Exception:
        return {"used": []}


def _save(d):
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    json.dump(d, open(LEDGER, "w"), indent=2, ensure_ascii=False)
    open(LEDGER, "a").write("\n")


def _last_used(used, lane):
    """world -> most-recent week number it was used in this lane (-1 if never)."""
    lu = {}
    for u in used:
        if u.get("lane") == lane:
            lu[u["world"]] = max(lu.get(u["world"], -1), _weeknum(u.get("week")))
    return lu


def stale_fallback_allowed():
    return os.getenv(ALLOW_STALE_ENV, "").strip().lower() in {"1", "true", "yes", "on"}


def _recent_weeks(used, lane, wid, avoid_weeks):
    wn = _weeknum(wid)
    return sorted({_weeknum(u["week"]) for u in used
                   if u.get("lane") == lane and _weeknum(u["week"]) != wn},
                  reverse=True)[:avoid_weeks]


def _blocked_worlds(used, lane, recent_weeks):
    return {u["world"] for u in used
            if u.get("lane") == lane and _weeknum(u["week"]) in recent_weeks}


def cycle_weeks(bank, n):
    """How many consecutive weeks this bank can serve with no world repeating.
    A bank of 18 picked 5-at-a-time only lasts 3 weeks, so no scheduling policy
    can push a repeat past week 4 - only a bigger bank can."""
    return max(1, len(bank) // max(1, n))


def _jitter(lane, wid, world):
    """Stable tie-break key. Worlds used in the SAME week share a last-used
    value, and Python's sort is stable, so they used to come back out in bank
    order - as a block. That is why whole weeks recurred verbatim (week15 ==
    week18 == 5/5 identical). Hashing (lane, week, world) shuffles within a tie
    tier so the GROUPING changes every cycle even when the gap cannot.
    hashlib, not hash(): str hashing is salted per process, which would make
    re-renders of the same week pick different designs."""
    return hashlib.sha1(f"{lane}|{wid}|{world}".encode()).hexdigest()


def pick(lane, bank, n, wid, avoid_weeks=None, strict=True):
    """Choose `n` worlds for `lane`/`wid`: block the worlds used in the recent
    window, then take the least-recently-used, breaking ties with a per-week
    hash so consecutive cycles do not reproduce the same cohort. The window
    defaults to everything the bank can afford (cycle_weeks - 1) rather than a
    flat 2, so a deep bank actually buys a longer gap. In strict mode, fail if
    the bank cannot satisfy the rule. Deterministic given the ledger + bank.
    Does not write."""
    if avoid_weeks is None:
        avoid_weeks = max(DEFAULT_AVOID_WEEKS, cycle_weeks(bank, n) - 1)
    used = _load().get("used", [])
    recent_weeks = _recent_weeks(used, lane, wid, avoid_weeks)
    blocked = _blocked_worlds(used, lane, recent_weeks)
    lu = _last_used(used, lane)
    fresh = sorted([w for w in bank if w not in blocked],
                   key=lambda w: (lu.get(w, -1), _jitter(lane, wid, w)))
    if len(fresh) >= n:
        return fresh[:n]
    if strict and not stale_fallback_allowed():
        missing = n - len(fresh)
        weeks = ", ".join(f"week{w}" for w in recent_weeks) or "recent weeks"
        raise DesignFreshnessError(
            f"{lane} needs {n} fresh design direction(s) for {wid}, but only "
            f"{len(fresh)} are available after blocking {weeks}. Add at least "
            f"{missing} new {lane} world(s), or set {ALLOW_STALE_ENV}=1 for an "
            "explicit one-off stale-design fallback."
        )
    print(f"WARNING: stale design fallback for {lane}/{wid}; add {n - len(fresh)} new world(s).")
    rest = sorted([w for w in bank if w in blocked],
                  key=lambda w: (lu.get(w, -1), _jitter(lane, wid, w)))
    return (fresh + rest)[:n]


def record(lane, wid, worlds):
    """Commit the worlds a lane used this week (replaces any prior entry for the pair)."""
    d = _load()
    d["used"] = [u for u in d.get("used", []) if not (u.get("lane") == lane and u.get("week") == wid)]
    for w in worlds:
        d["used"].append({"lane": lane, "week": wid, "world": w})
    _save(d)


def shortfall(lane, bank, n, wid, avoid_weeks=None):
    """How many posts this week are forced to reuse a recent world (0 = fully fresh).
    A positive number means author that many more worlds for the lane."""
    if avoid_weeks is None:
        avoid_weeks = max(DEFAULT_AVOID_WEEKS, cycle_weeks(bank, n) - 1)
    used = _load().get("used", [])
    recent_weeks = _recent_weeks(used, lane, wid, avoid_weeks)
    blocked = _blocked_worlds(used, lane, recent_weeks)
    fresh = [w for w in bank if w not in blocked]
    return max(0, n - len(fresh))
