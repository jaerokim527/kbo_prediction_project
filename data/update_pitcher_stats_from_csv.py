import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from io import StringIO

def get_basic_stats(player_id):
    print(f"===[{player_id}] 테이블 내용 미리보기===")
    print(table.prettify()[:300])  # 앞부분만 출력

    url = f"https://www.koreabaseball.com/Record/Player/PitcherDetail/Basic.aspx?playerId={player_id}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    table = soup.find("table", {"class": "tData01 tt"})
    if not table:
        return None, None

    try:
        df = pd.read_html(StringIO(str(table)))[0]
        era = float(df.iloc[0]["ERA"])
        whip = float(df.iloc[0]["WHIP"])
        return era, whip
    except Exception as e:
        print(f"⚠️ ERA/WHIP 추출 실패: {e}")
        return None, None

def parse_inning(text):
    if isinstance(text, str) and '.' in text:
        main, sub = text.split('.')
        return int(main) + int(sub)/3
    try:
        return float(text)
    except:
        return 0.0

def get_recent_5_era(player_id):
    url = f'https://www.koreabaseball.com/Record/Player/PitcherDetail/Game.aspx?playerId={player_id}'
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    table = soup.find('table', {'class': 'tData01 tt'})
    if not table:
        return None
    try:
        df = pd.read_html(StringIO(str(table)))[0]
        df = df[df['출장'] == '선발']
        recent_5 = df.head(5)

        if recent_5.empty:
            return None

        total_er = recent_5['자책'].astype(float).sum()
        total_ip = recent_5['이닝'].apply(parse_inning).sum()

        if total_ip == 0:
            return None
        return round((total_er / total_ip) * 9, 2)
    except Exception as e:
        print(f"⚠️ 최근 5경기 ERA 추출 실패: {e}")
        return None



    

def update_pitcher_stats_from_csv(csv_path="data/selected_pitchers_stats.csv"):
    df = pd.read_csv(csv_path)
    updated_data = []

    for _, row in df.iterrows():
        name = row["name"]
        pid = str(row["playerId"])
        print(f"[업데이트 중] {name} ({pid})")
        time.sleep(1)

        era, whip = get_basic_stats(pid)
        recent_era = get_recent_5_era(pid)

        updated_data.append({
            "name": name,
            "playerId": pid,
            "ERA": era,
            "Recent5_ERA": recent_era,
            "WHIP": whip
        })

    updated_df = pd.DataFrame(updated_data)
    updated_df.to_csv(csv_path, index=False)
    print(f"\n✅ 업데이트 완료: {csv_path}")

if __name__ == "__main__":
    update_pitcher_stats_from_csv()

