from pydantic import BaseModel, Field
from typing import Literal, List
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# --- Pydantic Model ---
class NewsAnalysis(BaseModel):
    title: str = Field(..., description="A short, punchy headline in Swedish.")
    summary: str = Field(..., description="Max 2 sentences summary.")
    country: str = Field(..., description="The country the news is mostly about (e.g. Sweden, USA).")
    category: Literal["Domestic", "Foreign", "Economy", "Sports", "Technology", "Climate", "Crime"]
    severity: int = Field(..., description="Rate the severity from 1 (curiosity) to 10 (crisis/war).")

class NewsList(BaseModel):
    articles: List[NewsAnalysis]

# --- 2. The function doing the magic ---
def analyze_news(raw_text):
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"You are a news editor. Analyze the text and extract data according to the schema.\n\nHere is the article: {raw_text}"

    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=NewsAnalysis
        )
    )

    # Returns a ready Python object
    return NewsAnalysis.model_validate_json(response.text)

# --- Test run (Pretend we scraped this from SVT) ---
scraped_text_svt = """
Regeringen meddelade idag att man skjuter till ytterligare 500 miljoner kronor till försvaret. 
Statsministern underströk att säkerhetsläget i Europa kräver prioriteringar. 
Oppositionen är dock kritisk och menar att pengarna tas från vården.
"""

analysis = analyze_news(scraped_text_svt)

# --- The Result ---
# Now you can use the data programmatically:
print(f"Category: {analysis.category}")  
print(f"Country: {analysis.country}")    
print(f"Severity: {analysis.severity}/10") 

# If you want to save it as JSON:
print(analysis.model_dump_json(indent=2))