#!/usr/bin/env python3
"""youtube_id 가 비어 있는 곡에 YouTube Data API v3 로 공식 노래방 채널의 영상 ID를 채운다.

- 환경 변수 YOUTUBE_API_KEY 가 없으면 아무것도 하지 않는다(워크플로는 그대로 성공).
- 무료 할당량(하루 10,000 unit, search 1회 = 100 unit)을 지키려고 한 번에 최대 MAX_PER_RUN 곡만 처리한다.
  매일 돌면 자연스럽게 전부 채워진다.
- 검색은 TJ 노래방 / 금영 노래방 공식 채널에 한정하려고 쿼리에 채널명을 넣고, 결과 제목에 곡명이 들어간 것만 받는다.
- 앱은 이 ID를 YouTube 공식 IFrame 플레이어로만 재생한다(다운로드·백그라운드 재생 없음).
"""
import csv
import json
import os
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "data", "songs.csv")
MAX_PER_RUN = int(os.environ.get("YOUTUBE_MAX_PER_RUN", "60"))
API_KEY = os.environ.get("YOUTUBE_API_KEY", "").strip()


def search(query):
    params = {
        "part": "snippet", "type": "video", "maxResults": 5, "videoEmbeddable": "true",
        "q": query, "key": API_KEY, "regionCode": "KR", "relevanceLanguage": "ko",
    }
    url = "https://www.googleapis.com/youtube/v3/search?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=20) as r:
        return json.load(r).get("items", [])


def norm(s):
    return "".join(ch for ch in s.lower() if ch.isalnum())


def main():
    if not API_KEY:
        print("YOUTUBE_API_KEY not set; skipping youtube id fetch")
        return
    with open(PATH, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
        fields = f and ["title", "artist", "tj", "ky", "genre", "month", "youtube_id"]
    done = 0
    for row in rows:
        if row.get("youtube_id") or done >= MAX_PER_RUN:
            continue
        q = f"{row['title']} {row['artist']} 노래방"
        try:
            items = search(q)
        except Exception as e:  # 할당량 초과 등: 다음 날 다시
            print("search failed:", e, file=sys.stderr)
            break
        done += 1
        want = norm(row["title"])
        for it in items:
            title = it["snippet"]["title"]
            channel = it["snippet"]["channelTitle"]
            if want and want in norm(title) and ("노래방" in channel or "KARAOKE" in channel.upper() or "노래방" in title):
                row["youtube_id"] = it["id"]["videoId"]
                print(f"{row['title']} -> {row['youtube_id']} ({channel})")
                break
    with open(PATH, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"searched {done} songs")


if __name__ == "__main__":
    main()
