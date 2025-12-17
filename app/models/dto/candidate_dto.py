from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CandidateDTO:
    candidate_id: str
    name: Optional[str]       
    email: Optional[str]
    location: Optional[str]
    highest_degree: Optional[str]
    total_experience_years: float
    skills: List[str]
    industries: List[str]