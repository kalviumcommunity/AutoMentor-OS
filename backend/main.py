# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

# Initialize FastAPI app
app = FastAPI()

# Configure the Gemini API key from your .env file
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# ===================================================================
# ===== SYSTEM AND USER PROMPT =====
# ===================================================================

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
    full_prompt = f"{system_prompt}\n\n{user_prompt}"

    # 4. Call the Gemini API
    response = model.generate_content(full_prompt)

    # 5. Return the AI's response
    return {"idea": response.text}

# ===================================================================
# ===== ZERO-SHOT PROMPTING =====
# ===================================================================

# 1. Create a new Pydantic model for the tagline generator's input
class TaglineRequest(BaseModel):
    concept: str

# 2. Create the new endpoint that demonstrates Zero-Shot Prompting
@app.post("/generate-tagline-zero-shot")
async def generate_tagline_zero_shot(request: TaglineRequest):
    """
    This endpoint demonstrates zero-shot prompting.
    It asks the AI to generate a tagline based on a startup concept
    without providing any examples of what a good tagline looks like.
    """
    
    # This prompt is direct and gives a command without any examples.
    # This is the core of "zero-shot".
    prompt = f"""
    You are a world-class branding expert.
    Your task is to generate a short, memorable, and catchy tagline for the following startup concept.

    Startup Concept: "{request.concept}"

    Tagline:
    """

    # Call the Gemini API with the zero-shot prompt
    response = model.generate_content(prompt)

    # Return the AI's generated tagline
    return {"tagline": response.text}

# ===================================================================
# =====  ONE SHOT PROMPTING ======
# ===================================================================

# 1. Create a new Pydantic model for the headline generator's input
class HeadlineRequest(BaseModel):
    description: str

# 2. Create the new endpoint that demonstrates One-Shot Prompting
@app.post("/generate-headline-one-shot")
async def generate_headline_one_shot(request: HeadlineRequest):
    """
    This endpoint demonstrates one-shot prompting.
    It provides the AI with a single, clear example of an input and
    the desired output format and style to guide its response.
    """
    
    # 3. Design the One-Shot Prompt
    # The key is the inclusion of the "**Example Input:**" and "**Example Output:**" block.
    prompt = f"""
    Generate a catchy landing page headline for a startup. The headline should be concise and benefit-oriented.

    --
    **Example Input:**
    A platform that connects local artists with coffee shops to display their work.

    **Example Output:**
    Turn Your Cafe into a Gallery. Discover Local Art.
    --

    **Startup Description:**
    {request.description}

    **Headline:**
    """

    # 4. Call the Gemini API
    response = model.generate_content(prompt)

    # 5. Return the AI's response
    return {"headline": response.text.strip().replace('"', '')}
