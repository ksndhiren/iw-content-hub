#!/usr/bin/env bash
# The build command for Cloudflare Pages, and the same staging step the GitHub
# Actions deploy runs - one script, so the two paths cannot drift.
#
# Set as the Pages project's build command (Settings -> Build configuration).
# The output directory comes from wrangler.toml's pages_build_output_dir.
#
# .cfignore was tried first and the build system ignores it, so exclusion is out:
# the deployment has to be an explicit subset instead. wrangler.toml itself is
# NOT copied - Cloudflare reads it from the repo root for the KV binding, and
# serving it only published the namespace id.
set -euo pipefail
rm -rf .pages-dist
mkdir -p .pages-dist
cp index.html app.js style.css logo.svg .pages-dist/
cp -R data functions .pages-dist/
[ -d images ] && cp -R images .pages-dist/ || true
echo "staged $(find .pages-dist -type f | wc -l) files into .pages-dist"
