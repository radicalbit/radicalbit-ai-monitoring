# Radicalbit AI Monitoring

This repository contains all the files and projects to run Radicalbit AI Monitoring Platform

- [ui](./ui/README.md)
- [api](./api/README.md)
- [sdk](./sdk/README.md)
- [spark](./spark/README.md)

## Docker compose

In this repository a docker compose file is available to run the platform in local with a k3s cluster where we can deploy Spark jobs.

To run, simply:

```bash
docker compose up
```

If the UI is needed:

```bash
docker compose --profile ui up
```

After all containers are up & running, you can go to [http://localhost:5173](http://127.0.0.1:5173) to play with the app.

### Interacting with k3s cluster

In the compose file is present a [k9s](https://k9scli.io/) container that can be used to monitor the k3s cluster.

```bash
docker compose up k9s -d && docker attach radicalbit-ai-monitoring-k9s-1
```

#### Other tools

In order to connect and interact with the k3s cluster from the local machine (for example with Lens or `kubectl`) is necessary to create another file starting from `./docker/k3s_data/kubeconfig/kubeconfig.yaml` (that is automatically generated when the docker compose is up and running).

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