import argparse
import asyncio

from app.config.settings import settings
from app.config.logging import get_logger
from app.db.mongo_connection import MongoClientProvider
from app.entry_points.cli_parser import CliArgumentParser
from app.entry_points.commands.get_candidates_command import GetCandidatesCommand
from app.entry_points.commands.filter_candidates_command import FilterCandidatesCommand
from app.entry_points.exceptions import InvalidCliArguments
from app.repositories.mongo_candidate_repository import MongoCandidateRepository as CandidateRepository
from app.services.candidate_loader_service import CandidateLoaderService
from app.services.candidate_presenter_service import CandidatePresenterService
from app.services.candidate_service import CandidateService
from app.services.experience_formatter import ExperienceFormatter
from app.services.gap_calculator_service import GapCalculatorService


logger = get_logger(__name__)

def build_command_registry(
    candidate_repository: CandidateRepository,
    candidate_loader: CandidateLoaderService,
):
    candidate_service = CandidateService(candidate_repository)

    gap_calculator = GapCalculatorService()
    formatter = ExperienceFormatter()

    presenter = CandidatePresenterService(
        gap_calculator=gap_calculator,
        formatter=formatter,
    )

    parser = CliArgumentParser()

    return {
        "get-candidates": GetCandidatesCommand(
            loader=candidate_loader,
            presenter=presenter,
        ),
        "filter-candidates": FilterCandidatesCommand(
            loader=candidate_loader,
            service=candidate_service,
            presenter=presenter,
            parser=parser,
        ),
    }

def parse_main_args():
    parser = argparse.ArgumentParser(
        description="Candidate CLI Application", add_help=True
    )

    parser.add_argument(
        "command",
        nargs="?",
        choices=["get-candidates", "filter-candidates"],
        help="Command to execute",
    )

    args, remaining_args = parser.parse_known_args()
    return args, remaining_args

async def main():
    try:
        args, remaining_args = parse_main_args()

        # ---- Infrastructure (async-safe) ----
        mongo_provider = MongoClientProvider()
        db = await mongo_provider.get_database()

        candidate_repository = CandidateRepository(
            db=db,
            collection_name=settings.FILTERED_CANDIDATES_COLLECTION,
        )

        candidate_loader = CandidateLoaderService(
            url=settings.CANDIDATE_SOURCE_URL,
            timeout=30,
        )

        # ---- Commands ----
        commands = build_command_registry(
            candidate_repository=candidate_repository,
            candidate_loader=candidate_loader,
        )

        command = commands.get(args.command)
        if not command:
            raise InvalidCliArguments(f"Unknown command '{args.command}'")

        logger.info("Executing command: %s", args.command)
        await command.execute(remaining_args)

    except InvalidCliArguments as e:
        logger.error("Invalid CLI arguments: %s", e)
        print(f"Error: {e}")

    except Exception:
        logger.exception("Unhandled application error")
        print("Unexpected error occurred. Check logs for details.")


if __name__ == "__main__":
    asyncio.run(main())
