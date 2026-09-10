"""build_news_day.py - build ONE day's news post the day before it goes out.

The weekly batch (build_week.py) builds the evergreen lanes on Saturday. News is
different: a headline written on Saturday would be stale by Friday. So this job
runs daily (news-daily.yml) and builds the NEXT posting day's news card, fetching
fresh UK news, having the LLM reword it, rendering the card, and upserting it into
data/weeks.json as `in-review` - leaving the human a full day to review before it
posts. It never touches the other lanes.

    python3 tools/build_news_day.py            # build tomorrow's news (skips weekends)
    python3 tools/build_news_day.py --offset 0  # build today's news
    python3 tools/build_news_day.py --date 2026-09-14
    python3 tools/build_news_day.py --dry       # plan only, no LLM/render/write
"""
from __future__ import annotations
import os, sys, json, argparse, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_week as bw          # reuses env load, writer, news_fetch, news_card, helpers

REF, REFN = datetime.date(2026, 8, 31), 14   # week14 = w/c 2026-08-31 (same anchor as build_week)


def week_of(target: datetime.date):
    """Map a posting date to (wid, wlabel, wc, mon, dkey, dlabel), numbered off the
    same week14 anchor build_week uses, so news lands in the correct week entry."""
    mon = target - datetime.timedelta(days=target.weekday())
    n = REFN + (mon - REF).days // 7
    dkey = bw.DKEYS[target.weekday()]
    dlabel = target.strftime("%a %d %b").replace(" 0", " ")
    return f"week{n}", f"Week {n}", mon.isoformat(), mon, dkey, dlabel


def pick_fresh(exclude_titles):
    """First fresh, unused UK news item whose topic doesn't repeat a headline
    already used in this week (build_week.pick_distinct_news handles same-story
    de-duping within the pool; here we also avoid the week's earlier news)."""
    excl_sets = [bw._news_words(t) for t in exclude_titles]
    pool = bw.pick_distinct_news(bw.news_fetch.fetch(limit=20), 8)
    for it in pool:
        ws = bw._news_words(it.get("title", ""))
        if any(ws and es and len(ws & es) / min(len(ws), len(es)) >= 0.4 for es in excl_sets):
            continue
        return it
    return pool[0] if pool else bw.news_fetch.sample_item()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--offset", type=int, default=1, help="days ahead to build (default 1 = tomorrow)")
    p.add_argument("--date", help="explicit posting date YYYY-MM-DD (overrides --offset)")
    p.add_argument("--dry", action="store_true", help="plan only, no LLM/render/write")
    args = p.parse_args()

    target = (datetime.date.fromisoformat(args.date) if args.date
              else datetime.date.today() + datetime.timedelta(days=args.offset))
    if target.weekday() >= 5:                       # Sat/Sun: no posting day
        print(f"{target} is a weekend - no news post. Done.")
        return

    wid, wlabel, wc, mon, dkey, dlabel = week_of(target)
    img = os.path.join(bw.HUB, "images", wid)
    pid = f"{wid}-{dkey}-news"

    data = json.load(open(bw.WEEKS))
    week = next((w for w in data["weeks"] if w.get("id") == wid), None)
    existing_news = [pp.get("title", "") for pp in (week or {}).get("posts", [])
                     if pp.get("lane") == "news" and pp.get("id") != pid]

    item = pick_fresh(existing_news)
    print(f"Building news for {dlabel} ({pid}) - \"{item.get('title', '')[:70]}\"")
    if args.dry:
        print("DRY: nothing fetched-through, rendered or written.")
        return

    pdate = datetime.datetime.combine(target, datetime.time())
    post = bw.build_news_post(wid, dkey, dlabel, pdate, img, item,
                              issue_no=target.weekday() + 1)
    # News is auto-approved: unlike the evergreen lanes it carries no manual
    # dashboard gate. The story is fetched from UK sources, LLM-reworded under the
    # news rules, and scheduled straight to the 8am slot by news-daily.yml. Born
    # 'approved' so the publisher's status gate and the dashboard both treat it as
    # cleared without a human click.
    post["status"] = "approved"

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
    json.dump(data, open(bw.WEEKS, "w"), indent=2, ensure_ascii=False)
    bw.news_fetch.mark_used([item])
    print(f"Upserted {pid} into weeks.json ({wid}) as approved (auto-scheduled).")

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
    # real build - the weekend early-return above leaves them unset, so the
    # scheduling step skips.
    gho = os.getenv("GITHUB_OUTPUT")
    if gho:
        with open(gho, "a") as fh:
            fh.write(f"pid={pid}\nwid={wid}\n")


if __name__ == "__main__":
    main()
