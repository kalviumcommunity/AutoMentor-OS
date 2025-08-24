# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

# Initialize FastAPI app
app = FastAPI()

# Configure the Gemini API key from your .env file
# Make sure you have python-dotenv installed: pip install python-dotenv
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Pydantic model for the request body to ensure we get the right data
class UserInput(BaseModel):
    skills: str
    interests: str

# --- This is the core of your assignment ---
@app.post("/generate-startup-idea")
async def generate_startup_idea(user_input: UserInput):
    # 1. Define the System Prompt using the RTFC framework
    system_prompt = """
    Role: You are AutoMentor, an expert startup advisor and business strategist with a knack for identifying innovative, monetizable business ideas.

    Task: Your task is to generate a unique and practical startup idea based on the user's provided skills and interests. You must analyze their input and create a concept that logically combines them.

    Format: You must respond only with a clean, well-formed JSON object. Do not include any introductory text, explanations, or markdown formatting like ```json. The JSON object must contain three keys: "startup_name" (a catchy name for the business), "concept" (a one-sentence elevator pitch), and "monetization_strategy" (a brief explanation of how it would make money).

    Context: The user is an aspiring entrepreneur who is in the early stages of brainstorming. Your tone should be encouraging and professional. The ideas should be suitable for a solo founder or a small team to start as a Minimum Viable Product (MVP).
    """

    # 2. Create the User Prompt from the user's input
    user_prompt = f"User's Skills: {user_input.skills}. User's Interests: {user_input.interests}."

    # 3. Combine the prompts for the final API call
    # The f-string combines the system instructions with the specific user query
    full_prompt = f"{system_prompt}\n\n{user_prompt}"

    # 4. Call the Gemini API
    response = model.generate_content(full_prompt)

    # 5. Return the AI's response
    # We will parse the text to ensure it's valid JSON later, but for now, we return the text
    return {"idea": response.text}