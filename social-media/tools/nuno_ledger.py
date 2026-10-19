"""nuno_ledger.py - stop the founder's face repeating, and flag when we need more.

The lanes render Nuno from a fixed library (assets/nuno/*.png). Left to their old
hard-coded pose per design world, the same ~12 cutouts recurred every week. This
ledger records every use and hands each render slot the FRESHEST layout-safe
cutout (never one used in the last `FRESH_DAYS`, never one already used that week),
so the face keeps changing. When a slot has no fresh option left, it still renders
(least-recently-used) but records a SHORTFALL, so we can tell the operator exactly
which poses to generate next - by family and count.

  pick(candidates, week_id, label=...)   -> a cutout name, recorded as used
  capacity(sequence, week_id)            -> dry shortfall report for a whole week

Ledger: social-media/content/nuno_ledger.json  {"uses":[{cutout,week,date}, ...]}
"""
from __future__ import annotations
import os, json, glob, datetime, copy

HERE = os.path.dirname(os.path.abspath(__file__))
SM   = os.path.dirname(HERE)
LEDGER = os.path.join(SM, "content", "nuno_ledger.json")
NUNO_DIR = os.path.join(SM, "assets", "nuno")
FRESH_DAYS = 30

# Tone tags per cutout, so a serious topic never gets a celebratory pose. A slot
# asks for a tone; we pick the freshest candidate that carries it (falling back
# to the full candidate list if none match, so a render never fails).
TONES = {
    # week21 additions (cut from the Gemini Solo/CV sets). Tones must come from
    # the vocabulary COVER_TONE/CTA_TONE actually request - serious, thoughtful,
    # practical, confident, positive - or by_tone() filters these straight out.
    "nuno_cv_6": {"practical", "serious"}, "nuno_cv_8": {"practical"},
    "nuno_howto_4": {"practical", "confident"},
    "nuno_dothis_5": {"confident", "positive"},
    "nuno_phone_2": {"positive", "confident"},
    "nuno_thoughtful_1": {"serious", "thoughtful"}, "nuno_thoughtful_2": {"serious", "thoughtful"},
    "nuno_thoughtful_3": {"serious", "thoughtful"},
    "nuno_authority_1": {"confident", "serious"}, "nuno_authority_2": {"confident", "serious"},
    "nuno_authority_3": {"confident", "serious"},
    "nuno_planning_1": {"serious", "practical"}, "nuno_planning_2": {"serious", "practical"},
    "nuno_planning_3": {"serious", "practical"},
    "nuno_cvpile": {"serious"}, "nuno_cv": {"practical", "confident"},
    "nuno_cv_1": {"practical"}, "nuno_cv_2": {"practical"}, "nuno_cv_3": {"practical", "serious"},
    "nuno_thumbsup": {"positive"}, "nuno_dothis_1": {"confident", "practical"},
    "nuno_dothis_2": {"confident", "positive"}, "nuno_dothis_3": {"practical"},
    "nuno_offers_1": {"positive", "confident"}, "nuno_offers_2": {"positive"},
    "nuno_offers_3": {"confident", "serious"},
    "nuno_welcoming_1": {"warm", "positive"}, "nuno_welcoming_2": {"warm", "positive"},
    "nuno_welcoming_3": {"warm", "positive"},
    "nuno_utility_1": {"practical"}, "nuno_utility_2": {"practical"}, "nuno_utility_3": {"practical"},
    "nuno_howto_1": {"practical", "confident"}, "nuno_howto_2": {"practical", "confident"},
    "nuno_howto_3": {"practical", "confident"},
    "nuno_attention_1": {"positive", "confident"}, "nuno_attention_2": {"positive", "confident"},
    # week17 fresh cutouts
    "nuno_cv_4": {"practical", "serious"}, "nuno_cv_5": {"practical", "confident"},
    "nuno_utility_4": {"practical", "confident"},
    "nuno_thumbsup_2": {"positive"}, "nuno_dothis_4": {"confident", "practical"},
    "nuno_offers_4": {"positive", "confident"},
    "nuno_interview_door": {"practical", "confident", "serious"},
    "nuno_cv_proof_highlight": {"practical", "serious"},
    "nuno_followup_phone": {"practical", "serious"},
}


def by_tone(pool, tone):
    """Filter a candidate pool to cutouts carrying any of `tone`; if that leaves
    nothing, return the pool unchanged so a render never fails."""
    if not tone:
        return pool
    want = {tone} if isinstance(tone, str) else set(tone)
    hit = [c for c in pool if TONES.get(c, set()) & want]
    return hit or pool

# Repeats recorded during the current process (build_week reads this to warn +
# write nuno_needed.json). Reset per run.
REPEATS: list[dict] = []


def family(cutout):
    """'nuno_authority_1' -> 'authority'; 'nuno_thumbsup' -> 'thumbsup'."""
    base = cutout.replace("nuno_", "")
    parts = base.rsplit("_", 1)
    return parts[0] if len(parts) == 2 and parts[1].isdigit() else base


def _on_disk():
    return {os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(NUNO_DIR, "*.png"))}


def _load():
    try:
        return json.load(open(LEDGER))
    except Exception:
        return {"uses": []}


def _save(log):
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    json.dump(log, open(LEDGER, "w"), indent=2, ensure_ascii=False)
    open(LEDGER, "a").write("\n")


def _last_use(log, cutout):
    ds = [u["date"] for u in log.get("uses", []) if u["cutout"] == cutout]
    return max(ds) if ds else None


def _used_in_week(log, week_id):
    return {u["cutout"] for u in log.get("uses", []) if u.get("week") == week_id}


def _choose(candidates, week_id, log, today, fresh_days, exclude=None):
    """Return (cutout, is_repeat). Freshest layout-safe candidate:
    prefer not-used-this-week, then never-used, then oldest last-use."""
    present = _on_disk()
    blocked = set(exclude or [])
    avail = [c for c in candidates if c in present and c not in blocked]
    if not avail:
        return (candidates[0] if candidates else None), True
    used_wk = _used_in_week(log, week_id)
    pool = [c for c in avail if c not in used_wk] or avail   # avoid intra-week dupes

    def key(c):
        lu = _last_use(log, c)
        fresh = lu is None or (datetime.date.fromisoformat(today) -
                               datetime.date.fromisoformat(lu)).days >= fresh_days
        # sort: fresh first, then oldest last-use first (never-used = "" sorts first)
        return (0 if fresh else 1, lu or "")
    pool.sort(key=key)
    best = pool[0]
    lu = _last_use(log, best)
    is_repeat = not (lu is None or
                     (datetime.date.fromisoformat(today) - datetime.date.fromisoformat(lu)).days >= fresh_days)
    return best, is_repeat


def pick(candidates, week_id, label=None, tone=None, today=None, fresh_days=FRESH_DAYS, exclude=None):
    """Pick + record the freshest layout-safe cutout for a render slot, preferring
    one whose tone matches `tone` (falls back to the full pool if none match)."""
    today = today or datetime.date.today().isoformat()
    log = _load()
    cutout, is_repeat = _choose(by_tone(candidates, tone), week_id, log, today, fresh_days, exclude=exclude)
    if cutout:
        log.setdefault("uses", []).append({"cutout": cutout, "week": week_id, "date": today})
        _save(log)
    if is_repeat:
        REPEATS.append({"label": label, "cutout": cutout, "family": family(cutout) if cutout else None,
                        "week": week_id})
    return cutout


def capacity(sequence, week_id, today=None, fresh_days=FRESH_DAYS):
    """Dry-simulate a week's picks (no writes) and report shortfalls.
    `sequence` = ordered list of (label, candidates) the week will render."""
    today = today or datetime.date.today().isoformat()
    log = copy.deepcopy(_load())
    shortfalls = []
    for entry in sequence:
        label, cands = entry[0], entry[1]
        tone = entry[2] if len(entry) > 2 else None
        cutout, is_repeat = _choose(by_tone(cands, tone), week_id, log, today, fresh_days)
        log.setdefault("uses", []).append({"cutout": cutout, "week": week_id, "date": today})
        if is_repeat:
            shortfalls.append({"label": label, "family": family(cutout) if cutout else None,
                               "cutout": cutout})
    by_family = {}
    for s in shortfalls:
        by_family[s["family"]] = by_family.get(s["family"], 0) + 1
    return {"week": week_id, "shortfalls": shortfalls, "needByFamily": by_family,
            "ok": not shortfalls}
