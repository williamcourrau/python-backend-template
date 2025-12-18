import argparse
import asyncio
import sys

from app.config.logging import get_logger
from app.db.mongo_connection import MongoClientProvider
from app.entry_points.commands.get_candidates_command import GetCandidatesCommand
from app.entry_points.commands.filter_candidates_command import FilterCandidatesCommand
from app.entry_points.exceptions import InvalidCliArguments
from app.repositories.mongo_candidate_repository import CandidateRepository
from app.services.candidate_service import CandidateService


logger = get_logger(__name__)

def build_command_registry():

    db = MongoClientProvider().get_database()

    candidate_repository = CandidateRepository(db)

    candidate_service = CandidateService(candidate_repository)

    return {
        "get-candidates": GetCandidatesCommand(),
        "filter-candidates": FilterCandidatesCommand(candidate_service),
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
        commands = build_command_registry()

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
