from uuid import UUID

from radicalbit_platform_sdk.models import ApiKeyDefinition


class ApiKey:
    def __init__(self, base_url: str, definition: ApiKeyDefinition):
        self.__name = definition.name
        self.__api_key = definition.api_key
        self.__project_uuid = definition.project_uuid
        self.__created_at = definition.created_at
        self.__updated_at = definition.updated_at
        self.__base_url = base_url

    @property
    def api_key(self) -> str:
        return self.__api_key

    @property
    def name(self) -> str:
        return self.__name

    @property
    def project_uuid(self) -> UUID:
        return self.__project_uuid

    @property
    def created_at(self) -> str:
        return self.__created_at

    @property
    def updated_at(self) -> str:
        return self.__updated_at

    def __repr__(self) -> str:
        """Return an unambiguous string representation of the ApiKey."""
        class_name = self.__class__.__name__
        return (
            f'{class_name}('
            f'name={self.name!r}, '
            f'api_key={self.api_key!r}, '
            f'project_uuid={self.project_uuid!r}, '
            f'created_at={self.created_at!r}, '
            f'updated_at={self.updated_at!r}, '
            f')'
        )

    def delete(self) -> None:
        pass
