import os
from conf import create_secrets
from uuid import uuid4
from spark_on_k8s.k8s.sync_client import KubernetesClientManager
from spark_on_k8s.client import SparkOnK8S

envs = ["KUBECONFIG_FILE_PATH", "JOB_NAME", "SPARK_IMAGE"]

for var in envs:
    if var not in os.environ:
        raise EnvironmentError("Failed because {} is not set.".format(var))

kube_conf = os.environ["KUBECONFIG_FILE_PATH"]
job_name = os.environ["JOB_NAME"]
spark_image = os.environ["SPARK_IMAGE"]

k8s_client_manager = KubernetesClientManager(kube_conf)
spark_k8s_client = SparkOnK8S(k8s_client_manager=k8s_client_manager)

path = "s3a://test-bucket/metrics_one.json"

spark_k8s_client.submit_app(
    image=spark_image,
    app_path=f"local:///opt/spark/custom_jobs/{job_name}_job.py",
    app_arguments=[
        path,
        str(uuid4()),
        "completion_dataset_metrics",
        "completion_dataset",
    ],
    app_name=f"{spark_image}-completion-job",
    namespace="spark",
    service_account="spark",
    app_waiter="no_wait",
    image_pull_policy="IfNotPresent",
    secret_values=create_secrets(),
)
