# 증권업 주요 뉴스 (모바일 웹앱) - 설정 순서

퇴직연금 도구와 별개로 **새 저장소**(예: securities-news-tool)를 만들어 올리세요. 인증키는 필요 없습니다.

1. GitHub에서 공개(Public) 저장소를 새로 만듭니다. (README 등 체크 항목은 모두 비움)
2. 이 폴더의 파일 중 `workflow-update.yml`을 뺀 나머지(index.html, manifest.json, sw.js, icon 3개, fetch_data.py, data.json, README.md)를 Upload files로 올립니다.
3. Settings > Pages: Branch `main` / `(root)` 저장.
4. Code 탭 > + > Create new file: 이름 `.github/workflows/update.yml`, 내용은 workflow-update.yml 전체를 붙여넣고 Commit. 첫 수집이 자동 실행됩니다.
5. Actions 탭에서 update-data가 초록 체크가 되면 완료. 주소: https://계정이름.github.io/저장소이름/

- 검색어, 기간, 제외할 단어는 `fetch_data.py` 위쪽 `TOPICS`에서 바꿉니다.
- 이미 운영 중일 때는 고칠 파일만 올리고 data.json은 다시 올리지 마세요(샘플로 덮어써짐).
