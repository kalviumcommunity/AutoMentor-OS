# 🧠 AutoMentor OS – Your AI Startup Co-Founder (Built with Gemini AI)

AutoMentor OS is an AI-powered assistant that acts like your startup co-founder. It helps users brainstorm unique startup ideas, conduct smart market research using RAG (Retrieval-Augmented Generation), and generate structured content like landing pages — all using **Gemini AI** with **Function Calling** and **structured outputs**.

---

## 🚀 Features

- 🔍 **Startup Idea Generator**  
  Describe your skills or interests, and AutoMentor will generate startup ideas with product name, audience, pain points, and monetization.

- 📊 **RAG-based Market Research**  
  Uses Gemini + RAG to pull insights from documents or online sources to validate your idea.

- 📝 **Landing Page Content Generator**  
  Creates headline, features, and CTA sections based on your startup idea using Gemini’s structured output capabilities.

- 🔧 **Function Calling + Structured Output**  
  Uses Gemini’s function calling to ensure clean, accurate, and structured data you can use directly in UI or automation.

---

## 💻 Tech Stack

| Layer        | Tools                                  |
|--------------|----------------------------------------|
| Frontend     | React.js + Tailwind CSS                |
| Backend      | Node.js + Express                      |
| AI Engine    | Gemini AI (Pro / 1.5)                  |
| RAG Layer    | LangChain + ChromaDB / file-based docs |
| Deployment   | Vercel (frontend), Render/Fly.io (API) |

---

## 📦 Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/AutoMentor-OS.git
   cd AutoMentor-OS

2. **Install frontend**
    cd client
    npm install
    npm run dev

3. **Install backend**
    cd server
    npm install
    npm start
4. **Setup Environment Variables**
    Create a .env file in /server with:

    GEMINI_API_KEY=your_google_ai_api_key
