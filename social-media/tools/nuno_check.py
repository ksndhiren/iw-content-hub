"""nuno_check.py - Friday capacity report: can the Nuno library cover next week
without repeating a face? Run it when the operator hands over the weekly data;
it dry-simulates the upcoming week's picks against the ledger and prints exactly
which pose families are short, and by how many, so fresh cutouts can be generated
BEFORE the Saturday build.

    python3 tools/nuno_check.py            # report for the upcoming week
    python3 tools/nuno_check.py --week week17
"""
from __future__ import annotations
import os, sys, json, argparse, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_week as bw
import lane_education as edu
import lane_employer as emp
import nuno_ledger


def upcoming_sequence(wid):
    """The ordered Nuno slots next week's build will fill (matches build_week:
    employer only on EMPLOYER_DAYS with week-rotated pairs, then education
    carousel cover + cta). Tone isn't known until write-time, so the capacity
    check counts general pool availability (conservative)."""
    try:
        wn = int(wid.replace("week", ""))
    except ValueError:
        wn = 14
    n_emp = len(bw.EMPLOYER_DAYS)
    estart = ((wn - 14) * n_emp) % len(bw.EMPLOYER_PAIRS)
    week_emp = {d: bw.EMPLOYER_PAIRS[(estart + i) % len(bw.EMPLOYER_PAIRS)]
                for i, d in enumerate(sorted(bw.EMPLOYER_DAYS))}
    seq = []
    for di in range(5):
        if di in bw.EMPLOYER_DAYS:
            ework = week_emp[di][0]
            seq.append((f"employer/{ework}", emp.EMP_POOLS.get(ework, ["nuno_authority_1"])))
        world, fmt = bw.EDU_WORLDS[di]
        if fmt == "carousel":
            seq.append((f"education/{world}/cover", edu.COVER_POOL))
            seq.append((f"education/{world}/cta", edu.CTA_POOL))
    return seq


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--week", help="week id (default: the upcoming week)")
    args = p.parse_args()
    wid = args.week or bw.target_week()[0]

    rep = nuno_ledger.capacity(upcoming_sequence(wid), wid)
    out = os.path.join(bw.L.BASE, "content", "nuno_needed.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    payload = {"week": wid, "generatedAt": datetime.datetime.now(datetime.timezone.utc)
               .strftime("%Y-%m-%dT%H:%M:%SZ"), **rep}
    json.dump(payload, open(out, "w"), indent=2, ensure_ascii=False); open(out, "a").write("\n")

    if rep["ok"]:
        print(f"Nuno library for {wid}: OK - covers the week with no repeats.")
    else:
        print(f"Nuno library for {wid}: SHORT - would repeat {len(rep['shortfalls'])} pose(s).")
        print("Generate fresh cutouts (family x count):")
        for fam, n in sorted(rep["needByFamily"].items(), key=lambda kv: -kv[1]):
            print(f"  - {n} x {fam}")
        print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
