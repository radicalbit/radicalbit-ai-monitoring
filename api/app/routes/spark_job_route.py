from fastapi import APIRouter, status

from app.services.spark_k8s_service import SparkK8SService


class SparkJobRoute:
    @staticmethod
    def get_router(spark_k8s_service: SparkK8SService) -> APIRouter:
        router = APIRouter()

        @router.post('/run', status_code=status.HTTP_200_OK)
        def run_job(job_name: str):
            return spark_k8s_service.run_job(job_name)

        return router
