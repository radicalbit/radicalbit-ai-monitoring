from pydantic import BaseModel


class AwsCredentials(BaseModel):
    access_key_id: str
    secret_access_key: str
    default_region: str
