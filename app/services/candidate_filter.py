from typing import List
from app.models.candidate_entity import Candidate
from datetime import datetime

class CandidateFilter:
    @staticmethod
    def filter_by_industry(candidates: List[Candidate], industry: str) -> List[Candidate]:
        if not industry:
            return candidates
        filtered = []
        for cand in candidates:
            if not cand.experience:
                continue
            for exp in cand.experience:
                if exp.company_details and exp.company_details.industry and industry.lower() in exp.company_details.industry.lower():
                    filtered.append(cand)
                    break
        return filtered

    @staticmethod
    def filter_by_skills(candidates: List[Candidate], skills: List[str]) -> List[Candidate]:
        if not skills:
            return candidates
        filtered = []
        for cand in candidates:
            cand_skills = set([s.lower() for s in (cand.extracted_skills or [])])
            if all(skill.lower() in cand_skills for skill in skills):
                filtered.append(cand)
        return filtered

    @staticmethod
    def filter_by_min_years(candidates: List[Candidate], min_years: float) -> List[Candidate]:
        if not min_years:
            return candidates
        filtered = []
        for cand in candidates:
            total_days = 0
            if not cand.experience:
                continue
            for exp in cand.experience:
                if exp.start_date and exp.end_date:
                    try:
                        start = datetime.strptime(exp.start_date, "%b/%d/%Y")
                        end = datetime.strptime(exp.end_date, "%b/%d/%Y")
                        total_days += (end - start).days + 1
                    except Exception:
                        continue
            total_years = total_days / 365.25
            if total_years >= min_years:
                filtered.append(cand)
        return filtered
