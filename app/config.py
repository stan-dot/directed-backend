from pydantic import BaseSettings

class Settings(BaseSettings):
    rds_hostname: str
    rds_port: str
    rds_password: str
    rds_db_name: str
    rds_username: str
    #secret_key: str
    #algorithm: str
    #access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()