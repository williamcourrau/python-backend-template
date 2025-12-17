from typing import List
from app.models.candidate_entity import Candidate
from app.services.url_connection_service import UrlConnectionService
from app.services.candidate_parser import CandidateParser
from app.models.candidate_entity import Candidate
from typing import List

class CandidateFetcher:
    def __init__(self, url: str, timeout: int = 10):
        self.url = url
        self.timeout = timeout

    def fetch(self) -> List[Candidate]:
        connection = UrlConnectionService(self.url, self.timeout)
        raw_json = connection.fetch()
        return CandidateParser.parse(raw_json)
