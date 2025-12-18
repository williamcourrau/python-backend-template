from typing import List
from app.entry_points.commands.base import Command
from app.services.candidate_loader_service import CandidateLoaderService
from app.services.candidate_service import CandidateService
from app.services.candidate_presenter_service import CandidatePresenterService
from app.entry_points.cli_parser import CliArgumentParser
from app.config.logging import get_logger

logger = get_logger(__name__)


class FilterCandidatesCommand(Command):
    """
    CLI command responsible for:
    - Parsing filter arguments
    - Coordinating candidate loading
    - Applying filters
    - Presenting results

    Business logic and infrastructure concerns are delegated.
    """

    def __init__(
        self,
        loader: CandidateLoaderService,
        service: CandidateService,
        presenter: CandidatePresenterService,
        parser: CliArgumentParser,
    ):
        self.loader = loader
        self.service = service
        self.presenter = presenter
        self.parser = parser

    async def execute(self, args: List[str]) -> None:
        try:
            logger.info("Parsing filter arguments")
            filters = self.parser.parse_filter_arguments(args)

            logger.info("Loading candidates")
            candidates = self.loader.fetch()

            if not candidates:
                print("No candidates were found.")
                return

            logger.info("Filtering candidates")
            result = await self.service.filter_candidates(
                candidates=candidates,
                filters=filters,
            )

            logger.info("Presenting filtered candidates")
            print("\nCandidate filtering completed successfully.\n")

            print("Filters applied:")
            if filters.industry:
                print(f"- Industry: {filters.industry}")
            if filters.skills:
                print(f"- Skills: {', '.join(filters.skills)}")
            if filters.min_years_experience is not None:
                print(f"- Minimum experience: {filters.min_years_experience} years")

            print("\nResults:")
            print(f"- Candidates matched: {result.get('matched_count', 0)}")
            print(f"- Candidates saved: {result.get('upserted_count', 0)}")
            print(f"- Candidates skipped: {result.get('skipped', 0)}")


        except Exception as e:
            logger.exception("Failed to execute filter-candidates command")
            print(
                "An error occurred while filtering candidates. "
                "Please try again later or contact support."
            )
