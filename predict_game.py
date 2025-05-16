import pandas as pd
import pickle

# 모델 불러오기
with open("kbo_rf_model.pkl", "rb") as f:
    model = pickle.load(f)

# 스탯 불러오기
pitchers = pd.read_csv("pitchers.csv")
teams = pd.read_csv("teams.csv")

# 예측 함수 정의
def predict_game(home_team, away_team, home_pitcher, away_pitcher):
    try:
        # 투수 스탯
        home_era = pitchers.loc[pitchers['이름'] == home_pitcher, 'ERA'].values[0]
        home_recent_era = pitchers.loc[pitchers['이름'] == home_pitcher, '최근5경기ERA'].values[0]
        away_era = pitchers.loc[pitchers['이름'] == away_pitcher, 'ERA'].values[0]
        away_recent_era = pitchers.loc[pitchers['이름'] == away_pitcher, '최근5경기ERA'].values[0]

        # 팀 스탯
        home_ops = teams.loc[teams['팀'] == home_team, 'OPS'].values[0]
        home_winrate = teams.loc[teams['팀'] == home_team, '최근5경기승률'].values[0]
        away_ops = teams.loc[teams['팀'] == away_team, 'OPS'].values[0]
        away_winrate = teams.loc[teams['팀'] == away_team, '최근5경기승률'].values[0]

        # 입력 데이터 구성
        input_df = pd.DataFrame([{
            '홈ERA': home_era,
            '원정ERA': away_era,
            '홈최근ERA': home_recent_era,
            '원정최근ERA': away_recent_era,
            '홈OPS': home_ops,
            '원정OPS': away_ops,
            '홈승률': home_winrate,
            '원정승률': away_winrate
        }])

        # 예측
        proba = model.predict_proba(input_df)[0][1]
        print(f"\n🏟️ {home_team} vs {away_team}")
        print(f"🎯 예측 결과: 홈팀({home_team}) 승리 확률 = {proba * 100:.2f}%\n")

    except IndexError:
        print("⚠️ 입력한 팀 또는 투수 이름이 데이터에 없습니다.")

# 테스트
predict_game("LG", "두산", "류현진", "박정수")
