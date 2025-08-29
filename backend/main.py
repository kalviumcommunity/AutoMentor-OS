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
# ===== SYSTEM/USER PROMPT, DYNAMIC PROMPTING & STRUCTURED OUTPUT =====
# ===================================================================

# 1. Define the Pydantic model for the user's input (this stays the same)
class UserInput(BaseModel):
    skills: str
    interests: str

# 2. Define the Pydantic model for the AI's STRUCTURED OUTPUT
#    This schema will be passed to the Gemini API.
class StartupIdea(BaseModel):
    startup_name: str = Field(description="A catchy and descriptive name for the startup.")
    concept: str = Field(description="A one-sentence elevator pitch for the startup.")
    monetization_strategy: str = Field(description="A brief explanation of how the business would make money.")

# 3. Update the endpoint to use the new structured output feature
@app.post("/generate-startup-idea", response_model=StartupIdea)
async def generate_startup_idea(user_input: UserInput):
    """
    This endpoint demonstrates Structured Output. It forces the Gemini model
    to respond with a JSON object that strictly adheres to the `StartupIdea`
    Pydantic schema.
    """
    
    # The prompt can now be simpler, as the schema handles the formatting instructions.
    prompt = f"""
    You are an expert startup advisor. Generate a unique and practical startup idea based on the user's provided skills and interests.


    User's Skills: {user_input.skills}
    User's Interests: {user_input.interests}
    """


    # 4. Create the generation_config with the new JSON mode settings
    generation_config = {
        "response_mime_type": "application/json",
        "response_schema": StartupIdea.model_json_schema(),
    }

    # 5. Call the Gemini API with the new configuration
    response = model.generate_content(
        prompt,
        generation_config=generation_config
    )

    # 6. Parse and return the validated JSON object
    # The response.text is a guaranteed valid JSON string, so we can parse it.
    # FastAPI will automatically convert the Pydantic object back to a JSON response.
    return StartupIdea.model_validate_json(response.text)

# ===================================================================
# ===== ZERO-SHOT PROMPTING =====
# ===================================================================

# Pydantic model for the tagline generator's input
class TaglineRequest(BaseModel):
    concept: str

@app.post("/generate-tagline-zero-shot")
async def generate_tagline_zero_shot(request: TaglineRequest):
    """
    This endpoint demonstrates zero-shot prompting.
    It asks the AI to generate a tagline based on a startup concept
    without providing any examples of what a good tagline looks like.
    """
    prompt = f"""
    You are a world-class branding expert.
    Your task is to generate a short, memorable, and catchy tagline for the following startup concept.

    Startup Concept: "{request.concept}"

    Tagline:
    """
    response = model.generate_content(prompt)
    return {"tagline": response.text}

# ===================================================================
# =====  ONE SHOT PROMPTING ======
# ===================================================================

# Pydantic model for the headline generator's input
class HeadlineRequest(BaseModel):
    description: str

@app.post("/generate-headline-one-shot")
async def generate_headline_one_shot(request: HeadlineRequest):
    """
    This endpoint demonstrates one-shot prompting.
    It provides the AI with a single, clear example of an input and
    the desired output format and style to guide its response.
    """
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
    response = model.generate_content(prompt)
    return {"headline": response.text.strip().replace('"', '')}

# ===================================================================
# ===== MULTI SHOT PROMPTING ======
# ===================================================================

# Pydantic model for the features generator's input
class FeaturesRequest(BaseModel):
    description: str

@app.post("/generate-features-multi-shot")
async def generate_features_multi_shot(request: FeaturesRequest):
    """
    This endpoint demonstrates multi-shot (or few-shot) prompting.
    It provides the AI with several examples to teach it a more complex
    pattern: generating a feature title and a benefit-oriented description.
    """
    prompt = f"""
    Generate a list of 3 key features with brief descriptions for a startup's landing page. The format should be a hyphenated list with the feature name in bold.

    --
    **Example 1:**
    Description: An app that uses AI to create personalized meal plans.
    Features:
    - **AI-Powered Personalization:** Get meal plans tailored to your dietary needs and goals.
    - **Automatic Grocery Lists:** Save time with shopping lists generated from your weekly plan.
    - **Recipe Discovery:** Explore thousands of healthy and delicious recipes.
    --
    **Example 2:**
    Description: A service that provides on-demand dog walkers.
    Features:
    - **GPS-Tracked Walks:** Monitor your dog's walk in real-time for peace of mind.
    - **Vetted & Insured Walkers:** Trust your pet with our community of certified professionals.
    - **Instant Booking:** Find and book a reliable walker in minutes.
    --

    **Startup Description:**
    {request.description}

    **Features:**
    """
    response = model.generate_content(prompt)
    return {"features": response.text.strip()}

# ===================================================================
# ===== CHAIN OF THOUGHT PROMPTING ======
# ===================================================================


# Pydantic model for the validation request
class ValidationRequest(BaseModel):
    idea: str


@app.post("/validate-idea-cot")
async def validate_idea_cot(request: ValidationRequest):
    """
    This endpoint demonstrates Chain of Thought (CoT) prompting.
    It instructs the model to follow a series of reasoning steps before
    providing a final summary, leading to a more thorough analysis.
    """

    prompt = f"""
    Analyze the market viability of the following startup idea. Let's think step by step.
    First, identify the primary target audience for this idea, including their key demographics and needs.
    Second, list 2-3 potential competitors or existing alternatives and what they do well or poorly.
    Third, based on the audience and competitors, provide a summary of the idea's potential strengths and weaknesses.

    Startup Idea: "{request.idea}"
    """

    response = model.generate_content(prompt)
    return {"validation_analysis": response.text.strip()}


# ===================================================================
# ===== TOKENS AND TOKENIZATION ======
# ===================================================================

# 1. Create Pydantic models for the response to structure the output
class TokenUsage(BaseModel):
    prompt_tokens: int
    response_tokens: int
    total_tokens: int

class ValidationResponseWithTokens(BaseModel):
    validation_analysis: str
    token_usage: TokenUsage

# 2. Create the new endpoint that logs and returns token counts
@app.post("/validate-idea-with-tokens", response_model=ValidationResponseWithTokens)
async def validate_idea_with_tokens(request: ValidationRequest):
    """
    This endpoint demonstrates token counting. It performs an analysis and
    returns the token usage details from the Gemini API's usage_metadata.
    """
    
    # Using the same powerful Chain of Thought prompt from before
    prompt = f"""
    Analyze the market viability of the following startup idea. Let's think step by step.
    First, identify the primary target audience for this idea.
    Second, list 2-3 potential competitors or existing alternatives.
    Third, provide a summary of the idea's potential strengths and weaknesses.

    Startup Idea: "{request.idea}"
    """

    # 3. Call the Gemini API
    response = model.generate_content(prompt)

    # 4. Extract token usage from the response metadata (the efficient way)
    usage_metadata = response.usage_metadata
    prompt_tokens = usage_metadata.prompt_token_count
    response_tokens = usage_metadata.candidates_token_count
    total_tokens = usage_metadata.total_token_count
    
    # 5. Log the number of tokens to the console/terminal
    print("--- Token Usage ---")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
    print(f"Total tokens: {total_tokens}")
    print("-------------------")

    # 6. Return the structured response including the token count
    return ValidationResponseWithTokens(
        validation_analysis=response.text.strip(),
        token_usage=TokenUsage(
            prompt_tokens=prompt_tokens,
            response_tokens=response_tokens,
            total_tokens=total_tokens
        )
    )

# ===================================================================
# ===== TEMPERATURE-CONTROL  ======
# ===================================================================
from pydantic import Field

# 1. Create a Pydantic model for the request. We'll allow the user
#    to pass in a temperature value, with validation.
class BrainstormRequest(BaseModel):
    description: str
    temperature: float = Field(
        0.7, 
        ge=0.0, 
        le=1.0, 
        description="The creativity of the response. 0.0 is deterministic, 1.0 is highly creative."
    )

# 2. Create the new endpoint that uses the temperature parameter
@app.post("/brainstorm-names-with-temperature")
async def brainstorm_names_with_temperature(request: BrainstormRequest):
    """
    This endpoint demonstrates the use of the 'temperature' parameter.
    A low temperature gives more predictable names, while a high
    temperature gives more creative, random names.
    """
    
    # 3. Create the generation_config object to pass to the API
    # This is how you send parameters like temperature, top_p, etc.
    generation_config = {
        "temperature": request.temperature,
    }

    prompt = f"""
    You are a creative branding expert. Brainstorm a list of 5 unique and catchy names for the following startup.

    Startup Description: "{request.description}"
    """

    # 4. Call the Gemini API, passing in the generation_config
    response = model.generate_content(
        prompt,
        generation_config=generation_config
    )

    # 5. Return the AI's response
    return {
        "startup_names": response.text.strip(),
        "temperature_used": request.temperature
    }


# ===================================================================
# ===== TEMPERATURE-CONTROL  ======
# ===================================================================
from pydantic import Field

# 1. Create a Pydantic model for the request. We'll allow the user
#    to pass in a temperature value, with validation.
class BrainstormRequest(BaseModel):
    description: str
    temperature: float = Field(
        0.7, 
        ge=0.0, 
        le=1.0, 
        description="The creativity of the response. 0.0 is deterministic, 1.0 is highly creative."
    )

# 2. Create the new endpoint that uses the temperature parameter
@app.post("/brainstorm-names-with-temperature")
async def brainstorm_names_with_temperature(request: BrainstormRequest):
    """
    This endpoint demonstrates the use of the 'temperature' parameter.
    A low temperature gives more predictable names, while a high
    temperature gives more creative, random names.
    """
    
    # 3. Create the generation_config object to pass to the API
    # This is how you send parameters like temperature, top_p, etc.
    generation_config = {
        "temperature": request.temperature,
    }

    prompt = f"""
    You are a creative branding expert. Brainstorm a list of 5 unique and catchy names for the following startup.

    Startup Description: "{request.description}"
    """

    # 4. Call the Gemini API, passing in the generation_config
    response = model.generate_content(
        prompt,
        generation_config=generation_config
    )

    # 5. Return the AI's response
    return {
        "startup_names": response.text.strip(),
        "temperature_used": request.temperature
    }

# ===================================================================
# ===== IMPLEMENTED TOP-P ======
# ===================================================================
from pydantic import Field

# 1. Create a Pydantic model for the request. We'll allow the user
#    to pass in a top_p value, with validation.
class MarketingAngleRequest(BaseModel):
    description: str
    top_p: float = Field(
        0.95, 
        ge=0.0, 
        le=1.0, 
        description="The diversity of the response. 0.1 is narrow, 0.95 is diverse."
    )

# 2. Create the new endpoint that uses the top_p parameter
@app.post("/generate-marketing-angles-with-top-p")
async def generate_marketing_angles_with_top_p(request: MarketingAngleRequest):
    """
    This endpoint demonstrates the use of the 'top_p' (nucleus sampling) parameter.
    A low top_p restricts the model to a small pool of high-probability tokens,
    leading to less diverse output. A high top_p allows for a wider, more
    diverse range of tokens to be considered.
    """
    
    # 3. Create the generation_config object. It's best practice to primarily
    #    tune either temperature or top_p, not both aggressively.
    generation_config = {
        "top_p": request.top_p,
        "temperature": 0.7 # Keep temperature stable to isolate the effect of Top P
    }

    prompt = f"""
    You are a senior marketing strategist. Generate a list of 3 distinct and creative marketing angles for the following startup.

    Startup Description: "{request.description}"
    """

    # 4. Call the Gemini API, passing in the generation_config
    response = model.generate_content(
        prompt,
        generation_config=generation_config
    )

    # 5. Return the AI's response
    return {
        "marketing_angles": response.text.strip(),
        "top_p_used": request.top_p
    }

# ===================================================================
# ===== IMPLEMENTED TOP-K ======
# ===================================================================
from pydantic import Field

# 1. Create a Pydantic model for the request. We'll allow the user
#    to pass in a top_k value.
class FaqRequest(BaseModel):
    description: str
    top_k: int = Field(
        40, 
        ge=1,
        description="Restricts the model's choices to the top K most likely tokens. 1 is very restrictive, 50 is less so."
    )

# 2. Create the new endpoint that uses the top_k parameter
@app.post("/generate-faq-with-top-k")
async def generate_faq_with_top_k(request: FaqRequest):
    """
    This endpoint demonstrates the use of the 'top_k' parameter.
    Top K restricts the model's choices to a fixed number of the most
    likely next tokens, which can make the output more focused and predictable.
    """
    
    # 3. Create the generation_config object.
    generation_config = {
        "top_k": request.top_k,
    }

    prompt = f"""
    You are a helpful customer support assistant. Generate one common question and a concise, clear answer for the following startup.

    Startup Description: "{request.description}"
    """

    # 4. Call the Gemini API, passing in the generation_config
    response = model.generate_content(
        prompt,
        generation_config=generation_config
    )

    # 5. Return the AI's response
    return {
        "faq": response.text.strip(),
        "top_k_used": request.top_k
    }

# ===================================================================
# ===== STOP SEQUENCE ======
# ===================================================================

# 1. Create a Pydantic model for the request.
class FirstStepRequest(BaseModel):
    description: str

# 2. Create the new endpoint that uses a stop sequence
@app.post("/generate-first-step-with-stop-sequence")
async def generate_first_step_with_stop_sequence(request: FirstStepRequest):
    """
    This endpoint demonstrates the use of a 'stop_sequence'.
    The prompt asks for a list, but the stop sequence will halt generation
    before the second item, ensuring only the first step is returned.
    """
    
    # 3. Create the generation_config object with a stop sequence.
    # We will stop the model right before it generates "2.".
    generation_config = {
        "stop_sequences": ["2."],
        "temperature": 0.7 # Using a moderate temperature for good suggestions
    }

    # This prompt asks for multiple steps, but our stop sequence will cut it short.
    prompt = f"""
    You are a marketing expert. Generate a numbered list of the first three marketing steps for the following startup.

    Startup Description: "{request.description}"

    1.
    """

    # 4. Call the Gemini API, passing in the generation_config
    response = model.generate_content(
        prompt,
        generation_config=generation_config
    )

    # 5. Return the AI's response, which will be just the first step.
    # We add "1." back to the front for a clean output.
    return {
        "first_step": "1. " + response.text.strip(),
    }

