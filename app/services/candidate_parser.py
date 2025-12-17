import json
from typing import List
from app.models.candidate_entity import Candidate

class CandidateParser:
    @staticmethod
    def parse(json_data: str) -> List[Candidate]:
        try:
            data = json.loads(json_data)
            return [Candidate(**candidate) for candidate in data]
        except Exception as e:
            print(f"Error parsing candidates: {e}")
            return []
