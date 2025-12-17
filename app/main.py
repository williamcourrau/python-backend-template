import asyncio

from app.services.candidate_fetcher import CandidateFetcher
from app.services.candidate_printer_service import CandidatePrinterService
from app.repositories.mongo_candidate_repository import CandidateRepository  
from app.services.candidate_service import CandidateService
from app.db.mongo_connection import MongoClientProvider

db = MongoClientProvider().get_database()

async def main():
    url = "https://recruiting-test-resume-data.hiredscore.com/ps-dev-allcands-full-api_hub_b1f6.json"
    fetcher = CandidateFetcher(url=url, timeout=30)
    candidates = fetcher.fetch()
    print(f"Retrieved {len(candidates)} candidates:\n")
    for candidate in candidates:
        CandidatePrinterService.print_candidate(candidate)
        
    
    repo = CandidateRepository(db)
    candidate_service = CandidateService(repo)
    
    result = await candidate_service.filter_and_persiste_candidates(candidates, "Real Estate", ["general ledger"], 3.0)

if __name__ == "__main__":
    asyncio.run(main())
