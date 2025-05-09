from typing import List
from uuid import UUID

from pydantic import TypeAdapter, ValidationError
import requests

from radicalbit_platform_sdk.apis import Model, Project
from radicalbit_platform_sdk.commons import invoke
from radicalbit_platform_sdk.errors import ClientError
from radicalbit_platform_sdk.models import (
    CreateModel,
    CreateProject,
    ModelDefinition,
    ProjectDefinition,
)


class Client:
    def __init__(self, base_url: str) -> None:
        self.__base_url = base_url

    def create_model(self, model: CreateModel) -> Model:
        def __callback(response: requests.Response) -> Model:
            try:
                response_model = ModelDefinition.model_validate(response.json())
                return Model(self.__base_url, response_model)
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e

        return invoke(
            method='POST',
            url=f'{self.__base_url}/api/models',
            valid_response_code=201,
            func=__callback,
            data=model.model_dump_json(),
        )

    def get_model(self, id: UUID) -> Model:
        def __callback(response: requests.Response) -> Model:
            try:
                response_model = ModelDefinition.model_validate(response.json())
                return Model(self.__base_url, response_model)
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e

        return invoke(
            method='GET',
            url=f'{self.__base_url}/api/models/{str(id)}',
            valid_response_code=200,
            func=__callback,
        )

    def search_models(self) -> List[Model]:
        def __callback(response: requests.Response) -> List[Model]:
            try:
                adapter = TypeAdapter(List[ModelDefinition])
                model_definitions = adapter.validate_python(response.json())
                return [Model(self.__base_url, model) for model in model_definitions]
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e

        return invoke(
            method='GET',
            url=f'{self.__base_url}/api/models/all',
            valid_response_code=200,
            func=__callback,
        )

    def create_project(self, project: CreateProject) -> Project:
        def __callback(response: requests.Response) -> Project:
            try:
                response_project = ProjectDefinition.model_validate(response.json())
                return Project(self.__base_url, response_project)
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e

        return invoke(
            method='POST',
            url=f'{self.__base_url}/api/projects',
            valid_response_code=201,
            func=__callback,
            data=project.model_dump_json(),
        )

    def get_project(self, id: UUID) -> Project:
        def __callback(response: requests.Response) -> Project:
            try:
                response_project = ProjectDefinition.model_validate(response.json())
                return Project(self.__base_url, response_project)
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e

        return invoke(
            method='GET',
            url=f'{self.__base_url}/api/projects/{str(id)}',
            valid_response_code=200,
            func=__callback,
        )

    def search_projects(self) -> List[Project]:
        def __callback(response: requests.Response) -> List[Project]:
            try:
                adapter = TypeAdapter(List[ProjectDefinition])
                projects_definitions = adapter.validate_python(response.json())
                return [
                    Project(self.__base_url, project)
                    for project in projects_definitions
                ]
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e

        return invoke(
            method='GET',
            url=f'{self.__base_url}/api/projects/all',
            valid_response_code=200,
            func=__callback,
        )
