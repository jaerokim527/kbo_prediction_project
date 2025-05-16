import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

start_date = datetime.strptime('2025-04-01', '%Y-%m-%d')
end_date = datetime.strptime('2025-05-15', '%Y-%m-%d')
games = []

while start_date <= end_date:
    date_str = start_date.strftime('%Y-%m-%d')
    url = f'https://sports.news.naver.com/kbaseball/schedule/index?date={date_str}'
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        rows = soup.select('.schedule_tb tbody tr')

        for game in rows:
            teams = game.select('td.team')
            if len(teams) == 2:
                home = teams[0].text.strip()
                away = teams[1].text.strip()
                score_td = game.select_one('td.vs')
                if score_td and ':' in score_td.text:
                    score = score_td.text.strip()
                    home_score, away_score = map(int, score.split(':'))
                    winner = home if home_score > away_score else away
                    games.append([date_str, home, away, home_score, away_score, winner])
    except Exception as e:
        print(f"[{date_str}] 오류 발생:", e)

    start_date += timedelta(days=1)

df = pd.DataFrame(games, columns=['날짜', '홈팀', '원정팀', '홈점수', '원정점수', '승팀'])
df.to_csv('kbo_2025_games.csv', index=False, encoding='utf-8-sig')
print("저장 완료: kbo_2025_games.csv")
