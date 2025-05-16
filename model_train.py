import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# CSV 불러오기
games = pd.read_csv("games.csv")
pitchers = pd.read_csv("pitchers.csv")
teams = pd.read_csv("teams.csv")

# games에 ERA 병합
games = pd.merge(games, pitchers[['이름', 'ERA', '최근5경기ERA']], left_on='홈선발', right_on='이름', how='left')
games.rename(columns={'ERA': '홈ERA', '최근5경기ERA': '홈최근ERA'}, inplace=True)
games.drop(columns=['이름'], inplace=True)

games = pd.merge(games, pitchers[['이름', 'ERA', '최근5경기ERA']], left_on='원정선발', right_on='이름', how='left')
games.rename(columns={'ERA': '원정ERA', '최근5경기ERA': '원정최근ERA'}, inplace=True)
games.drop(columns=['이름'], inplace=True)

# teams.csv에서 OPS, 승률 병합
games = pd.merge(games, teams, left_on='홈팀', right_on='팀', how='left')
games.rename(columns={'OPS': '홈OPS', '최근5경기승률': '홈승률'}, inplace=True)
games.drop(columns=['팀'], inplace=True)

games = pd.merge(games, teams, left_on='원정팀', right_on='팀', how='left')
games.rename(columns={'OPS': '원정OPS', '최근5경기승률': '원정승률'}, inplace=True)
games.drop(columns=['팀'], inplace=True)

# 정답 라벨 생성
games['홈승'] = (games['승팀'] == games['홈팀']).astype(int)

# Feature와 Label 설정
X = games[['홈ERA', '원정ERA', '홈최근ERA', '원정최근ERA', '홈OPS', '원정OPS', '홈승률', '원정승률']]
y = games['홈승']

# 학습/테스트 분리 및 모델 학습
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# 모델 저장
with open("kbo_rf_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ 모델 학습 및 저장 완료: kbo_rf_model.pkl")
