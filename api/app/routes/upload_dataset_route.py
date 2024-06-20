from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, File, Form, UploadFile, status
from fastapi.params import Query
from fastapi_pagination import Page, Params

from app.models.dataset_dto import (
    CurrentDatasetDTO,
    FileReference,
    OrderType,
    ReferenceDatasetDTO,
)
from app.services.file_service import FileService


class UploadDatasetRoute:
    @staticmethod
    def get_router(file_service: FileService) -> APIRouter:
        router = APIRouter(tags=['file_api'])

        @router.post(
            '/{model_uuid}/reference/upload',
            status_code=status.HTTP_200_OK,
            response_model=ReferenceDatasetDTO,
        )
        def upload_reference_file(
            model_uuid: UUID, csv_file: UploadFile = File(...), sep: str = Form(',')
        ) -> ReferenceDatasetDTO:
            return file_service.upload_reference_file(model_uuid, csv_file, sep)

        @router.post(
            '/{model_uuid}/reference/bind',
            status_code=status.HTTP_200_OK,
            response_model=ReferenceDatasetDTO,
        )
        def bind_reference_file(
            model_uuid: UUID, file_ref: FileReference
        ) -> ReferenceDatasetDTO:
            return file_service.bind_reference_file(model_uuid, file_ref)

        @router.post(
            '/{model_uuid}/current/upload',
            status_code=status.HTTP_200_OK,
            response_model=CurrentDatasetDTO,
        )
        def upload_current_file(
            model_uuid: UUID,
            csv_file: UploadFile = File(...),
            sep: str = Form(','),
            correlation_id_column: str = Form(''),
        ) -> CurrentDatasetDTO:
            return file_service.upload_current_file(
                model_uuid, csv_file, correlation_id_column, sep
            )

        @router.post(
            '/{model_uuid}/current/bind',
            status_code=status.HTTP_200_OK,
            response_model=CurrentDatasetDTO,
        )
        def bind_current_file(
            model_uuid: UUID, file_ref: FileReference
        ) -> CurrentDatasetDTO:
            return file_service.bind_current_file(model_uuid, file_ref)

        @router.get(
            '/{model_uuid}/reference',
            status_code=200,
            response_model=Page[ReferenceDatasetDTO],
        )
        def get_all_reference_datasets_by_model_uuid(
            model_uuid: UUID,
            _page: Annotated[int, Query()] = 1,
            _limit: Annotated[int, Query()] = 50,
            _order: Annotated[OrderType, Query()] = OrderType.ASC,
            _sort: Annotated[Optional[str], Query()] = None,
        ):
            params = Params(page=_page, size=_limit)
            return file_service.get_all_reference_datasets_by_model_uuid(
                model_uuid, params=params, order=_order, sort=_sort
            )

        @router.get(
            '/{model_uuid}/current',
            status_code=200,
            response_model=Page[CurrentDatasetDTO],
        )
        def get_all_current_datasets_by_model_uuid(
            model_uuid: UUID,
            _page: Annotated[int, Query()] = 1,
            _limit: Annotated[int, Query()] = 50,
            _order: Annotated[OrderType, Query()] = OrderType.ASC,
            _sort: Annotated[Optional[str], Query()] = None,
        ):
            params = Params(page=_page, size=_limit)
            return file_service.get_all_current_datasets_by_model_uuid(
                model_uuid, params=params, order=_order, sort=_sort
            )

        return router
