# IW Content Hub

A lightweight static dashboard for the Internwise social media content team. Each week the team uploads graphics and captions here for review before publishing to Instagram, LinkedIn, and other platforms.

No build step. No framework. Pure HTML, CSS, and JavaScript — deployable anywhere static files are served.

---

## Adding a new week

1. Create a folder under `images/` matching the week ID, e.g. `images/week4/`.
2. Inside it, create one subfolder per post (e.g. `d1-salaries/`, `d2-cv/`) and drop the PNG slides in.
3. Open `data/weeks.json` and add a new entry to the `"weeks"` array:

```json
{
  "id": "week4",
  "label": "Week 4",
  "dateRange": "May 2026",
  "posts": [
    {
      "id": "d1-example",
      "day": "Monday",
      "title": "Post Title Here",
      "platform": "Instagram",
      "format": "Carousel",
      "slides": ["slide_1.png", "slide_2.png"],
      "status": "draft",
      "caption": "Caption text here.",
      "hashtags": ["#Example", "#UKGraduate"]
    }
  ]
}
```

4. Add the new week at the top of the `"weeks"` array so it appears first in the selector.
5. Commit and push — Cloudflare Pages deploys automatically.

---

## Deploying to Cloudflare Pages

1. Push this repository to GitHub.
2. In the Cloudflare dashboard, go to Workers and Pages > Create application > Pages > Connect to Git.
3. Select your repository.
4. Build settings:
   - Build command: *(leave blank)*
   - Build output directory: `/`
5. Save and deploy.

Every push to the main branch triggers an automatic redeploy. No build command or node_modules needed.

---

## Post statuses

Status changes made in the browser are saved to `localStorage` — they persist between sessions on the same device but are not shared across team members. This is intentional: the dashboard is for local review. The source-of-truth status lives in `weeks.json`.
