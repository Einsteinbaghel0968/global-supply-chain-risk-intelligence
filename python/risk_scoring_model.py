import pandas as pd

# =========================
# LOAD DATA
# =========================
news_df = pd.read_csv("data/processed_news.csv")
global_df = pd.read_csv("data/global_factors.csv")

# =========================
# 1. NEWS RISK
# =========================
news_risk = news_df["impact_score"].mean()

# =========================
# 2. WEATHER RISK
# =========================
weather = global_df.loc[0, "weather"]

def get_weather_risk(weather):
    weather = str(weather).lower()

    if "clear" in weather:
        return 0.1
    elif "cloud" in weather:
        return 0.3
    elif "rain" in weather:
        return 0.6
    elif "storm" in weather:
        return 0.9
    elif "haze" in weather:
        return 0.4
    else:
        return 0.2

weather_risk = get_weather_risk(weather)

# =========================
# 3. OIL RISK
# =========================
oil_price = global_df.loc[0, "oil_price"]

if oil_price is None:
    oil_risk = 0.3
else:
    oil_risk = float(oil_price) / 150

# =========================
# FINAL RISK SCORE
# =========================
risk_score = (
    0.5 * news_risk +
    0.3 * weather_risk +
    0.2 * oil_risk
)

# =========================
# OUTPUT
# =========================
result = {
    "news_risk": news_risk,
    "weather_risk": weather_risk,
    "oil_risk": oil_risk,
    "final_risk_score": risk_score
}

result_df = pd.DataFrame([result])
result_df.to_csv("data/final_risk.csv", index=False)

print("\n🚀 FINAL RISK SCORE GENERATED")
print(result_df)