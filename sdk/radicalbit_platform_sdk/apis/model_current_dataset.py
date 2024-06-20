from radicalbit_platform_sdk.models import CurrentFileUpload
from uuid import UUID


class ModelCurrentDataset:
    def __init__(self, base_url: str, upload: CurrentFileUpload) -> None:
        self.__base_url = base_url
        self.__uuid = upload.uuid
        self.__path = upload.path
        self.__correlation_id_column = upload.correlation_id_column
        self.__date = upload.date
        self.__status = upload.status

    def uuid(self) -> UUID:
        return self.__uuid

    def path(self) -> str:
        return self.__path

    def correlation_id_column(self) -> str:
        return self.__correlation_id_column

    def date(self) -> str:
        return self.__date

    def status(self) -> str:
        return self.__status

    def statistics(self):
        # TODO: implement get statistics
        pass

    def drift(self):
        # TODO: implement get drift
        pass

    def data_quality(self):
        # TODO: implement get data quality
        pass

    def model_quality(self):
        # TODO: implement get model quality
        pass
