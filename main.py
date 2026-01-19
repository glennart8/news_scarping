from pydantic import BaseModel, Field
from typing import Literal, List
from openai import OpenAI
import os

# Initiera klienten (kräver API-nyckel)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# --- 1. Definiera din Pydantic-modell ---
# Detta är "mallen" du tvingar LLM att följa
class NyhetsAnalys(BaseModel):
    titel: str = Field(..., description="En kort, kärnfull rubrik på svenska.")
    sammanfattning: str = Field(..., description="Max 2 meningar sammanfattning.")
    land: str = Field(..., description="Vilket land nyheten handlar om mest (t.ex. Sverige, USA).")
    kategori: Literal["Inrikes", "Utrikes", "Ekonomi", "Sport", "Teknik", "Klimat"]
    allvarlighetsgrad: int = Field(..., description="Betygsätt nyhetens allvar från 1 (kuriosa) till 10 (kris/krig).")

class NyhetsLista(BaseModel):
    artiklar: List[NyhetsAnalys]

# --- 2. Funktionen som gör magin ---
def analysera_nyhet(rå_text):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",  # Modeller som stöder "Structured Outputs"
        messages=[
            {"role": "system", "content": "Du är en nyhetsredaktör. Analysera texten och extrahera data enligt schemat."},
            {"role": "user", "content": f"Här är artikeln: {rå_text}"},
        ],
        response_format=NyhetsAnalys, # HÄR kopplar vi på Pydantic-modellen
    )

    # Returnerar ett färdigt Python-objekt (inte en sträng!)
    return completion.choices[0].message.parsed

# --- 3. Testkörning (Låtsas att vi skrapat detta från SVT) ---
skrapad_text_från_svt = """
Regeringen meddelade idag att man skjuter till ytterligare 500 miljoner kronor till försvaret. 
Statsministern underströk att säkerhetsläget i Europa kräver prioriteringar. 
Oppositionen är dock kritisk och menar att pengarna tas från vården.
"""

analys = analysera_nyhet(skrapad_text_från_svt)

# --- 4. Resultatet ---
# Nu kan du använda datan programmeringstekniskt:
print(f"Kategori: {analys.kategori}")  # Output: Inrikes
print(f"Land: {analys.land}")          # Output: Sverige
print(f"Allvar: {analys.allvarlighetsgrad}/10") 

# Om du vill spara det som JSON:
print(analys.model_dump_json(indent=2))