import asyncio
import sys

from app.entry_points.cli_parser import CliArgumentParser
from app.db.mongo_connection import MongoClientProvider
from app.entry_points.exceptions import InvalidCliArguments
from app.repositories.mongo_candidate_repository import CandidateRepository
from app.services.candidate_fetcher import CandidateFetcher
from app.services.candidate_service import CandidateService


async def main():
    try:
        filters = CliArgumentParser().parse_filter_arguments()
    except InvalidCliArguments as e:
        print(f"Invalid arguments: {e}")
        sys.exit(1)

    db = MongoClientProvider().get_database()
    repository = CandidateRepository(db)
    service = CandidateService(repository)

    url = "https://recruiting-test-resume-data.hiredscore.com/ps-dev-allcands-full-api_hub_b1f6.json"
    fetcher = CandidateFetcher(url=url, timeout=30)
    candidates = fetcher.fetch()
    
    result = await service.filter_candidates(candidates, filters)

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
