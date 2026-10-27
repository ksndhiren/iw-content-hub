#!/usr/bin/env bash
# FALLBACK build command for Cloudflare Pages.
#
# Not needed while .cfignore is honoured: the Pages project builds from the repo
# root with no build command, and .cfignore keeps the 958 MB asset tree out of
# the upload. If a Cloudflare build ever fails on size again, set the project's
# build command to `bash scripts/pages-build.sh`, set wrangler.toml's
# pages_build_output_dir to ".pages-dist", and this stages the same file set
# explicitly instead of relying on exclusion.
set -euo pipefail
rm -rf .pages-dist
mkdir -p .pages-dist
cp index.html app.js style.css logo.svg wrangler.toml .pages-dist/
cp -R data functions .pages-dist/
[ -d images ] && cp -R images .pages-dist/ || true
echo "staged $(find .pages-dist -type f | wc -l) files into .pages-dist"
