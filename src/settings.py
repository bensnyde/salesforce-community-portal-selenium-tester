from typing import List
from pydantic import BaseSettings, HttpUrl


class Settings(BaseSettings):

    SELENIUM_HUB_URL : HttpUrl
    SELENIUM_WAIT_TIME : int  

    EMAIL_TO : List[str]
    EMAIL_FROM : str
    EMAIL_SUBJECT : str
    EMAIL_TEMPLATE: str

    SMTP_SERVER : str
    SMTP_PORT : int
    SMTP_USER : str
    SMTP_PASS : str

    SALESFORCE_USERNAME : str
    SALESFORCE_PASSWORD : str
    SALESFORCE_ORG_DOMAIN : str
    SALESFORCE_CONTACT_ID : str

    COMMUNITY_PORTAL_URL : HttpUrl
    COMMUNITY_PORTAL_URLS_TO_SCREENSHOT : List[HttpUrl]

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'