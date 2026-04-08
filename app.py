# ============================================================
# 🌾 KissanAI — Backend (Final with Weather API)
# ============================================================

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from deep_translator import GoogleTranslator
from groq import Groq
import requests
import os
from dotenv import load_dotenv

# ============================================================
# 🚀 FastAPI App Setup
# ============================================================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# 🔑 API KEYS (SAFE)
# ============================================================
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

groq_client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "llama-3.1-8b-instant"

# ============================================================
# 🌍 Language Detection
# ============================================================
def detect_language(text: str):
    tamil_chars = set("அஆஇஈஉஊஎஏஐஒஓஔகஙசஞடணதநபமயரலவஶஷஸஹ")
    hindi_chars = set("अआइईउऊएऐओऔकखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह")
    if any(ch in tamil_chars for ch in text):
        return "ta"
    if any(ch in hindi_chars for ch in text):
        return "hi"
    return "en"

# ============================================================
# 💾 Chat Memory
# ============================================================
chat_history = []

# ============================================================
# 🌾 AI AGENTS
# ============================================================
class FertilizerCalcAgent:
    def recommend(self, q):
        prompt = f"You are an Indian agriculture expert. Give 2-line fertilizer advice: {q}"
        return groq_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content.strip()

class SoilHealthAgent:
    def analyze(self, q):
        prompt = f"Soil health expert. Give 2-line soil advice: {q}"
        return groq_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content.strip()

class OrganicAgent:
    def suggest(self, q):
        prompt = f"Organic farming expert. Give 2-line eco advice: {q}"
        return groq_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content.strip()

class MarketAgent:
    def handle(self, q):
        prompt = f"Farmer query: {q}. Give 2-line market or selling advice."
        return groq_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content.strip()

class PriceAgent:
    def get_prices(self, q):
        prompt = f"Farmer query: {q}. Give 2-line crop price summary."
        return groq_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content.strip()

class CropAgent:
    def handle(self, q):
        prompt = f"Farmer query: {q}. Give 2-line crop or season advice."
        return groq_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content.strip()

class IrrigationAgent:
    def handle(self, q):
        prompt = f"Farmer query: {q}. Give 2-line irrigation advice."
        return groq_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content.strip()

# ============================================================
# 🌦️ Weather Agent
# ============================================================
class WeatherAgent:
    def handle(self, query):
        try:
            q = query.lower()

            for word in ["weather", "temperature", "forecast", "in", "today", "tomorrow"]:
                q = q.replace(word, "")

            location = q.strip()

            if not location:
                return "🌦️ Please enter a city name (example: Chennai weather)."

            url = f"https://api.openweathermap.org/data/2.5/weather?q={location},IN&appid={WEATHER_API_KEY}&units=metric"
            data = requests.get(url).json()

            if data.get("cod") != 200:
                return f"❌ Unable to fetch weather for '{location}'."

            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            condition = data["weather"][0]["description"].capitalize()

            summary = f"🌦️ {location.title()}: {temp}°C, {humidity}% humidity, {condition}"

            prompt = f"{summary}. Give 2-line farming advice."
            ai = groq_client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}]
            )

            return summary + "\n\n🌾 Advice: " + ai.choices[0].message.content.strip()

        except Exception as e:
            return f"⚠️ Error: {str(e)}"

# ============================================================
# 🧭 QUERY ROUTER
# ============================================================
def classify_query(q):
    q = q.lower()

    if any(w in q for w in ["weather","rain","temperature","forecast","climate","வானிலை","मौसम"]):
        return "weather"

    if any(w in q for w in ["sell","market","mandi","demand","சந்தை","मंडी"]):
        return "market"

    if any(w in q for w in ["price","rate","cost","விலை","कीमत"]):
        return "price"

    if any(w in q for w in ["organic","bio","vermicompost","உயிர்","जैविक"]):
        return "organic"

    if any(w in q for w in ["soil","ph","மண்","मिट्टी"]):
        return "soil"

    if any(w in q for w in ["irrigation","drip","sprinkler","நீர்ப்பாசனம்","सिंचाई"]):
        return "irrigation"

    if any(w in q for w in ["crop","seed","sow","பயிர்","फसल"]):
        return "crop"

    return "fertilizer"

AGENTS = {
    "fertilizer": FertilizerCalcAgent().recommend,
    "soil": SoilHealthAgent().analyze,
    "organic": OrganicAgent().suggest,
    "weather": WeatherAgent().handle,
    "market": MarketAgent().handle,
    "price": PriceAgent().get_prices,
    "crop": CropAgent().handle,
    "irrigation": IrrigationAgent().handle,
}

# ============================================================
# 🌐 ROOT CHECK
# ============================================================
@app.get("/")
async def root():
    return {"message": "Backend is working"}

# ============================================================
# 💬 API ENDPOINTS
# ============================================================
@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    query = data.get("question", "")
    lang = data.get("language", detect_language(query))

    query_en = query if lang == "en" else GoogleTranslator(source=lang, target="en").translate(query)
    agent = classify_query(query_en)

    reply_en = AGENTS[agent](query_en)
    reply = reply_en if lang == "en" else GoogleTranslator(source="en", target=lang).translate(reply_en)

    chat_history.append({"agent": agent, "question": query, "reply": reply})

    return JSONResponse({
        "agent": agent,
        "reply": reply,
        "history_count": len(chat_history)
    })

@app.post("/clear")
async def clear_chat():
    chat_history.clear()
    return {"message": "Chat cleared successfully"}

# ============================================================
# 🚀 RUN SERVER
# ============================================================
if __name__ == "__main__":
    import uvicorn
    print("🚀 KissanAI Backend running at http://127.0.0.1:4000")
    uvicorn.run(app, host="0.0.0.0", port=4000)