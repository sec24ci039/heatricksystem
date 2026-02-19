import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestRegressor


# -------------------
# Load dataset
df = pd.read_csv("chennai_climate_with_labels.csv", engine="python", encoding="utf-8")


df["date"] = pd.to_datetime(df["date"])

# -------------------
# Feature Engineering
# -------------------
df["lag1"] = df["max_temp"].shift(1)
df["lag2"] = df["max_temp"].shift(2)
df["lag3"] = df["max_temp"].shift(3)

df["rolling3"] = df["max_temp"].rolling(3).mean()
df["rolling7"] = df["max_temp"].rolling(7).mean()

monthly_avg = df.groupby("month")["max_temp"].transform("mean")
df["temp_anomaly"] = df["max_temp"] - monthly_avg
# Temperature Forecast Targets
df["temp_1day"] = df["max_temp"].shift(-1)
df["temp_2day"] = df["max_temp"].shift(-2)


# -------------------
# Create Tomorrow & Day-After Targets
# -------------------
df["heatwave_1day"] = df["heatwave"].shift(-1)
df["heatwave_2day"] = df["heatwave"].shift(-2)

df = df.dropna()

# -------------------
# Feature List
# -------------------
features = [
    "max_temp",
    "humidity",
    "heat_index",
    "lag1",
    "lag2",
    "lag3",
    "rolling3",
    "rolling7",
    "temp_anomaly"
]

# -------------------
# Train-Test Split (ONLY ONCE)
# -------------------
train = df[df["date"] < "2022-01-01"]
test = df[df["date"] >= "2022-01-01"]

X_train = train[features]
X_test = test[features]

# =====================================================
# 🔥 TOMORROW MODEL
# =====================================================

y_train_1 = train["heatwave_1day"]
y_test_1 = test["heatwave_1day"]

model_1 = RandomForestClassifier(
    n_estimators=200,
    max_depth=6,
    random_state=42,
    class_weight="balanced"
)

model_1.fit(X_train, y_train_1)

y_prob_1 = model_1.predict_proba(X_test)[:, 1]
y_pred_1 = (y_prob_1 > 0.6).astype(int)

print("\n================ TOMORROW PREDICTION ================")
print("Accuracy:", accuracy_score(y_test_1, y_pred_1))
print("Confusion Matrix:\n", confusion_matrix(y_test_1, y_pred_1))
print("Classification Report:\n", classification_report(y_test_1, y_pred_1))

# =====================================================
# 🔥 DAY AFTER TOMORROW MODEL
# =====================================================

y_train_2 = train["heatwave_2day"]
y_test_2 = test["heatwave_2day"]

model_2 = RandomForestClassifier(
    n_estimators=200,
    max_depth=6,
    random_state=42,
    class_weight="balanced"
)

model_2.fit(X_train, y_train_2)

y_prob_2 = model_2.predict_proba(X_test)[:, 1]
y_pred_2 = (y_prob_2 > 0.6).astype(int)

print("\n============= DAY AFTER TOMORROW PREDICTION ==========")
print("Accuracy:", accuracy_score(y_test_2, y_pred_2))
print("Confusion Matrix:\n", confusion_matrix(y_test_2, y_pred_2))
print("Classification Report:\n", classification_report(y_test_2, y_pred_2))
# =====================================================
# 🔥 TEMPERATURE REGRESSION MODELS
# =====================================================

# Tomorrow temperature
y_train_temp1 = train["temp_1day"]
y_test_temp1 = test["temp_1day"]

reg_1 = RandomForestRegressor(
    n_estimators=200,
    max_depth=6,
    random_state=42
)

reg_1.fit(X_train, y_train_temp1)

temp_pred_1 = reg_1.predict(X_test)

print("\nTomorrow Temperature MAE:",
      abs(temp_pred_1 - y_test_temp1).mean())


# Day-after temperature
y_train_temp2 = train["temp_2day"]
y_test_temp2 = test["temp_2day"]

reg_2 = RandomForestRegressor(
    n_estimators=200,
    max_depth=6,
    random_state=42
)

reg_2.fit(X_train, y_train_temp2)

temp_pred_2 = reg_2.predict(X_test)

print("\nDay After Temperature MAE:",
      abs(temp_pred_2 - y_test_temp2).mean())
# =====================================================
# 🔥 LIVE FORECAST PREDICTION BLOCK
# =====================================================

latest = df.iloc[-1]
latest_features = pd.DataFrame([latest[features]])

# Today's temperature (already known)
today_temp = latest["max_temp"]

# Tomorrow predicted temperature
predicted_temp_1 = reg_1.predict(latest_features)[0]

# Day-after predicted temperature
predicted_temp_2 = reg_2.predict(latest_features)[0]

# Tomorrow heatwave probability
prob_tomorrow = model_1.predict_proba(latest_features)[0][1]

# Day-after heatwave probability
prob_day_after = model_2.predict_proba(latest_features)[0][1]

print("\n================ LIVE FORECAST ================")
print("Today's Temperature:", today_temp)
print("Predicted Tomorrow Temperature:", predicted_temp_1)
print("Predicted Day After Tomorrow Temperature:", predicted_temp_2)



