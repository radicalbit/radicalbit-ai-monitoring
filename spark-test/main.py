import os

from conf import create_secrets
from spark_on_k8s.k8s.sync_client import KubernetesClientManager
from spark_on_k8s.client import SparkOnK8S

import json

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


def load_json():
    with open("./modelout.json", "r") as f:
        data = json.load(f)
    return json.dumps(data, indent=2)

current_path = "s3a://test-bucket/df_current1-5cac31fe358e0efaab9d8ea844d3f15b.csv"
reference_path = "s3a://test-bucket/df_reference-1894ad2a37bbcc09d7bbc333f368208c.csv"
embeddings_path = "s3a://test-bucket/embeddings.csv"
spark_k8s_client.submit_app(
    image=spark_image,
    app_path=f"local:///opt/spark/custom_jobs/{job_name}_job.py",
    app_arguments=[
        load_json(),
        embeddings_path,
        "8aa09366-5d37-4721-a20a-7f6638fb6d27",
        "embeddings_reference_dataset_metrics",
        "embeddings_reference_dataset",
    ],
    app_name=f"{spark_image}-completion-job",
    namespace="spark",
    service_account="spark",
    app_waiter="no_wait",
    image_pull_policy="IfNotPresent",
    secret_values=create_secrets(),
)
