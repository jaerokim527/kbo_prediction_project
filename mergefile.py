import pandas as pd

# 파일 불러오기
kbo_df = pd.read_csv("kbo_2024_to_now.csv")
pitchers_df = pd.read_csv("pitchers.csv")
teams_df = pd.read_csv("teams.csv")

# 1. 홈팀 승리 여부 만들기 (타겟값)
kbo_df["홈팀승"] = (kbo_df["승리팀"] == kbo_df["홈팀"]).astype(int)

# 2. 선발투수 ERA/WHIP 병합
pitchers_df = pitchers_df.rename(columns={"이름": "선발투수"})
kbo_df = kbo_df.merge(pitchers_df.add_prefix("홈_"), left_on="홈선발", right_on="홈_선발투수", how="left")
kbo_df = kbo_df.merge(pitchers_df.add_prefix("원정_"), left_on="원정선발", right_on="원정_선발투수", how="left")

# ✅ 3. 팀 통계 컬럼 공백 제거 먼저!
teams_df.columns = teams_df.columns.str.strip()
teams_df = teams_df.rename(columns={"팀": "팀명"})

# 4. 팀 통계 병합
kbo_df = kbo_df.merge(teams_df.add_prefix("홈_"), left_on="홈팀", right_on="홈_팀명", how="left")
kbo_df = kbo_df.merge(teams_df.add_prefix("원정_"), left_on="원정팀", right_on="원정_팀명", how="left")

# ✅ 5. 병합된 컬럼 공백 제거 (strip) 한 번 더
kbo_df.columns = kbo_df.columns.str.strip()

# ✅ 6. 컬럼명 확인 (선택)
# print(kbo_df.columns.tolist())  # 확인용

print("\n💡 현재 컬럼명 목록:")
for col in kbo_df.columns:
    if "승률" in col:
        print(f"'{col}'")


# 7. 사용할 피처 목록 정의 (정확한 컬럼명 사용)
feature_cols = [
    "홈_ERA", "홈_최근5경기ERA", "홈_WHIP",
    "원정_ERA", "원정_최근5경기ERA", "원정_WHIP",
    "홈_팀OPS", "홈_팀ERA", "홈_타율", "홈_최근5경기 득점평균", "홈_시즌 승률", "홈_최근 5경기 승률",
    "원정_팀OPS", "원정_팀ERA", "원정_타율", "원정_최근5경기 득점평균", "원정_시즌 승률", "원정_최근 5경기 승률"
    
]

# 8. 숫자형으로 변환 및 결측치 제거
kbo_df[feature_cols] = kbo_df[feature_cols].apply(pd.to_numeric, errors="coerce")
final_df = kbo_df.dropna(subset=feature_cols + ["홈팀승"])

# 9. 결과 확인용
print("✅ 최종 데이터 개수:", len(final_df))
print(final_df[feature_cols + ["홈팀승"]].head())
