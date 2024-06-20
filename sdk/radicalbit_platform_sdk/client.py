from radicalbit_platform_sdk.commons import invoke
from radicalbit_platform_sdk.apis import Model
from radicalbit_platform_sdk.models import (
    CreateModel,
    ModelDefinition,
    PaginatedModelDefinitions,
)
from radicalbit_platform_sdk.errors import ClientError
from pydantic import ValidationError
from typing import List
from uuid import UUID
import requests


class Client:
    def __init__(self, base_url: str) -> None:
        self.__base_url = base_url

    def create_model(self, model: CreateModel) -> Model:
        def __callback(response: requests.Response) -> Model:
            try:
                response_model = ModelDefinition.model_validate(response.json())
                return Model(self.__base_url, response_model)
            except ValidationError as _:
                raise ClientError(f"Unable to parse response: {response.text}")

        return invoke(
            method="POST",
            url=f"{self.__base_url}/api/models",
            valid_response_code=201,
            func=__callback,
            data=model.model_dump_json(),
        )

    def get_model(self, id: UUID) -> Model:
        def __callback(response: requests.Response) -> Model:
            try:
                response_model = ModelDefinition.model_validate(response.json())
                return Model(self.__base_url, response_model)
            except ValidationError as _:
                raise ClientError(f"Unable to parse response: {response.text}")

        return invoke(
            method="GET",
            url=f"{self.__base_url}/api/models/{str(id)}",
            valid_response_code=200,
            func=__callback,
        )

    def search_models(self) -> List[Model]:
        def __callback(response: requests.Response) -> Model:
            try:
                paginated_response = PaginatedModelDefinitions.model_validate(
                    response.json()
                )
                return list(
                    map(
                        lambda model: Model(self.__base_url, model),
                        paginated_response.items,
                    )
                )
            except ValidationError as _:
                raise ClientError(f"Unable to parse response: {response.text}")

        return invoke(
            method="GET",
            url=f"{self.__base_url}/api/models",
            valid_response_code=200,
            func=__callback,
        )
