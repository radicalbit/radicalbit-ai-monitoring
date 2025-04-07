from app.db.dao.api_key_dao import ApiKeyDAO
from app.models.traces.api_key_dto import ApiKeyIn, ApiKeyOut
from app.services.api_key_security import ApiKeySecurity


class ApiKeyService:
    def __init__(self, api_key_dao: ApiKeyDAO, api_key_security: ApiKeySecurity):
        self.api_key_dao = api_key_dao
        self.api_key_security = api_key_security

    def create_api_key(self, api_key_in: ApiKeyIn) -> ApiKeyOut:
        pass
