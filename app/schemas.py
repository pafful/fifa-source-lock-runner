from pydantic import BaseModel
from typing import Optional



class FixtureRunRequest(BaseModel):
    fixture: str
    prediction_mode: str = "pre_match"
    cutoff_policy: str = "before_kickoff"
    source_policy: str = "official_fifa_only"
    pdf_url: Optional[str] = None