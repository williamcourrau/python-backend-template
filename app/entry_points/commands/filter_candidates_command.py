from app.entry_points.commands.base import Command
from app.services.candidate_fetcher import CandidateFetcher
from app.services.candidate_service import CandidateService
from app.services.candidate_printer_service import CandidatePrinterService
from app.entry_points.cli_parser import CliArgumentParser

class FilterCandidatesCommand(Command):
    def __init__(self, service: CandidateService):
        self.service = service
        self.cli_parser = CliArgumentParser()
    
    async def execute(self, args : list[str]) -> None:
        url = "https://recruiting-test-resume-data.hiredscore.com/ps-dev-allcands-full-api_hub_b1f6.json"
        fetcher = CandidateFetcher(url=url, timeout=30)
        candidates = fetcher.fetch()
        
        params = self.cli_parser.parse_filter_arguments(args)
        
        filtered_candidates = await self.service.filter_candidates(
            candidates,
            params
        )