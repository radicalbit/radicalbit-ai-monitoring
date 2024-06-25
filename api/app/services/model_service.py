from typing import Optional
from uuid import UUID

from fastapi_pagination import Page, Params

from app.db.dao.current_dataset_dao import CurrentDatasetDAO
from app.db.dao.model_dao import ModelDAO
from app.db.dao.reference_dataset_dao import ReferenceDatasetDAO
from app.db.tables.model_table import Model
from app.models.exceptions import ModelInternalError, ModelNotFoundError
from app.models.model_dto import ModelIn, ModelOut
from app.models.model_order import OrderType


class ModelService:
    def __init__(
        self,
        model_dao: ModelDAO,
        reference_dataset_dao: ReferenceDatasetDAO,
        current_dataset_dao: CurrentDatasetDAO,
    ):
        self.model_dao = model_dao
        self.rd_dao = reference_dataset_dao
        self.cd_dao = current_dataset_dao

    def create_model(self, model_in: ModelIn) -> ModelOut:
        try:
            to_insert = model_in.to_model()
            inserted = self.model_dao.insert(to_insert)
            return ModelOut.from_model(inserted)
        except Exception as e:
            raise ModelInternalError(
                f'An error occurred while creating the model: {e}'
            ) from e

    def get_model_by_uuid(self, model_uuid: UUID) -> Optional[ModelOut]:
        model = self.check_and_get_model(model_uuid)
        latest_reference_uuid, latest_current_uuid = self.get_latest_dataset_uuids(
            model_uuid
        )
        return ModelOut.from_model(
            model=model,
            latest_reference_uuid=latest_reference_uuid,
            latest_current_uuid=latest_current_uuid,
        )

    def delete_model(self, model_uuid: UUID) -> Optional[ModelOut]:
        model = self.check_and_get_model(model_uuid)
        self.model_dao.delete(model_uuid)
        return ModelOut.from_model(model)

    def get_all_models(
        self,
        params: Params = Params(),
        order: OrderType = OrderType.ASC,
        sort: Optional[str] = None,
    ) -> Page[ModelOut]:
        models: Page[Model] = self.model_dao.get_all(
            params=params, order=order, sort=sort
        )

        _items = []
        for model in models.items:
            latest_reference_uuid, latest_current_uuid = self.get_latest_dataset_uuids(
                model.uuid
            )
            model_out = ModelOut.from_model(
                model=model,
                latest_reference_uuid=latest_reference_uuid,
                latest_current_uuid=latest_current_uuid,
            )
            _items.append(model_out)

        return Page.create(items=_items, params=params, total=models.total)

    def check_and_get_model(self, model_uuid: UUID) -> Model:
        model = self.model_dao.get_by_uuid(model_uuid)
        if not model:
            raise ModelNotFoundError(f'Model {model_uuid} not found')
        return model

    def get_latest_dataset_uuids(
        self, model_uuid: UUID
    ) -> (Optional[UUID], Optional[UUID]):
        latest_reference_dataset = (
            self.rd_dao.get_latest_reference_dataset_by_model_uuid(model_uuid)
        )
        latest_current_dataset = self.cd_dao.get_latest_current_dataset_by_model_uuid(
            model_uuid
        )

        latest_reference_uuid = (
            latest_reference_dataset.uuid if latest_reference_dataset else None
        )
        latest_current_uuid = (
            latest_current_dataset.uuid if latest_current_dataset else None
        )

        return latest_reference_uuid, latest_current_uuid
