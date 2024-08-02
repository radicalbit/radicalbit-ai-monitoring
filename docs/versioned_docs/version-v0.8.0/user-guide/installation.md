---
sidebar_position: 1
---

# Installation
The platform is composed of different modules
* **UI:** the front-end application
* **API:** the back-end application
* **Processing:** the Spark jobs
* **SDK:** the Python SDK

## Development & Testing with Docker Compose
You can easily run the platform locally using Docker and the provided Docker Compose file. 

**Important:** This setup is intended for development and testing only, not for production environments.

### Prerequisites
To run the platform successfully, you'll need to have both Docker and Docker Compose installed on your machine.

### Procedure
Once you've installed Docker and Docker Compose, clone the repository to your local machine:

```bash
git clone git@github.com:radicalbit/radicalbit-ai-monitoring.git
```

This repository provides a Docker Compose file to set up the platform locally alongside a Rancher Kubernetes cluster. This allows you to deploy Spark jobs within the cluster.

For streamlined development and testing, you can execute these steps to run the platform locally without the graphical user interface:

```bash
docker compose up
```

If you want to access the platform's user interface (UI):

```bash
docker compose --profile ui up
```

After all containers are up and running, you can access the platform at [http://localhost:5173](http://localhost:5173) to start using it.

#### Accessing the Kubernetes Cluster
The platform creates a Kubernetes cluster for managing deployments. You can connect and interact with this cluster from your local machine using tools like Lens or `kubectl`.

In the compose file is present a [k9s](https://k9scli.io/) container that can be used to monitor the k3s cluster.

```bash
docker compose up k9s -d && docker attach radicalbit-ai-monitoring-k9s-1
```

##### Using the kubeconfig File
A file named `kubeconfig.yaml` is automatically generated within the directory `./docker/k3s_data/kubeconfig/` when the platform starts. This file contains sensitive information used to authenticate with the Kubernetes cluster.

##### Here's how to connect to the cluster:
1. Copy the `kubeconfig.yaml` file to a desired location on your local machine.
1. Edit the copied file and replace the server address `https://k3s:6443` with `https://127.0.0.1:6443`. This points the kubeconfig file to the local Kubernetes cluster running on your machine.
1. Use the modified `kubeconfig.yaml` file with tools like Lens or `kubectl` to interact with the cluster.

#### Using Real AWS Credentials
In order to use a real AWS instead of MinIO is necessary to modify the environment variables of the api container, putting real `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION` and `S3_BUCKET_NAME` and removing `S3_ENDPOINT_URL`.

#### Teardown
To completely clean up the environment we can use [docker compose](https://docs.docker.com/reference/cli/docker/compose/down/)

```bash
docker compose --profile ui --profile k9s down -v --remove-orphans
```

To remove everything including container images:

```bash
docker compose --profile ui --profile k9s down -v --remove-orphans --rmi all
```
