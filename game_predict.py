import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score

# 데이터 불러오기
kbo_df = pd.read_csv("kbo_2024_to_now.csv")
pitchers_df = pd.read_csv("pitchers.csv")
teams_df = pd.read_csv("teams.csv")

# 병합 및 전처리
kbo_df["홈팀승"] = (kbo_df["승리팀"] == kbo_df["홈팀"]).astype(int)
pitchers_df = pitchers_df.rename(columns={"이름": "선발투수"})
teams_df.columns = teams_df.columns.str.strip()
teams_df = teams_df.rename(columns={"팀": "팀명"})

kbo_df = kbo_df.merge(pitchers_df.add_prefix("홈_"), left_on="홈선발", right_on="홈_선발투수", how="left")
kbo_df = kbo_df.merge(pitchers_df.add_prefix("원정_"), left_on="원정선발", right_on="원정_선발투수", how="left")
kbo_df = kbo_df.merge(teams_df.add_prefix("홈_"), left_on="홈팀", right_on="홈_팀명", how="left")
kbo_df = kbo_df.merge(teams_df.add_prefix("원정_"), left_on="원정팀", right_on="원정_팀명", how="left")
kbo_df.columns = kbo_df.columns.str.strip()

# 피처 목록
feature_cols = [
    
    "홈_ERA", "홈_최근5경기ERA", "홈_WHIP",
    "원정_ERA", "원정_최근5경기ERA", "원정_WHIP",
    "홈_팀OPS", "홈_팀ERA", "홈_타율", "홈_최근5경기 득점평균", "홈_시즌 승률", "홈_최근 5경기 승률",
    "원정_팀OPS", "원정_팀ERA", "원정_타율", "원정_최근5경기 득점평균", "원정_시즌 승률", "원정_최근 5경기 승률"


]

# 학습 데이터 준비
kbo_df[feature_cols] = kbo_df[feature_cols].apply(pd.to_numeric, errors="coerce")
final_df = kbo_df.dropna(subset=feature_cols + ["홈팀승"])
X = final_df[feature_cols]
y = final_df["홈팀승"]

# 학습
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 평가
y_proba = model.predict_proba(X_test)[:, 1]
print(f"✅ 정확도: {accuracy_score(y_test, model.predict(X_test)):.4f}")
print(f"✅ ROC AUC: {roc_auc_score(y_test, y_proba):.4f}")

# 예측 함수
def predict_game(home_team, away_team, home_pitcher, away_pitcher):
    home_team_row = teams_df[teams_df["팀명"] == home_team].iloc[0]
    away_team_row = teams_df[teams_df["팀명"] == away_team].iloc[0]
    home_pitcher_row = pitchers_df[pitchers_df["선발투수"] == home_pitcher].iloc[0]
    away_pitcher_row = pitchers_df[pitchers_df["선발투수"] == away_pitcher].iloc[0]

    input_data = pd.DataFrame([{
        "홈_ERA": home_pitcher_row["ERA"],
        "홈_최근5경기ERA": home_pitcher_row["최근5경기ERA"],
        "홈_WHIP": home_pitcher_row["WHIP"],
        "원정_ERA": away_pitcher_row["ERA"],
        "원정_최근5경기ERA": away_pitcher_row["최근5경기ERA"],
        "원정_WHIP": away_pitcher_row["WHIP"],
        "홈_팀OPS": home_team_row["팀OPS"],
        "홈_팀ERA": home_team_row["팀ERA"],
        "홈_타율": home_team_row["타율"],
        "홈_최근5경기 득점평균": home_team_row["최근5경기 득점평균"],
        "홈_시즌 승률": home_team_row["시즌 승률"],
        "홈_최근 5경기 승률": home_team_row["최근 5경기 승률"],
        "원정_팀OPS": away_team_row["팀OPS"],
        "원정_팀ERA": away_team_row["팀ERA"],
        "원정_타율": away_team_row["타율"],
        "원정_최근5경기 득점평균": away_team_row["최근5경기 득점평균"],
        "원정_시즌 승률": away_team_row["시즌 승률"],
        "원정_최근 5경기 승률": away_team_row["최근 5경기 승률"]
    }])

    return model.predict_proba(input_data)[0][1]




# 예시 실행
if __name__ == "__main__":
    prob = predict_game("LG", "한화", "임찬규", "류현진")
    print(f"🎯 LG vs 한화 (임찬규 vs 류현진) → 홈팀 승리 확률: {prob * 100:.2f}%")
