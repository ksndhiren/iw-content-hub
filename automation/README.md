# Featured Jobs automation

Scrapes the live **Featured Jobs** section of
<https://www.internwise.co.uk/internship-search>, generates an on-brand portrait
(1080×1350) job-ad graphic for every **new** featured job, and updates
`../data/featured.json` so the graphics appear in the Content Hub's **Featured
Jobs** tab.

Self-contained: the generator, fonts, and brand logos all live in this folder, so
it runs anywhere (locally or in a cloud routine) with only `playwright` installed.

## What it does

`sync_featured_jobs.py`:

1. Loads the search page with headless Chromium and reads the featured job cards
   (title, company, sector, location, type, duration) plus each job's stable
   numeric id from its `/job/<id>/` URL.
2. For each job **not already present**, picks a colour scheme + 3D object cluster
   from its sector and renders `../images/featured/job-<id>/job-<id>.png`.
3. Rewrites `../data/featured.json` (status `in-review`), preserving any hand-made
   demo entries (those without a `sourceId`) and dropping auto entries whose job is
   no longer featured.

It **never commits or pushes** — see "Hold for review" below.

### Sector → visual style

| Style     | Sectors                                              | Cluster            |
|-----------|------------------------------------------------------|--------------------|
| design    | Graphic / Web / Brand Design                         | pen + colour wheel |
| social    | Photography / Videography, Home Staging              | camera + play      |
| property  | Surveying, Real Estate, Construction, Architecture   | hard hat + blueprint |
| marketing | Marketing, Advertising, PR, Sales                    | megaphone + chart  |
| generic   | everything else (IT, Legal, Finance, Admin, …)       | briefcase + chart  |

## Run locally

```bash
pip install -r requirements.txt
python -m playwright install chromium
python sync_featured_jobs.py            # writes into the repo it lives in
```

Override the target hub with `FEATURED_HUB_DIR=/path/to/hub`.

## Hold for review (cloud routine)

The script only writes files. The scheduled cloud routine wraps it: it runs the
sync, and **if `git status` shows changes**, commits them to a new branch and opens
a **pull request** for a human to approve. Nothing reaches the live dashboard until
that PR is merged.
