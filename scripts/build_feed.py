#!/usr/bin/env python3
"""data/*.csv → feed/songs.json

싱넘버 앱이 매일 새벽에 내려받는 피드 파일을 만든다.
서버 없이 GitHub Pages(또는 raw.githubusercontent.com)에서 정적 파일로 제공한다.

피드 형식 (앱의 FeedUpdater가 읽는다):
{
  "version": "2026-10-21",          # 바뀌었을 때만 앱이 반영
  "generated_at": "2026-10-21T19:00:00Z",
  "notice": "...",
  "songs": [ {title, artist, tj, ky, genre, month, youtube_id,
              tj_week, tj_month, ky_week, ky_month} ... ]
}
"""
import csv
import datetime as dt
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
FEED = os.path.join(ROOT, "feed")


def read_csv(name):
    path = os.path.join(DATA, name)
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def to_int(v):
    v = (v or "").strip()
    return int(v) if v.isdigit() else None


def main():
    songs = read_csv("songs.csv")
    charts = read_csv("charts.csv")

    rank = {}  # (title, artist) -> {tj_week: n, ...}
    for c in charts:
        key = (c["title"].strip(), c["artist"].strip())
        col = f"{c['machine'].strip().lower()}_{c['period'].strip().lower()}"
        if col not in ("tj_week", "tj_month", "ky_week", "ky_month"):
            print(f"skip chart row with unknown machine/period: {c}", file=sys.stderr)
            continue
        rank.setdefault(key, {})[col] = to_int(c["rank"])

    out = []
    seen = set()
    for s in songs:
        title, artist = s["title"].strip(), s["artist"].strip()
        if not title or (title, artist) in seen:
            continue
        seen.add((title, artist))
        tj, ky = to_int(s.get("tj")), to_int(s.get("ky"))
        if tj is None and ky is None:
            continue
        r = rank.get((title, artist), {})
        out.append({
            "title": title,
            "artist": artist,
            "tj": tj,
            "ky": ky,
            "genre": (s.get("genre") or "기타").strip() or "기타",
            "month": (s.get("month") or "").strip() or None,
            "youtube_id": (s.get("youtube_id") or "").strip() or None,
            "tj_week": r.get("tj_week"),
            "tj_month": r.get("tj_month"),
            "ky_week": r.get("ky_week"),
            "ky_month": r.get("ky_month"),
        })

    now = dt.datetime.now(dt.timezone.utc)
    kst = now + dt.timedelta(hours=9)
    feed = {
        "version": kst.strftime("%Y-%m-%d"),
        "generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "notice": "곡 번호·순위는 data/*.csv 를 기준으로 생성됩니다. 실제 기기에서 확인하세요.",
        "songs": out,
    }
    os.makedirs(FEED, exist_ok=True)
    path = os.path.join(FEED, "songs.json")
    # 내용이 같으면 version만 바뀌는 커밋을 피하기 위해 songs 부분을 비교한다
    if os.path.exists(path):
        try:
            old = json.load(open(path, encoding="utf-8"))
            if old.get("songs") == out:
                print("feed unchanged; keeping existing version", old.get("version"))
                return
        except Exception:
            pass
    with open(path, "w", encoding="utf-8") as f:
        json.dump(feed, f, ensure_ascii=False, indent=1)
    print(f"wrote {path}: {len(out)} songs, version {feed['version']}")


if __name__ == "__main__":
    main()
