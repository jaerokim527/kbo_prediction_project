import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import csv

# 날짜 설정
start_date = datetime(2024, 3, 23)
end_date = datetime.today()

results = []

while start_date <= end_date:
    year = start_date.year
    month = start_date.month
    day = start_date.day
    date_str = start_date.strftime("%Y-%m-%d")

    url = f"http://www.statiz.co.kr/boxscore.php?opt=1&year={year}&month={month}&day={day}"
    print(f"📅 {date_str} 크롤링 중...")

    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        games = soup.select("div.boxscore_game")

        if not games:
            print(f"❌ {date_str} 경기 없음")
        for game in games:
            teams = game.select("table.boxscore_team tr")[1:3]
            if len(teams) < 2:
                continue

            away_team = teams[0].select_one("td").text.strip()
            home_team = teams[1].select_one("td").text.strip()
            away_score = teams[0].select("td")[-1].text.strip()
            home_score = teams[1].select("td")[-1].text.strip()

            pitcher_tables = game.select("table.boxscore_player")
            if len(pitcher_tables) < 2:
                continue
            away_pitcher = pitcher_tables[1].select("tr")[1].select("td")[1].text.strip()
            home_pitcher = pitcher_tables[0].select("tr")[1].select("td")[1].text.strip()

            winner = home_team if int(home_score) > int(away_score) else away_team

            results.append([
                date_str,
                home_team, away_team,
                home_pitcher, away_pitcher,
                home_score, away_score,
                winner
            ])
    except Exception as e:
        print(f"⚠️ {date_str} 오류 발생: {e}")

    start_date += timedelta(days=1)

# CSV로 저장
with open("statiz_kbo_2024_to_2025.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["날짜", "홈팀", "원정팀", "홈선발", "원정선발", "홈점수", "원정점수", "승팀"])
    writer.writerows(results)

print("✅ 크롤링 완료! 결과 저장됨.")
