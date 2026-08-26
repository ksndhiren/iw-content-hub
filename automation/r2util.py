"""Featured-jobs R2 helpers: shrink graphics and mirror them to Cloudflare R2.

Featured graphics no longer live in git (they bloated the repo). They live in
Cloudflare R2, served from IMAGE_BASE at  featured/<post-id>/<file>.png , which
is exactly what the dashboard resolves against IMAGE_BASE_URL.

This module does two jobs:
  - optimize_png()  shrinks each render (downscale + dithered 256-colour PNG)
  - upload_file() / delete_prefix()  keep R2 in sync with the local render state

All R2 operations are no-ops when credentials are absent (local dev), mirroring
the weekly build's "upload only when R2_* is set" behaviour. Credentials come
from the environment in CI, or from the repo/social-media .env locally.
"""
import os, mimetypes

_HERE = os.path.dirname(os.path.abspath(__file__))


def _load_env():
    """Populate R2_* from a local .env if not already in the environment.

    Tolerates case variants (R2_Access_Key_ID) and the R2_Public_URL alias by
    normalising everything to the canonical UPPER_SNAKE names boto3 expects.
    """
    candidates = (
        os.path.join(os.path.dirname(_HERE), ".env"),          # repo root
        os.path.join(os.path.dirname(_HERE), "social-media", ".env"),
    )
    for p in candidates:
        if not os.path.exists(p):
            continue
        for line in open(p):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())
    # Canonicalise case + aliases -> UPPER names.
    upper = {k.upper(): v for k, v in os.environ.items()}
    aliases = {
        "R2_ACCOUNT_ID":        ("R2_ACCOUNT_ID",),
        "R2_ACCESS_KEY_ID":     ("R2_ACCESS_KEY_ID",),
        "R2_SECRET_ACCESS_KEY": ("R2_SECRET_ACCESS_KEY",),
        "R2_BUCKET":            ("R2_BUCKET",),
        "IMAGE_BASE_URL":       ("IMAGE_BASE_URL", "R2_PUBLIC_URL", "R2_PUBLIC_DEV_URL"),
    }
    for want, cands in aliases.items():
        if want in os.environ:
            continue
        for c in cands:
            if c.upper() in upper:
                os.environ[want] = upper[c.upper()]
                break


_load_env()

BUCKET = os.getenv("R2_BUCKET") or "iw-content-graphics"
# Featured graphics render at 2160x2700 (device_scale_factor=2). The feed display
# size is 1080-wide, so 1440 keeps headroom while cutting ~80% of the bytes.
MAX_W  = int(os.getenv("FEATURED_MAX_WIDTH", "1440"))


def optimize_png(path, max_w=MAX_W):
    """Shrink a rendered PNG in place: downscale to <= max_w wide, then re-encode
    as a Floyd-Steinberg-dithered 256-colour PNG. These are flat-gradient brand
    graphics, so a dithered palette is visually lossless while cutting file size
    from ~3.8 MB to ~0.6 MB."""
    from PIL import Image
    im = Image.open(path).convert("RGB")
    if im.width > max_w:
        h = round(im.height * max_w / im.width)
        im = im.resize((max_w, h), Image.LANCZOS)
    im.convert("P", palette=Image.ADAPTIVE, colors=256,
               dither=Image.FLOYDSTEINBERG).save(path, "PNG", optimize=True)
    return path


def enabled():
    return bool(os.getenv("R2_ACCESS_KEY_ID")
                and os.getenv("R2_SECRET_ACCESS_KEY")
                and os.getenv("R2_ACCOUNT_ID"))


def _client():
    import boto3
    from botocore.config import Config
    acct = os.getenv("R2_ACCOUNT_ID", "")
    return boto3.client(
        "s3",
        endpoint_url=f"https://{acct}.r2.cloudflarestorage.com",
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        region_name="auto", config=Config(signature_version="s3v4"))


def upload_file(local_path, key, c=None):
    """Upload one file to R2. No-op (returns False) when creds are absent."""
    if not enabled():
        return False
    c = c or _client()
    ct = mimetypes.guess_type(local_path)[0] or "application/octet-stream"
    c.upload_file(local_path, BUCKET, key,
                  ExtraArgs={"ContentType": ct,
                             "CacheControl": "public, max-age=31536000, immutable"})
    print(f"  R2 put {key}")
    return True


def delete_prefix(prefix, c=None):
    """Delete every object under `prefix` from R2. No-op when creds are absent."""
    if not enabled():
        return 0
    c = c or _client()
    keys, token = [], None
    while True:
        kw = {"Bucket": BUCKET, "Prefix": prefix}
        if token:
            kw["ContinuationToken"] = token
        resp = c.list_objects_v2(**kw)
        keys += [{"Key": o["Key"]} for o in resp.get("Contents", [])]
        if not resp.get("IsTruncated"):
            break
        token = resp.get("NextContinuationToken")
    for i in range(0, len(keys), 1000):
        c.delete_objects(Bucket=BUCKET, Delete={"Objects": keys[i:i + 1000]})
    if keys:
        print(f"  R2 del {prefix} ({len(keys)})")
    return len(keys)
