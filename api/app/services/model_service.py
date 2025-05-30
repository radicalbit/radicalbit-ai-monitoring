from typing import List, Optional
from uuid import UUID

from fastapi_pagination import Page, Params

from app.db.dao.completion_dataset_dao import CompletionDatasetDAO
from app.db.dao.current_dataset_dao import CurrentDatasetDAO
from app.db.dao.model_dao import ModelDAO
from app.db.dao.reference_dataset_dao import ReferenceDatasetDAO
from app.db.tables.completion_dataset_table import CompletionDataset
from app.db.tables.current_dataset_metrics_table import CurrentDatasetMetrics
from app.db.tables.current_dataset_table import CurrentDataset
from app.db.tables.model_table import Model
from app.db.tables.reference_dataset_table import ReferenceDataset
from app.models.alert_dto import AlertDTO, AnomalyType
from app.models.commons.order_type import OrderType
from app.models.exceptions import ModelError, ModelInternalError, ModelNotFoundError
from app.models.metrics.tot_percentages_dto import TotPercentagesDTO
from app.models.model_dto import ModelFeatures, ModelIn, ModelOut, ModelType


class ModelService:
    def __init__(
        self,
        model_dao: ModelDAO,
        reference_dataset_dao: ReferenceDatasetDAO,
        current_dataset_dao: CurrentDatasetDAO,
        completion_dataset_dao: CompletionDatasetDAO,
    ):
        self.model_dao = model_dao
        self.reference_dataset_dao = reference_dataset_dao
        self.current_dataset_dao = current_dataset_dao
        self.completion_dataset_dao = completion_dataset_dao

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
        model = self._check_and_get_model(model_uuid)
        latest_reference_dataset, latest_current_dataset, latest_completion_dataset = (
            self._get_latest_datasets(model_uuid, model.model_type)
        )
        return ModelOut.from_model(
            model=model,
            latest_reference_dataset=latest_reference_dataset,
            latest_current_dataset=latest_current_dataset,
            latest_completion_dataset=latest_completion_dataset,
        )

    def update_model_features_by_uuid(
        self, model_uuid: UUID, model_features: ModelFeatures
    ) -> bool:
        latest_reference_dataset = (
            self.reference_dataset_dao.get_latest_reference_dataset_by_model_uuid(
                model_uuid
            )
        )
        if latest_reference_dataset is not None:
            raise ModelError(
                'Model already has a reference dataset, could not be updated', 400
            ) from None
        return (
            self.model_dao.update_features(
                model_uuid, [feature.to_dict() for feature in model_features.features]
            )
            > 0
        )

    def delete_model(self, model_uuid: UUID) -> Optional[ModelOut]:
        model = self._check_and_get_model(model_uuid)
        self.model_dao.delete(model_uuid)
        return ModelOut.from_model(model)

    def get_all_models(
        self,
    ) -> List[ModelOut]:
        models = self.model_dao.get_all()
        model_out_list = []
        for model in models:
            (
                latest_reference_dataset,
                latest_current_dataset,
                latest_completion_dataset,
            ) = self._get_latest_datasets(model.uuid, model.model_type)
            model_out = ModelOut.from_model(
                model=model,
                latest_reference_dataset=latest_reference_dataset,
                latest_current_dataset=latest_current_dataset,
                latest_completion_dataset=latest_completion_dataset,
            )
            model_out_list.append(model_out)
        return model_out_list

    def get_summarized_percentages(self) -> TotPercentagesDTO:
        models: List[(Model, CurrentDatasetMetrics)] = (
            self.model_dao.get_last_n_percentages()
        )
        dq, dq_c = 0, 0
        mq, mq_c = 0, 0
        dr, dr_c = 0, 0
        for _, metrics in models:
            if metrics and metrics.percentages:
                dq = dq + (
                    metrics.percentages['data_quality']['value']
                    if metrics.percentages['data_quality']['value'] >= 0
                    else 0
                )
                dq_c = dq_c + (
                    1 if metrics.percentages['data_quality']['value'] >= 0 else 0
                )
                mq = mq + (
                    metrics.percentages['model_quality']['value']
                    if metrics.percentages['model_quality']['value'] >= 0
                    else 0
                )
                mq_c = mq_c + (
                    1 if metrics.percentages['model_quality']['value'] >= 0 else 0
                )
                dr = dr + (
                    metrics.percentages['drift']['value']
                    if metrics.percentages['drift']['value'] >= 0
                    else 0
                )
                dr_c = dr_c + (1 if metrics.percentages['drift']['value'] >= 0 else 0)
        return TotPercentagesDTO.from_dict(
            {
                'data_quality': dq / dq_c if dq_c > 0 else 0,
                'model_quality': mq / mq_c if mq_c > 0 else -1,
                'drift': dr / dr_c if dr_c > 0 else 0,
            }
        )

    def get_last_n_alerts(self, n_alerts) -> List[AlertDTO]:
        models: List[(Model, CurrentDatasetMetrics)] = (
            self.model_dao.get_last_n_percentages()
        )
        res = []
        count_alerts = 0
        for model, metrics in models:
            (
                latest_reference_dataset,
                latest_current_dataset,
                latest_completion_dataset,
            ) = self._get_latest_datasets(model.uuid, model.model_type)
            if metrics and metrics.percentages:
                for perc in ['data_quality', 'model_quality', 'drift']:
                    if count_alerts == n_alerts:
                        return res
                    if 0 <= metrics.percentages[perc]['value'] < 1:
                        res.append(
                            AlertDTO(
                                model_name=model.name,
                                model_uuid=model.uuid,
                                reference_uuid=latest_reference_dataset.uuid
                                if latest_reference_dataset
                                else None,
                                current_uuid=latest_current_dataset.uuid
                                if latest_current_dataset
                                else None,
                                completion_uuid=latest_completion_dataset.uuid
                                if latest_completion_dataset
                                else None,
                                anomaly_type=AnomalyType[perc.upper()],
                                anomaly_features=[
                                    x['feature_name']
                                    for x in sorted(
                                        metrics.percentages[perc]['details'],
                                        key=lambda e: e['score'],
                                        reverse=True,
                                    )
                                    if x['score'] > 0
                                ],
                            )
                        )
                        count_alerts += 1

        return res

    def get_last_n_models_percentages(self, n_models) -> List[ModelOut]:
        models = self.model_dao.get_last_n_percentages(n_models)
        model_out_list_tmp = []
        for model, metrics in models:
            (
                latest_reference_dataset,
                latest_current_dataset,
                latest_completion_dataset,
            ) = self._get_latest_datasets(model.uuid, model.model_type)
            model_out = ModelOut.from_model(
                model=model,
                latest_reference_dataset=latest_reference_dataset,
                latest_current_dataset=latest_current_dataset,
                latest_completion_dataset=latest_completion_dataset,
                percentages=metrics.percentages if metrics else None,
            )
            model_out_list_tmp.append(model_out)
        return model_out_list_tmp

    def get_all_models_paginated(
        self,
        params: Params = Params(),
        order: OrderType = OrderType.ASC,
        sort: Optional[str] = None,
    ) -> Page[ModelOut]:
        models: Page[(Model, CurrentDatasetMetrics)] = self.model_dao.get_all_paginated(
            params=params, order=order, sort=sort
        )
        _items = []
        for model, metrics in models.items:
            (
                latest_reference_dataset,
                latest_current_dataset,
                latest_completion_dataset,
            ) = self._get_latest_datasets(model.uuid, model.model_type)
            model_out = ModelOut.from_model(
                model=model,
                latest_reference_dataset=latest_reference_dataset,
                latest_current_dataset=latest_current_dataset,
                latest_completion_dataset=latest_completion_dataset,
                percentages=metrics.percentages if metrics else None,
            )
            _items.append(model_out)

        return Page.create(items=_items, params=params, total=models.total)

    def _check_and_get_model(self, model_uuid: UUID) -> Model:
        model = self.model_dao.get_by_uuid(model_uuid)
        if not model:
            raise ModelNotFoundError(f'Model {model_uuid} not found')
        return model

    def _get_latest_datasets(
        self, model_uuid: UUID, model_type: ModelType
    ) -> (
        Optional[ReferenceDataset],
        Optional[CurrentDataset],
        Optional[CompletionDataset],
    ):
        latest_reference_dataset = None
        latest_current_dataset = None
        latest_completion_dataset = None

        if model_type == ModelType.TEXT_GENERATION:
            latest_completion_dataset = (
                self.completion_dataset_dao.get_latest_completion_dataset_by_model_uuid(
                    model_uuid
                )
            )
        else:
            latest_reference_dataset = (
                self.reference_dataset_dao.get_latest_reference_dataset_by_model_uuid(
                    model_uuid
                )
            )
            latest_current_dataset = (
                self.current_dataset_dao.get_latest_current_dataset_by_model_uuid(
                    model_uuid
                )
            )

        return (
            latest_reference_dataset,
            latest_current_dataset,
            latest_completion_dataset,
        )
