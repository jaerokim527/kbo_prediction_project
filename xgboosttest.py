from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split


import xgboost as xgb
# 병합 및 전처리 이후
kbo_df[feature_cols] = kbo_df[feature_cols].apply(pd.to_numeric, errors="coerce")
final_df = kbo_df.dropna(subset=feature_cols + ["홈팀승"])


X = final_df[feature_cols]
y = final_df["홈팀승"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

param_grid = {
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1, 0.2],
    'n_estimators': [100, 200],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0]
}

xgb_model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)

grid = GridSearchCV(xgb_model, param_grid, cv=3, scoring='accuracy', verbose=1, n_jobs=-1)
grid.fit(X_train, y_train)

best_model = grid.best_estimator_
accuracy = accuracy_score(y_test, best_model.predict(X_test))
