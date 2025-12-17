from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Language(BaseModel):
    read: str
    write: str
    speak: str
    comments: str
    language_code: str

class Location(BaseModel):
    region: Optional[str] = None
    country_code: Optional[str] = None
    municipality: Optional[str] = None
    short_display_address: Optional[str] = None

class CompanyDetails(BaseModel):
    company_type: Optional[str] = None
    company: Optional[str] = None
    _id: Optional[str] = None
    company_url: Optional[str] = None
    number_of_time_seen: Optional[int] = None
    industry: Optional[str] = None
    size: Optional[str] = None

class Experience(BaseModel):
    company_normalized_name: Optional[str] = None
    last_job: Optional[bool] = None
    company_name: Optional[str] = None
    position_type: Optional[str] = None
    duration_in_month: Optional[int] = None
    current_job: Optional[bool] = None
    title: Optional[str] = None
    start_date: Optional[str] = None
    same_company: Optional[bool] = None
    description_short: Optional[str] = None
    company_details: Optional[CompanyDetails] = None
    end_date: Optional[str] = None
    employer_org_name: Optional[str] = None
    location: Optional[Location] = None
    description: Optional[str] = None

class Education(BaseModel):
    degree_major: Optional[str] = None
    institution_name: Optional[str] = None
    institution_location: Optional[Location] = None
    degree_type: Optional[str] = None
    normalized_GPA: Optional[float] = None
    graduated: Optional[bool] = None
    degree_minor: Optional[str] = None
    end_date: Optional[str] = None
    institution_normalized_name: Optional[str] = None
    GPA: Optional[str] = None
    institute_type: Optional[str] = None
    degree_level: Optional[str] = None
    graduation_date: Optional[str] = None
    description: Optional[str] = None
    degree_name: Optional[str] = None
    institution_details: Optional[Dict[str, Any]] = None
    start_date: Optional[str] = None

class PostalAddress(BaseModel):
    address_line: Optional[str] = None
    country_code: Optional[str] = None
    postal_code: Optional[str] = None
    region: Optional[str] = None
    municipality: Optional[str] = None
    short_display_address: Optional[str] = None

class Name(BaseModel):
    formatted_name: Optional[str] = None
    family_name: Optional[str] = None
    middle_name: Optional[str] = None
    given_name: Optional[str] = None

class ContactInfo(BaseModel):
    location: Optional[Dict[str, float]] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    postal_address: Optional[PostalAddress] = None
    image_url: Optional[str] = None
    name: Optional[Name] = None

class MilitaryHistory(BaseModel):
    country_served: Optional[str] = None
    comments: Optional[str] = None

class ResumeSkill(BaseModel):
    last_used: Optional[str] = None
    total_months: Optional[str] = None
    name: Optional[str] = None

class Certificate(BaseModel):
    description: Optional[str] = None
    name: Optional[str] = None

class Candidate(BaseModel):
    highest_degree: Optional[str] = None
    languages: Optional[List[Language]] = None
    experience: Optional[List[Experience]] = None
    extracted_skills: Optional[List[str]] = None
    education: Optional[List[Education]] = None
    contact_info: Optional[ContactInfo] = None
    military_history: Optional[MilitaryHistory] = None
    skills_text: Optional[str] = None
    resume_as_text: Optional[str] = None
    resume_skills: Optional[List[ResumeSkill]] = None
    sources: Optional[List[str]] = None
    certificate: Optional[List[Certificate]] = None
    skill_groups: Optional[Dict[str, List[str]]] = None

