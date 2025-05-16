from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import csv

# 셀레니움 옵션 (모바일 위장)
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1")

driver = webdriver.Chrome(options=options)

start_date = datetime(2024, 3, 23)
end_date = datetime.today()

results = []

while start_date <= end_date:
    date_str = start_date.strftime("%Y-%m-%d")
    url = f"https://m.sports.naver.com/kbaseball/schedule/index?date={date_str}"
    print(f"📅 {date_str} 크롤링 중...")
    
    try:
        driver.get(url)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        games = soup.select("li.MatchBox_match_item__3_D0Q")

        for game in games:
            try:
                team_blocks = game.select("div.MatchBoxHeadToHeadArea_team_item__25jg6")
                if len(team_blocks) != 2:
                    continue

                team_data = []

                for team in team_blocks:
                    team_name = team.select_one(".MatchBoxHeadToHeadArea_team__40JQL").text.strip()
                    score = int(team.select_one(".MatchBoxHeadToHeadArea_score__e2D7k").text.strip())

                    pitcher_tags = team.select(".MatchBoxHeadToHeadArea_item__1IPbQ")
                    result = pitcher_tags[0].text.strip() if len(pitcher_tags) > 0 else ""
                    pitcher = pitcher_tags[1].text.strip() if len(pitcher_tags) > 1 else ""

                    is_home = team.select_one(".MatchBoxHeadToHeadArea_home_mark__i18Sf") is not None

                    team_data.append({
                        "team": team_name,
                        "score": score,
                        "result": result,
                        "pitcher": pitcher,
                        "is_home": is_home
                    })

                home = next(t for t in team_data if t["is_home"])
                away = next(t for t in team_data if not t["is_home"])
                winner = home["team"] if home["score"] > away["score"] else away["team"]

                results.append([
                    date_str, home["team"], away["team"],
                    home["pitcher"], away["pitcher"],
                    home["score"], away["score"],
                    winner
                ])

                print(f"→ {away['team']}({away['score']}) vs {home['team']}({home['score']}) → 승: {winner}")

            except Exception as e:
                print(f"⚠️ 경기 파싱 오류: {e}")

    except Exception as e:
        print(f"❌ 페이지 접근 오류: {e}")

    start_date += timedelta(days=1)

driver.quit()

# 저장
with open("kbo_2024_to_now.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["날짜", "홈팀", "원정팀", "홈선발", "원정선발", "홈점수", "원정점수", "승리팀"])
    writer.writerows(results)

print("✅ 전체 기간 크롤링 완료! 'kbo_2024_to_now.csv' 저장됨.")
print(f"총 수집된 경기 수: {len(results)}")
print("샘플 출력 (앞 5경기):")
for row in results[:5]:
    print(row)

