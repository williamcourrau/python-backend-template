from typing import Iterable, List, Dict, Any
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import UpdateOne
from pymongo.errors import BulkWriteError
from pymongo.operations import IndexModel

from app.config.logging import get_logger
from app.models.candidate_entity import Candidate as CandidateEntity
from app.repositories.base_candidate_repository import ICandidateRepository

logger = get_logger(__name__)


class MongoCandidateRepository(ICandidateRepository):
    """
    Generic MongoDB repository for candidate-like documents.

    This repository:
    - Is idempotent
    - Is concurrency-safe
    - Does NOT assume document schema
    - Does NOT define index strategy
    """

    def __init__(
        self,
        db: AsyncIOMotorDatabase,
        collection_name: str,
        indexes: List[IndexModel] | None = None,
    ):
        self._col = db[collection_name]
        self._indexes = indexes or []

    async def ensure_indexes(self) -> None:
        """
        Creates indexes provided at construction time.

        Index responsibility belongs to the application layer,
        not the repository itself.
        """
        if not self._indexes:
            logger.info(
                "No indexes configured for collection '%s'",
                self._col.name,
            )
            return

        try:
            logger.info(
                "Ensuring %d indexes for collection '%s'",
                len(self._indexes),
                self._col.name,
            )
            await self._col.create_indexes(self._indexes)
        except Exception:
            logger.exception(
                "Failed to create indexes for collection '%s'",
                self._col.name,
            )

    async def upsert_filtered_candidates(
        self,
        candidates: Iterable[CandidateEntity],
        ordered: bool = False,
    ) -> Dict[str, Any]:

        ops: List[UpdateOne] = []
        now = datetime.utcnow()
        skipped = 0

        for c in candidates:
            if not c.candidate_id:
                logger.warning(
                    "Skipping document due to missing candidate_id: %s",
                    c,
                )
                skipped += 1
                continue

            update = {
                "$setOnInsert": {
                    "candidate_id": c.candidate_id,
                    "created_at": now,
                },
                "$set": {
                    **c.to_persistence_dict(),
                    "updated_at": now,
                },
            }

            ops.append(
                UpdateOne(
                    {"candidate_id": c.candidate_id},
                    update,
                    upsert=True,
                )
            )

        if not ops:
            return {
                "success": True,
                "total_processed": skipped,
                "upserted_count": 0,
                "matched_count": 0,
                "skipped": skipped,
                "errors": [],
            }

        try:
            result = await self._col.bulk_write(ops, ordered=ordered)
            return {
                "success": True,
                "total_processed": result.matched_count + result.upserted_count + skipped,
                "upserted_count": result.upserted_count,
                "matched_count": result.matched_count,
                "skipped": skipped,
                "errors": [],
            }

        except BulkWriteError as bwe:
            logger.exception("Bulk write error")
            return {
                "success": False,
                "total_processed": len(ops) + skipped,
                "upserted_count": 0,
                "matched_count": 0,
                "skipped": skipped,
                "errors": ["Duplicate key or index violation"],
            }

        except Exception as e:
            logger.exception("Unexpected database error")
            return {
                "success": False,
                "total_processed": len(ops) + skipped,
                "upserted_count": 0,
                "matched_count": 0,
                "skipped": skipped,
                "errors": ["Unexpected database error"],
            }
