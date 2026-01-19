from google import genai
from backend.data_models import NewsAnalysis
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

# --- AI-Analysfunktionen ---
def analyze_news(raw_text):
    try:
        prompt = f"You are a news editor. Analyze the text and extract data according to the schema.\n\nHere is the article: {raw_text}"

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": NewsAnalysis,
            }
        )
        return response.parsed
    except Exception as e:
        print(f"AI-Analys misslyckades: {e}")
        return None

# --- Skapar manus för uppläsning ---
def generate_radio_script(articles: List[NewsAnalysis]):
    """Sammanfattar en lista med analyserade artiklar till ett radiomanus."""
    try:
        # Bygg en kontextsträng av alla artiklar
        context_text = ""
        for i, art in enumerate(articles, 1):
            context_text += f"Nyhet {i}: {art.title}. {art.summary}. Kategori: {art.category}.\n"

        prompt = f"""
        Du är en professionell nyhetsuppläsare på radio (Sveriges Radio).
        Din uppgift är att sammanfatta följande nyheter till ett kort, engagerande manus på svenska som ska läsas upp.
        Börja med en välkomsthälsning och avsluta tydligt. Håll en saklig men engagerande ton.
        Använd inte punktlistor eller konstiga tecken, skriv som talspråk.
        
        Nyheter att rapportera om:
        {context_text}
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Kunde inte skapa manus: {e}")
        return "Tyvärr kunde inga nyheter sammanställas just nu."