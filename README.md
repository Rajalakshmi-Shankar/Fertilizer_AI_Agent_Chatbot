**🌾 Smart Multi-Agent Farming Assistant**

FastAPI | Groq LLaMA 3.1 | Multi-Agent System | NLP | Weather API | Multilingual Support

This AI-powered farming assistant delivers instant 2-line agricultural guidance using a multi-agent architecture, multilingual processing, real-time weather data, and ultra-fast inference via Groq's LLaMA 3.1.

It supports English, Tamil, and Hindi, allowing farmers to access knowledge in their local language.


🚀 Features

🤖 Multi-Agent AI System

Includes 8 specialized expert agents:

Fertilizer Recommendations

Soil Health

Organic Farming

Weather Insights

Crop Selection

Irrigation Guidance

Market Price Advisory

General Farming Queries


🌐 Multilingual Support

Auto language detection

English / Tamil / Hindi

Smart input & output translation


⚡ High-Speed Backend

FastAPI framework

Groq LLaMA 3.1-8B for ultra-low latency

Smart agent routing logic


☁️ Weather Integration

Live temperature

Real-time humidity

Weather conditions

AI-generated actionable farm tips


💬 Chat Memory

Remembers past chats

One-click clear memory


🎨 Frontend

HTML + CSS + JavaScript

Clean and responsive

Language switcher

One-click popular questions

Text-to-speech output



---

🛠️ Tech Stack

Layer	Technologies

Backend	FastAPI, Groq SDK, Python
AI/NLP	LLaMA 3.1 Model (Groq)
Translation	GoogleTranslator
Weather	OpenWeather API
Frontend	HTML, CSS, JavaScript
Architecture	Multi-Agent System



---

🧩 System Architecture Diagram (ASCII)

┌─────────────────────────┐
              │       FRONTEND UI       │
              │  HTML / CSS / JS        │
              └────────────┬────────────┘
                           │
                           ▼
               ┌────────────────────────┐
               │      FASTAPI API       │
               └────────────┬───────────┘
                           │
                           ▼
           ┌───────────────────────────────────┐
           │       LANGUAGE DETECTOR           │
           └───────────────────┬──────────────┘
                               │
                               ▼
                  ┌────────────────────┐
                  │  MULTI-AGENT CORE  │
                  └─┬───────┬─────────┘
           ┌────────┘       │
           ▼                 ▼
  ┌────────────────┐   ┌────────────────┐
  │  FARM AGENTS   │   │  WEATHER AGENT │
  └───┬──────┬─────┘   └──────┬────────┘
      │      │                │
      ▼      ▼                ▼
┌────────┐ ┌────────┐   ┌────────────┐
│ Groq   │ │ Translate│  │ OpenWeather│
│ Model  │ │ (IN/OUT) │  │   API      │
└────────┘ └────────┘   └────────────┘


---

🔄 Workflow Diagram

User Query → Language Detection → Translation →  
Agent Selection → Groq Inference → Response Translation → Frontend Output


---

📂 Project Structure

/project
│── main.py              # Backend & routing
│── agents/              # All expert agents
│── templates/index.html # UI
│── static/css/style.css
│── static/js/app.js
│── requirements.txt
│── README.md


---

▶️ Installation & Setup

1️⃣ Install dependencies

pip install -r requirements.txt

2️⃣ Add API keys

Create .env:

GROQ_API_KEY=your_key
OPENWEATHER_API_KEY=your_key

3️⃣ Run the server

uvicorn main:app --reload

4️⃣ Open the app

http://localhost:8000

🎯 Outcome

This system gives farmers instant, accurate, multilingual agricultural advice with a strong combination of:

AI

NLP

Multi-agent architecture

API integration

Full-stack development


Perfect for real-world use and educational demos.


---

👥 Team

Sankar Pandi S

Raja Lakshmi S



---

⭐ Contributing

Pull requests are welcome!
For major changes, open an issue first.


---

📄 License

For educational and research use only.
