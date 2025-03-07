from radicalbit_platform_sdk.models import ProjectDefinition


class Project:
    def __init__(self, base_url: str, definition: ProjectDefinition) -> None:
        self.__base_url = base_url
        self.__name = definition.name

    def name(self) -> str:
        return self.__name
