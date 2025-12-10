from fastapi import APIRouter, File, UploadFile, status

from app.models.inferred_schema_dto import InferredSchemaDTO
from app.services.file_service import FileService


class InferSchemaRoute:
    @staticmethod
    def get_router(file_service: FileService) -> APIRouter:
        router = APIRouter(tags=['infer_schema_api'])

        @router.post(
            '/infer-schema',
            status_code=status.HTTP_200_OK,
            response_model=InferredSchemaDTO,
        )
        def infer_schema_from_file(
            data_file: UploadFile = File(...),
        ):
            schema_result: InferredSchemaDTO = file_service.infer_schema(data_file)
            return schema_result

        return router
