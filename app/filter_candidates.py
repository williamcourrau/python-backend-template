import asyncio

from app.entry_points.cli_parser import CliArgumentParser
from app.db.mongo_connection import MongoClientProvider
from app.repositories.mongo_candidate_repository import CandidateRepository
from app.services.candidate_fetcher import CandidateFetcher
from app.services.candidate_service import CandidateService


async def main():
    filters = CliArgumentParser().parse()

    db = MongoClientProvider().get_database()
    repository = CandidateRepository(db)
    service = CandidateService(repository)

    url = "https://recruiting-test-resume-data.hiredscore.com/ps-dev-allcands-full-api_hub_b1f6.json"
    fetcher = CandidateFetcher(url=url, timeout=30)
    candidates = fetcher.fetch()
    
    result = await service.filter_and_persist(candidates, filters)

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
