from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "Ranking Service"
    ENV : str = "local"
    LOG_LEVEL: str = "INFO"
    
    MONGO_URI: str = Field(default="mongodb://localhost:27017", env="MONGO_URI")
    MONGO_DB : str = Field(default="rankings_db", env="MONGO_DB")
    
    HOST : str = "0.0.0.0"
    PORT : int = 8000
    
    FILTERED_CANDIDATES_COLLECTION: str = "filtered_candidates"
    
    CANDIDATE_SOURCE_URL: str = (
        "https://recruiting-test-resume-data.hiredscore.com/ps-dev-allcands-full-api_hub_b1f6.json"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()