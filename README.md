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
The **Radicalbit AI Monitoring Platform** provides a comprehensive solution for monitoring your Machine Learning and Large Language models in production.

## 🤔 Why Monitor AI Models?
While models often perform well during development and validation, their effectiveness can degrade over time in production due to various factors like data shifts or concept drift. The Radicalbit AI Monitor platform helps you proactively identify and address potential performance issues.

## 🗝️ Key Functionalities
The platform provides extensive monitoring capabilities to ensure optimal performance of your AI models in production. It analyzes both your reference dataset (used for pre-production validation) and the current datasets, allowing you to control:
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

This repository provides a Docker Compose file for running the platform locally with a K3s cluster. This setup allows you to deploy Spark jobs.

To run, simply:

```bash
docker compose up
```

If the UI is needed:

```bash
docker compose --profile ui up
```

In order to initialize the platform with demo models you can run:

```bash
docker compose --profile ui --profile init-data up
```

Once all containers are up & running, you can go to [http://localhost:5173](http://127.0.0.1:5173) to play with the app.

### Interacting with K3s cluster

The compose file includes a [k9s](https://k9scli.io/) container that can be used to monitor the K3s cluster.

```bash
docker compose up k9s -d && docker attach radicalbit-ai-monitoring-k9s-1
```

#### Other tools

In order to connect and interact with the K3s cluster from the local machine (for example with Lens or `kubectl`), it is necessary to create another file starting from `./docker/k3s_data/kubeconfig/kubeconfig.yaml` (that is automatically generated when the docker compose is up and running).

Copy the above file and modify `https://k3s:6443` with `https://127.0.0.1:6443` and use this new file to interact with the cluster from the local machine

### Real AWS

In order to use a real AWS instead of MinIO it is necessary to modify the environment variables of the api container, putting real `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION` and `S3_BUCKET_NAME` and removing `S3_ENDPOINT_URL`.

### Teardown

To completely clean up the environment we can use [docker compose](https://docs.docker.com/reference/cli/docker/compose/down/)

```bash
docker compose --profile ui --profile k9s --profile init-data down -v --remove-orphans
```

To remove everything including container images:

```bash
docker compose --profile ui --profile k9s --profile init-data down -v --remove-orphans --rmi all
```

## Spark tuning
We use Spark jobs to calculate metrics: if you need to tune Spark configuration in order to optimize performance for large files or accelerate computations, please refer to the corresponding section of this [README file](https://github.com/radicalbit/radicalbit-ai-monitoring/blob/main/api/README.md).

## 📖 Documentation
You can find the following documentation:
* An extensive [step-by-step guide](https://docs.oss-monitoring.radicalbit.ai/user-guide/installation) to install the development/testing version of the platform, followed by all [key concepts](https://docs.oss-monitoring.radicalbit.ai/user-guide/key-concepts) and a [hands-on guide](https://docs.oss-monitoring.radicalbit.ai/user-guide/how-to) on how to use the GUI.
* A practical [guide](https://docs.oss-monitoring.radicalbit.ai/quickstart) that walks users through monitoring an AI solution on the platform.
* A detailed [explanation](https://docs.oss-monitoring.radicalbit.ai/category/model-sections) on the three main model sections.
* An exhaustive [description](https://docs.oss-monitoring.radicalbit.ai/python-sdk) of all classes implemented inside the Python SDK.
* A list of [all available metrics and charts](https://docs.oss-monitoring.radicalbit.ai/all-metrics).
* A page related to the [architecture](https://docs.oss-monitoring.radicalbit.ai/architecture) of the platform.
* A [community support](https://docs.oss-monitoring.radicalbit.ai/support) page.

## 🤝 Community
Please join us on our [Discord server](https://discord.gg/x2Ze8TMRsD), to discuss the platform, share ideas, and help shape its future! Get help from experts and fellow users.

## 📦 Functionalities & Roadmap
We've released a first few dashboards, covering Classification, both Binary and Multiclass, and Regression models for tabular data.
Over the coming weeks, we will be adding the following functionalities to the platform:

* **Batch workloads**
  * [x] Binary Classification (Tabular Data)
  * [x] Multiclass Classification (Tabular Data)
  * [x] Regression (Tabular Data)
  * [x] LLMs (Data Quality)
  * [ ] LLMs (Model Quality)
  * [ ] Computer Vision (Images)
  * [ ] Clustering (Tabular Data)

* **Real-Time workloads**
  * [ ] Binary Classification
  * [ ] Multiclass Classification
  * [ ] Regression
  * [ ] Computer Vision
  * [ ] Clustering

## We Value Your Privacy
We collect anonymous usage data to improve our software. This information helps us understand how the software is used and identify areas for improvement. No personally identifiable information is collected.

The first time you start using the platform you will be explicitly asked whether you prefer to opt-in or opt-out this anonymous usage data collection.
