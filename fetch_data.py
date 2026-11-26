"""증권업 뉴스 + 현대차증권 뉴스를 구글뉴스 RSS에서 모아 data.json으로 저장 (표준 라이브러리만 사용, 인증키 불필요)"""
import difflib, json, os, re, sys, urllib.request, urllib.parse, xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

KST = timezone(timedelta(hours=9))
NOW = datetime.now(KST)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")

# 꼭지별 검색어 / 최근 며칠 / 제목에 있으면 뺄 말(종목 리포트성 기사 등). 필요하면 여기만 고치면 됨
TOPICS = {
    "industry": {"q": "증권업 OR 증권사 OR 증권업계", "days": 2, "exclude": ["목표주가", "목표가", "투자의견", "특징주"]},
    "hmc": {"q": '"현대차증권"', "days": 14, "exclude": []},
}

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

def norm(t):
    return re.sub(r"[^0-9a-z가-힣]", "", t.lower())

def news(q, days, exclude=()):
    """기사를 모두 가져와 제목이 거의 같은 기사는 하나만 남기고 최신순 정렬"""
    url = "https://news.google.com/rss/search?" + urllib.parse.urlencode(
        {"q": q + f" when:{days}d", "hl": "ko", "gl": "KR", "ceid": "KR:ko"})
    items, seen = [], []
    for it in ET.fromstring(get(url)).iter("item"):
        title = (it.findtext("title") or "").strip()
        src = (it.findtext("source") or "").strip()
        if src and title.endswith(" - " + src):
            title = title[: -len(src) - 3]
        k = norm(title)
        if not k or any(w in title for w in exclude):
            continue
        if any(difflib.SequenceMatcher(None, k, o).ratio() >= 0.8 for o in seen):
            continue
        seen.append(k)
        try:
            dt = parsedate_to_datetime(it.findtext("pubDate")).astimezone(KST)
        except Exception:
            dt = None
        items.append((dt or NOW, {"title": title, "source": src,
                                  "date": dt.strftime("%m.%d %H:%M") if dt else "", "url": it.findtext("link")}))
    items.sort(key=lambda x: x[0], reverse=True)
    return [i[1] for i in items]

def main():
    try:
        old = json.load(open(OUT, encoding="utf-8"))
    except Exception:
        old = {}
    stamp = NOW.strftime("%Y-%m-%d %H:%M")
    data = {"notes": [], "sample": old.get("sample", False)}
    for key, t in TOPICS.items():
        data[key] = old.get(key, []); data[key + "_updated"] = old.get(key + "_updated", ""); data[key + "_days"] = t["days"]
        try:
            data[key] = news(t["q"], t["days"], t["exclude"]); data[key + "_updated"] = stamp; data["sample"] = False
        except Exception as e:
            print(key, "실패:", e, file=sys.stderr)
            data["notes"].append(f"{key} 갱신 실패(이전 내용 표시): " + str(e)[:200])
    data["updated"] = stamp
    json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()
