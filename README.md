# 🧠 AutoMentor OS – MVP (Gemini AI)

AutoMentor OS is an AI-powered startup assistant built with **Gemini AI**.  
It uses **Function Calling**, **RAG (Retrieval-Augmented Generation)**, **Structured Output**, and **Dynamic Prompting** to help users:

- Generate startup ideas based on their skills & interests  
- Validate them with AI-powered market research  
- Create landing page content instantly

---

## 🚀 Features

- **Startup Idea Generator** – Converts skills + interests into a structured, monetizable business concept  
- **Market Research with RAG** – Fetches relevant trends and competitor info from local/preloaded documents  
- **Landing Page Content Generator** – Auto-generates headlines, features, and CTAs  
- **Structured JSON Output** – Clean, machine-readable responses  
- **Function Calling** – Modular AI actions for different tasks

---

## 🛠 Tech Stack

| Layer        | Tools |
|--------------|-------|
| Frontend     | React.js + CSS |
| Backend      | Python + FastAPI |
| AI Engine    | Google Gemini Pro / 1.5 |
| RAG          | LangChain + Local Files |
| Deployment   | Vercel (Frontend), Render (Backend) |

---

## 📂 Project Structure

AutoMentor-OS/
│
├── client/ # React Frontend
│ ├── src/
│ └── package.json
│
├── server/ # Node.js Backend
│ ├── routes/
│ ├── utils/
│ └── package.json
│
├── docs/ # Architecture diagrams, prompts, notes
├── README.md
└── .env.example


---

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/kalviumcommunity/AutoMentor-OS.git
cd AutoMentor-OS-MVP

2️⃣ Setup Backend

cd server
npm install
cp .env.example .env   # Add GEMINI_API_KEY here
npm run dev

3️⃣ Setup Frontend

cd ../client
npm install
npm run dev

🧩 Environment Variables

Create .env in /server:

GEMINI_API_KEY=your_google_ai_api_key

▶️ Usage

    Enter your skills & interests in the UI

    Get a structured startup idea instantly

    Click “Validate Idea” for RAG-based market research

    Generate landing page content with one click

🧪 Running Tests

cd server
npm run test

Evaluation dataset is located in /server/tests/data.
📅 MVP Development Plan
Day	Task
1	Setup frontend + backend
2	Integrate Gemini API + Function Calling
3	Build Startup Idea Generator
4	Display ideas in UI
5	Add RAG with local docs
6	Add Landing Page Generator
7	Polish UI + deploy
📈 Future Scope

    Live market data in RAG

    AI-generated logo & visuals

    PDF export of plans

    MongoDB storage for session history
