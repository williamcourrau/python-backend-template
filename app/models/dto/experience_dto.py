from dataclasses import dataclass

@dataclass
class ExperienceDTO:
    title: str
    company: str
    industry: str | None
    start_date: str | None
    end_date: str | None
    location: str | None