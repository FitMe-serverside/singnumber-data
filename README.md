# singnumber-data — 싱넘버 데이터 피드 (서버 없음)

싱넘버 앱의 **신곡 · 인기곡 · 번호 데이터**를 매일 새벽 4시(KST)에 갱신해 정적 JSON으로 제공하는 저장소입니다.
유료 서버 대신 **GitHub Actions(스케줄 실행) + GitHub의 정적 파일 제공**만 씁니다. 전부 무료입니다.

```
data/songs.csv   ← 곡 마스터 (제목, 가수, TJ, KY, 장르, 등록월, youtube_id)   ← 여기만 고치면 됨
data/charts.csv  ← 인기곡 순위 (machine=TJ/KY, period=week/month, rank, 제목, 가수)
scripts/build_feed.py        data/*.csv → feed/songs.json
scripts/fetch_youtube_ids.py 비어 있는 youtube_id 를 YouTube Data API로 채움 (선택)
feed/songs.json  ← 앱이 내려받는 파일 (자동 생성, 직접 수정 금지)
docs/privacy.html ← 개인정보처리방침 (GitHub Pages: Settings → Pages → main, /docs)
.github/workflows/daily.yml  매일 04:00 KST 실행 + data/ 변경 push 시 즉시 실행 (_setup/daily.yml 의 복사본)
_setup/push-to-github.bat    처음 한 번: 워크플로 배치 + git init + push
```

## 처음 한 번만 (약 3분)

1. GitHub에서 **새 공개 저장소 `singnumber-data`** 를 만듭니다 (README 없이 빈 저장소). https://github.com/new
2. 이 폴더의 `_setup\push-to-github.bat` 을 더블클릭합니다. (워크플로 파일을 `.github\workflows\` 에 넣고,
   git 저장소를 만들어 GitHub로 올립니다. Git for Windows가 없으면 안내가 뜹니다.)
   수동으로 하려면 PowerShell에서:
   ```powershell
   cd C:\Users\user\Desktop\my-android-app\singnumber-data
   mkdir .github\workflows; copy _setup\daily.yml .github\workflows\daily.yml
   git init -b main; git add .; git commit -m "init data feed"
   git remote add origin https://github.com/FitMe-serverside/singnumber-data.git
   git push -u origin main
   ```
3. 저장소 → Settings → Actions → General → **Workflow permissions: Read and write** 로 바꿉니다 (봇이 feed를 커밋하려면 필요).
4. (선택) 앱 안 유튜브 재생용 영상 ID 자동 채우기: Google Cloud에서 **YouTube Data API v3** 키를 만들고
   저장소 Settings → Secrets → Actions → `YOUTUBE_API_KEY` 로 등록. 무료 할당량 안에서 하루 60곡씩 채웁니다.
5. 저장소 → Settings → Pages → Source: Deploy from a branch, Branch: main, Folder: /docs → Save.
   몇 분 뒤 `https://fitme-serverside.github.io/singnumber-data/privacy.html` 이 개인정보처리방침 URL이 됩니다(스토어 등록에 필요).
6. 앱의 피드 주소(기본값): `https://raw.githubusercontent.com/FitMe-serverside/singnumber-data/main/feed/songs.json`
   — 앱 설정 화면에서 바꿀 수 있습니다. GitHub Pages를 켜면 `https://fitme-serverside.github.io/singnumber-data/feed/songs.json` 도 됩니다.

## 매일 하는 일 (자동)
- 04:00 KST에 Actions가 돌아 `feed/songs.json` 을 다시 만들고, 내용이 바뀐 날만 커밋합니다.
- 앱은 하루 한 번(새벽 4~6시 사이, Wi-Fi/배터리 조건 충족 시) 피드의 `version` 이 바뀌었을 때만 DB에 반영합니다.
  사용자가 직접 추가한 곡·노트·플레이리스트는 건드리지 않습니다.

## 데이터는 어디서 오나 (중요)
- 지금 CSV는 **샘플**입니다. 실제 값은 사람이 CSV를 고치거나, 별도 수집 스크립트가 채워야 합니다.
- TJ미디어·금영 공식 사이트의 신곡/인기차트 페이지를 자동 수집(스크래핑)하는 것은 기술적으로 가능하지만
  각 사이트 이용약관에 따라 제한될 수 있어 **이 저장소에는 넣지 않았습니다**. 상용 서비스라면
  (1) 공식 제휴/데이터 제공 문의, (2) 공개 데이터(공식 유튜브 채널 공지 등) 수동 반영 중 하나를 권합니다.
- 노래 제목·가수명·곡 번호 자체는 사실 정보라 저작권 대상이 아닙니다. 가사는 저작물이므로 넣지 않습니다.

## 수동 실행
저장소 → Actions → "Build daily feed" → Run workflow. 또는 `python scripts/build_feed.py` 를 로컬에서 실행.
