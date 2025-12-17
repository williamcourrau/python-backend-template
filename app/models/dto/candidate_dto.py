from dataclasses import dataclass
from typing import List
from app.models.dto.experience_dto import ExperienceDTO

@dataclass
class CandidateDTO:
    candidate_id: str
    candidate_name: str
    highest_degree: str | None
    total_experience_years: float
    skills: List[str]
    experiences: List[ExperienceDTO]
    source: List[str]