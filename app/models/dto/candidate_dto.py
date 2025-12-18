from dataclasses import dataclass, asdict
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
    
    def to_persistence_dict(self) -> dict:
        """
        Returns a MongoDB-safe dictionary representation.
        Excludes candidate_id because it is used as the upsert key.
        """
        data = asdict(self)
        data.pop("candidate_id", None)
        return data