"""design_ledger.py - enforce the HARD RULE: a new design for every post every week.

Every lane picks its per-post art-directions ("worlds") THROUGH this ledger instead
of a fixed weekly rotation. The ledger records which worlds each lane used each week
and, when picking, EXCLUDES any world used in the last `avoid_weeks` weeks - so a
design never repeats week-to-week while the bank is deep enough. When a bank is too
shallow to avoid all recent worlds, it falls back to the least-recently-used ones
(and that shortfall is the signal to author more worlds for that lane).

  worlds = design_ledger.pick("quote", QUOTE_WORLDS, 5, "week16")   # choose + reserve
  design_ledger.record("quote", "week16", worlds)                    # commit after render

Kept deliberately tiny and file-based (matches the education topic-dedup pattern).
"""
from __future__ import annotations
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
SM = os.path.dirname(HERE)
LEDGER = os.path.join(SM, "content", "design_ledger.json")


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


def pick(lane, bank, n, wid, avoid_weeks=1):
    """Choose `n` worlds for `lane`/`wid`: prefer worlds NOT used in the last
    `avoid_weeks` weeks, least-recently-used first; top up by LRU if the bank is
    too shallow. Deterministic given the ledger + bank. Does not write."""
    used = _load().get("used", [])
    wn = _weeknum(wid)
    recent_weeks = sorted({_weeknum(u["week"]) for u in used
                           if u.get("lane") == lane and _weeknum(u["week"]) != wn}, reverse=True)[:avoid_weeks]
    blocked = {u["world"] for u in used
               if u.get("lane") == lane and _weeknum(u["week"]) in recent_weeks}
    lu = _last_used(used, lane)
    fresh = sorted([w for w in bank if w not in blocked], key=lambda w: lu.get(w, -1))
    if len(fresh) >= n:
        return fresh[:n]
    # bank too shallow to fully avoid recent worlds -> fill remainder by LRU.
    rest = sorted([w for w in bank if w in blocked], key=lambda w: lu.get(w, -1))
    return (fresh + rest)[:n]


def record(lane, wid, worlds):
    """Commit the worlds a lane used this week (replaces any prior entry for the pair)."""
    d = _load()
    d["used"] = [u for u in d.get("used", []) if not (u.get("lane") == lane and u.get("week") == wid)]
    for w in worlds:
        d["used"].append({"lane": lane, "week": wid, "world": w})
    _save(d)


def shortfall(lane, bank, n, wid, avoid_weeks=1):
    """How many posts this week are forced to reuse a recent world (0 = fully fresh).
    A positive number means author that many more worlds for the lane."""
    used = _load().get("used", [])
    wn = _weeknum(wid)
    recent_weeks = sorted({_weeknum(u["week"]) for u in used
                           if u.get("lane") == lane and _weeknum(u["week"]) != wn}, reverse=True)[:avoid_weeks]
    blocked = {u["world"] for u in used
               if u.get("lane") == lane and _weeknum(u["week"]) in recent_weeks}
    fresh = [w for w in bank if w not in blocked]
    return max(0, n - len(fresh))
