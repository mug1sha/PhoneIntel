from google import genai
from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def explain_analysis(data: dict):
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"Explain this phone number analysis clearly:\n{data}"
        )
        return response.text
    except Exception as e:
        return f"AI service error: {str(e)}"