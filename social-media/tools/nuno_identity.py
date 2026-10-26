"""nuno_identity.py - collapse visually identical cutouts to ONE pose.

The library is keyed by filename, but the same generation was ingested more than
once under different family names: nuno_howto_4 and nuno_utility_4 are the
same picture, as are nuno_cv_5 / nuno_cv_8 and nuno_dothis_1 /
nuno_thumbsup. 66 files hold only 53 distinct poses.

That made the no-repeat ledger lie. It tracked freshness per FILENAME, so a pose
that ran last week came back this week under an alias and counted as fresh -
week21 shipped nuno_howto_4 and week22 shipped nuno_utility_4, the same image on
consecutive weeks, with no shortfall warning. Deduping by content is what makes
"never repeat a pose within FRESH_DAYS" actually true.

The signature is alpha-cropped, greyscaled, resized to 32x32 and normalised, so
it keys on the silhouette and tonal layout rather than exact bytes - re-cutting a
source with slightly different rembg output still matches.

    python3 tools/nuno_identity.py            # rebuild content/nuno_identity.json
    python3 tools/nuno_identity.py --show     # print the duplicate groups

nuno_ledger imports `canonical()` and resolves every cutout through it before
recording or comparing. The map is a cache: a cutout missing from it falls back
to its own name, so a newly added file is never wrong, only un-deduped until the
map is rebuilt.
"""
from __future__ import annotations
import os, sys, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
SM = os.path.dirname(HERE)
NUNO_DIR = os.path.join(SM, "assets", "nuno")
MAP = os.path.join(SM, "content", "nuno_identity.json")

# Below this normalised L2 distance two cutouts are the same photograph. Measured
# spread: true duplicates sit at ~0.00-0.06, genuinely different poses at >0.45.
THRESHOLD = 0.25

_cache = None


def _signature(path):
    import numpy as np
    from PIL import Image
    im = Image.open(path).convert("RGBA")
    alpha = np.asarray(im)[..., 3]
    ys, xs = np.where(alpha > 40)
    if len(xs) == 0:
        return None
    im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    v = np.asarray(im.convert("L").resize((32, 32), Image.LANCZOS)).astype(np.float32)
    return ((v - v.mean()) / (v.std() + 1e-6)).ravel()


def build():
    """Group the library by visual identity and return {cutout: canonical}."""
    import numpy as np
    sigs = {}
    for p in sorted(glob.glob(os.path.join(NUNO_DIR, "*.png"))):
        s = _signature(p)
        if s is not None:
            sigs[os.path.splitext(os.path.basename(p))[0]] = s
    names, out, taken = sorted(sigs), {}, set()
    for i, a in enumerate(names):
        if a in taken:
            continue
        # The canonical is the first name alphabetically in the group, so the
        # mapping is stable across rebuilds and independent of scan order.
        group = [a]
        for b in names[i + 1:]:
            if b not in taken and float(np.linalg.norm(sigs[a] - sigs[b])) / 32 < THRESHOLD:
                group.append(b)
                taken.add(b)
        taken.add(a)
        for n in group:
            out[n] = a
    return out


def load():
    """{cutout: canonical}, read once per process. Missing file = no deduping."""
    global _cache
    if _cache is None:
        try:
            _cache = json.load(open(MAP))
        except Exception:
            _cache = {}
    return _cache


def canonical(cutout):
    """The pose identity a cutout belongs to; its own name if unknown."""
    return load().get(cutout, cutout)


def groups(m=None):
    m = m or load()
    g = {}
    for k, v in m.items():
        g.setdefault(v, []).append(k)
    return {k: sorted(v) for k, v in g.items() if len(v) > 1}


if __name__ == "__main__":
    m = build()
    if "--show" not in sys.argv:
        json.dump(m, open(MAP, "w"), indent=2, ensure_ascii=False, sort_keys=True)
        open(MAP, "a").write("\n")
    dup = groups(m)
    for canon, members in sorted(dup.items()):
        print("  " + " == ".join(members))
    print(f"{len(m)} files, {len(set(m.values()))} distinct poses, "
          f"{len(m) - len(set(m.values()))} redundant")
