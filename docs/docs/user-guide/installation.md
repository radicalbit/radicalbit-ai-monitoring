---
sidebar_position: 1
---

# Installation
The platform is composed by different modules
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
docker compose --profile ui up --force-recreate
```

After all containers are up and running, you can access the platform at [http://localhost:5173](http://localhost:5173) to start using it.

*Notes: The `--force-recreate` flag forces Docker Compose to restart all containers, even if running. This is useful when making configuration or image changes and wanting a fresh start. [More info](https://docs.docker.com/reference/cli/docker/compose/up/)*

#### Start from a clean workspace
To ensure a clean environment for running the platform, it's recommended to remove any existing named volumes and container images related to previous runs. You can find detailed information about this process in the [Docker Compose documentation](https://docs.docker.com/reference/cli/docker/compose/down/)

```bash
docker compose down -v --rmi all
```

The `-v` flag is optional but recommended in this case. It removes any named volumes associated with the platform, such as those used for storing data from services like Postgres or Kubernetes. The `--rmi all` flag also removes all images that were defined in the Docker Compose file. By default, `docker-compose down` only removes running containers, so these flags ensure a clean state for starting the platform.

If you want to delete just volume data run:

```bash
docker compose down -v
```

#### Accessing the Kubernetes Cluster
The platform creates a Kubernetes cluster for managing deployments. You can connect and interact with this cluster from your local machine using tools like Lens or `kubectl`.

##### Using the kubeconfig File
A file named `kubeconfig.yaml` is automatically generated within the directory `./docker/k3s_data/kubeconfig/` when the platform starts. This file contains sensitive information used to authenticate with the Kubernetes cluster.

##### Security Considerations (Important!)
*Do not modify the original `kubeconfig.yaml` file.* Modifying the server address within the original file can potentially expose the cluster to unauthorized access from outside your local machine.

*Instead, create a copy of the `kubeconfig.yaml` file and modify the copy for local use.* This ensures the original file with the default server address remains secure.

##### Here's how to connect to the cluster:
1. Copy the `kubeconfig.yaml` file to a desired location on your local machine.
1. Edit the copied file and replace the server address `https://k3s:6443` with `https://127.0.0.1:6443`. This points the kubeconfig file to the local Kubernetes cluster running on your machine.
1. Use the modified `kubeconfig.yaml` file with tools like Lens or `kubectl` to interact with the cluster.

#### Using Real AWS Credentials
In order to use a real AWS instead of MinIO is necessary to modify the environment variables of the api container, putting real `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION` and `S3_BUCKET_NAME` and removing `S3_ENDPOINT_URL`.

#### Teardown
To clean the environment or if something happens and a clean start is needed:

* Stop the docker compose
* Remove all containers
* Remove the volume
* Delete the `./docker/k3s_data/kubeconfig` folder