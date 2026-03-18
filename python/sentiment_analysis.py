import pandas as pd
from textblob import TextBlob

# =========================
# LOAD NEWS DATA
# =========================
df = pd.read_csv("data/news.csv")

# =========================
# SENTIMENT FUNCTION
# =========================
def get_sentiment(text):
    try:
        return TextBlob(str(text)).sentiment.polarity
    except:
        return 0

# =========================
# EVENT DETECTION
# =========================
def detect_event(text):
    text = str(text).lower()

    if any(word in text for word in ["war", "conflict", "attack"]):
        return "WAR"
    elif any(word in text for word in ["strike", "shutdown", "disruption"]):
        return "DISRUPTION"
    elif any(word in text for word in ["oil", "gas", "energy"]):
        return "OIL_EVENT"
    else:
        return "NORMAL"

# =========================
# IMPACT SCORE
# =========================
def calculate_impact(sentiment, event):
    base = abs(sentiment)

    if event == "WAR":
        return base + 0.6
    elif event == "DISRUPTION":
        return base + 0.5
    elif event == "OIL_EVENT":
        return base + 0.4
    else:
        return base

# =========================
# APPLY NLP
# =========================
df["sentiment"] = df["title"].apply(get_sentiment)
df["event_type"] = df["title"].apply(detect_event)

df["impact_score"] = df.apply(
    lambda row: calculate_impact(row["sentiment"], row["event_type"]),
    axis=1
)

# =========================
# SAVE OUTPUT
# =========================
df.to_csv("data/processed_news.csv", index=False)

print("✅ NLP + Event Detection Completed!")