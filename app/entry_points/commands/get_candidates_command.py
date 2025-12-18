from typing import List
from app.entry_points.commands.base import Command
from app.services.candidate_loader_service import CandidateLoaderService
from app.services.candidate_presenter_service import CandidatePresenterService
from app.config.logging import get_logger

logger = get_logger(__name__)


class GetCandidatesCommand(Command):
    """
    CLI command responsible for retrieving and presenting all candidates.

    Responsibilities:
    - Coordinate candidate loading
    - Delegate presentation
    - Handle user-friendly errors

    Infrastructure and formatting are delegated.
    """

    def __init__(
        self,
        loader: CandidateLoaderService,
        presenter: CandidatePresenterService,
    ):
        self._loader = loader
        self._presenter = presenter

    async def execute(self, args: List[str]) -> None:
        try:
            logger.info("Loading candidates")
            candidates = self._loader.fetch()

            if not candidates:
                print("No candidates were found.")
                return

            print(f"Retrieved {len(candidates)} candidates:\n")

            for candidate in candidates:
                ouput = self._presenter.build_lines(candidate)
                print()
                print(ouput)

        except Exception:
            logger.exception("Failed to execute get-candidates command")
            print(
                "We were unable to retrieve candidate information at this time. "
                "Please try again later or contact support."
            )
