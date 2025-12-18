from abc import ABC, abstractmethod
from typing import Iterable, Dict, Any
from app.models.dto.candidate_dto import CandidateDTO


class ICandidateRepository(ABC):

    @abstractmethod
    async def upsert_filtered_candidates(
        self,
        candidates: Iterable[CandidateDTO],
        ordered: bool = False,
    ) -> Dict[str, Any]:
        pass