<p align="center">
    <a href="https://radicalbit.ai/">
      <img src="docs/static/img/radicalbit.svg" width="100">
    </a>
</p>
<br />

[![Docs Latest](https://img.shields.io/badge/docs-latest-blue.svg)](https://docs.oss-monitoring.radicalbit.ai)
![GitHub Release](https://img.shields.io/github/v/release/radicalbit/radicalbit-ai-monitoring)
![GitHub License](https://img.shields.io/github/license/radicalbit/radicalbit-ai-monitoring)
![Discord](https://img.shields.io/discord/1252978922962817034)
[![Security Scan](https://img.shields.io/github/actions/workflow/status/radicalbit/radicalbit-ai-monitoring/trivy-scan.yaml?branch=main&label=Security%20Scan
)](./.github/workflows/trivy-scan.yaml)

# Radicalbit AI Monitoring

# 👋 Welcome!
The **Radicalbit AI Monitoring Platform** provides a comprehensive solution for monitoring your Artificial Intelligence models in production.

## 🤔 Why Monitor AI Models?
While models often perform well during development and validation, their effectiveness can degrade over time in production due to various factors like data shifts or concept drift. The Radicalbit AI Monitor platform helps you proactively identify and address potential performance issues.

## 🗝️ Key Functionalities
The platform provides extensive monitoring capabilities to ensure optimal performance of your AI models in production. It analyzes both your reference dataset (used for pre-production validation) and the current datasets, allowing you to put under control:
* **Data Quality**
* **Model Quality**
* **Model Drift**

# 🏗️ Repository Structure
This repository contains all the files and projects to run Radicalbit AI Monitoring Platform

- [ui](./ui/README.md)
- [api](./api/README.md)
- [sdk](./sdk/README.md)
- [spark](./spark/README.md)

## 🚀 Installation using Docker compose

In this repository a docker compose file is available to run the platform in local with a K3s cluster where we can deploy Spark jobs.

To run, simply:

```bash
docker compose up
```

If the UI is needed:

```bash
docker compose --profile ui up
```

After all containers are up & running, you can go to [http://localhost:5173](http://127.0.0.1:5173) to play with the app.

### Interacting with K3s cluster

In the compose file is present a [k9s](https://k9scli.io/) container that can be used to monitor the K3s cluster.

```bash
docker compose up k9s -d && docker attach radicalbit-ai-monitoring-k9s-1
```

#### Other tools

In order to connect and interact with the K3s cluster from the local machine (for example with Lens or `kubectl`) is necessary to create another file starting from `./docker/k3s_data/kubeconfig/kubeconfig.yaml` (that is automatically generated when the docker compose is up and running).

Copy the above file and modify `https://k3s:6443` with `https://127.0.0.1:6443` and use this new file to interact with the cluster from the local machine

### Real AWS

In order to use a real AWS instead of Minio is necessary to modify the environment variables of the api container, putting real `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION` and `S3_BUCKET_NAME` and removing `S3_ENDPOINT_URL`.

### Teardown

To completely clean up the environment we can use [docker compose](https://docs.docker.com/reference/cli/docker/compose/down/)

```bash
docker compose --profile ui --profile k9s down -v --remove-orphans
```

To remove everything including container images:

```bash
docker compose --profile ui --profile k9s down -v --remove-orphans --rmi all
```

## 📖 Documentation
You can find the following documentation:
* An extensive [step-by-step guide](https://docs.oss-monitoring.radicalbit.ai/user-guide/installation) to install the development/testing version of the platform.
* A [guide](https://docs.oss-monitoring.radicalbit.ai/user-guide/quickstart) that walks users through creating dashboards on the platform.

## 🤝 Community
Please join us on our [Discord server](https://discord.gg/x2Ze8TMRsD), to discuss the platform, share ideas, and help shape its future! Get help from experts and fellow users.

## 📦 Functionalities & Roadmap
We've released a first dashboard, covering Binary Classification models for tabular data.
Over the coming weeks, we will be adding the following functionalities to the platform:

* **Batch workloads**
  * [x] Binary Classification (Tabular Data)
  * [x] LLMs (Data Quality)
  * [ ] LLMs (Model Quality)
  * [ ] Multiclass Classification (Tabular Data)
  * [ ] Regression (Tabular Data)
  * [ ] Computer Vision (Images)
  * [ ] Clustering (Tabular Data)
       
* **Real-Time workloads**
  * [ ] Binary Classification
  * [ ] Multiclass Classification
  * [ ] Regression
  * [ ] Computer Vision
  * [ ] Clustering
