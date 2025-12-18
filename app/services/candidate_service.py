from typing import List, Dict
from app.models.candidate_entity import Candidate
from app.models.dto.candidate_dto import CandidateDTO
from app.models.dto.filter_params import CandidateFilterParams
from app.repositories.base_candidate_repository import ICandidateRepository
from app.utils.candidate_id import generate_candidate_id


class CandidateService:

    def __init__(self, candidate_repository: ICandidateRepository):
        self._repository = candidate_repository

    async def filter_candidates(
        self,
        candidates: List[Candidate],
        filters: CandidateFilterParams,
    ) -> Dict:

        entities: List[CandidateDTO] = []

        for c in candidates:
            experience = c.experience or []
            if not experience:
                continue

            extracted_skills = [s.lower() for s in (c.extracted_skills or [])]

            if filters.skills and not any(
                s.lower() in extracted_skills for s in filters.skills
            ):
                continue

            industries = {
                e.company_details.industry
                for e in experience
                if e.company_details and e.company_details.industry
            }

            if filters.industry and not any(
                filters.industry.lower() in i.lower() for i in industries
            ):
                continue

            total_months = sum(e.duration_in_month or 0 for e in experience)
            total_years = round(total_months / 12, 2)

            if filters.min_years_experience and total_years < filters.min_years_experience:
                continue

            contact = c.contact_info
            name = contact.name.formatted_name if contact and contact.name else None
            email = contact.email if contact else None
            location = (
                contact.postal_address.short_display_address
                if contact and contact.postal_address
                else None
            )

            education = c.education or []
            institution = education[0].institution_name if education else None

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

        return await self._repository.upsert_candidates(entities)
