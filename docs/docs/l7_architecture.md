---
sidebar_position: 1
---

# Architecture

In this section we'll explore the architecture of the Radicalbit AI platform.
The image below shows all the components of the platform:

![Alt text](/img/architecture/architecture.png "Architecture")

## API

API is the core of the platform, it exposes all the functionalities via REST APIs.
It requires a PostgreSQL database to store data and a Kubernetes cluster to run Spark jobs for metrics evaluations.
To store all dataset files a distributed storage is used.
REST APIs could be used via user interface or using the provided Python SDK.

## UI

To use REST APIs with a human friendly interface, a UI is provided.
It covers all the implemented APIs, starting from models creation and ending with all metrics visualization.

## SDK

To interact with API programmatically, a Python SDK is provided.
The SDK implements all functionalities exposed via REST API.