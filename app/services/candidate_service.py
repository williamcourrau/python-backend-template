from typing import List, Dict
from app.models.candidate_entity import Candidate
from app.models.dto.candidate_dto import CandidateDTO
from app.repositories.base_candidate_repository import ICandidateRepository


class CandidateService:

    def __init__(self, candidate_repository: ICandidateRepository):
        self.candidate_repository = candidate_repository

    async def filter_and_persiste_candidates(
        self,
        raw_candidates: List[Candidate],  # ✅ Candidate objects, not Dicts
        industry: str | None,
        skills: List[str] | None,
        min_years: float | None,
    ) -> Dict:

        entities: List[CandidateDTO] = []

        for c in raw_candidates:
            # --- experience
            experience = c.experience or []
            if not experience:
                continue

            # --- extracted skills
            extracted_skills = [s.lower() for s in (c.extracted_skills or [])]

            if skills and not any(s.lower() in extracted_skills for s in skills):
                continue

            # --- industries from experience
            industries = list({
                j.company_details.industry
                for j in experience
                if j.company_details and j.company_details.industry
            })

            if industry and not any(industry.lower() in i.lower() for i in industries):
                continue

            # --- total experience
            total_months = sum(j.duration_in_month or 0 for j in experience)
            total_years = round(total_months / 12, 2)

            if min_years and total_years < min_years:
                continue

            # --- safe contact info access
            contact = c.contact_info
            name = contact.name.formatted_name if contact and contact.name else None
            email = contact.email if contact else None
            location = (
                contact.postal_address.short_display_address
                if contact and contact.postal_address
                else None
            )

            entity = CandidateDTO(
                candidate_id=email,  # or another stable ID
                name=name,
                email=email,
                location=location,
                highest_degree=c.highest_degree,
                total_experience_years=total_years,
                skills=extracted_skills,
                industries=industries,
            )

            entities.append(entity)

        return await self.candidate_repository.upsert_candidates(entities)
