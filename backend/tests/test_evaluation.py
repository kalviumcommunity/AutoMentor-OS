import pytest
import requests
import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

# --- SETUP ---
# Load environment variables to get the API key for the "judge" LLM
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
judge_model = genai.GenerativeModel('gemini-1.5-flash')

# Define the URL of your running FastAPI application
API_URL = "http://127.0.0.1:8000/generate-startup-idea"

# Load the evaluation dataset
def load_test_cases():
    with open("tests/evaluation_dataset.json", "r") as f:
        return json.load(f)

# Use pytest's parametrize feature to create a test for each case in the dataset
@pytest.mark.parametrize("test_case", load_test_cases())
def test_startup_idea_generation(test_case):
    """
    This test runs for each entry in the evaluation_dataset.json file.
    It calls the API, gets the result, and uses a "judge" LLM to evaluate the quality.
    """
    # 1. ACT: Call your FastAPI endpoint with the input from the test case
    response = requests.post(API_URL, json=test_case["input"])
    assert response.status_code == 200
    
    # The actual output from your main.py endpoint
    actual_output = response.json()["idea"]

    # 2. JUDGE: Create the prompt for the evaluation "judge"
    judge_prompt = f"""
    You are an expert evaluator for a Generative AI system. Your task is to determine if the AI's output meets the required criteria based on the user's input.
    Respond with only the word "PASS" or "FAIL".

    ---
    USER INPUT:
    - Skills: {test_case["input"]["skills"]}
    - Interests: {test_case["input"]["interests"]}

    ---
    EXPECTED CRITERIA:
    {test_case["expected_criteria"]}

    ---
    ACTUAL AI OUTPUT:
    {actual_output}
    ---

    Based on the criteria, does the AI output pass the evaluation?
    Answer with only "PASS" or "FAIL".
    """

    # Call the judge LLM to get the verdict
    judge_response = judge_model.generate_content(judge_prompt)
    verdict = judge_response.text.strip().upper()

    # 3. ASSERT: Check if the judge's verdict is "PASS"
    assert verdict == "PASS", f"Evaluation failed for test case '{test_case['id']}'. Judge said: {verdict}. AI Output was: {actual_output}"