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

