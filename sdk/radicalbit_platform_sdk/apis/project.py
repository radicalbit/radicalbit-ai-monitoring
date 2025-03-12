from uuid import UUID

from radicalbit_platform_sdk.commons import invoke
from radicalbit_platform_sdk.models import ProjectDefinition


class Project:
    def __init__(self, base_url: str, definition: ProjectDefinition) -> None:
        self.__uuid = definition.uuid
        self.__base_url = base_url
        self.__name = definition.name

    def uuid(self) -> UUID:
        return self.__uuid

    def name(self) -> str:
        return self.__name

    def delete(self) -> None:
        """Delete the actual `Project` from the platform

        :return: None
        """
        invoke(
            method='DELETE',
            url=f'{self.__base_url}/api/projects/{str(self.__uuid)}',
            valid_response_code=200,
            func=lambda _: None,
        )
