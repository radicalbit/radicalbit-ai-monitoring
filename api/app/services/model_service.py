from typing import List, Optional
from uuid import UUID

from fastapi_pagination import Page, Params

from app.db.dao.model_dao import ModelDAO
from app.db.tables.model_table import Model
from app.models.exceptions import ModelInternalError, ModelNotFoundError
from app.models.model_dto import ModelIn, ModelOut
from app.models.model_order import OrderType


class ModelService:
    def __init__(self, model_dao: ModelDAO):
        self.model_dao = model_dao

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
        return ModelOut.from_model(model)

    def delete_model(self, model_uuid: UUID) -> Optional[ModelOut]:
        model = self.check_and_get_model(model_uuid)
        self.model_dao.delete(model_uuid)
        return ModelOut.from_model(model)

    def get_all_models(
        self,
    ) -> List[ModelOut]:
        models = self.model_dao.get_all()
        return [ModelOut.from_model(model) for model in models]

    def get_all_models_paginated(
        self,
        params: Params = Params(),
        order: OrderType = OrderType.ASC,
        sort: Optional[str] = None,
    ) -> Page[ModelOut]:
        models: Page[Model] = self.model_dao.get_all_paginated(
            params=params, order=order, sort=sort
        )
        _items = [ModelOut.from_model(model) for model in models.items]

        return Page.create(items=_items, params=params, total=models.total)

    def check_and_get_model(self, model_uuid: UUID) -> Model:
        model = self.model_dao.get_by_uuid(model_uuid)
        if not model:
            raise ModelNotFoundError(f'Model {model_uuid} not found')
        return model
