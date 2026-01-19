from pydantic import BaseModel, Field
from typing import Literal

# --- Pydantic Models  ---
class NewsAnalysis(BaseModel):
    title: str = Field(..., description="A short, punchy headline in Swedish.")
    summary: str = Field(..., description="Max 2 sentences summary.")
    country: str = Field(..., description="The country the news is mostly about (e.g. Sweden, USA).")
    category: Literal["Domestic", "Foreign", "Economy", "Sports", "Technology", "Climate", "Crime"]
    severity: int = Field(..., description="Rate the severity from 1 (curiosity) to 10 (crisis/war).", ge=1, le=10)