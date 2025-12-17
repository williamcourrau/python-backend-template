from typing import Iterable, List, Dict, Any
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import UpdateOne
from pymongo.errors import BulkWriteError

from app.config.logging import get_logger
from app.models.dto.candidate_dto import CandidateDTO
from app.models.candidate_entity import Candidate as CandidateEntity
from app.repositories.base_candidate_repository import ICandidateRepository

logger = get_logger(__name__)


class CandidateRepository(ICandidateRepository):

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.col = self.db["filtered_candidates"]

    async def ensure_indexes(self) -> None:
        try:
            logger.info("Ensuring indexes for filtered_candidates collection")
            await self.col.create_index("candidate_id", unique=True)
            await self.col.create_index("email", unique=True, sparse=True)
            await self.col.create_index("skills")
            await self.col.create_index("industries")
            await self.col.create_index("total_experience_years")
        except Exception:
            logger.exception("Error creating database indexes")

    def _to_document(self, c: CandidateEntity) -> Dict[str, Any]:
        return {
            "candidate_id": c.candidate_id,
            "name": c.name,
            "email": c.email,
            "location": c.location,
            "highest_degree": c.highest_degree,
            "total_experience_years": c.total_experience_years,
            "skills": c.skills,
            "industries": c.industries,
        }

    async def upsert_candidates(
        self,
        candidates: Iterable[CandidateEntity],
        ordered: bool = False,
    ) -> Dict[str, Any]:

        ops: List[UpdateOne] = []
        now = datetime.utcnow()
        skipped = 0

        for c in candidates:
            if not c.candidate_id:
                logger.warning("Skipping candidate %s: missing candidate_id", c.name)
                skipped += 1
                continue

            update = {
                "$setOnInsert": {
                    "candidate_id": c.candidate_id,
                    "created_at": now,
                },
                "$set": {
                    "name": c.name,
                    "email": c.email,
                    "location": c.location,
                    "highest_degree": c.highest_degree,
                    "total_experience_years": c.total_experience_years,
                    "updated_at": now,
                },
                "$addToSet": {
                    "skills": {"$each": c.skills},
                    "industries": {"$each": c.industries},
                },
            }

            ops.append(
                UpdateOne(
                    {"candidate_id": c.candidate_id},
                    update,
                    upsert=True,
                )
            )

        result_summary = {
            "success": True,
            "total_processed": len(ops) + skipped,
            "upserted_count": 0,
            "matched_count": 0,
            "skipped": skipped,
            "errors": [],
        }

        if not ops:
            return result_summary

        try:
            result = await self.col.bulk_write(ops, ordered=ordered)
            result_summary["matched_count"] = result.matched_count
            result_summary["upserted_count"] = result.upserted_count

            logger.info(
                "Candidates processed: %d inserted, %d updated",
                result.upserted_count,
                result.matched_count,
            )

        except BulkWriteError as bwe:
            logger.exception("Bulk write error")
            result_summary["success"] = False
            if "duplicate key" in str(bwe).lower():
                result_summary["errors"].append("Duplicate candidate_id or email")
            else:
                result_summary["errors"].append("Bulk write failure")

        except Exception as e:
            logger.exception("Unexpected database error")
            result_summary["success"] = False
            if "timeout" in str(e).lower() or "connection" in str(e).lower():
                result_summary["errors"].append("Database connection issue")
            else:
                result_summary["errors"].append("Unexpected error")

        return result_summary
