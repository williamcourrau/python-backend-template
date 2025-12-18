from typing import List
from app.models.candidate_entity import Candidate
from app.services.url_connection_service import UrlConnectionService
from app.services.candidate_parser import CandidateParser
from app.config.logging import get_logger

logger = get_logger(__name__)


class CandidateLoaderService:
    """
    Fetches candidate data from an external source and parses it.
    Provides user-friendly error handling for non-technical users.
    """

    def __init__(self, url: str, timeout: int = 10):
        self.url = url
        self.timeout = timeout

    def fetch(self) -> List[Candidate]:
        logger.info("Starting candidate fetch from URL: %s", self.url)

        try:
            connection = UrlConnectionService(self.url, self.timeout)
            raw_json = connection.fetch()
        except Exception as e:
            logger.exception("Failed to retrieve candidate data from URL")
            raise RuntimeError(
                "We were unable to retrieve candidate information at this time. "
                "Please check the data source URL or try again later."
            ) from e

        if not raw_json or not raw_json.strip():
            logger.warning("Candidate source returned an empty response")
            raise RuntimeError(
                "The candidate data source returned no information. "
                "Please verify that the source contains candidate data."
            )

        try:
            candidates = CandidateParser.parse(raw_json)
        except Exception as e:
            logger.exception("Failed to parse candidate data")
            raise RuntimeError(
                "Candidate data was retrieved but could not be processed. "
                "Please contact support or verify the data format."
            ) from e

        logger.info(
            "Candidate fetch completed successfully. %d candidates loaded.",
            len(candidates),
        )

        return candidates
