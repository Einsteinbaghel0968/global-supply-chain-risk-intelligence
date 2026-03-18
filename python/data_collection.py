import requests
import pandas as pd
from datetime import datetime
import os

# =========================
# API KEYS (FOR LOCAL TEST)
# =========================
NEWS_API_KEY = "4c62a75721f74a4a9dd169e202489b63"
WEATHER_API_KEY = "4feb31693309a632bb208b58b3c4ac44"
ALPHA_VANTAGE_KEY = "TEPN38OXPH4X7GBH"

# =========================
# CREATE DATA FOLDER
# =========================
os.makedirs("data", exist_ok=True)

# =========================
# 1. FETCH NEWS DATA
# =========================
def get_news():
    try:
        url = f"https://newsapi.org/v2/everything?q=logistics OR supply chain OR oil OR war&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        data = response.json()

        news_list = []

        for article in data.get("articles", []):
            news_list.append({
                "source": article["source"]["name"],
                "title": article["title"],
                "date": article["publishedAt"]
            })

        df = pd.DataFrame(news_list)
        print(f"✅ News fetched: {len(df)} articles")
        return df

    except Exception as e:
        print("❌ News API Error:", e)
        return pd.DataFrame()

# =========================
# 2. FETCH WEATHER DATA
# =========================
def get_weather(city="Delhi"):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        # DEBUG PRINT
        print("Weather API Response:", data)

        if "main" not in data:
            print("❌ Invalid weather response")
            return {}

        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["main"]
        }

    except Exception as e:
        print("❌ Weather API Error:", e)
        return {}

# =========================
# 3. FETCH OIL PRICE
# =========================
def get_oil_price():
    try:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=USO&apikey={ALPHA_VANTAGE_KEY}"
        response = requests.get(url)
        data = response.json()

        print("Oil API Response:", data)

        if "Global Quote" not in data:
            print("❌ Oil API limit reached or invalid data")
            return None

        price = data["Global Quote"]["05. price"]

        return float(price)

    except Exception as e:
        print("❌ Oil API Error:", e)
        return None

# =========================
# MAIN FUNCTION
# =========================
def main():
    print("\n🚀 STARTING DATA COLLECTION...\n")

    news_df = get_news()
    weather_data = get_weather()
    oil_price = get_oil_price()

    # =========================
    # SAVE NEWS DATA
    # =========================
    if not news_df.empty:
        news_df.to_csv("data/news.csv", index=False)
        print("💾 news.csv saved")

    # =========================
    # SAVE GLOBAL FACTORS
    # =========================
    summary = {
        "date": datetime.now(),
        "city": weather_data.get("city"),
        "temperature": weather_data.get("temperature"),
        "weather": weather_data.get("weather"),
        "oil_price": oil_price
    }

    summary_df = pd.DataFrame([summary])
    summary_df.to_csv("data/global_factors.csv", index=False)
    print("💾 global_factors.csv saved")

    print("\n🎯 DATA COLLECTION COMPLETED SUCCESSFULLY\n")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    main()