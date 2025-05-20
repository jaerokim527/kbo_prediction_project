import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 윈도우 사용자라면 맑은 고딕(Malgun Gothic) 사용
plt.rcParams["font.family"] = "Malgun Gothic"

# 또는 macOS라면 AppleGothic, Ubuntu는 NanumGothic 등 사용

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# 🔹 데이터 불러오기
kbo_df = pd.read_csv("kbo_2024_to_now.csv")
pitchers_df = pd.read_csv("pitchers.csv")
teams_df = pd.read_csv("teams.csv")

# 🔹 병합 전처리
kbo_df["홈팀승"] = (kbo_df["승리팀"] == kbo_df["홈팀"]).astype(int)
pitchers_df = pitchers_df.rename(columns={"이름": "선발투수"})
teams_df.columns = teams_df.columns.str.strip()
teams_df = teams_df.rename(columns={"팀": "팀명"})

kbo_df = kbo_df.merge(pitchers_df.add_prefix("홈_"), left_on="홈선발", right_on="홈_선발투수", how="left")
kbo_df = kbo_df.merge(pitchers_df.add_prefix("원정_"), left_on="원정선발", right_on="원정_선발투수", how="left")
kbo_df = kbo_df.merge(teams_df.add_prefix("홈_"), left_on="홈팀", right_on="홈_팀명", how="left")
kbo_df = kbo_df.merge(teams_df.add_prefix("원정_"), left_on="원정팀", right_on="원정_팀명", how="left")
kbo_df.columns = kbo_df.columns.str.strip()

# 🔹 피처 목록
feature_cols = [
    "홈_ERA", "홈_최근5경기ERA", "홈_WHIP",
    "원정_ERA", "원정_최근5경기ERA", "원정_WHIP",
    "홈_팀OPS", "홈_팀ERA", "홈_타율", "홈_최근5경기 득점평균", "홈_시즌 승률", "홈_최근 5경기 승률",
    "원정_팀OPS", "원정_팀ERA", "원정_타율", "원정_최근5경기 득점평균", "원정_시즌 승률", "원정_최근 5경기 승률"
]

# 🔹 숫자형 변환 및 결측 제거
kbo_df[feature_cols] = kbo_df[feature_cols].apply(pd.to_numeric, errors="coerce")
final_df = kbo_df.dropna(subset=feature_cols + ["홈팀승"])

X = final_df[feature_cols]
y = final_df["홈팀승"]

# 🔹 모델 학습
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 🔹 피처 중요도 시각화
importances = model.feature_importances_
feature_importance_df = pd.DataFrame({
    "Feature": feature_cols,
    "Importance": importances
}).sort_values(by="Importance", ascending=True)

plt.figure(figsize=(10, 8))
plt.barh(feature_importance_df["Feature"], feature_importance_df["Importance"])
plt.xlabel("Importance")
plt.title("🎯 Feature Importance (Random Forest)")
plt.tight_layout()
plt.grid(axis="x")
plt.show()
