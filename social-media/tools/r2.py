"""Cloudflare R2 helper (S3-compatible) - object storage for generated graphics.

Reads R2_ACCOUNT_ID / R2_ACCESS_KEY_ID / R2_SECRET_ACCESS_KEY / R2_BUCKET from env
(or social-media/.env locally; cloud secrets win). Used by the build to upload
PNGs and by r2_sync.py for the one-time backfill.

    from r2 import ensure_bucket, upload_file, upload_tree
"""
import os, sys, mimetypes

HERE = os.path.dirname(os.path.abspath(__file__))
SM   = os.path.dirname(HERE)                      # social-media/


_WANT = ("R2_ACCOUNT_ID", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY", "R2_BUCKET", "IMAGE_BASE_URL")

def _load_env():
    for p in (os.path.join(SM, ".env"), os.path.join(os.path.dirname(SM), ".env")):
        if os.path.exists(p):
            for line in open(p):
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())
    # tolerate case variants (e.g. R2_Access_Key_ID) + aliases -> canonical UPPER names
    upper = {k.upper(): k for k in os.environ}
    aliases = {"IMAGE_BASE_URL": ("IMAGE_BASE_URL", "R2_PUBLIC_URL", "R2_PUBLIC_DEV_URL")}
    for want in _WANT:
        if want in os.environ:
            continue
        for cand in aliases.get(want, (want,)):
            if cand in upper:
                os.environ[want] = os.environ[upper[cand]]
                break
_load_env()

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

BUCKET   = os.getenv("R2_BUCKET") or "iw-content-graphics"
_ACCOUNT = os.getenv("R2_ACCOUNT_ID", "")
ENDPOINT = f"https://{_ACCOUNT}.r2.cloudflarestorage.com"


def client():
    return boto3.client(
        "s3", endpoint_url=ENDPOINT,
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        region_name="auto", config=Config(signature_version="s3v4"))


def ensure_bucket(c=None):
    c = c or client()
    try:
        c.head_bucket(Bucket=BUCKET)
    except ClientError:
        c.create_bucket(Bucket=BUCKET)
        print(f"  created bucket {BUCKET}")
    return BUCKET


def upload_file(local_path, key, c=None):
    c = c or client()
    ct = mimetypes.guess_type(local_path)[0] or "application/octet-stream"
    c.upload_file(local_path, BUCKET, key,
                  ExtraArgs={"ContentType": ct, "CacheControl": "public, max-age=31536000, immutable"})
    return key


def upload_tree(root, prefix="", workers=12):
    """Upload every file under `root`; key = path relative to `root` (prefixed)."""
    from concurrent.futures import ThreadPoolExecutor, as_completed
    c = client()
    files = []
    for dp, _, fns in os.walk(root):
        for fn in fns:
            lp = os.path.join(dp, fn)
            key = (prefix + os.path.relpath(lp, root)).replace(os.sep, "/")
            files.append((lp, key))
    done = [0]
    def _do(pair):
        upload_file(pair[0], pair[1], c)
        done[0] += 1
        if done[0] % 50 == 0:
            print(f"  uploaded {done[0]}/{len(files)}")
    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(as_completed(ex.submit(_do, p) for p in files))
    print(f"  uploaded {done[0]}/{len(files)} total")
    return done[0]


if __name__ == "__main__":
    ensure_bucket()
    print("bucket ok:", BUCKET, "| endpoint:", ENDPOINT)
