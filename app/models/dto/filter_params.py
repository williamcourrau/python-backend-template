from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class CandidateFilterParams:
    industry: Optional[str]
    skills: Optional[List[str]]
    min_years_experience: Optional[int]
