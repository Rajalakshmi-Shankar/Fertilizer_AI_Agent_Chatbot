# ============================================================
# 🌾 KissanAI — Backend + Frontend (Single Deploy)
# ============================================================

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from deep_translator import GoogleTranslator
from groq import Groq
import requests
import os
import re
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
# 🔑 API KEYS
# ============================================================
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
MANDI_API_KEY = os.getenv("MANDI_API_KEY")

groq_client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "llama-3.1-8b-instant"

# ============================================================
# 🌐 SERVE FRONTEND
# ============================================================
@app.get("/")
async def serve_frontend():
    return FileResponse("index.html")

# ============================================================
# 🌍 Language Detection
# ============================================================
def detect_language(text: str):
    tamil_chars = set("அஆஇஈஉஊஎஏஐஒஓஔகஙசஞடணதநபமயரலவ")
    hindi_chars = set("अआइईउऊएऐओऔकखगघङचछजझञटठडढणतथदधन")

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
        prompt = f"You are Indian agriculture expert. Give 2-line fertilizer advice: {q}"
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


# ============================================================
# 💰 MARKET AGENT (FINAL FIXED)
# ============================================================
class MarketAgent:
    def handle(self, q):
        try:
            q = q.lower()

            crops = {
                "Tomato":["tomato","தக்காளி","टमाटर"],
                "Onion":["onion","வெங்காயம்","प्याज"],
                "Rice":["rice","நெல்","धान"],
                "Wheat":["wheat","கோதுமை","गेहूं"],
                "Potato":["potato","உருளைக்கிழங்கு","आलू"],
                "Maize":["maize","மக்காச்சோளம்","मक्का"],
                "Cotton":["cotton","பருத்தி","कपास"],
                "Groundnut":["groundnut","வேர்க்கடலை","मूंगफली"]
            }

            crop = None

            for key, words in crops.items():
                for w in words:
                    if re.search(rf"\b{w}\b", q):
                        crop = key
                        break
                if crop:
                    break

            if not crop:
                return "Please ask crop price like tomato price"

            url = (
                "https://api.data.gov.in/resource/"
                "9ef84268-d588-465a-a308-a864a43d0070"
                f"?api-key={MANDI_API_KEY}"
                "&format=json"
                "&limit=5"
                f"&filters[commodity]={crop}"
            )

            data = requests.get(url).json()
            records = data.get("records", [])

            if not records:
                return f"No market data for {crop}"

            result = f"💰 {crop} Market Price (₹)\n\n"

            for r in records[:5]:
                market = r.get("market","")
                state = r.get("state","")
                price = r.get("modal_price","")

                result += f"{market} ({state}) : ₹{price}\n"

            return result

        except:
            return "Unable to fetch live market price"


class PriceAgent:
    def get_prices(self, q):
        return MarketAgent().handle(q)


class CropAgent:
    def handle(self, q):
        prompt = f"Farmer query: {q}. Give crop advice."
        return groq_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content.strip()


class IrrigationAgent:
    def handle(self, q):
        prompt = f"Farmer query: {q}. Give irrigation advice."
        return groq_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content.strip()


# ============================================================
# 🌦️ WEATHER AGENT
# ============================================================
class WeatherAgent:
    def handle(self, query):
        try:
            q = query.lower().strip()

            location = "Chennai"

            remove_words = [
                "weather","temperature","forecast","rain","today",
                "வானிலை","மழை",
                "मौसम","बारिश"
            ]

            for word in remove_words:
                q = q.replace(word,"")

            q = q.strip()

            if len(q) > 2:
                location = q.split()[-1]

            url = f"https://api.openweathermap.org/data/2.5/weather?q={location},IN&appid={WEATHER_API_KEY}&units=metric"
            data = requests.get(url).json()

            if data.get("cod") != 200:
                location = "Chennai"
                url = f"https://api.openweathermap.org/data/2.5/weather?q={location},IN&appid={WEATHER_API_KEY}&units=metric"
                data = requests.get(url).json()

            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            condition = data["weather"][0]["description"].capitalize()

            summary = f"🌦️ {location.title()}: {temp}°C, {humidity}% humidity, {condition}"

            return summary

        except:
            return "🌦️ Unable to fetch weather now"


# ============================================================
# 🧭 QUERY ROUTER
# ============================================================
def classify_query(q):
    q = q.lower()

    if any(w in q for w in ["weather","rain","temperature","வானிலை","மழை","मौसम"]):
        return "weather"

    if any(w in q for w in ["market","mandi","சந்தை","मंडी"]):
        return "market"

    if any(w in q for w in ["price","rate","cost","விலை","कीमत"]):
        return "price"

    if any(w in q for w in ["organic","உயிர்","जैविक"]):
        return "organic"

    if any(w in q for w in ["soil","மண்","मिट्टी"]):
        return "soil"

    if any(w in q for w in ["irrigation","நீர்ப்பாசனம்","सिंचाई"]):
        return "irrigation"

    if any(w in q for w in ["crop","பயிர்","फसल"]):
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
# API
# ============================================================
@app.post("/ask")
async def ask(request: Request):

    data = await request.json()
    query = data.get("question", "")
    lang = data.get("language", detect_language(query))

    query_en = query if lang == "en" else GoogleTranslator(
        source=lang, target="en"
    ).translate(query)

    agent = classify_query(query_en)

    reply_en = AGENTS[agent](query_en)

    reply = reply_en if lang == "en" else GoogleTranslator(
        source="en", target=lang
    ).translate(reply_en)

    chat_history.append({
        "agent": agent,
        "question": query,
        "reply": reply
    })

    return JSONResponse({
        "agent": agent,
        "reply": reply,
        "history_count": len(chat_history)
    })


# ============================================================
# 🚀 RUN SERVER
# ============================================================
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
