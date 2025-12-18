from app.entry_points.commands.base import Command
from app.services.candidate_fetcher import CandidateFetcher
from app.services.candidate_printer_service import CandidatePrinterService

class GetCandidatesCommand(Command):

    async def execute(self, args) -> None:
        url = "https://recruiting-test-resume-data.hiredscore.com/ps-dev-allcands-full-api_hub_b1f6.json"
        fetcher = CandidateFetcher(url=url, timeout=30)
        candidates = fetcher.fetch()
        print(f"Retrieved {len(candidates)} candidates:\n")
        for candidate in candidates:
            CandidatePrinterService.print_candidate(candidate)