"""build_news_day.py - build ONE day's news post the day before it goes out.

The weekly batch (build_week.py) builds the evergreen lanes on Saturday. News is
different: a headline written on Saturday would be stale by Friday. So this job
runs daily (news-daily.yml) and builds the NEXT posting day's news card, fetching
fresh UK news, having the LLM reword it, rendering the card, and upserting it into
data/weeks.json as `approved`, then schedules it to the next morning's news slot.
It never touches the other lanes.

    python3 tools/build_news_day.py            # build tomorrow's news only
    python3 tools/build_news_day.py --date 2026-09-14

Normal runs must build exactly one day ahead. Standard posting is Mon-Fri.
Weekend news is allowed only for a dated temporary catch-up window such as the
week18 late-start run; set IW_TEMP_WEEKEND_NEWS_UNTIL=YYYY-MM-DD for that.
Emergency backfills require IW_ALLOW_NEWS_NOT_DAY_PRIOR=1 so news can never be
generated early by accident.
    python3 tools/build_news_day.py --dry       # plan only, no LLM/render/write
"""
from __future__ import annotations
import os, sys, json, argparse, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_week as bw          # reuses env load, writer, news_fetch, news_card, helpers

REF, REFN = datetime.date(2026, 8, 31), 14   # week14 = w/c 2026-08-31 (same anchor as build_week)
ALLOW_NOT_DAY_PRIOR_ENV = "IW_ALLOW_NEWS_NOT_DAY_PRIOR"
TEMP_WEEKEND_NEWS_UNTIL_ENV = "IW_TEMP_WEEKEND_NEWS_UNTIL"


def today():
    """Return the local run date. IW_TODAY is a test/operator escape hatch so
    day-prior enforcement can be verified without waiting for the calendar."""
    if os.getenv("IW_TODAY"):
        return datetime.date.fromisoformat(os.environ["IW_TODAY"])
    return datetime.date.today()


def not_day_prior_allowed():
    return os.getenv(ALLOW_NOT_DAY_PRIOR_ENV, "").strip().lower() in {"1", "true", "yes", "y"}


def enforce_day_prior(target: datetime.date):
    expected = today() + datetime.timedelta(days=1)
    if target == expected:
        return
    if not_day_prior_allowed():
        print(f"WARNING: building {target} although day-prior target is {expected}; "
              f"{ALLOW_NOT_DAY_PRIOR_ENV}=1 is set.")
        return
    raise SystemExit(
        f"Refusing to build news for {target}: news must be generated exactly one day "
        f"before posting ({expected} today). Set {ALLOW_NOT_DAY_PRIOR_ENV}=1 only "
        "for an explicit emergency backfill."
    )


def allow_weekend_target(target: datetime.date):
    if target.weekday() < 5:
        return True
    raw_until = os.getenv(TEMP_WEEKEND_NEWS_UNTIL_ENV, "").strip()
    if raw_until:
        try:
            until = datetime.date.fromisoformat(raw_until)
        except ValueError:
            raise SystemExit(f"{TEMP_WEEKEND_NEWS_UNTIL_ENV} must be YYYY-MM-DD, got {raw_until!r}.")
        if target <= until:
            print(f"Temporary weekend news enabled through {until}; building {target}.")
            return True
    print(f"{target} is a weekend target. Standard news cadence is Mon-Fri; no news post. Done.")
    return False


def week_of(target: datetime.date):
    """Map a posting date to (wid, wlabel, wc, mon, dkey, dlabel), numbered off the
    same week14 anchor build_week uses, so news lands in the correct week entry."""
    mon = target - datetime.timedelta(days=target.weekday())
    n = REFN + (mon - REF).days // 7
    dkey = bw.DKEYS[target.weekday()]
    dlabel = target.strftime("%a %d %b").replace(" 0", " ")
    return f"week{n}", f"Week {n}", mon.isoformat(), mon, dkey, dlabel


# When the requested window comes back empty, look back a little further before
# giving up. The story must still be real, UK, on-topic and unused - only the
# age limit relaxes, so quality is unchanged. Feeds carry ~20 items each, so a
# wider window mostly helps on quiet news days and bank holidays.
AGE_LADDER = (7, 10, 14)


def pick_fresh(exclude_titles, max_age_days=5):
    """First fresh, unused UK news item whose topic doesn't repeat a headline
    already used in this week. Raises instead of silently repeating unless
    IW_ALLOW_TOPIC_REPEAT=1 is set."""
    excl_sets = [bw._news_words(t) for t in exclude_titles]
    fetched = bw.news_fetch.fetch(max_age_days=max_age_days, limit=20)
    for wider in AGE_LADDER:
        if fetched or wider <= max_age_days:
            break
        print(f"  no items within {max_age_days}d; retrying with a {wider}d window")
        fetched = bw.news_fetch.fetch(max_age_days=wider, limit=20)
    if not fetched and not bw.topic_repeat_allowed():
        raise bw.TopicFreshnessError(
            "No live news items were fetched (tried "
            f"{max_age_days}d then {'/'.join(str(d) for d in AGE_LADDER)}d). "
            "The '!' lines above show which feeds failed; a run where every feed "
            "returned items but none passed the relevance filter means the day "
            "genuinely had no UK early-careers story. Refusing to use sample news "
            f"unless {bw.TOPIC_REPEAT_OVERRIDE_ENV}=1 is set."
        )
    pool = bw.pick_distinct_news(fetched, 8)
    for it in pool:
        ws = bw._news_words(it.get("title", ""))
        if any(ws and es and len(ws & es) / min(len(ws), len(es)) >= 0.4 for es in excl_sets):
            continue
        return it
    if bw.topic_repeat_allowed():
        return pool[0] if pool else bw.news_fetch.sample_item()
    raise bw.TopicFreshnessError(
        "All fetched news items repeat a story already used this week. Add a fresh source item "
        f"or set {bw.TOPIC_REPEAT_OVERRIDE_ENV}=1 for an explicit emergency repeat."
    )


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--offset", type=int, default=1, help="days ahead to build (default 1 = tomorrow; must resolve to tomorrow unless override env is set)")
    p.add_argument("--date", help="explicit posting date YYYY-MM-DD (must be tomorrow unless override env is set)")
    p.add_argument("--image", help="explicit editorial image path for the news card when stock fetch is unavailable")
    p.add_argument("--max-age-days", type=int, default=5, help="maximum RSS story age in days (default 5; widen only for manual dashboard review)")
    p.add_argument("--status", default="approved", choices=("approved", "in-review"),
                   help="dashboard status for the generated post (default approved; use in-review for dashboard-only review builds)")
    p.add_argument("--dry", action="store_true", help="plan only, no LLM/render/write")
    args = p.parse_args()

    target = (datetime.date.fromisoformat(args.date) if args.date
              else today() + datetime.timedelta(days=args.offset))
    enforce_day_prior(target)
    if not allow_weekend_target(target):
        return

    wid, wlabel, wc, mon, dkey, dlabel = week_of(target)
    img = os.path.join(bw.HUB, "images", wid)
    pid = f"{wid}-{dkey}-news"

    data = json.load(open(bw.WEEKS))
    week = next((w for w in data["weeks"] if w.get("id") == wid), None)
    existing_news = [pp.get("title", "") for pp in (week or {}).get("posts", [])
                     if pp.get("lane") == "news" and pp.get("id") != pid]
    existing_news += bw.posted_titles({"news"})

    item = pick_fresh(existing_news, max_age_days=args.max_age_days)
    print(f"Building news for {dlabel} ({pid}) - \"{item.get('title', '')[:70]}\"")
    if args.dry:
        print("DRY: nothing fetched-through, rendered or written.")
        return

    pdate = datetime.datetime.combine(target, datetime.time())
    post = bw.build_news_post(wid, dkey, dlabel, pdate, img, item,
                              issue_no=target.weekday() + 1,
                              image_path=args.image)
    try:
        import story_card
        src = os.path.join(img, post["id"], "slide_1.png")
        if os.path.exists(src):
            story_card.make_story(src, os.path.join(img, post["id"], "story.png"))
            print(f"rendered Story companion for {post['id']}.")
    except Exception as e:
        print("story render skipped:", e)

    # News is auto-approved: unlike the evergreen lanes it carries no manual
    # dashboard gate. The story is fetched from UK sources, LLM-reworded under the
    # news rules, and scheduled straight to the 8am slot by news-daily.yml. Born
    # 'approved' so the publisher's status gate and the dashboard both treat it as
    # cleared without a human click.
    post["status"] = args.status

    # Upsert into weeks.json: create the week entry if the Saturday batch hasn't
    # run yet, else replace only this day's news post - never touch other lanes.
    data = json.load(open(bw.WEEKS))
    week = next((w for w in data["weeks"] if w.get("id") == wid), None)
    if week is None:
        week = {"id": wid, "label": wlabel, "weekCommencing": wc,
                "builtAt": int(datetime.datetime.now(datetime.timezone.utc).timestamp()),
                "posts": []}
        data["weeks"].append(week)
    week["posts"] = [pp for pp in week["posts"] if pp.get("id") != pid] + [post]
    week["builtAt"] = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    json.dump(data, open(bw.WEEKS, "w"), indent=2, ensure_ascii=False)
    bw.news_fetch.mark_used([item])
    print(f"Upserted {pid} into weeks.json ({wid}) as {post['status']}.")

    try:
        import r2                                    # normalises R2_* env on import
        if os.getenv("R2_ACCESS_KEY_ID"):
            r2.ensure_bucket()
            r2.upload_tree(os.path.join(img, pid), prefix=f"{wid}/{pid}/")
            print(f"uploaded {pid} to R2.")
    except Exception as e:
        print("R2 upload skipped:", e)

    # Hand the built ids to the workflow so it can schedule this post to Ayrshare
    # at the news slot (news-daily.yml reads these step outputs). Only emitted on a
    # real build.
    gho = os.getenv("GITHUB_OUTPUT")
    if gho:
        with open(gho, "a") as fh:
            fh.write(f"pid={pid}\nwid={wid}\n")


if __name__ == "__main__":
    main()
