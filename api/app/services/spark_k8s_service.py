import logging

from spark_on_k8s.client import SparkOnK8S

from app.core.config.config import get_config

logger = logging.getLogger(get_config().log_config.logger_name)


class SparkK8SService:
    def __init__(self, spark_k8s_client: SparkOnK8S) -> 'SparkK8SService':
        self.spark_k8s_client = spark_k8s_client
        logger.info('SparkK8SService Initialized.')

    # TODO this is only a placeholder that will run an example job
    def run_job(self, job_name: str) -> str:
        return self.spark_k8s_client.submit_app(
            image='radicalbit/radicalbit-spark-py:latest',
            app_path='local:///opt/spark/examples/src/main/python/pi.py',
            app_arguments=['100'],
            app_name=job_name,
            namespace='spark',
            service_account='spark',
            app_waiter='no_wait',
            image_pull_policy='IfNotPresent',
        )
