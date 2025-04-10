import secrets
import string

from app.models.traces.api_key_dto import ApiKeySec
from app.services.commons.keyed_hash_algorithm import hash_key


class ApiKeySecurity:
    def __init__(self):
        pass

    @staticmethod
    def _create_secret() -> str:
        return 'sk-rb-' + ''.join(
            secrets.choice(string.ascii_letters + string.digits) for _ in range(48)
        )

    def generate_key(self) -> ApiKeySec:
        key = self._create_secret()
        hashed_key = hash_key(key)
        return ApiKeySec(plain_key=key, hashed_key=hashed_key)
