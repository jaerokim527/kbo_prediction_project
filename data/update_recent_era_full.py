import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import urllib.parse
import time
import difflib

# 1. 전체 투수 테이블에서 선수 이름 ↔ playerId 추출
def get_all_pitcher_ids():
    url = "https://www.koreabaseball.com/Record/Player/PitcherBasic/Basic1.aspx"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    pitcher_ids = {}
    links = soup.select("table.tData01.tt a")

    for link in links:
        name = link.text.strip().replace(" ", "")
        href = link.get("href", "")
        match = re.search(r'playerId=(\d+)', href)
        if match:
            pitcher_ids[name] = match.group(1)

    return pitcher_ids

# 2. 이름 유사도 기반 playerId 매칭
def get_player_id_fuzzy(name, pitcher_ids):
    name_clean = name.replace(" ", "")
    candidates = list(pitcher_ids.keys())
    match = difflib.get_close_matches(name_clean, candidates, n=1, cutoff=0.7)
    return pitcher_ids[match[0]] if match else None

# 3. 기본 ERA, WHIP 가져오기
def get_basic_stats(player_id):
    url = f"https://www.koreabaseball.com/Record/Player/PitcherDetail/Basic.aspx?playerId={player_id}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    table = soup.find("table", {"class": "tData01 tt"})
    if not table:
        return None, None

    df = pd.read_html(str(table))[0]
    if "ERA" not in df.columns or "WHIP" not in df.columns:
        return None, None

    era = float(df.iloc[0]["ERA"])
    whip = float(df.iloc[0]["WHIP"])
    return era, whip

# 4. 이닝 문자열 → 소수로 변환
def parse_inning(text):
    if isinstance(text, str) and '.' in text:
        main, sub = text.split('.')
        return int(main) + int(sub)/3
    try:
        return float(text)
    except:
        return 0.0

# 5. 최근 5경기 ERA 계산
def get_recent_5_era(player_id):
    url = f'https://www.koreabaseball.com/Record/Player/PitcherDetail/Game.aspx?playerId={player_id}'
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    table = soup.find('table', {'class': 'tData01 tt'})
    if not table:
        return None

    df = pd.read_html(str(table))[0]
    df = df[df['출장'] == '선발']
    recent_5 = df.head(5)

    if recent_5.empty:
        return None

    total_er = recent_5['자책'].astype(float).sum()
    total_ip = recent_5['이닝'].apply(parse_inning).sum()

    if total_ip == 0:
        return None

    era = round((total_er / total_ip) * 9, 2)
    return era

# 6. 전체 실행 함수
def update_selected_pitchers(names):
    pitcher_ids = get_all_pitcher_ids()
    results = []

    for name in names:
        print(f"[처리 중] {name}")
        pid = get_player_id_fuzzy(name, pitcher_ids)
        time.sleep(1)

        if not pid:
            print(f"⚠️  {name}의 playerId를 찾지 못함")
            results.append({'name': name, 'playerId': None, 'ERA': None, 'Recent5_ERA': None, 'WHIP': None})
            continue

        era, whip = get_basic_stats(pid)
        recent_era = get_recent_5_era(pid)
        results.append({'name': name, 'playerId': pid, 'ERA': era, 'Recent5_ERA': recent_era, 'WHIP': whip})

    df = pd.DataFrame(results)
    df.to_csv("data/selected_pitchers_stats.csv", index=False)
    print("\n✅ 저장 완료: data/selected_pitchers_stats.csv")

# 7. 너가 입력한 선수들
manual_pitchers = [
    "에르난데스", "치리노스", "손주영", "임찬규", "코엔윈", "최채흥", "송승기", "폰세", "류현진", "문동주",
    "와이스", "엄상백", "데이비슨", "박세웅", "나균안", "박진", "이민석", "김진욱", "후라도", "원태인",
    "최원태", "레예스", "이승현", "앤더슨", "화이트", "문승원", "김광현", "송영진", "박종훈", "라일리",
    "로건", "신민혁", "최성영", "목지훈", "김녹원", "잭로그", "박정수", "콜어빈", "최원준", "최승용",
    "최준호", "김유성", "네일", "김도현", "올러", "황동하", "양현종", "윤영철", "헤이수스", "오원석",
    "소형준", "고영표", "쿠에바스", "로젠버그", "정현우", "하영민", "김선기", "김윤하", "조영건", "김연주", "박주성"
]

if __name__ == "__main__":
    update_selected_pitchers(manual_pitchers)

