# Internwise Content Hub — Agent Handoff

This repo is the canonical home for both the dashboard and the social-media build pipeline.

## Layout
- Dashboard/site: repo root (`index.html`, `app.js`, `style.css`, `data/`, `images/`).
- Featured jobs automation: `automation/`.
- Weekly social-media build workspace: `social-media/`.

Before building weekly graphics, read `social-media/AGENTS.md` fully. It contains the current Week 12 plan, design rules, Nuno usage rules, rendering pipeline, and publish steps.

## Secrets
Never commit or print local secrets: `.env`, `.canva_tokens.json`, `secrets/`, `analytics/ig_token.txt`, or the same paths inside `social-media/`.

## Publishing
Do not commit or push unless explicitly asked. Dashboard deployments happen from commits pushed to this repo.
