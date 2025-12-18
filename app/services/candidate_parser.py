import json
from typing import List
from app.models.candidate_entity import Candidate
from app.config.logging import get_logger

logger = get_logger(__name__)


class CandidateParser:
    """
    Parses raw JSON into Candidate entities.
    Skips invalid records but preserves valid ones.
    """

    @staticmethod
    def parse(json_data: str) -> List[Candidate]:
        if not json_data or not json_data.strip():
            logger.warning("Empty candidate JSON received")
            return []

        try:
            data = json.loads(json_data)
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON format received")
            raise ValueError(
                "Candidate data could not be read. The file format is invalid."
            ) from e

        if not isinstance(data, list):
            logger.error("Candidate JSON root is not a list")
            raise ValueError(
                "Candidate data format is invalid. Expected a list of candidates."
            )

        candidates: List[Candidate] = []
        skipped = 0

        for idx, raw_candidate in enumerate(data):
            if not isinstance(raw_candidate, dict):
                logger.warning(
                    "Skipping candidate at index %d: not a JSON object", idx
                )
                skipped += 1
                continue

            try:
                candidates.append(Candidate(**raw_candidate))
            except Exception:
                skipped += 1
                logger.exception(
                    "Skipping malformed candidate at index %d", idx
                )

        logger.info(
            "Candidate parsing completed: %d valid, %d skipped",
            len(candidates),
            skipped,
        )

        return candidates
