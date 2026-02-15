from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.services.phone_service import analyze_number
from app.config import GEMINI_API_KEY
from google import genai
import time

# Initialize FastAPI
app = FastAPI(title="PhoneIntel API")

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# Request model (clean validation)
class PhoneRequest(BaseModel):
    number: str


@app.post("/lookup")
def lookup(request: PhoneRequest):
    start_time = time.time()

    # Step 1: Analyze phone number
    data = analyze_number(request.number)

    if not data.get("valid"):
        raise HTTPException(status_code=400, detail="Invalid phone number")

    # Step 2: Call Gemini AI safely
    try:
        ai_response = client.models.generate_content(
        model="models/gemini-1.0-pro",
        contents=f"""
        Explain this phone number analysis clearly and professionally.
        Add useful security insights if relevant.

        Data:
        {data}
        """
    )

        explanation = ai_response.text

    except Exception as e:
        explanation = f"AI service error: {str(e)}"

    end_time = time.time()

    return {
        "analysis": data,
        "ai_explanation": explanation,
        "processing_time_seconds": round(end_time - start_time, 3)
    }