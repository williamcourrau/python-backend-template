from typing import List, Dict
from app.models.candidate_entity import Candidate
from app.models.dto.candidate_dto import CandidateDTO
from app.models.dto.filter_params import CandidateFilterParams
from app.repositories.base_candidate_repository import ICandidateRepository
from app.services.url_connection_service import UrlConnectionService
from app.utils.candidate_id import generate_candidate_id
from app.config.logging import get_logger
from app.services.candidate_loader_service import CandidateParser

logger = get_logger(__name__)

class CandidateService:
    """
        Service responsible for applying business rules to candidate data
        and persisting the filtered results.

        This class:
        - Applies skill, industry, and experience-based filters
        - Computes total years of professional experience
        - Generates stable candidate identifiers
        - Maps domain entities to persistence DTOs
        - Delegates persistence to a repository abstraction

        This class does NOT:
        - Fetch data from external sources
        - Parse raw JSON
        - Handle user input (CLI / UI)
        - Format output for display
    """

    def __init__(self, candidate_repository: ICandidateRepository):
        self._repository = candidate_repository

    async def filter_candidates(
        self,
        candidates: List[Candidate],
        filters: CandidateFilterParams,
    ) -> Dict:

        """
        Applies business filters to candidates and persists results.
        Per-candidate errors are logged and skipped.
        Repository errors are propagated.
        """

        entities: List[CandidateDTO] = []
        skipped = 0

        for c in candidates:
            try:
                experience = c.experience or []
                if not isinstance(experience, list) or not experience:
                    logger.debug("Skipping candidate: no valid experience")
                    skipped += 1
                    continue

                extracted_skills = [
                    s.lower()
                    for s in (c.extracted_skills or [])
                    if isinstance(s, str)
                ]

                # Skills filter
                if filters.skills and not any(
                    s in extracted_skills for s in filters.skills
                ):
                    continue

                # Industry filter
                industries = {
                    e.company_details.industry
                    for e in experience
                    if e.company_details and e.company_details.industry
                }

                if filters.industry and not any(
                    filters.industry.lower() in i.lower()
                    for i in industries
                ):
                    continue

                # Experience calculation
                total_months = sum(
                    e.duration_in_month or 0
                    for e in experience
                    if isinstance(e.duration_in_month, (int, float))
                )

                total_years = round(total_months / 12, 2)

                if (
                    filters.min_years_experience
                    and total_years < filters.min_years_experience
                ):
                    continue

                # Contact info
                contact = c.contact_info
                name = contact.name.formatted_name if contact and contact.name else None
                email = contact.email if contact else None
                location = (
                    contact.postal_address.short_display_address
                    if contact and contact.postal_address
                    else None
                )

                education = c.education or []
                institution = (
                    education[0].institution_name
                    if education and education[0].institution_name
                    else None
                )

                candidate_id = generate_candidate_id(
                    full_name=name,
                    highest_degree=c.highest_degree,
                    institution=institution,
                )

                entities.append(
                    CandidateDTO(
                        candidate_id=candidate_id,
                        name=name,
                        email=email,
                        location=location,
                        highest_degree=c.highest_degree,
                        total_experience_years=total_years,
                        skills=extracted_skills,
                        industries=list(industries),
                    )
                )

            except Exception as e:
                skipped += 1
                logger.exception(
                    "Failed to process candidate safely; candidate skipped. "
                    "Candidate snapshot: %s",
                    c,
                )

        logger.info(
            "Filtering completed: %d processed, %d skipped, %d total",
            len(entities),
            skipped,
            len(candidates),
        )

        return await self._repository.upsert_filtered_candidates(entities)
